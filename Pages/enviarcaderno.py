import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import date

SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para buscar dados
def get_caderno():
    response = supabase.table("caderno").select("*").execute()
    return response.data

# Função para adicionar dados
def add_caderno(conteudo, usuario, data_upload, data_aula, semana_aula, disciplina):
    supabase.table("caderno").insert({
        "conteudo": conteudo,
        "usuario": usuario,
        "data_upload": data_upload,
        "data_aula": data_aula,
        "semana_aula": semana_aula,
        "disciplina": disciplina
    }).execute()

# --- INTERFACE STREAMLIT ---
st.subheader("📘 Gerenciamento de Caderno da Turma", divider="rainbow", anchor=False)

# Expander com widgets para manipular os dados
usuario = st.session_state.usuario_logado
data_upload = date.today()
disciplinas = [
        "Métodologia de Projetos", "Estatística Empresarial",
        "Gestão Organizacional", "Infraestrutura de Redes",
        "Processo e Desv. de Sistemas"
    ]

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    data_aula = st.date_input("Data da Aula")
with col2:
    semana_aula = st.number_input("Semana da Aula", min_value=1, max_value=20, step=1, value=1)
with col3:
    disciplina = st.selectbox('Selecione a Disciplina', options=disciplinas, index=0)
conteudo = st.text_area("Conteúdo", placeholder="Digite o conteúdo do caderno...")

if st.button("Adicionar no Banco"):
    if conteudo and usuario and disciplina:
        add_caderno(conteudo, usuario, str(data_upload), str(data_aula), int(semana_aula), disciplina)
        st.success("✅ Registro adicionado com sucesso!")
    else:
        st.error("⚠️ Preencha todos os campos obrigatórios.")
    

# Exibir os dados cadastrados
st.subheader("📊 Registros do Caderno")
dados = get_caderno()

if dados:
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)
else:

    st.info("Nenhum registro encontrado.")


