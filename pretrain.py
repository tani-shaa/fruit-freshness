"""
Run this once to train the model on the full dataset before launching the app.
  python pretrain.py
"""

from model.train import retrain, get_dataset_stats

stats = get_dataset_stats()
print(f"Dataset — Fresh: {stats['fresh']}  Rotten: {stats['rotten']}  Total: {stats['total']}")

if stats['total'] < 4:
    print("\nNot enough images. Run prepare_dataset.py first.")
else:
    print("\nStarting training — this may take a few minutes...\n")
    success = retrain()
    if success:
        print("\nModel trained and saved to model/freshness_model.h5")
        print("You can now run:  python app.py")
    else:
        print("\nTraining failed. Check dataset/fresh and dataset/rotten folders.")
