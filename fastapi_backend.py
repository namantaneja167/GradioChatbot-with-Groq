# fastapi_backend.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Load Hugging Face model and tokenizer
model_name = "gpt2"  # You can change this to any other suitable model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

class TextRequest(BaseModel):
    text: str
    max_length: int = 100

@app.post("/generate")
async def generate_text(request: TextRequest):
    try:
        # Tokenize input text
        input_ids = tokenizer.encode(request.text, return_tensors="pt")
        
        # Generate text
        output = model.generate(
            input_ids,
            max_length=request.max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )
        
        # Decode generated text
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        
        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)