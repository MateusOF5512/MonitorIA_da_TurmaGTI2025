from datetime import date, timedelta
import json
# Importações de Functions.database e Functions.grok mantidas, mas sem uso direto neste snippet.
# from Functions.database import *
# from Functions.grok import *
import pdfplumber
import requests
import streamlit as st  # Streamlit precisa ser importado

from Functions.interface import *

raw_conteudos_por_disciplina = {
    'Proc. e Desv. de Sistemas': [
        ('27/08', 'Mapeamento de processos e BPMN'),
        ('02/09', 'Conceitos de Engenharia de Software'),
        ('03/09', 'Levantamento de requisitos'),
        ('17/09', 'Diagramas de casos de uso'),
        ('24/09', 'Histórias de usuário'),
        ('15/10', 'Diagrama de classes'),
    ],
    'Qualidade de Software': [
        ('19/08', 'Apresentação Qualidade de Software'),
        ('16/09', 'Instalação e Auditoria do Calcurse no Ubuntu'),
        ('23/09', 'Qualidade de Software e Normas ISO'),
        ('09/09', 'Gerenciamento da Qualidade de Software'),
        ('04/11', 'Introdução a Engenharia de Software'),
        ('11/11', 'Introdução a Engenharia de Requisitos'),
        ('18/11', 'Metodologias Ágeis, Interface e Ergonomia '),
     ],

    'Gestão Organizacional': [
        ('22/08', 'Teoria geral de administração'),
        ('29/08', 'Fundamentos da administração de negócios'),
        ('05/09', 'Cultura Organizacional e do Clima Organizacional'),
        ('12/09', 'Gestão do conhecimento nas organizações'),
    ],
    'Infraestrutura de Redes': [
        ('18/08', 'Protocolo DHCP'),
        ('25/08', 'Cabeamento Estruturado'),
        ('28/08', 'Conexão WAN e LAN'),
        ('08/09', 'Camada 3 - Roteadores'),
        ('06/10', 'Camada 2 - Switches'),
        ('13/10', 'NAT - Network Address Translation')
    ],
    'Metodologia de Projetos': [
        ('18/08', 'Introdução a projetos: conceitos'),
        ('25/08', 'Gestão de Projetos'),
        ('08/09', 'Desempenho do Planejamento'),
        ('15/09', 'Ferramentas Clássicas de Projetos'),
        ('13/10', 'Etapas do Projeto'),
        ('28/10', 'Metodologias ágeis (Scrum)'),
        ('03/11', 'Softwares para Gestão de Projetos'),
    ],
}

