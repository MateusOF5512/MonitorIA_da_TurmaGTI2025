import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
import json
from Functions.database import *
from Functions.grok import *


if "selected_model" not in st.session_state:
    st.session_state.selected_model = []

with st.sidebar:

    with st.container(border=True):
        models = {
            "groq/compound-mini": {"name": "Gorq | Compound Mini | 09/2023", "tokens": 8192},
            "groq/compound": {"name": "Gorq | Compound | 09/2023", "tokens": 8192},
            "openai/gpt-oss-20b": {"name": "OpenAI | GPT OSS 20B | 08/2025", "tokens": 65536},
            "openai/gpt-oss-120b": {"name": "OpenAI | GPT OSS 120B | 08/2025", "tokens": 65536},
            "gemma2-9b-it": {"name": "Google | Gemma 2 9B | 09/2023", "tokens": 8192},
            "llama-3.3-70b-versatile": {"name": "Meta | Llama 3.3 70B | 12/2024", "tokens": 32768},
            "meta-llama/llama-4-maverick-17b-128e-instruct": {"name": "Meta | Llama 4 Maverick 17B | 04/2025", "tokens": 8192,},
            "qwen/qwen3-32b": {"name":"Alibaba | Qwen3 32B | 05/2025", "tokens": 16384},
            "deepseek-r1-distill-llama-70b": {"name": "DeepSeek | R1 Llama 70B | 01/2025", "tokens": 4096}
        }

        model_options = st.selectbox(
                "Selecione um Modelo de Linguagem Natural:",
                options=list(models.keys()),
                format_func=lambda x: models[x]["name"],
                index=0
            )

        if st.session_state.selected_model != model_options:
            st.session_state.mensagem = []
            st.session_state.selected_model = model_options
            st.rerun()

        temperature = st.slider("Selecione a Criatividade do Modelo:",
                               min_value=0.1, max_value=2.0,
                               value=0.4, step=0.2)

# --- Interface ---
st.header("🌐 Infraestrutura de Redes", divider="rainbow", anchor=False)


with st.container(border=True):
    dados_supa1 = get_data_disciplina("Infraestrutura de Redes", 1)


    st.subheader("Semana 1 - 18/08/2025", divider="green", anchor=False)

    df1 = pd.DataFrame(dados_supa1)

    st.dataframe(df1, use_container_width=True)
    st.markdown("")

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        st.markdown("")
    with col2:
        st.markdown("")
    with col3:
        resumo = st.button("Resumo da Aula 1")
    with col4:
        st.markdown("")
    with col5:
        st.markdown("")

    st.markdown("---")

    if resumo:
        try:
            dados1 = transforma_json(df1)

            # Chamada à IA e Captura da resposta
            resposta = chat_completion_disciplina(dados1, model_options, temperature)

            # Exibição no Markdown
            st.subheader("📌 Resumo Gerado pela IA")
            st.markdown(resposta)

        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")

