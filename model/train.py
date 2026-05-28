import os
import numpy as np
import cv2
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, confusion_matrix)

MODEL_PATH  = os.path.join(os.path.dirname(__file__), 'freshness_model.h5')
DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
STATS_PATH  = os.path.join(os.path.dirname(__file__), 'model_stats.json')
IMG_SIZE    = (100, 100)
BATCH_SIZE  = 16


# ── OpenCV preprocessing ─────────────────────────────────────────
def preprocess(img_path):
    """
    Load image with OpenCV, apply:
      - resize to 100x100
      - Gaussian blur to reduce noise
      - CLAHE on L-channel for contrast enhancement
      - normalize to [0, 1]
    Returns numpy array shape (100, 100, 3) float32.
    """
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Cannot read image: {img_path}")

    img = cv2.resize(img, IMG_SIZE)

    # Denoise
    img = cv2.GaussianBlur(img, (3, 3), 0)

    # CLAHE contrast enhancement on L channel (LAB color space)
    lab   = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l     = clahe.apply(l)
    lab   = cv2.merge([l, a, b])
    img   = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # BGR → RGB, normalize
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img.astype(np.float32) / 255.0


# ── Model ────────────────────────────────────────────────────────
def build_model():
    model = models.Sequential([
        layers.Input(shape=(100, 100, 3)),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')   # 0=fresh, 1=rotten (alphabetical)
    ])
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    return model


def load_or_create_model():
    if os.path.exists(MODEL_PATH):
        return tf.keras.models.load_model(MODEL_PATH)
    return build_model()


# ── Dataset helpers ──────────────────────────────────────────────
def _count(folder):
    if not os.path.exists(folder):
        return 0
    return len([f for f in os.listdir(folder)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))])


def get_dataset_stats():
    fresh  = _count(os.path.join(DATASET_DIR, 'fresh'))
    rotten = _count(os.path.join(DATASET_DIR, 'rotten'))
    return {'fresh': fresh, 'rotten': rotten, 'total': fresh + rotten}


def has_enough_data():
    s = get_dataset_stats()
    return s['fresh'] >= 2 and s['rotten'] >= 2


def _load_dataset():
    images, labels = [], []
    for label_idx, cls in enumerate(['fresh', 'rotten']):
        folder = os.path.join(DATASET_DIR, cls)
        if not os.path.exists(folder):
            continue
        for fname in os.listdir(folder):
            if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            path = os.path.join(folder, fname)
            try:
                arr = preprocess(path)
                images.append(arr)
                labels.append(label_idx)
            except Exception as e:
                print(f"[FreshScan] Skipping {fname}: {e}")
    return np.array(images, dtype=np.float32), np.array(labels, dtype=np.float32)


# ── Training ─────────────────────────────────────────────────────
# Shared training state for status endpoint
training_state = {'running': False, 'accuracy': None, 'val_accuracy': None}


