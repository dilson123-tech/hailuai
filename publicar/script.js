const form = document.getElementById('chatForm');
const respostaDiv = document.getElementById('resposta');
const limparBtn = document.getElementById('limparBtn');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const mensagem = document.getElementById('mensagem').value;

  respostaDiv.innerHTML = '<div class="typing">🤖 Pensando na melhor resposta pra sua empresa...</div>';


  try {
    const resposta = await fetch('http://localhost:8000/chat', {
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
  document.getElementById('mensagem').value = '';
  respostaDiv.style.opacity = '0';
  setTimeout(() => {
    respostaDiv.innerHTML = '';
    respostaDiv.style.opacity = '1';
  }, 300);
});
