from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Libera o acesso do front (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina o domínio exato
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo da mensagem
class Mensagem(BaseModel):
    mensagem: str

# Rota principal de chat
@app.post("/chat")
async def chat(mensagem: Mensagem):
    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é o HailuAI, um assistente de IA para empresas. Responda de forma educada, profissional e direta."},
            {"role": "user", "content": mensagem.mensagem}
        ]
    )
    return {"resposta": resposta.choices[0].message.content}