def retrain():
    global training_state
    if not has_enough_data():
        return False

    X, y = _load_dataset()
    if len(X) < 4:
        return False

    training_state['running'] = True
    try:
        model = build_model()
        X_aug, y_aug = _augment(X, y)

        # 80/20 train-test split on original (non-augmented) data
        split = int(len(X) * 0.8)
        idx   = np.random.permutation(len(X))
        train_idx, test_idx = idx[:split], idx[split:]
        X_test, y_test = X[test_idx], y[test_idx]

        # Augment only training data
        X_train_aug, y_train_aug = _augment(X[train_idx], y[train_idx])

        history = model.fit(
            X_train_aug, y_train_aug,
            epochs=30,
            batch_size=BATCH_SIZE,
            validation_split=0.2,
            verbose=1
        )
        model.save(MODEL_PATH)

        # ── Full evaluation on held-out test set ──────────────────
        y_pred_prob = model.predict(X_test, verbose=0).flatten()
        y_pred      = (y_pred_prob > 0.5).astype(int)
        y_true      = y_test.astype(int)

        acc       = round(accuracy_score(y_true, y_pred) * 100, 2)
        precision = round(precision_score(y_true, y_pred, zero_division=0) * 100, 2)
        recall    = round(recall_score(y_true, y_pred, zero_division=0) * 100, 2)
        f1        = round(f1_score(y_true, y_pred, zero_division=0) * 100, 2)
        cm        = confusion_matrix(y_true, y_pred).tolist()

        train_acc = round(history.history['accuracy'][-1] * 100, 2)
        val_acc   = round(history.history.get('val_accuracy', [0])[-1] * 100, 2)
        train_loss= round(history.history['loss'][-1], 4)
        val_loss  = round(history.history.get('val_loss', [0])[-1], 4)

        # Overfitting check
        gap = train_acc - val_acc
        if gap > 10:
            fit_status = f'Overfitting (gap: {gap:.1f}%)'
        elif gap < -5:
            fit_status = f'Underfitting (gap: {gap:.1f}%)'
        else:
            fit_status = f'Good fit (gap: {gap:.1f}%)'

        stats = {
            'dataset': {
                'total_images':    len(X),
                'fresh_images':    int(np.sum(y == 0)),
                'rotten_images':   int(np.sum(y == 1)),
                'train_samples':   len(train_idx),
                'test_samples':    len(test_idx),
                'train_split':     '80%',
                'test_split':      '20%',
                'after_augmentation': len(X_train_aug),
            },
            'training': {
                'epochs':          30,
                'batch_size':      BATCH_SIZE,
                'optimizer':       'Adam (lr=0.0001)',
                'loss_function':   'Binary Crossentropy',
                'train_accuracy':  train_acc,
                'val_accuracy':    val_acc,
                'train_loss':      train_loss,
                'val_loss':        val_loss,
                'fit_status':      fit_status,
            },
            'evaluation': {
                'test_accuracy':   acc,
                'precision':       precision,
                'recall':          recall,
                'f1_score':        f1,
                'confusion_matrix': cm,
                'notes': 'confusion_matrix: [[TN, FP], [FN, TP]] — 0=fresh, 1=rotten'
            }
        }

        with open(STATS_PATH, 'w') as f:
            json.dump(stats, f, indent=2)

        training_state['accuracy']     = acc
        training_state['val_accuracy'] = val_acc

        print('\n' + '='*55)
        print('  FRESHSCAN MODEL STATS')
        print('='*55)
        print(f'  Dataset        : {len(X)} images ({int(np.sum(y==0))} fresh, {int(np.sum(y==1))} rotten)')
        print(f'  Train/Test     : {len(train_idx)} / {len(test_idx)} (80/20 split)')
        print(f'  After augment  : {len(X_train_aug)} training samples')
        print(f'  Train accuracy : {train_acc}%')
        print(f'  Val accuracy   : {val_acc}%')
        print(f'  Test accuracy  : {acc}%')
        print(f'  Precision      : {precision}%')
        print(f'  Recall         : {recall}%')
        print(f'  F1 Score       : {f1}%')
        print(f'  Fit status     : {fit_status}')
        print(f'  Saved to       : {MODEL_PATH}')
        print('='*55 + '\n')
        return True
    finally:
        training_state['running'] = False


def _augment(X, y):
    """Simple augmentation: horizontal flip + slight brightness jitter."""
    aug_x, aug_y = list(X), list(y)
    for img, label in zip(X, y):
        aug_x.append(np.fliplr(img))
        aug_y.append(label)
        # brightness jitter ±15%
        factor = np.random.uniform(0.85, 1.15)
        aug_x.append(np.clip(img * factor, 0, 1))
        aug_y.append(label)
    return np.array(aug_x, dtype=np.float32), np.array(aug_y, dtype=np.float32)


# ── Prediction ───────────────────────────────────────────────────
def predict(img_path):
    """
    Returns (label, fresh_pct, rotten_pct).
    fresh_pct + rotten_pct = 100
    """
    model = load_or_create_model()
    arr   = preprocess(img_path)
    arr   = np.expand_dims(arr, axis=0)

    # sigmoid score: 0 = fully fresh, 1 = fully rotten
    score       = float(model.predict(arr, verbose=0)[0][0])
    rotten_pct  = round(score * 100, 1)
    fresh_pct   = round((1 - score) * 100, 1)
    label       = 'Rotten' if score > 0.5 else 'Fresh'
    return label, fresh_pct, rotten_pct
