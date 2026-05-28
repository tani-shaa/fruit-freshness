"""
One-shot migration script: converts freshness_model.h5 (old Keras serialization
format with `batch_shape`/`optional` parameters) to freshness_model.keras
(native Keras v3 format compatible with TensorFlow 2.15.0+).

Run once as a pre-deploy command:
    python model/migrate_model.py

The original .h5 file is left untouched so the migration is non-destructive.
After a successful migration the app will automatically prefer the new .keras
file (see load_or_create_model() in train.py).
"""

import os
import sys

# Suppress TF C++ noise
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf

_DIR       = os.path.dirname(__file__)
H5_PATH    = os.path.join(_DIR, 'freshness_model.h5')
KERAS_PATH = os.path.join(_DIR, 'freshness_model.keras')


def migrate():
    if not os.path.exists(H5_PATH):
        print(f'[migrate] Nothing to do — {H5_PATH} not found.')
        return False

    if os.path.exists(KERAS_PATH):
        print(f'[migrate] {KERAS_PATH} already exists — skipping migration.')
        return True

    print(f'[migrate] Loading {H5_PATH} ...')

    model = None

    # Strategy 1: safe_mode=False bypasses strict config validation introduced
    # in TF 2.14+ that rejects unknown keys like `batch_shape` and `optional`.
    try:
        model = tf.keras.models.load_model(H5_PATH, safe_mode=False)
        print('[migrate] Loaded with safe_mode=False.')
    except Exception as e1:
        print(f'[migrate] safe_mode=False failed: {e1}')

    # Strategy 2: pass an empty custom_objects dict — sometimes enough to
    # suppress the strict deserialisation path in older TF 2.x builds.
    if model is None:
        try:
            model = tf.keras.models.load_model(H5_PATH, custom_objects={})
            print('[migrate] Loaded with custom_objects={}.')
        except Exception as e2:
            print(f'[migrate] custom_objects={{}} failed: {e2}')

    # Strategy 3: compile=False skips optimizer/loss deserialisation entirely,
    # preserving weights and architecture even when config keys are unrecognised.
    if model is None:
        try:
            model = tf.keras.models.load_model(
                H5_PATH, compile=False, safe_mode=False
            )
            print('[migrate] Loaded with compile=False + safe_mode=False.')
        except Exception as e3:
            print(f'[migrate] compile=False failed: {e3}')

    if model is None:
        print('[migrate] ERROR: all loading strategies failed — cannot migrate.')
        sys.exit(1)

    # Resave in the native Keras v3 format (.keras).  This format stores the
    # full model config, weights, and optimizer state in a single zip archive
    # and is the recommended format for TF 2.12+.
    print(f'[migrate] Saving to {KERAS_PATH} ...')
    model.save(KERAS_PATH)
    print('[migrate] Migration complete.')
    return True


if __name__ == '__main__':
    migrate()