with st.container(border=True):

    dados2 = get_data_disciplina("Infraestrutura de Redes", 2)

    
    if dados2 and len(dados2) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 2 - 25/08/2025", divider="green", anchor=False)
        st.dataframe(dados2, key=22)

        st.markdown("")

        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.markdown("")
        with col2:
            st.markdown("")
        with col3:
            resumo = st.button("Resumo da Aula 2")
        with col4:
            st.markdown("")
        with col5:
            st.markdown("")

        st.markdown("---")

        if resumo:
            try:
                dados2 = transforma_json(dados2)

                # Chamada à IA e Captura da resposta
                resposta = chat_completion_disciplina(dados2, model_options, temperature)

                # Exibição no Markdown
                st.subheader("📌 Resumo Gerado pela IA")
                st.markdown(resposta)

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

    else:
        # Se não retornou nada → divider vermelho e mensagem de aviso
        st.subheader("Semana 2 - 25/08/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):

    dados_supa3 = get_data_disciplina("Infraestrutura de Redes", 3)

    if dados_supa3 and len(dados_supa3) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 3 - 01/09/2025", divider="green", anchor=False)

        df3 = pd.DataFrame(dados_supa3)
        st.dataframe(df3, key=23)

        st.markdown("")

        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.markdown("")
        with col2:
            st.markdown("")
        with col3:
            resumo3 = st.button("Resumo da Aula 3", key="botao_resumo3")
        with col4:
            st.markdown("")
        with col5:
            st.markdown("")

        st.markdown("---")

        if resumo3:
            try:
                dados_json3 = transforma_json(df3)

                # Chamada à IA e Captura da resposta
                resposta3 = chat_completion_disciplina(dados_json3, model_options, temperature)

                # Exibição no Markdown
                st.markdown(resposta3)

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

    else:
        # Se não retornou nada → divider vermelho e mensagem de aviso
        st.subheader("Semana 3 - 01/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):

    dados = get_data_disciplina("Infraestrutura de Redes", 4)
    if dados and len(dados) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 4 - 08/09/2025", divider="green", anchor=False)
        st.dataframe(dados, key=24)
    else:
        # Se não retornou nada → divider vermelho e mensagem de aviso
        st.subheader("Semana 4 - 08/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 5)
    if dados and len(dados) > 0:
        st.subheader("Semana 5 - 15/09/2025", divider="green", anchor=False)
        st.dataframe(dados, key=25)
    else:
        st.subheader("Semana 5 - 15/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 6)
    if dados and len(dados) > 0:
        st.subheader("Semana 6 - 22/09/2025", divider="green", anchor=False)
        st.dataframe(dados, key=26)
    else:
        st.subheader("Semana 6 - 22/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados7 = get_data_disciplina("Infraestrutura de Redes", 7)
    df7 = pd.DataFrame(dados7)


    if dados7 and len(dados7) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 7 - 29/09/2025", divider="green", anchor=False)
        st.dataframe(df7, key=327)
        

        st.markdown("")

        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.markdown("")
        with col2:
            st.markdown("")
        with col3:
            resumo7 = st.button("Resumo da Aula", key="botao_resumo7")
        with col4:
            st.markdown("")
        with col5:
            st.markdown("")

        st.markdown("---")

        if resumo7:
            try:
                dados_json7 = transforma_json(df7)

                # Chamada à IA e Captura da resposta
                resposta7 = chat_completion_disciplina(dados_json7, model_options, temperature)

                # Exibição no Markdown
                st.markdown(resposta7)

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")

    else:
        st.subheader("Semana 7 - 29/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados8 = get_data_disciplina("Infraestrutura de Redes", 8)
    df8 = pd.DataFrame(dados8)

    if dados8 and len(dados8) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 8 - 06/10/2025", divider="green", anchor=False)
        st.dataframe(df8, key=377)
        

        st.markdown("")

        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col1:
            st.markdown("")
        with col2:
            st.markdown("")
        with col3:
            resumo8 = st.button("Resumo da Aula", key="botao_resumo8")
        with col4:
            st.markdown("")
        with col5:
            st.markdown("")

        st.markdown("---")

        if resumo8:
            try:
                dados_json8 = transforma_json(df8)

                # Chamada à IA e Captura da resposta
                resposta8 = chat_completion_disciplina(dados_json8, model_options, temperature)

                # Exibição no Markdown
                st.markdown(resposta8)

            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")
    
    if dados and len(dados) > 0:
        st.subheader("Semana 8 - 06/10/2025", divider="green", anchor=False)
        st.dataframe(dados, key=248)
    else:
        st.subheader("Semana 8 - 06/10/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 9)
    if dados and len(dados) > 0:
        st.subheader("Semana 9 - 13/10/2025", divider="green", anchor=False)
        st.dataframe(dados, key=29)
    else:
        st.subheader("Semana 9 - 13/10/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 10)
    if dados and len(dados) > 0:
        st.subheader("Semana 10 - 20/10/2025", divider="green", anchor=False)
        st.dataframe(dados, key=30)
    else:
        st.subheader("Semana 10 - 20/10/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 11)
    if dados and len(dados) > 0:
        st.subheader("Semana 11 - 27/10/2025", divider="green", anchor=False)
        st.dataframe(dados, key=31)
    else:
        st.subheader("Semana 11 - 27/10/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 12)
    if dados and len(dados) > 0:
        st.subheader("Semana 12 - 03/11/2025", divider="green", anchor=False)
        st.dataframe(dados, key=32)
    else:
        st.subheader("Semana 12 - 03/11/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 13)
    if dados and len(dados) > 0:
        st.subheader("Semana 13 - 10/11/2025", divider="green", anchor=False)
        st.dataframe(dados, key=33)
    else:
        st.subheader("Semana 13 - 10/11/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 14)
    if dados and len(dados) > 0:
        st.subheader("Semana 14 - 17/11/2025", divider="green", anchor=False)
        st.dataframe(dados, key=34)
    else:
        st.subheader("Semana 14 - 17/11/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 15)
    if dados and len(dados) > 0:
        st.subheader("Semana 15 - 24/11/2025", divider="green", anchor=False)
        st.dataframe(dados, key=35)
    else:
        st.subheader("Semana 15 - 24/11/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 16)
    if dados and len(dados) > 0:
        st.subheader("Semana 16 - 01/12/2025", divider="green", anchor=False)
        st.dataframe(dados, key=36)
    else:
        st.subheader("Semana 16 - 01/12/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 17)
    if dados and len(dados) > 0:
        st.subheader("Semana 17 - 08/12/2025", divider="green", anchor=False)
        st.dataframe(dados, key=37)
    else:
        st.subheader("Semana 17 - 08/12/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 18)
    if dados and len(dados) > 0:
        st.subheader("Semana 18 - 15/12/2025", divider="green", anchor=False)
        st.dataframe(dados, key=38)
    else:
        st.subheader("Semana 18 - 15/12/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 19)
    if dados and len(dados) > 0:
        st.subheader("Semana 19 - 22/12/2025", divider="green", anchor=False)
        st.dataframe(dados, key=39)
    else:
        st.subheader("Semana 19 - 22/12/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 20)
    if dados and len(dados) > 0:
        st.subheader("Semana 20 - 29/12/2025", divider="green", anchor=False)
        st.dataframe(dados, key=40)
    else:
        st.subheader("Semana 20 - 29/12/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")



