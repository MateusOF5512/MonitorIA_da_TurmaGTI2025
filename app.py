import streamlit as st

st.set_page_config(page_title="Caderno da Turma", layout='wide',page_icon='📚',
                   initial_sidebar_state=None)


if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "logado" not in st.session_state:
    st.session_state.logado = False
if "deslogado" not in st.session_state:
    st.session_state.deslogado = True

def login():
    st.markdown("<h1 style='font-size:200%;text-align:center;color: black;padding: 0px 0px 40px 0px;'" +
                ">📚 Caderno da Turma 2025 GTI IFSC</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown('')
    with col2:
        with st.container(border=True):
            st.markdown("<h2 style='font-size:200%;text-align:center;color: black;padding: 0px 0px 40px 0px;'" +
                        ">Faça seu Login para começar</h2>", unsafe_allow_html=True)

            usuario_digitado = st.text_input("**Usuário do SIGAA:**", max_chars=20)
            password = st.text_input("**Senha LAB04:**", type="password", max_chars=10)

            usuario_digitado = usuario_digitado.strip().lower()
            password = password.strip().lower()
          
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown('')
            with col2:
                submitted = st.button("Entrar",use_container_width=True, type='primary')
            with col3:
                st.markdown('')

    with col3:
        st.markdown('')

    if submitted:
        autenticado = False

        for role_key, dados in st.secrets["usuarios"].items():
            if usuario_digitado == dados["usuario"] and password == dados["senha"]:
                st.session_state.usuario_logado = usuario_digitado
                autenticado = True
                break

        if autenticado:
            st.session_state.logado = True
            st.rerun()
        else:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown('')
            with col2:
                st.error("Usuário ou senha incorretos.")
            with col3:
                st.markdown('')


def logout():
    st.session_state.deslogado = True
    st.rerun()



pages = {
    "Geral": [
        st.Page("Pages/home.py", title="Página Inicial", icon='🏠'),
        st.Page("Pages/monitoria.py", title="MonitorIA", icon='👨‍🏫'),
        st.Page("Pages/enviarcaderno.py", title="Enviar Anotações", icon='📚'),
        st.Page("Pages/dashboard.py", title="Dashboards", icon='📊')
    ],
    "Cadernos": [
        st.Page("Pages/metodologiadeprojetos.py", title="Métodologia de Projetos", icon='🎯'),
        st.Page("Pages/estatisticaempresarial.py", title="Estatística Empresarial", icon='📈'),
        st.Page("Pages/gestaoorganizacional.py", title="Gestão Organizacional", icon='🏢'),
        st.Page("Pages/infraestruturaderedes.py", title="Infraestrutura de Redes", icon='🌐'),
        st.Page("Pages/processodedesenvolvimentodesistemas.py", title="Processo e Desv. de Sistemas", icon='💻'),
        st.Page("Pages/qualidadedesoftware.py", title="Qualidade de Software", icon='🌐'),
        st.Page("Pages/sistemaoperacionalwindows.py", title="Sistema Operacional (Windows)", icon='🌐'),
        st.Page("Pages/tecnologiadehardware.py", title="Tecnologia de Hardware", icon='🌐'),
    ],
}

if st.session_state.logado is not True:
    pg = st.navigation([st.Page(login)])
else:
    pg = st.navigation(pages, position="sidebar", expanded=True)


pg.run()




