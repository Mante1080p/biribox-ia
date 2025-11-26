const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');

function addMessage(text, from='bot', id=null){
  // remove empty state
  const empty = document.querySelector('.empty');
  if(empty) empty.remove();

  const el = document.createElement('div');
  el.className = 'message ' + (from === 'user' ? 'user' : 'bot');
  if(id) el.dataset.id = id;
  el.textContent = text;
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return el;
}

function setTyping(el, on=true){
  if(!el) return;
  if(on){ el.textContent = 'Digitando...'; el.classList.add('typing'); }
  else el.classList.remove('typing');
}

async function sendMessage(){
  const text = inputEl.value.trim();
  if(!text) return;
  addMessage(text, 'user');
  inputEl.value = '';
  sendBtn.disabled = true;

  // placeholder bot message (typing)
  const botEl = addMessage('...', 'bot');
  setTyping(botEl, true);

  try {
    const res = await fetch('/perguntar', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({mensagem: text})
    });
    if(!res.ok){
      throw new Error('Status ' + res.status);
    }
    const data = await res.json();
    setTyping(botEl, false);
    botEl.textContent = data.resposta || 'Sem resposta.';
  } catch (err) {
    // fallback local "fachada" answer
    setTyping(botEl, false);
    console.error(err);
    const fallback = generateFallback(text);
    botEl.textContent = fallback;
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

function generateFallback(userText){
  const t = userText.toLowerCase();
  if(t.includes('docker')) return 'Docker é uma plataforma de containers que empacota aplicações com dependências.';
  if(t.includes('python')) return 'Python é uma linguagem de programação versátil, usada em web, IA e automação.';
  if(t.includes('api')) return 'API (Interface de Programação) permite que aplicações conversem entre si.';
  return 'Interessante pergunta. Em resumo: pesquise a documentação oficial ou peça um exemplo específico.';
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', e => { if(e.key === 'Enter') sendMessage(); });
clearBtn.addEventListener('click', () => { messagesEl.innerHTML = '<div class="empty">Envie uma pergunta sobre tecnologia</div>'; inputEl.focus(); });
inputEl.focus();