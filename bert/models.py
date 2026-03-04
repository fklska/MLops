from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from settings import MODEL_NAME, NUM_CLASSES, CPU

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_CLASSES)

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_strategy="steps",
    logging_steps=100,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    gradient_accumulation_steps=2,
    num_train_epochs=2,
    weight_decay=0.01,
    load_best_model_at_end=True,
    dataloader_num_workers=CPU,
    no_cuda=True,
    fp16=False,
    bf16=False
)
trainer = Trainer(
    model=model,
    args=training_args,
)