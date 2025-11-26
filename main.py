import re
import unicodedata
import difflib
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="../Frontend", static_folder="../Frontend", static_url_path="/static")

# Perguntas e respostas pré-programadas (mantém forma original para leitura)
respostas = {
    "oi": "Oi, tudo bem?",
    "tudo bem": "Estou bem! E você?",
    "qual seu nome": "Meu nome é Biribox!",
    "tchau": "Até mais!",
    "o que é uma inteligência artificial?": "Inteligência Artificial é a área da computação que cria sistemas capazes de realizar tarefas que normalmente exigem inteligência humana, como reconhecer voz, entender texto, aprender padrões e tomar decisões.",
    "o que é um modelo de ia?": "Um modelo de IA é uma representação matemática ou computacional que é treinada para realizar tarefas específicas, como reconhecimento de imagem, processamento de linguagem natural ou tomada de decisões.",
    "ia vai substituir os humanos?": "A IA é projetada para complementar e auxiliar os humanos, não para substituí-los completamente. Ela pode automatizar tarefas repetitivas e ajudar na tomada de decisões, mas muitas funções ainda exigem criatividade e julgamento humano.",
    "o que é deep learning?": "Deep Learning é um subcampo do Machine Learning que utiliza redes neurais profundas para aprender representações hierárquicas a partir de grandes volumes de dados.",
    "qual a diferença entre aprendizado supervisionado e não supervisionado?": "Aprendizado supervisionado usa dados rotulados para treinar modelos; não supervisionado busca padrões e estruturas em dados sem rótulos.",
    "o que é uma rede neural?": "Uma rede neural é um modelo inspirado no cérebro composto por camadas de unidades (neurônios) que aprendem pesos para mapear entradas em saídas.",
    "o que são embeddings?": "Embeddings são vetores numéricos que representam palavras, sentenças ou documentos em um espaço contínuo onde similaridade semântica é preservada.",
    "o que é fine-tuning?": "Fine-tuning é o ajuste de um modelo pré-treinado em um conjunto de dados específico para melhorar desempenho em uma tarefa alvo.",
    "o que é prompt engineering?": "Prompt engineering são técnicas para formular entradas (prompts) ao modelo de forma a guiar saídas desejadas sem re-treinar o modelo.",
    "o que é transformer?": "Transformer é uma arquitetura baseada em atenção que revolucionou NLP por modelar dependências entre tokens de forma eficiente e escalável.",
    "o que é overfitting?": "Overfitting ocorre quando um modelo aprende detalhes e ruído do conjunto de treino e falha em generalizar para dados novos.",
    "o que é reinforcement learning?": "Reinforcement Learning é um paradigma onde um agente aprende a tomar ações em um ambiente para maximizar uma recompensa acumulada.",
    "o que é transferência de aprendizado?": "Transfer learning consiste em reutilizar um modelo ou partes dele treinadas em uma tarefa para acelerar ou melhorar o treinamento em outra tarefa.",
    "o que é hallucination em modelos de linguagem?": "Hallucination é quando o modelo gera informações incorretas ou inventadas com aparência de verdade.",
    "como melhorar explicabilidade de modelos?": "Use modelos mais simples, técnicas de interpretação (ex: SHAP, LIME), visualizações de atenção e documentação clara do processo de treino.",
    "quais os riscos éticos da ia?": "Riscos incluem vieses, violação de privacidade, desinformação e uso indevido; mitigação exige governança, auditoria e diversidade de dados.",
    "qual a diferença entre inferência e treinamento?": "Treinamento ajusta os parâmetros do modelo (alto custo computacional); inferência aplica o modelo treinado para gerar previsões (geralmente menos custoso).",
    "o que é um dataset balanceado?": "Um dataset balanceado tem distribuição similar entre classes, reduzindo viés e melhorando a performance do modelo para todas as classes."
}

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    # remove acentos
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    # Keep letters, numbers and spaces only
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

# mapa normalizado -> resposta
normalized_map = {normalize_text(k): v for k, v in respostas.items()}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/perguntar", methods=["POST"])
def perguntar():
    data = request.get_json() or {}
    mensagem = data.get("mensagem", "")
    if not mensagem or not mensagem.strip():
        return jsonify({"resposta": "Envie uma mensagem válida."}), 400

    norm = normalize_text(mensagem)
    # match exato
    if norm in normalized_map:
        return jsonify({"resposta": normalized_map[norm]})

    # match aproximado
    close = difflib.get_close_matches(norm, normalized_map.keys(), n=1, cutoff=0.6)
    if close:
        return jsonify({"resposta": normalized_map[close[0]]})

    # fallback
    return jsonify({"resposta": "Não entendi, pode reformular ou ser mais específico?"})

if __name__ == "__main__":
    app.run(debug=True)