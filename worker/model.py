from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("fklska/bert-imdb")
tokenizer = AutoTokenizer.from_pretrained("fklska/bert-imdb")

save_path = "models/"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
