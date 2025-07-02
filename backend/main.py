from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Libera acesso de fora (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Rota raiz (mantém container Railway vivo)
@app.get("/")
def root():
    return {"status": "✅ HailuAI API online e funcionando!"}

# 🤖 Rota do chat
@app.post("/chat")
async def chat(request: Request):
    dados = await request.json()
    prompt = dados.get("mensagem")

    if not prompt:
        return {"resposta": "⚠️ Nenhuma mensagem enviada."}

    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente de IA especializado em ajudar empresas com inteligência artificial."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return {"resposta": resposta.choices[0].message.content}
