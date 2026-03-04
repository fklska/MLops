from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from settings import MODEL_NAME, NUM_CLASSES, CPU

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_CLASSES)

training_args = TrainingArguments(
    output_dir="bert",  
    
)

trainer = Trainer(
    model=model,
    args=training_args,
)