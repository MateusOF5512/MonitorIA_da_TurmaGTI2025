import streamlit as st

# 🛠️ Configuração Inicial da Página
st.set_page_config(
    page_title="Caderno da Turma GTI - Landing Page",
    layout="wide",
)

# Define a conta do usuário (placeholder para o nome)
conta_usuario = st.session_state.usuario_logado


# 🎨 INJETAR O CSS A PARTIR DO ARQUIVO
with open("style/style.css", encoding="utf-8") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



# 🚀 Seção de Título e Chamada Principal
st.markdown('<div class="main-header">', unsafe_allow_html=True)

# Título 1 (Centralizado por CSS)
st.subheader(f"🏠 Bem vindo(a) ao Caderno da Turma *{conta_usuario}*", divider="rainbow", anchor=False)

st.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #1f3044; font-size: 2.5em;">Seu Hub Colaborativo de Conhecimento GTI</h1>
    </div>
""", unsafe_allow_html=True)

# Texto de Apresentação (Mais longo e convincente)
st.markdown("""
    <div style="text-align: center;">
        <p style="font-size: 1.3em; color: #5a6268; margin-top: 10px; line-height: 1.5;">
            Chega de anotações dispersas! O Caderno da Turma resolve a falta de organização e colaboração, <br>
            transformando seus registros de aula em uma poderosa fonte de estudo centralizada e interativa, com o apoio de uma IA.
        </p>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")

# 🌟 Seção de Benefícios e Características (Landing Page Cards)
st.header("Por que usar o Caderno da Turma?")

col_benefits = st.columns(3)

with col_benefits[0]:
    # INÍCIO DO WRAPPER DE BORDA (CORREÇÃO APLICADA)
    st.markdown('<div class="feature-icon">🔎</div>', unsafe_allow_html=True)
    st.markdown('<p class="feature-title">Centralização de Conteúdo</p>', unsafe_allow_html=True)
    # Texto do Card Centralizado
    st.markdown(
        '<div class="card-text-center">Reúna todos os <b>resumos e anotações da turma em um único ambiente digital acessível</b>, permitindo a organização das informações e um estudo mais aprofundado e personalizado.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)  # FIM DO WRAPPER DE BORDA

with col_benefits[1]:
    # INÍCIO DO WRAPPER DE BORDA (CORREÇÃO APLICADA)
    st.markdown('<div class="feature-icon">👨‍💻</div>', unsafe_allow_html=True)
    st.markdown('<p class="feature-title">MonitorIA: Agente RAG Inteligente</p>', unsafe_allow_html=True)
    # NOVO FOCO: Agent RAG
    st.markdown(
        '<div class="card-text-center">Funciona como um Agent RAG (Retrieval-Augmented Generation) que <b>analisa todos os cadernos, slides, livros e anotações usados em sala</b> para responder perguntas complexas e específicas sobre o conteúdo das aulas.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)  # FIM DO WRAPPER DE BORDA

with col_benefits[2]:
    # INÍCIO DO WRAPPER DE BORDA (CORREÇÃO APLICADA)
    st.markdown('<div class="feature-icon">🗓️</div>', unsafe_allow_html=True)
    st.markdown('<p class="feature-title">Resumo Semanal e Atividades</p>', unsafe_allow_html=True)
    # NOVO FOCO: Resumos semanais e atividades
    st.markdown(
        '<div class="card-text-center">Alunos podem acessar a disciplina, visualizar ao longo das semanas o conteúdo abordado, ter o <b>resumo com os principais tópicos e desenvolver atividades para cada semana</b>, reforçando o aprendizado.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)  # FIM DO WRAPPER DE BORDA

st.write("---")

# 💻 Seção de Equipe e Tecnologias
st.header("Detalhes do Projeto")

col3, col_spacer, col4 = st.columns([1, 0.05, 1])

with col3:
    # Adicionando um divisor sutil para harmonizar com a seção de cima
    st.subheader("Time de Desenvolvimento", divider="gray")
    st.markdown(
        "O projeto simula um cenário de execução profissional, com papéis bem definidos para garantir a qualidade e organização.")
    st.dataframe({
        'Nome Aluno': ['João Victor', 'Mateus Ortiz', 'Pedro Paulo'],
        'Cargo Projeto': ['Líder e Gerente de Projeto', 'Programador Full-Stack Web', ''],
    }, hide_index=True)

# A coluna col_spacer fica vazia, criando o espaço
with col_spacer:
    st.write("")

with col4:
    # Adicionando um divisor sutil para harmonizar com a seção de cima
    st.subheader("Stack Tecnológica", divider="gray")
    st.markdown(
        "Desenvolvido com foco em soluções eficientes e gratuitas (versões gratuitas das ferramentas) para assegurar a viabilidade do projeto.")
    st.markdown("""
    * **Linguagem de Programação:** Python 3.13
    * **Interface Web:** Streamlit
    * **Banco de Dados:** Supabase
    * **Inteligência Artificial (LLM):** Groq e ChatGPT
    """)

st.markdown('')
st.write("---")