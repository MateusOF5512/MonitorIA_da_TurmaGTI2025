import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date, datetime, timedelta
import json
# Certifique-se que suas importações locais estão corretas
from Functions.database import *
from Functions.grok import *
from Functions.interface import *

# 🎨 INJETAR O CSS
try:
    with open("style/style.css", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- Interface Geral ---
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.subheader(f"🌐 Infraestrutura de Redes de Computadores", divider="rainbow", anchor=False)
st.markdown("")

with st.expander("❓ Como usar o Caderno da Turma"):
    st.markdown("""
    Aqui, você pode visualizar os **cadernos e anotações de todas as semanas e disciplinas do semestre**.
    Use os botões para gerar resumos e quizzes interativos.
    """)
    st.markdown("")


# ===============================================================
# FUNÇÃO PARA RENDERIZAR UMA SEMANA ESPECÍFICA
# ===============================================================
def renderizar_semana(numero_semana, data_semana):
    # Identificadores únicos
    key_resumo = f"resumo_gerado_s{numero_semana}"
    key_perguntas = f"perguntas_s{numero_semana}"
    key_respostas_user = f"respostas_usuario_s{numero_semana}"

    # Session State
    if key_resumo not in st.session_state:
        st.session_state[key_resumo] = None
    if key_perguntas not in st.session_state:
        st.session_state[key_perguntas] = None
    if key_respostas_user not in st.session_state:
        st.session_state[key_respostas_user] = {}

    # ===============================================================
    # BLOCO PRINCIPAL DA SEMANA
    # ===============================================================
    with st.container(border=True):
        data_formatada = data_semana.strftime("%d/%m/%Y")
        st.subheader(f"📅 Semana {numero_semana} - {data_formatada}", divider="green", anchor=False)

        dados = get_data_disciplina("Infraestrutura de Redes", numero_semana)

        if not dados:
            st.info(f"Não há anotações cadastradas para a Semana {numero_semana}.")
        else:
            df = pd.DataFrame(dados)
            if "conteudo" in df.columns and "usuario" in df.columns:
                df["resumir"] = True
                df = df[["resumir", "conteudo", "usuario"]]

                # Exibe o editor apenas se o resumo AINDA NÃO foi gerado para limpar a tela
                # (Ou você pode manter o editor sempre visível, depende do gosto.
                #  Aqui mantive visível para permitir ver o que foi selecionado).
                st.markdown("Selecione os cadernos para o resumo:")
                editor = st.data_editor(
                    df,
                    hide_index=True,
                    use_container_width=True,
                    key=f"editor_semana_{numero_semana}",
                )

                # Se ainda não tem resumo, mostra o botão de gerar
                if st.session_state[key_resumo] is None:
                    col1, col2, col3 = st.columns([1, 1, 1])

                    # 1. Botão VER RESULTADO
                    with col1:
                        st.markdown("")
                    with col2:
                        resumo_btn = st.button(f"Gerar resumo da semana {numero_semana}",
                                               key=f"btn_resumo_s{numero_semana}", use_container_width=True)
                    with col3:
                        st.markdown("")

                    if resumo_btn:
                        try:
                            linhas_resumir = editor[editor["resumir"] == True].drop(columns=["resumir"])
                            if linhas_resumir.empty:
                                st.warning("Selecione ao menos uma linha.")
                            else:
                                with st.spinner(f"Gerando resumo da Semana {numero_semana}..."):
                                    dados_modelo = transforma_json(linhas_resumir)
                                    resposta = chat_completion_disciplina(dados_modelo)
                                    st.session_state[key_resumo] = resposta

                                    # Gera perguntas iniciais
                                    questoes = criar_questoes_com_groq(resposta, 'Infraestrutura de Redes')
                                    if isinstance(questoes, str):
                                        perguntas = json.loads(questoes)
                                    else:
                                        perguntas = questoes

                                    st.session_state[key_perguntas] = perguntas
                                    st.rerun()  # Recarrega para esconder o botão e mostrar o resumo
                        except Exception as e:
                            st.error(f"Erro: {e}")

                # ===============================================================
                # EXIBIR RESUMO E QUIZ (Se já existir resumo no state)
                # ===============================================================
                if st.session_state[key_resumo]:
                    st.success(f"✅ Resumo gerado da semana {numero_semana}!")
                    st.markdown(st.session_state[key_resumo])
                    st.divider()

                if st.session_state[key_perguntas]:
                    st.subheader(f"🧠 Quiz Interativo - Semana {numero_semana}")

                    respostas_usuario = st.session_state[key_respostas_user]
                    lista_perguntas = st.session_state[key_perguntas]

                    # Renderiza as perguntas
                    for i, q in enumerate(lista_perguntas):
                        with st.expander(f"Questão {i + 1}: {q['pergunta']}", expanded=True):
                            resposta_salva = respostas_usuario.get(i)
                            idx = q["opcoes"].index(resposta_salva) if resposta_salva in q["opcoes"] else 0

                            r = st.radio("Alternativas:", q["opcoes"], key=f"q{i}_s{numero_semana}", index=idx)
                            st.session_state[key_respostas_user][i] = r

                    st.markdown("---")

                    # === BOTÕES DE AÇÃO (LADO A LADO) ===
                    col1, col2, col3 = st.columns([1, 1, 1])

                    # 1. Botão VER RESULTADO
                    with col1:
                        if st.button("📊 Ver Resultado", key=f"btn_result_s{numero_semana}", use_container_width=True):
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

                    # 2. Botão GERAR NOVAS PERGUNTAS
                    with col2:
                        if st.button("🔄 Novas Perguntas", key=f"btn_newq_s{numero_semana}", use_container_width=True):
                            with st.spinner("Criando novas questões..."):
                                try:
                                    # Usa o resumo que JÁ existe no state
                                    resumo_atual = st.session_state[key_resumo]
                                    novas_q = criar_questoes_com_groq(resumo_atual, 'Infraestrutura de Redes')

                                    if isinstance(novas_q, str):
                                        perguntas_novas = json.loads(novas_q)
                                    else:
                                        perguntas_novas = novas_q

                                    # Atualiza state e limpa respostas anteriores
                                    st.session_state[key_perguntas] = perguntas_novas
                                    st.session_state[key_respostas_user] = {}
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Erro ao recriar: {e}")

                    # 3. Botão REINICIAR (Limpar tudo da semana)
                    with col3:
                        if st.button(f"📅 Novo Resumo Semana {numero_semana}", key=f"btn_reset_s{numero_semana}",
                                     use_container_width=True):
                            # Limpa os estados desta semana específica
                            st.session_state[key_resumo] = None
                            st.session_state[key_perguntas] = None
                            st.session_state[key_respostas_user] = {}
                            st.rerun()

            else:
                st.warning("Erro na estrutura dos dados.")


# ===============================================================
# LOOP GERAL
# ===============================================================
data_inicial = date(2025, 8, 18)

for i in range(1, 8):
    d = data_inicial + timedelta(weeks=(i - 1))
    renderizar_semana(i, d)
    st.markdown("<br>", unsafe_allow_html=True)

criar_rodape()