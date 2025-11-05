import streamlit as st
import requests
import time

# ================================================================
# CONFIGURAÇÃO GERAL
# ================================================================
st.set_page_config(page_title="MonitorIA da Turma", page_icon="🎓", layout="centered")

# Inicializa variáveis de sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "resposta_agent" not in st.session_state:
    st.session_state.resposta_agent = []

# Variáveis auxiliares
resposta_agent = ''
elapsed = 0.00
total_tokens = 0
prompt_tokens = 0
completion_tokens = 0

usuario_app = st.session_state.get("usuario_logado", "usuário_teste")
start_time = 0

# URL do webhook do n8n
N8N_WEBHOOK_URL = "https://n8n.srv1101373.hstgr.cloud/webhook/monitor-ia"

# ================================================================
# SIDEBAR
# ================================================================
with st.sidebar:
    st.title("⚙️ Configurações")
    st.markdown("O chat está conectado ao agente via **n8n**.")
    st.divider()

# ================================================================
# CABEÇALHO
# ================================================================
st.subheader("👨‍🏫 MonitorIA da Turma", divider="rainbow")

# ================================================================
# HISTÓRICO DE MENSAGENS
# ================================================================
for mensagem in st.session_state.mensagens:
    avatar = "👨‍🏫" if mensagem["role"] == "assistant" else "👨‍🎓"
    with st.chat_message(mensagem["role"], avatar=avatar):
        st.markdown(mensagem["content"])

# ================================================================
# CAMPO DE ENTRADA DO USUÁRIO
# ================================================================
if prompt := st.chat_input("Digite sua pergunta para o MonitorIA..."):
    # Adiciona mensagem do usuário no histórico
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    # ============================================================
    # ENVIA MENSAGEM PARA O N8N VIA WEBHOOK
    # ============================================================
    try:
        start_time = time.time()

        payload = {
            "mensagem": prompt,
            "usuario": usuario_app,
        }

        resposta = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,
            timeout=120
        )

        if resposta.status_code == 200:
            data = resposta.json()

            # Caso a resposta venha dentro de lista
            if isinstance(data, list):
                data = data[0]

            # Captura os campos retornados pelo agente
            resposta_agent = data.get("resposta_agent_rag", "⚠️ Nenhuma resposta recebida.")
            total_tokens = data.get("totalTokens", 0)
            prompt_tokens = data.get("promptTokens", 0)
            completion_tokens = data.get("completionTokens", 0)

        else:
            resposta_agent = f"⚠️ Erro na resposta do agente: {resposta.status_code}"

    except Exception as e:
        resposta_agent = f"⚠️ Erro na conexão com o agente: {e}"

    # ============================================================
    # EXIBE RESPOSTA DO AGENTE
    # ============================================================
    elapsed = time.time() - start_time

    with st.chat_message("assistant", avatar="👨‍🏫"):
        st.markdown(resposta_agent)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta_agent})

# ================================================================
# SIDEBAR: MÉTRICAS
# ================================================================
with st.sidebar:
    st.sidebar.markdown(f"⏱️ Tempo de resposta: {elapsed:.2f}s")
    st.sidebar.markdown(f"🧮 Total de Tokens: {total_tokens}")
    st.sidebar.markdown(f"💬 Entrada de Tokens: {prompt_tokens}")
    st.sidebar.markdown(f"✍️ Saída de Tokens: {completion_tokens}")

    st.divider()
    if st.button("🔄 Reiniciar conversa"):
        st.session_state.mensagens = []
        st.rerun()
