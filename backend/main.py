from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Libera acesso de fora
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (ideal ajustar em produção)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa cliente OpenAI com a chave secreta
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Rota raiz só pra manter o container vivo
@app.get("/")
def root():
    return {"status": "✅ HailuAI API online e funcionando!"}

# 🤖 Rota principal da IA
@app.post("/chat")
async def chat(request: Request):
    dados = await request.json()
    mensagem_usuario = dados.get("mensagem")

    if not mensagem_usuario:
        return {"resposta": "⚠️ Nenhuma mensagem enviada."}

    resposta = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": mensagem_usuario}],
        temperature=0.7
    )

    texto_gerado = resposta.choices[0].message.content
    return {"resposta": texto_gerado}