# 🎨 INJETAR O CSS
try:
    with open("style/style.css", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    pass

disciplinas = list(raw_conteudos_por_disciplina.keys())
primeira_disciplina = disciplinas[0]
TIPOS_CONTEUDO = ["Caderno", "Material Didático (Slides, Livro, etc.)"]

# --- Variável global para a data base (para inferir o ano) ---
START_YEAR = 2025  # O ano é fixo para permitir a conversão de dd/mm para YYYY-MM-DD


# --- Função para estruturar os dados com Semana e Data (AGORA DINÂMICA) ---
def generate_content_structure(raw_contents_with_dates):
    """
    Associa cada conteúdo a uma semana (1 a N) e USA a data fornecida na lista.
    """
    structured_contents = []
    # raw_contents_with_dates é uma lista de tuplas (data_ddmm, content)
    for i, (formatted_date_ddmm, content) in enumerate(raw_contents_with_dates):
        # Objeto que será armazenado na session_state para ser usado no selectbox
        structured_contents.append({
            'week': i + 1,
            'date': formatted_date_ddmm,  # Data no formato dd/mm para a UI
            'content': content,
            # Label formatado para o usuário: [Semana] - [Data dd/mm] - [Conteúdo]
            'label': f"{i + 1} - {formatted_date_ddmm} - {content}"
        })
    return structured_contents


# --- Dicionário final estruturado com as informações de Semana e Data ---
# Este dicionário contém uma lista de objetos para cada disciplina.
conteudos_por_disciplina = {
    disc: generate_content_structure(raw_list)
    for disc, raw_list in raw_conteudos_por_disciplina.items()
}


# ------------------- FUNÇÃO DE CONVERSÃO INTERNA (BACKEND) -------------------

def convert_ddmm_to_iso(ddmm_str, year=START_YEAR):
    """Converte 'dd/mm' para o formato 'YYYY-MM-DD'."""
    try:
        day, month = map(int, ddmm_str.split('/'))
        # Usa o ano fixo (START_YEAR) para montar o formato ISO
        return date(year, month, day).strftime('%Y-%m-%d')
    except ValueError:
        # Em caso de falha na conversão
        st.error(f"Erro de formato de data: '{ddmm_str}'. Não foi possível converter para YYYY-MM-DD.")
        return str(date.today())  # Retorna a data de hoje como fallback


# ------------------- FUNÇÕES PARA CALLBACKS -------------------

def update_text_content_options():
    """Atualiza a lista de conteúdos para a aba de Texto."""
    disc_selecionada = st.session_state.disc_text_key
    # Pega os objetos de conteúdo da disciplina selecionada
    conteudos_objs = conteudos_por_disciplina.get(disc_selecionada, [])
    # Extrai apenas os 'labels' formatados para o selectbox
    st.session_state.conteudos_text_labels = [obj['label'] for obj in conteudos_objs]

    # Garante que o conteúdo selecionado é o primeiro da nova lista
    if st.session_state.conteudos_text_labels:
        st.session_state.content_text_key = st.session_state.conteudos_text_labels[0]
    else:
        st.session_state.content_text_key = ""


def update_pdf_content_options():
    """Atualiza a lista de conteúdos para a aba de PDF."""
    disc_selecionada = st.session_state.disc_pdf_key
    # Pega os objetos de conteúdo da disciplina selecionada
    conteudos_objs = conteudos_por_disciplina.get(disc_selecionada, [])
    # Extrai apenas os 'labels' formatados para o selectbox
    st.session_state.conteudos_pdf_labels = [obj['label'] for obj in conteudos_objs]

    # Garante que o conteúdo selecionado é o primeiro da nova lista
    if st.session_state.conteudos_pdf_labels:
        st.session_state.content_pdf_key = st.session_state.conteudos_pdf_labels[0]
    else:
        st.session_state.content_pdf_key = ""


# ------------------- FUNÇÕES (MANTIDAS) -------------------

def extract_text_from_pdf(uploaded_file):
    """Extrai texto de PDF usando pdfplumber"""
    if isinstance(uploaded_file, str):
        return f"Texto simulado de: {uploaded_file}"

    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def enviar_n8n(dados):
    WEBHOOK_URLS = "https://n8n-n8n-ortiz.q2cira.easypanel.host/webhook-test/caderno-turma"
    response = requests.post(WEBHOOK_URLS, json=dados)
    if response.status_code == 200:
        st.success("✅ Dados enviados com sucesso (TESTE)!")
        return None

    # Caso a primeira tentativa falhe (mantido da lógica original)
    if response.status_code != 200:
        WEBHOOK_URLS2 = "https://n8n-n8n-ortiz.q2cira.easypanel.host/webhook/caderno-turma"
        response = requests.post(WEBHOOK_URLS2, json=dados)
        if response.status_code == 200:
            st.success("✅ Dados enviados com sucesso (PRODUÇÃO)!")
            return None
    else:
        st.error(f"❌ Erro ao enviar dados: {response.text}")

    return None


# ------------------- CONFIGURAÇÃO E ESTILOS -------------------

st.set_page_config(page_title="Envio de Caderno", page_icon="📚", layout="wide")

# 🎨 INJETAR O CSS A PARTIR DO ARQUIVO (BLOQUEIO DE ERROS INESPERADOS)
custom_css = """
.main-header {
    padding-bottom: 20px;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 15px;
}
.stTabs [data-baseweb="tab"] {
    font-size: 18px;
    padding: 10px 15px;
    border-radius: 8px 8px 0 0;
}
"""
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# ===============================================================
# DADOS GLOBAIS E INICIALIZAÇÃO DO ESTADO
# ===============================================================
usuario = st.session_state.get("usuario_logado", "Usuário desconhecido")
data_upload = date.today()

# --- Inicialização de Session State para Reatividade (usando os labels formatados) ---

initial_content_objs = conteudos_por_disciplina[primeira_disciplina]
initial_labels = [obj['label'] for obj in initial_content_objs]

# Aba de Texto
if 'disc_text_key' not in st.session_state:
    st.session_state.disc_text_key = primeira_disciplina
if 'conteudos_text_labels' not in st.session_state:
    st.session_state.conteudos_text_labels = initial_labels
if 'content_text_key' not in st.session_state:
    st.session_state.content_text_key = initial_labels[0] if initial_labels else ""
if 'tipo_conteudo_text_key' not in st.session_state:  # NOVO
    st.session_state.tipo_conteudo_text_key = TIPOS_CONTEUDO[0]  # NOVO: Inicia com "Caderno"

# Aba de PDF
if 'disc_pdf_key' not in st.session_state:
    st.session_state.disc_pdf_key = primeira_disciplina
if 'conteudos_pdf_labels' not in st.session_state:
    st.session_state.conteudos_pdf_labels = initial_labels
if 'content_pdf_key' not in st.session_state:
    st.session_state.content_pdf_key = initial_labels[0] if initial_labels else ""
if 'tipo_conteudo_pdf_key' not in st.session_state:  # NOVO
    st.session_state.tipo_conteudo_pdf_key = TIPOS_CONTEUDO[0]  # NOVO: Inicia com "Caderno"

# --- Estado de Upload de PDF (Mantido) ---
if 'extracted_text_pdf' not in st.session_state:
    st.session_state.extracted_text_pdf = ""
if 'uploaded_file_pdf_name' not in st.session_state:
    st.session_state.uploaded_file_pdf_name = ""
if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = None

# ------------------- INTERFACE PRINCIPAL -------------------

st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.subheader("📝 Enviar Anotações e Cadernos para Base de Dados", divider="rainbow")

with st.expander("❓ Como enviar os cadernos, anotações, livros e slides."):
    st.markdown('')
    st.markdown(
        """
        Esta ferramenta permite o envio dos seus materiais de estudo **(cadernos, anotações, slides e livros)** para o banco de dados do sistema.
        Este conteúdo será lido e processado pelo sistema e pelas IAs para gerar resumos, insights e respostas precisas na MonitorIA.

        Você pode enviar o material de duas formas:
        1.  **Cópia e Cola:** Insira o texto diretamente no campo.
        2.  **Upload de Arquivo:** Carregue um arquivo **PDF**.
        """
    )
    st.markdown("---")
    st.markdown("##### Processamento das Anotações")
    st.markdown(
        """
        Ao carregar um **arquivo**, o sistema automaticamente gera **dois bancos de dados**:

        * **Banco de Dados Vetorizado:** Utilizado pelo **Agente RAG (Retrieval-Augmented Generation)** da MonitorIA para consultas precisas e respostas baseadas no seu conteúdo.
        * **Banco de Dados em Tabela:** Utilizado pelo **Gerador de Resumos** para processamento e estruturação de texto em formatos legíveis e organizados.
        """
    )
    st.divider()

tab_pdf, tab_text = st.tabs(["📄 Upload de PDF", "✍️Texto (Copia e Cola)", ])

# ===============================================================
# TAB 1: TEXTO COPIA E COLA
# ===============================================================
with tab_text:
    with st.container(border=True):
        st.subheader("✍️Inserir Anotações Manualmente")

        st.info("Preencher os **parâmetros** abaixo com atenção!")

        # Novo Layout com 3 Colunas: Disciplina, Conteúdo e Tipo de Conteúdo
        col_disc_t, col_cont_t, col_tipo_t = st.columns(3)

        with col_disc_t:
            # Disciplina (com on_change para atualizar o Conteúdo)
            st.selectbox(
                "Selecione a Disciplina",
                options=disciplinas,
                key="disc_text_key",
                on_change=update_text_content_options,
                help="Disciplina relacionada ao conteúdo deste caderno."
            )

        with col_cont_t:
            # Conteúdo (dinâmico, lendo de st.session_state, e contendo a Semana e a Data)
            st.selectbox(
                "Selecione o Conteúdo (Semana - Data - Tópico)",
                options=st.session_state.conteudos_text_labels,
                key="content_text_key",
                help="Tópico específico abordado. O formato é: [Semana] - [Data (dd/mm)] - [Tópico]."
            )

        with col_tipo_t:
            # Tipo de Conteúdo
            st.selectbox(
                "Selecione o Tipo de Conteúdo",
                options=TIPOS_CONTEUDO,
                key="tipo_conteudo_text_key",
                help="Identifica se o material é um caderno pessoal ou um material didático oficial."
            )

        st.markdown("##### Conteúdo em Texto")
        st.text_area(
            "Cole o conteúdo do caderno/anotações aqui:",
            placeholder="Cole aqui seu texto da sua anotação/caderno aqui...",
            height=300,
            key="conteudo_text",
            help="Copie e cole aqui o texto integral das anotações ou resumo da aula."
        )

        st.markdown("---")

        # Botão de envio
        if st.button("📤 Adicionar no Banco", key="submit_text", type="primary"):

            disc_selecionada = st.session_state.disc_text_key
            conteudo_input = st.session_state.conteudo_text
            cont_selecionado_completo = st.session_state.content_text_key
            tipo_conteudo = st.session_state.tipo_conteudo_text_key

            if conteudo_input.strip() == "":
                st.warning("📌 O conteúdo não pode estar vazio. Cole suas anotações antes de enviar.")
            elif not cont_selecionado_completo:
                st.warning("📌 Selecione um Conteúdo Específico antes de enviar.")
            else:
                try:
                    # Extração 'backend-only': Separa Semana, Data (dd/mm) e Conteúdo do string selecionado
                    # A função split(' - ', 2) garante que o conteúdo específico pode conter hífens ou ' - '
                    week_str, date_str_ddmm, conteudo_especifico = cont_selecionado_completo.split(' - ', 2)
                    semana_aula = int(week_str)
                    # CONVERSÃO INTERNA (BACKEND-ONLY)
                    data_aula_iso = convert_ddmm_to_iso(date_str_ddmm)

                except ValueError:
                    st.error(
                        "❌ Erro ao extrair o número da semana, data e conteúdo selecionado. Verifique o formato. String de conteúdo: " + cont_selecionado_completo)

                dados = {
                    "conteudo": conteudo_input,
                    "usuario": usuario,
                    "data_upload": str(data_upload),
                    "data_aula": data_aula_iso,  # Enviado no formato YYYY-MM-DD
                    "semana_aula": semana_aula,
                    "disciplina": disc_selecionada,
                    "conteudo_especifico": conteudo_especifico,
                    "tipo_conteudo": tipo_conteudo
                }
                enviar_n8n(dados)
                # Opcional: Limpar o text_area após o envio

# ===============================================================
# TAB 2: PDF UPLOAD
# ===============================================================

with tab_pdf:
    with st.container(border=True):
        st.subheader("📄 Extrair e Enviar Conteúdo de Arquivo PDF")

        # 1. Parâmetros
        st.info("Preencher os **parâmetros** abaixo com atenção!")

        # Novo Layout com 3 Colunas: Disciplina, Conteúdo e Tipo de Conteúdo
        col_disc_p, col_cont_p, col_tipo_p = st.columns(3)

        with col_disc_p:
            # Disciplina (com on_change para atualizar o Conteúdo)
            st.selectbox(
                "Selecione a Disciplina",
                options=disciplinas,
                key="disc_pdf_key",
                on_change=update_pdf_content_options,
                help="Disciplina relacionada ao conteúdo deste caderno."
            )

        with col_cont_p:
            # Conteúdo (dinâmico, lendo de st.session_state, e contendo a Semana e a Data)
            st.selectbox(
                "Selecione o Conteúdo (Semana - Data - Tópico)",
                options=st.session_state.conteudos_pdf_labels,
                key="content_pdf_key",
                help="Tópico específico abordado. O formato é: [Semana] - [Data (dd/mm)] - [Tópico]."
            )

        with col_tipo_p:
            # Tipo de Conteúdo
            st.selectbox(
                "Selecione o Tipo de Conteúdo",
                options=TIPOS_CONTEUDO,
                key="tipo_conteudo_pdf_key",
                help="Identifica se o material é um caderno pessoal ou um material didático oficial."
            )

        st.markdown("#### Seleção do Arquivo")


        # 2. Upload do Arquivo (A extração é disparada no 'on_change')
        def handle_pdf_upload():
            """Lida com o upload, extrai o texto e armazena no session_state."""
            uploaded_file = st.session_state.get('file_pdf_uploader')

            # Limpa o feedback anterior ao iniciar a extração ou se o arquivo for removido
            st.session_state.feedback_message = None

            if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_file_pdf_name:
                try:
                    # NOTA: O pdfplumber requer um objeto de arquivo aberto.
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    st.session_state.extracted_text_pdf = extracted_text
                    st.session_state.uploaded_file_pdf_name = uploaded_file.name
                    st.session_state.feedback_message = {
                        "type": "success",
                        "text": f"✅ Texto extraído de {uploaded_file.name} com sucesso! Verifique a prévia abaixo."
                    }
                except Exception as e:
                    st.session_state.extracted_text_pdf = ""
                    st.session_state.uploaded_file_pdf_name = ""
                    st.session_state.feedback_message = {
                        "type": "error",
                        "text": f"⚠️ Erro na extração: {e}"
                    }
            elif uploaded_file is None:
                st.session_state.extracted_text_pdf = ""
                st.session_state.uploaded_file_pdf_name = ""


        uploaded_file_obj = st.file_uploader(
            "Selecione o arquivo PDF com conteúdo da aula (O texto será extraído automaticamente):",
            type=["pdf"],
            key="file_pdf_uploader",
            on_change=handle_pdf_upload
        )

        # 3. Exibição e Confirmação
        extracted_text = st.session_state.extracted_text_pdf

        # Exibir feedback de sucesso/erro da extração
        if st.session_state.feedback_message:
            if st.session_state.feedback_message["type"] == "success":
                st.success(st.session_state.feedback_message["text"])
            elif st.session_state.feedback_message["type"] == "error":
                st.error(st.session_state.feedback_message["text"])

        if extracted_text:
            st.markdown("---")
            # Exibir prévia do texto extraído para confirmação
            with st.expander(f"✅ Prévia do Conteúdo Extraído de: **{st.session_state.uploaded_file_pdf_name}**"):
                st.markdown(extracted_text[:5000] + (
                    "\n\n*(... Conteúdo cortado na prévia. O texto COMPLETO será enviado para o banco de dados.)*" if len(
                        extracted_text) > 5000 else ""))

            # 4. Botão de Submissão Final
            st.markdown("#### Confirmação de Envio")
            st.info(
                "⚠️ Ao clicar no botão abaixo, o texto extraído será enviado para a fila de processamento da MonitorIA (Supabase/n8n).")

            if st.button("📤 Adicionar no Banco", key="submit_pdf", type="primary"):

                # Usa os valores armazenados no session_state
                disc_selecionada = st.session_state.disc_pdf_key
                cont_selecionado_completo = st.session_state.content_pdf_key
                extracted_text_to_send = st.session_state.extracted_text_pdf  # Pega o texto completo
                tipo_conteudo = st.session_state.tipo_conteudo_pdf_key  # NOVO

                if extracted_text_to_send.strip() == "":
                    st.error("⚠️ Nenhum texto encontrado para enviar. Por favor, carregue um PDF válido.")
                elif not cont_selecionado_completo:
                    st.warning("📌 Selecione um Conteúdo Específico antes de enviar.")
                else:
                    try:
                        # Extração 'backend-only': Separa Semana, Data (dd/mm) e Conteúdo do string selecionado
                        week_str, date_str_ddmm, conteudo_especifico = cont_selecionado_completo.split(' - ', 2)
                        semana_aula = int(week_str)
                        # CONVERSÃO INTERNA (BACKEND-ONLY)
                        data_aula_iso = convert_ddmm_to_iso(date_str_ddmm)

                    except ValueError:
                        st.error(
                            "❌ Erro ao extrair o número da semana, data e conteúdo selecionado. Verifique o formato. String de conteúdo: " + cont_selecionado_completo)
                        # st.stop()

                    # Preparar e enviar dados
                    with st.spinner("🚀 Enviando para o Banco de Dados (Supabase/n8n)..."):
                        dados = {
                            "conteudo": extracted_text_to_send,  # Variável para o texto
                            "usuario": usuario,
                            "data_upload": str(data_upload),
                            "data_aula": data_aula_iso,  # Enviado no formato YYYY-MM-DD
                            "semana_aula": semana_aula,  # Variável para o número da semana
                            "disciplina": disc_selecionada,
                            "conteudo_especifico": conteudo_especifico,
                            "tipo_conteudo": tipo_conteudo  # NOVO: Adicionado ao envio
                        }
                        enviar_n8n(dados)

                    # Limpar estados após o envio final
                    st.session_state.extracted_text_pdf = ""
                    st.session_state.uploaded_file_pdf_name = ""
                    st.session_state.feedback_message = None
        elif uploaded_file_obj is not None:
            # Exibe mensagem de erro se a extração falhou
            pass

criar_rodape()