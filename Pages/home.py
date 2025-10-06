import streamlit as st

conta = st.session_state.usuario_logado

st.subheader("🏠 Bem vindo(a)  ***"+conta+"***  ao Caderno da Turma", divider="rainbow", anchor=False)


TEXTO = '''
O projeto **Caderno da Turma GTI** tem como objetivo desenvolver um **caderno digital coletivo** para os alunos da segunda fase do curso de Gestão da Tecnologia da Informação (GTI 2025). A proposta busca **centralizar anotações, materiais e recursos de estudo em um ambiente colaborativo**, enfrentando desafios como a dispersão de informações e a falta de organização dos registros acadêmicos. O sistema pretende oferecer uma solução simples, moderna e integrada ao contexto da turma, promovendo a **troca de conhecimento e fortalecendo o aprendizado coletivo**.

O projeto será restrito à turma de GTI 2025 e operará dentro das limitações das ferramentas gratuitas utilizadas, assegurando viabilidade e execução completa. O desenvolvimento seguirá etapas que incluem diagnóstico, definição de requisitos, construção, testes e implantação final, com acompanhamento inicial do uso. Seu desempenho será avaliado por métricas como engajamento, frequência de acesso, volume de anotações, interações com a IA e satisfação dos usuários, permitindo mensurar o impacto do caderno digital na organização, colaboração e aprendizado da turma.

'''
st.markdown('')
st.markdown('')
st.markdown('**Objetivo Geral**')
st.markdown(TEXTO)
st.markdown('')
st.markdown('')
st.divider()








