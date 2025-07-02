from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Libera o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: coloque seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Rota para verificar status da API
@app.get("/")
def root():
    return {"mensagem": "🚀 HailuAI API no ar com sucesso!"}

# 🤖 Rota de chat com IA
@app.post("/chat")
async def chat(request: Request):
    dados = await request.json()
    mensagem_usuario = dados.get("mensagem")

    if not mensagem_usuario:
        return {"resposta": "⚠️ Nenhuma mensagem foi enviada."}

    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": mensagem_usuario}],
        temperature=0.7
    )

    texto_gerado = resposta.choices[0].message.content
    return {"resposta": texto_gerado}
