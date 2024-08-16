from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

def generate_response(retrieved_docs, model_name="t5-base"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    input_text = " ".join([f"{doc[0]}: {doc[1]}" for doc in retrieved_docs])
    inputs = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    
    with torch.no_grad():
        outputs = model.generate(inputs, max_length=150, num_beams=5, early_stopping=True)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return response

if __name__ == "__main__":
    retrieved_docs = [("Document1", "This is content from document 1."),
                      ("Document2", "This is content from document 2.")]
    
    response = generate_response(retrieved_docs)
    print("Generated Response:")
    print(response)
