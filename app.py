import os, uuid, threading, traceback, time, socket

# Suppress TensorFlow C++ logs (INFO, WARNING) — only errors shown
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from database import db, Prediction

# ── App setup ────────────────────────────────────────────────────
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH']             = 10 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///freshscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ── Upload folder ────────────────────────────────────────────────
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXT = {'jpg', 'jpeg', 'png'}

# ── Database ─────────────────────────────────────────────────────
db.init_app(app)

with app.app_context():
    db.create_all()
    # Auto-migrate: add filename column if missing
    try:
        from sqlalchemy import text
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE predictions ADD COLUMN filename VARCHAR(120)'))
            conn.commit()
    except Exception:
        pass  # Column already exists — ignore

# ── Lazy model loading ───────────────────────────────────────────
# model is None until first prediction request — no TF at startup.
model = None

def get_model():
    """
    Lazy-load the Keras model on first call, then return the cached instance.
    Returns None if the model file doesn't exist or loading fails.
    """
    global model
    if model is not None:
        return model

    try:
        from model.train import load_or_create_model, MODEL_PATH
        if not os.path.exists(MODEL_PATH):
            print('[FreshScan] Model file not found — predictions unavailable.')
            return None
        model = load_or_create_model()
        print('[FreshScan] Model loaded into memory.')
        return model
    except Exception:
        print('[FreshScan] Failed to load model:')
        traceback.print_exc()
        return None

# ── Constants ────────────────────────────────────────────────────
SHELF_LIFE = {
    'apple': 14, 'banana': 5,  'mango': 6,    'orange': 14, 'grapes': 7,
    'strawberry': 3, 'watermelon': 10, 'pineapple': 5, 'papaya': 5,
    'kiwi': 7,   'cherry': 5,  'pomegranate': 14, 'pear': 7, 'peach': 5,
    'blueberry': 7,
}

# ── Helpers ──────────────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def get_verdict(fresh_pct):
    if fresh_pct >= 70:
        return 'Fresh'
    if fresh_pct >= 40:
        return 'Can be Eaten'
    return 'Rotten'

def estimate_shelf_life(fruit, fresh_pct):
    max_days = SHELF_LIFE.get(fruit.lower(), 7)
    return max(0, round((fresh_pct / 100) * max_days))

def cleanup_uploads(max_age=3600):
    """Delete uploaded files older than max_age seconds."""
    now = time.time()
    try:
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            fp = os.path.join(app.config['UPLOAD_FOLDER'], f)
            try:
                if os.path.isfile(fp) and (now - os.path.getmtime(fp)) > max_age:
                    os.remove(fp)
            except Exception:
                pass
    except Exception:
        pass

# ── Routes ───────────────────────────────────────────────────────
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/app')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    preds        = Prediction.query.order_by(Prediction.created_at.desc()).all()
    total        = len(preds)
    fresh_count  = sum(1 for p in preds if p.verdict == 'Fresh')
    rotten_count = sum(1 for p in preds if p.verdict == 'Rotten')
    return render_template('history.html', predictions=preds,
                           total=total, fresh_count=fresh_count, rotten_count=rotten_count)

@app.route('/stats')
def stats_page():
    import json
    path = os.path.join('model', 'model_stats.json')
    if not os.path.exists(path):
        return '<h2 style="font-family:sans-serif;padding:40px">Run pretrain.py first.</h2>'
    with open(path) as f:
        return jsonify(json.load(f))

@app.route('/status')
def status():
    try:
        from model.train import training_state, MODEL_PATH
        model_ready = os.path.exists(MODEL_PATH)
        accuracy    = training_state['accuracy'] if training_state['accuracy'] else ('Ready' if model_ready else None)
        return jsonify({
            'model_ready':       model_ready,
            'training':          training_state['running'],
            'accuracy':          accuracy,
            'total_predictions': Prediction.query.count(),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    filepath = None
    try:
        from model.train import MODEL_PATH, preprocess
        import numpy as np

        # ── Validate request ─────────────────────────────────────
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file  = request.files['image']
        fruit = request.form.get('fruit', 'unknown').strip().lower()

        if not file or not file.filename:
            return jsonify({'error': 'Empty file received'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only JPG and PNG are accepted.'}), 400

        # ── Save upload ──────────────────────────────────────────
        ext      = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{fruit}_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Kick off background cleanup (non-blocking)
        threading.Thread(target=cleanup_uploads, daemon=True).start()

        # ── Model check ──────────────────────────────────────────
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                'label': 'Unknown', 'fresh_pct': 0,
                'fruit': fruit, 'filename': filename,
                'message': 'Model not trained yet. Run pretrain.py first.'
            })

        # ── Lazy-load model ──────────────────────────────────────
        model = get_model()
        if model is None:
            return jsonify({'error': 'Model could not be loaded. Check server logs.'}), 500

        # ── Inference ────────────────────────────────────────────
        arr   = preprocess(filepath)
        arr   = np.expand_dims(arr, axis=0)
        score = float(model.predict(arr, verbose=0)[0][0])

        rotten_pct = round(score * 100, 1)
        fresh_pct  = round((1 - score) * 100, 1)
        label      = 'Rotten' if score > 0.5 else 'Fresh'
        verdict    = get_verdict(fresh_pct)
        days_left  = estimate_shelf_life(fruit, fresh_pct)

        # ── Persist to DB ────────────────────────────────────────
        db.session.add(Prediction(
            fruit=fruit, verdict=verdict,
            fresh_pct=fresh_pct, filename=filename
        ))
        db.session.commit()

        return jsonify({
            'label': label, 'fresh_pct': fresh_pct, 'rotten_pct': rotten_pct,
            'fruit': fruit, 'filename': filename,
            'verdict': verdict, 'days_left': days_left,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Server error: ' + str(e)}), 500

# ── Entry point ──────────────────────────────────────────────────
if __name__ == '__main__':
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        local_ip = '0.0.0.0'
    print(f'\n * Network URL: http://{local_ip}:5000')
    print(f' * Local URL:   http://127.0.0.1:5000\n')
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
