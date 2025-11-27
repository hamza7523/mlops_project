import os
import torch
import io
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification, AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError: pass 

app = FastAPI(title="Flora-Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

CV_DIR = "./flora_cv_model"
RAG_DIR = "./flora_rag_db"
LLM_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 


sys_comps = {}

@app.on_event("startup")
async def startup_event():
    print("⚙️ Initializing Free Tier Mode (CPU)...")
    
    if not os.path.exists(CV_DIR):
        raise RuntimeError("❌ Models missing! Run download_models.py")
    
    sys_comps['cv_proc'] = AutoImageProcessor.from_pretrained(CV_DIR)
    sys_comps['cv_model'] = AutoModelForImageClassification.from_pretrained(CV_DIR)
    
    embed_fn = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    sys_comps['rag'] = Chroma(persist_directory=RAG_DIR, embedding_function=embed_fn)
    
   
    print(f"Loading {LLM_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(LLM_ID)
    model = AutoModelForCausalLM.from_pretrained(LLM_ID)
    
    sys_comps['llm'] = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=256,
        device_map="cpu" 
    )
    sys_comps['tokenizer'] = tokenizer
    print("API READY.")

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
       
        img = Image.open(io.BytesIO(await file.read())).convert("RGB")
        inputs = sys_comps['cv_proc'](img, return_tensors="pt")
        with torch.no_grad():
            outputs = sys_comps['cv_model'](**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            conf, pred_idx = torch.max(probs, dim=-1)
            diagnosis = sys_comps['cv_model'].config.id2label[pred_idx.item()]

  
        docs = sys_comps['rag'].similarity_search(
            query=f"{diagnosis} treatment", k=2, filter={"disease": diagnosis}
        )
       
        if not docs: docs = sys_comps['rag'].similarity_search(f"{diagnosis} treatment", k=2)
        context_text = "\n".join([d.page_content[:500] for d in docs]) 

    
        prompt = f"<|system|>\nYou are a botanist. Explain {diagnosis} and treatment based on context.\n<|user|>\nContext: {context_text}\n<|assistant|>\n"
        output = sys_comps['llm'](prompt)
        response = output[0]['generated_text'].split("<|assistant|>\n")[-1].strip()

        return {
            "diagnosis": diagnosis,
            "confidence": f"{conf.item()*100:.1f}%",
            "explanation": response,
            "chat_context": context_text
        }
    except Exception as e:
        return {"error": str(e)}

class ChatPayload(BaseModel):
    question: str
    context: str
    diagnosis: str

@app.post("/chat")
async def chat(payload: ChatPayload):
    prompt = f"<|system|>\nAnswer based on context.\n<|user|>\nContext: {payload.context}\nQuestion: {payload.question}\n<|assistant|>\n"
    output = sys_comps['llm'](prompt)
    return {"answer": output[0]['generated_text'].split("<|assistant|>\n")[-1].strip()}