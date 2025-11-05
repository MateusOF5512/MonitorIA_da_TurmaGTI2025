import streamlit as st
from datetime import date
import pdfplumber
import requests

# ------------------- FUNÇÕES -------------------

def extract_text_from_pdf(uploaded_file):
    """
    Extrai texto de PDF usando pdfplumber
    """
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def enviar_n8n(dados):
    """
    Envia dados para webhook n8n (teste + produção)
    """

    WEBHOOK_URLS = "https://n8n.srv1101373.hstgr.cloud/webhook-test/caderno-turma"
    response = requests.post(WEBHOOK_URLS, json=dados)
    if response.status_code == 200:
        st.success("✅ Dados enviados com sucesso (TESTE)!")
        return None

    if response.status_code != 200:
        WEBHOOK_URLS2 = "https://n8n.srv1101373.hstgr.cloud/webhook/caderno-turma"
        response = requests.post(WEBHOOK_URLS2, json=dados)
        if response.status_code == 200:
            st.success("✅ Dados enviados com sucesso (PRODUÇÃO)!")
            return None
    else:
        st.error(f"❌ Erro ao enviar dados: {response.text}")

    return None


# ------------------- INTERFACE -------------------

st.set_page_config(page_title="Envio de Caderno", page_icon="📚", layout="wide")
st.title("📚 Gerenciamento de Caderno/Aula")

with st.sidebar:
    menu = st.radio(
        "Selecione uma opção para enviar:",
        ["Texto Copia e Cola", "PDF"]
    )

usuario = st.session_state.get("usuario_logado", "Usuário desconhecido")
data_upload = date.today()
disciplinas = [
    "Métodologia de Projetos",
    "Estatística Empresarial",
    "Gestão Organizacional",
    "Infraestrutura de Redes",
    "Processo e Desv. de Sistemas"
]

# ------------------- MENU: TEXTO -------------------
if menu == "Texto Copia e Cola":
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        data_aula = st.date_input("Data da Aula", value=data_upload)
    with col2:
        semana_aula = st.number_input("Semana da Aula", min_value=1, max_value=20, step=1, value=1)
    with col3:
        disciplina = st.selectbox("Selecione a Disciplina", options=disciplinas)

    conteudo = st.text_area("Conteúdo", placeholder="Digite o conteúdo do caderno...")

    if st.button("📤 Adicionar no Banco"):
        if conteudo.strip() == "":
            st.warning("📌 O conteúdo não pode estar vazio.")
        else:
            dados = {
                "conteudo": conteudo,
                "usuario": usuario,
                "data_upload": str(data_upload),
                "data_aula": str(data_aula),
                "semana_aula": int(semana_aula),
                "disciplina": disciplina
            }
            enviar_n8n(dados)

# ------------------- MENU: PDF -------------------
elif menu == "PDF":
    st.write("📄 Carregue um PDF e extraia todo o conteúdo em Markdown")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        data_aula = st.date_input("Data da Aula", value=data_upload, key=77)
    with col2:
        semana_aula = st.number_input("Semana da Aula", min_value=1, max_value=20, step=1, value=1, key=78)
    with col3:
        disciplina = st.selectbox("Selecione a Disciplina", options=disciplinas, key=79)

    uploaded_file = st.file_uploader("📂 Selecione o arquivo PDF com conteúdo da aula:", type=["pdf"])

    if uploaded_file:
        st.success(f"Arquivo carregado: {uploaded_file.name}")


        with st.spinner("⌛ Extraindo texto do PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        with st.expander("Arquivo PDF em Markdown"):
            if extracted_text.strip() == "":
                st.warning("⚠️ Nenhum texto encontrado no PDF. Talvez seja uma imagem ou PDF protegido.")
            else:
                # Exibir Markdown
                st.markdown("### ✅ Conteúdo extraído:")
                st.markdown(extracted_text)

            dados = {
                    "conteudo": extracted_text,
                    "usuario": usuario,
                    "data_upload": str(data_upload),
                    "data_aula": str(data_upload),
                    "semana_aula": semana_aula,
                    "disciplina": disciplina,
            }
        enviar_n8n(dados)

    else:
        st.info("📥 Envie um PDF para começar ✅")
