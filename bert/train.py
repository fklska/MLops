from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset
from settings import MODEL_NAME, NUM_CLASSES, CPU
import torch


def tokenize_function(examples, tokenizer):
    return tokenizer(
        examples["text"],
    )


def main():
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_CLASSES)
    dataset = load_dataset("stanfordnlp/imdb")

    dataset = dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        num_proc=CPU,
        remove_columns=["text", "token_type_ids"]
    )
    torch.set_num_threads(CPU)
    torch.set_num_interop_threads(CPU)

    training_args = TrainingArguments(
        output_dir="bert",
        per_device_train_batch_size=8,
        num_train_epochs=2,

        # Gradient Checkpointing
        gradient_checkpointing=True,
        # Compilation
        torch_compile=True,
        # Logging & Monitoring Training
        logging_steps=1000,

        evaluation_strategy="epoch",
        per_device_eval_batch_size=8,
        use_cpu=True,                   
        dataloader_num_workers=0,
        gradient_accumulation_steps=4,
    )


"""
training_args = TrainingArguments(
    output_dir="bert",  
    
)

trainer = Trainer(
    model=model,
    args=training_args,
)
"""
if __name__ == "__main__":
    main()