from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configuração do CORS (libera o acesso de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Rota raiz para evitar erro 404
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <h1>🚀 HailuAI API</h1>
    <p>API no ar com sucesso! Está tudo funcionando.</p>
    <p>Use o front-end para enviar suas mensagens para a IA.</p>
    """

# 🔍 Rota principal de análise
@app.post("/chat")
async def analisar_texto(request: Request):
    dados = await request.json()
    mensagem = dados.get("mensagem")

    if not mensagem:
        return JSONResponse(content={"erro": "Mensagem vazia."}, status_code=400)

    try:
        resposta = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional de IA para empresas."},
                {"role": "user", "content": mensagem}
            ]
        )

        resposta_ia = resposta.choices[0].message.content.strip()
        return {"resposta": resposta_ia}

    except Exception as e:
        return JSONResponse(content={"erro": f"Erro ao processar a mensagem: {str(e)}"}, status_code=500)
