import kagglehub
import os
import shutil

# Скачиваем датасет
path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
print(f"Dataset downloaded to: {path}")

# Копируем в нужную папку
os.makedirs("data/raw", exist_ok=True)
for file in os.listdir(path):
    if file.endswith(".csv"):
        shutil.copy(os.path.join(path, file), "data/raw/IMDB Dataset.csv")
        print("Copied to data/raw/IMDB Dataset.csv")