import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
import json
# Certifique-se que suas importações locais estão corretas
from Functions.database import *
from Functions.grok import *
from Functions.interface import *

# ===============================================================
# ⚙️ CONFIGURAÇÕES DA PÁGINA
# ===============================================================

NOME_MATERIA = "Tecnologia de Hardware"
KEY_PREFIX = "tec_hardware"

# Definição MANUAL das datas
CRONOGRAMA = {
    1: date(2025, 8, 18),
    2: date(2025, 8, 25),
    3: date(2025, 9, 1),
    4: date(2025, 9, 8),
    5: date(2025, 9, 15),
    6: date(2025, 9, 22),
}

# 🎨 INJETAR O CSS
try:
    with open("style/style.css", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Interface Geral ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.subheader(f"🖥️ {NOME_MATERIA}", divider="rainbow", anchor=False)
st.markdown("")

with st.expander(f"❓ Como usar o Caderno de {NOME_MATERIA}"):
    st.markdown(f"""
    Aqui, você pode visualizar os **cadernos e anotações da disciplina de {NOME_MATERIA}**.
    Use os botões para gerar resumos e quizzes interativos baseados nas anotações semanais.
    """)
    st.markdown("")


# ===============================================================
# FUNÇÃO PARA RENDERIZAR UMA SEMANA ESPECÍFICA
# ===============================================================
def renderizar_semana_custom(numero_semana, data_semana):
    # Identificadores únicos
    key_resumo = f"resumo_{KEY_PREFIX}_s{numero_semana}"
    key_perguntas = f"perguntas_{KEY_PREFIX}_s{numero_semana}"
    key_respostas_user = f"respostas_{KEY_PREFIX}_s{numero_semana}"

    # Keys para widgets
    k_editor = f"editor_{KEY_PREFIX}_s{numero_semana}"
    k_btn_resumo = f"btn_resumo_{KEY_PREFIX}_s{numero_semana}"
    k_radio_base = f"radio_{KEY_PREFIX}_s{numero_semana}"
    k_btn_result = f"btn_result_{KEY_PREFIX}_s{numero_semana}"
    k_btn_newq = f"btn_newq_{KEY_PREFIX}_s{numero_semana}"
    k_btn_reset = f"btn_reset_{KEY_PREFIX}_s{numero_semana}"

    # Inicializa Session State
    if key_resumo not in st.session_state:
        st.session_state[key_resumo] = None
    if key_perguntas not in st.session_state:
        st.session_state[key_perguntas] = None
    if key_respostas_user not in st.session_state:
        st.session_state[key_respostas_user] = {}

    # ===============================================================
    # BLOCO VISUAL DA SEMANA
    # ===============================================================
    with st.container(border=True):
        # 1. BUSCAR DADOS ANTES DE RENDERIZAR O TÍTULO
        dados = get_data_disciplina(NOME_MATERIA, numero_semana)
        data_formatada = data_semana.strftime("%d/%m/%Y")

        # 2. EXTRAIR O PLANO DE ENSINO (SE HOUVER DADOS)
        texto_plano = ""
        if dados and len(dados) > 0:
            # Pega o plano do primeiro registro encontrado na semana
            # Usa .get() para evitar erro se a coluna não vier
            plano_raw = dados[0].get('plano_de_ensino', '')
            if plano_raw:
                texto_plano = f" - {plano_raw}"

        # 3. RENDERIZAR O CABEÇALHO COM O PLANO
        st.subheader(f"📅 Semana {numero_semana} - {data_formatada}{texto_plano}", divider="green", anchor=False)

        if not dados:
            st.info(f"Não há anotações cadastradas para a Semana {numero_semana}.")
        else:
            df = pd.DataFrame(dados)
            # Verifica colunas essenciais
            if "conteudo" in df.columns and "usuario" in df.columns:
                df["resumir"] = True

                # Selecionamos apenas as colunas úteis para o editor visual
                # (Não precisamos mostrar o plano_de_ensino repetido na tabela)
                df_editor = df[["resumir", "conteudo", "usuario"]]

                st.markdown("Selecione os cadernos para o resumo:")
                editor = st.data_editor(
                    df_editor,
                    hide_index=True,
                    use_container_width=True,
                    key=k_editor,
                )

                # --- Botão de Gerar Resumo ---
                if st.session_state[key_resumo] is None:
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        if st.button(f"Gerar resumo da semana {numero_semana}", key=k_btn_resumo,
                                     use_container_width=True):
                            try:
                                linhas_resumir = editor[editor["resumir"] == True].drop(columns=["resumir"])
                                if linhas_resumir.empty:
                                    st.warning("Selecione ao menos uma linha.")
                                else:
                                    with st.spinner(f"Lendo anotações de {NOME_MATERIA}..."):
                                        dados_modelo = transforma_json(linhas_resumir)

                                        resposta = chat_completion_disciplina(dados_modelo)
                                        st.session_state[key_resumo] = resposta

                                        questoes = criar_questoes_com_groq(resposta, NOME_MATERIA)
                                        if isinstance(questoes, str):
                                            perguntas = json.loads(questoes)
                                        else:
                                            perguntas = questoes

                                        st.session_state[key_perguntas] = perguntas
                                        st.rerun()
                            except Exception as e:
                                st.error(f"Erro: {e}")

                # --- Exibir Resumo e Quiz ---
                if st.session_state[key_resumo]:
                    st.success(f"✅ Resumo gerado com sucesso!")
                    st.markdown(st.session_state[key_resumo])
                    st.divider()

                if st.session_state[key_perguntas]:
                    st.subheader(f"🧠 Quiz: {NOME_MATERIA} - S{numero_semana}")

                    respostas_usuario = st.session_state[key_respostas_user]
                    lista_perguntas = st.session_state[key_perguntas]

                    for i, q in enumerate(lista_perguntas):
                        with st.expander(f"Questão {i + 1}: {q['pergunta']}", expanded=True):
                            resposta_salva = respostas_usuario.get(i)
                            idx = q["opcoes"].index(resposta_salva) if resposta_salva in q["opcoes"] else 0

                            r = st.radio("Alternativas:", q["opcoes"], key=f"{k_radio_base}_{i}", index=idx)
                            st.session_state[key_respostas_user][i] = r

                    st.markdown("---")

                    col1, col2, col3 = st.columns([1, 1, 1])

                    with col1:
                        if st.button("📊 Ver Resultado", key=k_btn_result, use_container_width=True):
                            acertos = 0
                            msg_resultado = []
                            for i, q in enumerate(lista_perguntas):
                                u = st.session_state[key_respostas_user].get(i)
                                if u == q["resposta_correta"]:
                                    acertos += 1
                                    msg_resultado.append(f"✅ Q{i + 1}: Correta")
                                else:
                                    msg_resultado.append(f"❌ Q{i + 1}: Errada (Correta: {q['resposta_correta']})")

                            nota = round((acertos / len(lista_perguntas)) * 10, 1)
                            st.toast(f"Nota: {nota}/10")
                            for msg in msg_resultado:
                                st.write(msg)

                    with col2:
                        if st.button("🔄 Novas Perguntas", key=k_btn_newq, use_container_width=True):
                            with st.spinner("Recriando perguntas..."):
                                try:
                                    resumo_atual = st.session_state[key_resumo]
                                    novas_q = criar_questoes_com_groq(resumo_atual, NOME_MATERIA)

                                    if isinstance(novas_q, str):
                                        perguntas_novas = json.loads(novas_q)
                                    else:
                                        perguntas_novas = novas_q

                                    st.session_state[key_perguntas] = perguntas_novas
                                    st.session_state[key_respostas_user] = {}
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao recriar: {e}")

                    with col3:
                        if st.button("🎯 Novo Resumo", key=k_btn_reset, use_container_width=True):
                            st.session_state[key_resumo] = None
                            st.session_state[key_perguntas] = None
                            st.session_state[key_respostas_user] = {}
                            st.rerun()

            else:
                st.warning("Erro na estrutura dos dados recuperados do banco.")


# ===============================================================
# LOOP GERAL BASEADO NO CRONOGRAMA
# ===============================================================
for semana_num, data_definida in CRONOGRAMA.items():
    renderizar_semana_custom(semana_num, data_definida)
    st.markdown("<br>", unsafe_allow_html=True)


criar_rodape()