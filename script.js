const form = document.getElementById('chatForm');
const respostaDiv = document.getElementById('resposta');
const limparBtn = document.getElementById('limparBtn');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const mensagem = document.getElementById('mensagem').value;

  respostaDiv.innerHTML = "<em>🤖 Pensando na resposta...</em>";

  try {
    const resposta = await fetch('https://hailuai-backend.up.railway.app/chat', {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ mensagem }),
    });

    const data = await resposta.json();
    respostaDiv.innerHTML = `<strong>Resposta:</strong><br>${data.resposta}`;
  } catch (error) {
    respostaDiv.innerHTML = "❌ Erro ao conectar com a IA.";
  }
});

limparBtn.addEventListener('click', () => {
  document.getElementById('mensagem').value = "";
  respostaDiv.innerHTML = "";
});
