import streamlit as st
import requests

st.subheader("📈 Estatística Empresarial", divider="rainbow", anchor=False)

# URL do webhook do n8n
WEBHOOK_URL = "https://n8n.srv1101373.hstgr.cloud/webhook-test/0304b731-1a3b-47d3-98d2-d1377c024abc"

st.title("Envio de Webhook para n8n")

dados = st.text_input("Digite algo para enviar ao n8n:")

if st.button("Enviar para n8n"):
    payload = {"message": dados}
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        st.success("Dados enviados com sucesso ao n8n!")
    else:
        st.error(f"Erro: {response.text}")