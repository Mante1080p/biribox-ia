import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Leia a variável de ambiente correta (NÃO coloque a chave diretamente no código)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Defina OPENAI_API_KEY no arquivo .env ou nas variáveis de ambiente.")

app = Flask(__name__)
CORS(app)

# Ajuste o modelo conforme sua conta (ex: "gpt-4o", "gpt-4", "gpt-5" se disponível)
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.2, openai_api_key=OPENAI_API_KEY)

# Memória simples em memória RAM por session_id
memories = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    session_id = data.get("session_id", "default")
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Campo 'message' obrigatório."}), 400

    # cria memória se necessário
    if session_id not in memories:
        memories[session_id] = ConversationBufferMemory(return_messages=True)

    chain = ConversationChain(llm=llm, memory=memories[session_id], verbose=False)

    # orienta o sistema para falar sobre tecnologia
    system_prompt = (
        "Você é um assistente especializado em tecnologia. Responda de forma clara, objetiva e"
        " com foco em conceitos, tutoriais curtos e recomendações práticas."
    )

    # gambiarras para incluir instrução do sistema no contexto inicial da conversa
    if not memories[session_id].buffer:  # primeira mensagem -> adicionar instrução inicial
        # enviar system prompt como primeira interação do usuário para preservar contexto
        chain.predict(input=system_prompt)

    resp = chain.predict(input=user_message)
    return jsonify({"response": resp})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)