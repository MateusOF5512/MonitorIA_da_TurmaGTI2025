import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
import json
from Functions.database import *
from Functions.grok import *

# ===============================================================
# CONFIGURAÇÃO INICIAL DO SESSION STATE
# ===============================================================
if "resumo_gerado" not in st.session_state:
    st.session_state["resumo_gerado"] = None

if "perguntas" not in st.session_state:
    st.session_state["perguntas"] = None

if "respostas_usuario" not in st.session_state:
    st.session_state["respostas_usuario"] = {}

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

# ===============================================================
# BLOCO DE SELEÇÃO DE CADERNOS
# ===============================================================

with st.container(border=True):
    st.subheader("📅 Semana 1 - 18/08/2025", divider="green", anchor=False)

    # 🔹 Obter dados da disciplina
    dados1 = get_data_disciplina("Infraestrutura de Redes", 1)

    df1 = pd.DataFrame(dados1)
    df1["resumir"] = True
    df1 = df1[["resumir", "conteudo", "usuario"]]

    st.markdown("Selecione as linhas (cadernos) que deseja incluir no resumo feito pelo ChatGPT:")

    editor = st.data_editor(
        df1,
        hide_index=True,
        use_container_width=True,
        key="editor_semana1",
    )

    resumo1 = st.button("Gerar resumo da aula")

    # ===============================================================
    # GERAR RESUMO E PERGUNTAS
    # ===============================================================
    if resumo1:
        try:
            linhas_resumir = editor[editor["resumir"] == True].drop(columns=["resumir"])
            if linhas_resumir.empty:
                st.warning("Nenhuma linha foi selecionada para resumo.")
            else:
                dados1_modelo = transforma_json(linhas_resumir)
                resposta = chat_completion_disciplina(dados1_modelo)

                # 🔹 Salva no session_state
                st.session_state["resumo_gerado"] = resposta

                # 🔹 Gera 4 perguntas, cada uma com 3 opções
                questoes = criar_questoes_com_groq(resposta, 'Metodologia de Projetos')

                # Se vier como string JSON válida → converte
                if isinstance(questoes, str):
                    perguntas = json.loads(questoes)
                else:
                    # Caso a IA já retorne objeto (raro, mas pode ocorrer)
                    perguntas = questoes

                # Garante que o resultado seja uma lista
                if not isinstance(perguntas, list):
                    raise ValueError("Formato inválido: o retorno não é uma lista JSON.")

                # Salva no session_state
                st.session_state["perguntas"] = perguntas




        except Exception as e:
            st.error(f"⚠️ Erro ao gerar resposta: {e}")

    # ===============================================================
    # EXIBIR RESUMO (DENTRO DO CONTAINER)
    # ===============================================================
    if st.session_state["resumo_gerado"]:
        st.success("✅ Resumo gerado com sucesso!")
        st.subheader("📘 Resumo gerado pelo ChatGPT OpenIA")
        st.markdown(st.session_state["resumo_gerado"])

    # ===============================================================
    # EXIBIR QUIZ (DENTRO DO CONTAINER)
    # ===============================================================
    if st.session_state["perguntas"]:
        st.success("✅ Perguntas geradas com sucesso!")
        st.markdown("---")
        st.subheader("🧠 Perguntas para fixação e revisão - Quiz Interativo")

        respostas_usuario = st.session_state["respostas_usuario"]

        for i, q in enumerate(st.session_state["perguntas"]):
            with st.expander(q["pergunta"]):
                resposta_salva = respostas_usuario.get(i)
                # Evita ValueError caso a resposta não esteja em q["opcoes"]
                if resposta_salva in q["opcoes"]:
                    index_inicial = q["opcoes"].index(resposta_salva)
                else:
                    index_inicial = 0

                resposta = st.radio(
                    "Selecione uma alternativa correta:",
                    q["opcoes"],
                    key=f"q{i}",
                    index=index_inicial
                )

                st.session_state["respostas_usuario"][i] = resposta

        if st.button("Ver resultado", key="resultado_semana1"):
            acertos = 0
            resultado_detalhado = []

            for i, q in enumerate(st.session_state["perguntas"]):
                correta = q["resposta_correta"]
                usuario = st.session_state["respostas_usuario"].get(i)
                if usuario == correta:
                    acertos += 1
                    resultado_detalhado.append(f"✅ Questão {i+1}: Correta!")
                else:
                    resultado_detalhado.append(f"❌ Questão {i+1}: Errada. Resposta certa: {correta}")

            nota_final = round((acertos / len(st.session_state["perguntas"])) * 10, 1)
            st.markdown("---")
            st.subheader(f"🏁 Sua nota: **{nota_final}/10**")
            st.write("\n".join(resultado_detalhado))

