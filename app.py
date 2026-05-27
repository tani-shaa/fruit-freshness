import os, uuid, threading, traceback, time, socket
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from database import db, Prediction

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH']             = 10 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///freshscan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXT   = {'jpg', 'jpeg', 'png'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

# Pre-load model at startup so first prediction is instant
_model_cache = None
def get_model():
    global _model_cache
    if _model_cache is None:
        from model.train import load_or_create_model
        _model_cache = load_or_create_model()
    return _model_cache

try:
    get_model()
    print('[FreshScan] Model loaded into memory.')
except Exception as e:
    print(f'[FreshScan] Model not loaded: {e}')

SHELF_LIFE = {
    'apple':14,'banana':5,'mango':6,'orange':14,'grapes':7,
    'strawberry':3,'watermelon':10,'pineapple':5,'papaya':5,
    'kiwi':7,'cherry':5,'pomegranate':14,'pear':7,'peach':5,'blueberry':7,
}

def allowed_file(f):
    return '.' in f and f.rsplit('.',1)[1].lower() in ALLOWED_EXT

def get_verdict(p):
    return 'Fresh' if p >= 70 else 'Can be Eaten' if p >= 40 else 'Rotten'

def estimate_shelf_life(fruit, fresh_pct):
    max_days = SHELF_LIFE.get(fruit.lower(), 7)
    return max(0, round((fresh_pct / 100) * max_days))

def cleanup_uploads(max_age=3600):
    now = time.time()
    for f in os.listdir(UPLOAD_FOLDER):
        fp = os.path.join(UPLOAD_FOLDER, f)
        try:
            if os.path.isfile(fp) and (now - os.path.getmtime(fp)) > max_age:
                os.remove(fp)
        except Exception:
            pass

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
    return jsonify(json.load(open(path)))

@app.route('/status')
def status():
    try:
        from model.train import training_state, MODEL_PATH
        model_ready = os.path.exists(MODEL_PATH)
        # If model exists but accuracy not in memory, show "Ready"
        accuracy = training_state['accuracy'] if training_state['accuracy'] else ('Ready' if model_ready else None)
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
    try:
        from model.train import MODEL_PATH, preprocess
        import numpy as np

        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file  = request.files['image']
        fruit = request.form.get('fruit', 'unknown')

        if not file.filename or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400

        ext      = file.filename.rsplit('.',1)[1].lower()
        filename = fruit + '_' + uuid.uuid4().hex[:8] + '.' + ext
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        threading.Thread(target=cleanup_uploads, daemon=True).start()

        if not os.path.exists(MODEL_PATH):
            return jsonify({
                'label':'Unknown', 'fresh_pct':0,
                'fruit':fruit, 'filename':filename,
                'message':'Model not trained yet. Run pretrain.py first.'
            })

        # Use cached model — no disk load on every request
        model = get_model()
        arr   = preprocess(filepath)
        arr   = np.expand_dims(arr, axis=0)
        score = float(model.predict(arr, verbose=0)[0][0])

        rotten_pct = round(score * 100, 1)
        fresh_pct  = round((1 - score) * 100, 1)
        label      = 'Rotten' if score > 0.5 else 'Fresh'
        verdict    = get_verdict(fresh_pct)
        days_left  = estimate_shelf_life(fruit, fresh_pct)

        db.session.add(Prediction(fruit=fruit, verdict=verdict, fresh_pct=fresh_pct, filename=filename))
        db.session.commit()

        return jsonify({
            'label':label, 'fresh_pct':fresh_pct, 'rotten_pct':rotten_pct,
            'fruit':fruit, 'filename':filename,
            'verdict':verdict, 'days_left':days_left,
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Server error: ' + str(e)}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Server error: ' + str(e)}), 500

if __name__ == '__main__':
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        local_ip = '0.0.0.0'
    print(f'\n * Network URL: http://{local_ip}:5000')
    print(f' * Local URL:   http://127.0.0.1:5000\n')
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)