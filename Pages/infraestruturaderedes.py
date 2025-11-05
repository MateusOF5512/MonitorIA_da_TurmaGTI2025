import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
import json
from Functions.database import *
from Functions.grok import *


# --- Interface ---
st.header("🌐 Infraestrutura de Redes de Computadores", divider="rainbow", anchor=False)
st.markdown("")

with st.expander("🧠 Como usar o Caderno da Turma!"):
    st.markdown("""
    Aqui, você pode visualizar os **cadernos e anotações de todas as semanas e disciplinas do semestre** e contar com o poder do modelo de linguagem **ChatGPT OSS 120B** para gerar **resumos personalizados** dos conteúdos abordados em aula.

    O sistema foi desenvolvido para auxiliar na **revisão e retomada de conteúdos**, especialmente em dias em que o aluno não pôde comparecer à aula. Além disso, é possível **comparar e analisar os cadernos em formato de tabela**, facilitando a identificação dos temas e anotações mais relevantes.

    ---

    #### 📘 **Como usar:**
    1. Visualize seus cadernos organizados por **semana e disciplina**.  
    2. Use a coluna **“Resumir”** para selecionar apenas os cadernos e anotações que deseja incluir no resumo.  
    3. Clique em **“Gerar resumo da aula”** para que o sistema produza uma **síntese automática** com base nas suas seleções.  
    4. Leia o resumo gerado e utilize-o como **apoio para estudos e revisões**.  
    5. Você pode repetir o processo a qualquer momento para diferentes semanas ou disciplinas.

    ---

    #### 💡 **Dica:**
    Quanto mais completas forem suas anotações, mais preciso e útil será o resumo gerado pelo modelo.  
    Use este recurso para **otimizar seu aprendizado**, revisar conteúdos perdidos e consolidar o conhecimento de todo o semestre.
    """)

    st.markdown("")

with st.container(border=True):
    dados1 = get_data_disciplina("Infraestrutura de Redes", 1)


    st.subheader("Semana 1 - 18/08/2025", divider="green", anchor=False)

    df1 = pd.DataFrame(dados1)
    df1["resumir?"] = True

    df1 = df1[["resumir?", "conteudo", "usuario"]]

    st.markdown("Selecione as linhas (cadernos) que deseja incluir no resumo feito pelo ChatGPT:")
    editor = st.data_editor(
        df1,
        hide_index=True,
        use_container_width=True,
        key="editor_semana1",
    )

    st.markdown("")

    col1, col2, col3 = st.columns([1.5, 1, 1])
    with col1:
        st.markdown("")
    with col2:
        resumo1 = st.button("Gerar resumo da aula")
    with col3:
        st.markdown("")

    st.markdown("---")


    if resumo1:
        try:
            # 🔹 Filtra apenas as linhas com Resumir == True
            linhas_resumir = editor[editor["resumir?"] == True].drop(columns=["resumir?"])

            # 🔹 Se nenhuma linha for marcada, mostra aviso
            if linhas_resumir.empty:
                st.warning("Nenhuma linha foi selecionada para resumo. Marque ao menos uma linha na coluna 'Resumir'.")
            else:
                # Chama a IA com apenas as linhas selecionadas
                dados1_modelo = transforma_json(linhas_resumir)
                resposta = chat_completion_disciplina(dados1_modelo)

                # Exibe resultado
                st.subheader("📌 Resumo gerado pela Inteligência Artificial")
                st.markdown(resposta)

        except Exception as e:
            st.error(f"⚠️ Erro ao gerar resposta: {e}")

with st.container(border=True):

    dados2 = get_data_disciplina("Infraestrutura de Redes", 2)
    if dados2 and len(dados2) > 0:
        # Se retornou algo → divider verde
        st.subheader("Semana 2 - 25/08/2025", divider="green", anchor=False)

        df2 = pd.DataFrame(dados2)
        df2["resumir"] = True

        df2 = df2[["resumir", "conteudo", "usuario"]]

        st.markdown("Selecione as linhas (cadernos) que deseja incluir no resumo feito pelo ChatGPT:")
        editor2 = st.data_editor(
            df2,
            hide_index=True,
            use_container_width=True,
            key="editor_semana2",
        )

        st.markdown("")

        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col1:
            st.markdown("")
        with col2:
            resumo2 = st.button("Gerar resumo da aula", key=113)
        with col3:
            st.markdown("")

        st.markdown("---")

        if resumo2:
            try:
                # 🔹 Filtra apenas as linhas com Resumir == True
                linhas_resumir2 = editor2[editor2["resumir"] == True].drop(columns=["resumir"])

                # 🔹 Se nenhuma linha for marcada, mostra aviso
                if linhas_resumir2.empty:
                    st.warning(
                        "Nenhuma linha foi selecionada para resumo. Marque ao menos uma linha na coluna 'Resumir'.")
                else:
                    # Chama a IA com apenas as linhas selecionadas
                    dados2_modelo = transforma_json(linhas_resumir2)
                    resposta2 = chat_completion_disciplina(dados2_modelo)

                    # Exibe resultado
                    st.subheader("📌 Resumo gerado pela Inteligência Artificial")
                    st.markdown(resposta2)

            except Exception as e:
                st.error(f"⚠️ Erro ao gerar resposta: {e}")
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
    dados = get_data_disciplina("Infraestrutura de Redes", 7)
    if dados and len(dados) > 0:
        st.subheader("Semana 7 - 29/09/2025", divider="green", anchor=False)
        st.dataframe(dados, key=27)
    else:
        st.subheader("Semana 7 - 29/09/2025", divider="red", anchor=False)
        st.warning("Ainda não há conteúdo disponível para esta semana.")

with st.container(border=True):
    dados = get_data_disciplina("Infraestrutura de Redes", 8)
    if dados and len(dados) > 0:
        st.subheader("Semana 8 - 06/10/2025", divider="green", anchor=False)
        st.dataframe(dados, key=28)
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
