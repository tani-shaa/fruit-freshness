"""
Run this once to prepare the Kaggle dataset.
Automatically extracts the zip and organises images into dataset/fresh and dataset/rotten.

Usage:
    python prepare_dataset.py
"""

import os, shutil, zipfile

ZIP_PATH   = r'C:\Users\tanis\OneDrive\Desktop\fruit_freshness\dataset.zip'
EXTRACT_TO = 'dataset_raw'
DEST_FRESH  = os.path.join('dataset', 'fresh')
DEST_ROTTEN = os.path.join('dataset', 'rotten')

os.makedirs(DEST_FRESH,  exist_ok=True)
os.makedirs(DEST_ROTTEN, exist_ok=True)

# Step 1 — extract zip
if not os.path.exists(EXTRACT_TO):
    print('Extracting zip...')
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        z.extractall(EXTRACT_TO)
    print('Extracted.')
else:
    print('Already extracted, skipping.')

# Step 2 — walk extracted folder and copy images
copied_fresh = copied_rotten = skipped = 0

for root, dirs, files in os.walk(EXTRACT_TO):
    folder_name = os.path.basename(root).lower()

    if folder_name.startswith('fresh'):
        dest = DEST_FRESH
    elif folder_name.startswith('rotten'):
        dest = DEST_ROTTEN
    else:
        continue

    for fname in files:
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        src = os.path.join(root, fname)
        # prefix with folder name to avoid collisions
        dst = os.path.join(dest, folder_name + '_' + fname)
        if os.path.exists(dst):
            skipped += 1
            continue
        shutil.copy2(src, dst)
        if dest == DEST_FRESH:
            copied_fresh += 1
        else:
            copied_rotten += 1

print(f'\nDone.')
print(f'  Fresh  → dataset/fresh/  : {copied_fresh} images')
print(f'  Rotten → dataset/rotten/ : {copied_rotten} images')
print(f'  Skipped (duplicates)     : {skipped}')
print(f'\nTotal: {copied_fresh + copied_rotten} images')
print('\nNow run: python pretrain.py')
