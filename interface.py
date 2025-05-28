import streamlit as st
import requests

st.set_page_config(page_title="Chat Médico com IA", layout="centered")

st.title("🩺 Simulador de Paciente com IA")
st.markdown("Converse com o paciente simulado. Envie sua pergunta abaixo.")

# Histórico de conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# Exibe as mensagens anteriores
for msg in st.session_state.mensagens:
    with st.chat_message(msg["autor"]):
        st.markdown(msg["texto"])

# Caixa de entrada do usuário
pergunta = st.chat_input("Digite sua pergunta como médico...")

if pergunta:
    # Adiciona pergunta ao histórico
    st.session_state.mensagens.append({"autor": "user", "texto": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Envia a pergunta ao backend FastAPI
    try:
        resposta = requests.post("http://127.0.0.1:8000/consulta", json={"pergunta": pergunta})
        resposta_json = resposta.json()

        resposta_paciente = resposta_json.get("resposta", "Erro ao obter resposta.")
    except Exception as e:
        resposta_paciente = f"Erro: {e}"

    # Adiciona resposta ao histórico
    st.session_state.mensagens.append({"autor": "assistant", "texto": resposta_paciente})
    with st.chat_message("assistant"):
        st.markdown(resposta_paciente)

