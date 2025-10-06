import streamlit as st

conta = st.session_state.usuario_logado

st.subheader("🏠 Bem vindo(a)  ***"+conta+"***  ao Caderno da Turma", divider="rainbow", anchor=False)


TEXTO = '''
O Caderno da Turma tem como objetivo principal melhorar a forma como a turma de GTI 2025 organiza, compartilha e revisa suas anotações de aula. A plataforma funciona como um caderno digital coletivo, onde os alunos podem armazenar seus resumos e anotações, incentivando a participação de todos e facilitando o acesso ao conteúdo de forma centralizada e prática.
Com o apoio da MonitorIA, o chatbot com inteligência artificial integrado aos cadernos, os registros feitos pelos alunos deixam de ser apenas anotações e passam a servir também como fonte para revisões, esclarecimentos de dúvidas e apoio ao estudo individual. Assim, o projeto busca resolver a falta de organização e de colaboração no processo de aprendizagem, tornando o estudo mais dinâmico, acessível e conectado entre os colegas.

'''
st.markdown('')
st.markdown('')
st.markdown('**Objetivo Geral**')
st.markdown(TEXTO)
st.markdown('')
st.markdown('')
st.divider()




