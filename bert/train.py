"""
Обучение модели DistilBERT для классификации тональности отзывов IMDB.
Использует библиотеку datasets и Trainer из transformers.
Адаптировано под transformers 5.2.0
"""
import os
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from datasets import Dataset
import torch

# ========== КОНФИГУРАЦИЯ ==========
DATA_PATH = "data/raw/IMDB Dataset.csv"
MODEL_OUTPUT_DIR = "models/bert/saved_model"
MODEL_NAME = "distilbert-base-uncased"

# Для быстрого теста: поставьте None для полного датасета, или число для сэмпла
SAMPLE_SIZE = 5000  # 5000 для быстрого теста, потом None или 50000

EPOCHS = 2
BATCH_SIZE = 16
LEARNING_RATE = 2e-5
MAX_LENGTH = 256
TEST_SIZE = 0.2
RANDOM_SEED = 42
# ==================================

def compute_metrics(eval_pred):
    """Метрики для оценки"""
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    acc = accuracy_score(labels, predictions)
    f1 = f1_score(labels, predictions, average='binary')
    return {
        'accuracy': acc,
        'f1': f1
    }

def main():
    print("=" * 50)
    print("НАЧАЛО ОБУЧЕНИЯ")
    print("=" * 50)
    
    # 1. Загрузка данных
    print("\nЗагрузка данных...")
    start = time.time()
    df = pd.read_csv(DATA_PATH)
    df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})
    print(f"Данные загружены за {time.time() - start:.2f} сек, размер: {len(df)}")
    
    # 2. Сэмплирование (опционально)
    if SAMPLE_SIZE and SAMPLE_SIZE < len(df):
        df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED)
        print(f"Используем сэмпл: {len(df)} строк")
    
    # 3. Разделение на train/val
    print("\nРазделение данных...")
    start = time.time()
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['review'].tolist(),
        df['sentiment'].tolist(),
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=df['sentiment'].tolist()
    )
    print(f"Разделение завершено за {time.time() - start:.2f} сек")
    print(f"Train: {len(train_texts)}, Val: {len(val_texts)}")
    
    # 4. Создание Dataset из списков
    print("\nСоздание датасетов...")
    train_dataset = Dataset.from_dict({
        'text': train_texts,
        'label': train_labels
    })
    val_dataset = Dataset.from_dict({
        'text': val_texts,
        'label': val_labels
    })
    
    # 5. Токенизация
    print("\nЗагрузка токенизатора...")
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)
    
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            padding='max_length',
            max_length=MAX_LENGTH
        )
    
    print("Токенизация train...")
    start = time.time()
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    print(f"Токенизация train завершена за {time.time() - start:.2f} сек")
    
    print("Токенизация val...")
    start = time.time()
    val_dataset = val_dataset.map(tokenize_function, batched=True)
    print(f"Токенизация val завершена за {time.time() - start:.2f} сек")
    
    # Удаляем текстовое поле (оставляем только input_ids, attention_mask, label)
    train_dataset = train_dataset.remove_columns(['text'])
    val_dataset = val_dataset.remove_columns(['text'])
    
    # 6. Загрузка модели
    print("\nЗагрузка модели...")
    start = time.time()
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        ignore_mismatched_sizes=True
    )
    print(f"Модель загружена за {time.time() - start:.2f} сек")
    
    # 7. Настройка Trainer (адаптировано под transformers 5.2.0)
    training_args = TrainingArguments(
        output_dir='./models/bert/training_output',
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LEARNING_RATE,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=100,
        eval_strategy="epoch",  # вместо evaluation_strategy
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=2,
        report_to="none",  # отключаем mlflow для первого запуска
        fp16=False  # если нет GPU, оставляем False
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    # 8. Обучение
    print("\n" + "=" * 50)
    print("НАЧАЛО ОБУЧЕНИЯ")
    print("=" * 50)
    start = time.time()
    trainer.train()
    print(f"\nОбучение завершено за {time.time() - start:.2f} сек")
    
    # 9. Сохранение модели
    print("\nСохранение модели...")
    os.makedirs(MODEL_OUTPUT_DIR, exist_ok=True)
    model.save_pretrained(MODEL_OUTPUT_DIR)
    tokenizer.save_pretrained(MODEL_OUTPUT_DIR)
    print(f"Модель сохранена в {MODEL_OUTPUT_DIR}")
    
    # 10. Финальная оценка
    print("\nФинальная оценка...")
    eval_results = trainer.evaluate()
    print(f"Accuracy: {eval_results['eval_accuracy']:.4f}")
    print(f"F1 Score: {eval_results['eval_f1']:.4f}")
    print("\n" + "=" * 50)
    print("ОБУЧЕНИЕ ЗАВЕРШЕНО УСПЕШНО")
    print("=" * 50)

if __name__ == "__main__":
    main()