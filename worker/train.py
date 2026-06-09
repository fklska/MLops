from core.db import get_training_data, mark_reviews_as_trained
from datasets import Dataset
from main import classifier, tokenizer
from register import reg_model
from transformers import DataCollatorWithPadding, Trainer, TrainingArguments

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

training_args = TrainingArguments(
    output_dir="model/",
    per_device_train_batch_size=32,
    num_train_epochs=1,
    gradient_checkpointing=False,
    gradient_accumulation_steps=2,
    fp16=True,
    use_cpu=True,
    torch_compile=False,
    logging_steps=20,
    disable_tqdm=False,
    save_only_model=True,
    save_strategy="epoch",
    save_total_limit=1,
    dataloader_num_workers=4,
    hub_model_id="fklska/bert-imdb",
)


def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=False, max_length=512)


def start_train():
    model = classifier.model
    texts, labels, ids = get_training_data()

    dataset = Dataset.from_dict({"text": texts, "label": labels}).map(tokenize_function)

    trainer = Trainer(model=model, args=training_args, train_dataset=dataset, data_collator=data_collator)

    trainer.train()

    reg_model(model, tokenizer)

    mark_reviews_as_trained(ids)


start_train()
