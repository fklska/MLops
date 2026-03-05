from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import load_dataset
from settings import MODEL_NAME, NUM_CLASSES, CPU
import torch


def tokenize_function(examples, tokenizer):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        
    )


def main():
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_CLASSES)
    dataset = load_dataset("stanfordnlp/imdb")

    dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        num_proc=CPU,
        remove_columns=["text"]
    )
    data_collator = DataCollatorWithPadding(tokenizer)

    torch.set_num_threads(CPU)
    torch.set_num_interop_threads(2)

    training_args = TrainingArguments(
        output_dir="bert",
        per_device_train_batch_size=8,
        num_train_epochs=2,
        # Gradient Checkpointing
        gradient_checkpointing=True,
        gradient_accumulation_steps=4,
        # Compilation
        torch_compile=False,
        # Logging & Monitoring Training
        logging_steps=1000,
        # Logging
        log_level="critical",
        disable_tqdm=False,
        # Evaluation
        eval_strategy="epoch",
        per_device_eval_batch_size=8,
        # Checkpointing & Saving
        save_only_model=True,
        save_strategy="epoch",
        save_total_limit=1,
        # Hardware Configuration
        use_cpu=True,
        # Dataloader                   
        dataloader_num_workers=2,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        data_collator=data_collator
    )

    trainer.train()


if __name__ == "__main__":
    main()