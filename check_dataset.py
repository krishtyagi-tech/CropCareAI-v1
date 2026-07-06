import os

DATASET_PATH = "dataset/PlantVillage"

classes = sorted(os.listdir(DATASET_PATH))

print(f"Total Classes: {len(classes)}\n")

for cls in classes:
    path = os.path.join(DATASET_PATH, cls)

    if os.path.isdir(path):
        print(f"{cls} --> {len(os.listdir(path))} images")