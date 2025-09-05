import streamlit as st

conta = st.session_state.usuario_logado

st.subheader("🏠 Bem vindo(a)  ***"+conta+"***  ao Cederno da Turma", divider="rainbow", anchor=False)

st.markdown("APRESENTAÇÃO DO PROJETO")
st.markdown("COMO USAR O SISTEMA")
st.markdown("OBJETIVO DO PROJETO")