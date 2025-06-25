from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import json

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def flan_t5_infer(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=128)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    try:
        return json.loads(response)
    except:
        return response  # fallback if not valid JSON