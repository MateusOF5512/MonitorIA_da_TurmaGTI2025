from datetime import date
import json
from Functions.database import *
from Functions.grok import *
import pdfplumber
import requests


# ------------------- FUNÇÕES (MANTIDAS) -------------------

def extract_text_from_pdf(uploaded_file):
    """
    Extrai texto de PDF usando pdfplumber
    """
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text


def enviar_n8n(dados):
    """
    Envia dados para webhook n8n (teste + produção)
    """

    WEBHOOK_URLS = "https://n8n-n8n-ortiz.q2cira.easypanel.host/webhook-test/caderno-turma"
    response = requests.post(WEBHOOK_URLS, json=dados)
    if response.status_code == 200:
        st.success("✅ Dados enviados com sucesso (TESTE)!")
        return None

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
try:
    with open("style/style.css", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Arquivo CSS não encontrado em 'style/style.css'. Estilos não aplicados.")
except Exception as e:
    st.warning(f"⚠️ Erro ao carregar CSS: {e}")
# Fim da injeção de CSS

# ===============================================================
# DADOS GLOBAIS
# ===============================================================
usuario = st.session_state.get("usuario_logado", "Usuário desconhecido")
data_upload = date.today()
disciplinas = [
    'Estatística Empresarial',
    'Gestão Organizacional',
    'Infraestrutura de Redes',
    'Metodologia de Projetos',
    'Processo e Desv. de Sistemas',
    'Qualidade de Software',
    'Sist. Operacional (Windows)',
    'Tecnologia de Hardware',
]

# ------------------- INTERFACE PRINCIPAL -------------------

# O CSS aplicado acima garantirá que este título seja estilizado
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
    st.markdown("##### Parâmetros CRÍTICOS para a Organização")
    st.markdown(
        """
        **Atenção!** Os parâmetros de contextualização são essenciais para que o sistema consiga **ler seus cadernos e organizar** o conteúdo de forma correta, garantindo que ele seja associado ao resumo certo.
        Se preenchido de forma incorreta, a informação pode se perder ou atrapalhar a geração de outros resumos.

        Preencha os seguintes parâmetros com precisão antes de clicar em 'Adicionar no Banco':

        | Parâmetro | Descrição e Importância |
        | :--- | :--- |
        | **Disciplina** | **CRÍTICO:** Define a matéria principal para consulta. |
        | **Semana da Aula** | **CRÍTICO:** O número da semana (ex: 1 a 20) do semestre. Esta é a **principal chave** para a IA organizar e recuperar as anotações. |
        | **Data da Aula** | A data específica em que o conteúdo foi lecionado (contexto adicional). |

        Após preencher os dados e inserir o conteúdo (por texto ou PDF), clique em **'Adicionar no Banco'** para salvar o material no seu banco de dados pessoal.
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

# 🌟 NOVO: Uso de st.tabs para um design mais limpo
tab_pdf, tab_text = st.tabs(["📄 Upload de PDF", "✍️Texto (Copia e Cola)",])

# ===============================================================
# TAB 1: TEXTO COPIA E COLA (Com st.form)
# ===============================================================
with tab_text:
    st.subheader("✍️Inserir Anotações Manualmente")

    with st.form("form_text_manual", clear_on_submit=True):
        st.error("Preencher os **parâmetros** abaixo com atenção!")

        # Uso de colunas para organizar os campos em uma linha
        col1_t, col2_t, col3_t = st.columns([1, 1, 1])
        with col1_t:
            data_aula = st.date_input(
                "Data da Aula",
                value=data_upload,
                key="date_text",
                help="A data em que o conteúdo foi lecionado."  # help adicionado
            )
        with col2_t:
            semana_aula = st.number_input(
                "Semana da Aula",
                min_value=1,
                max_value=20,
                step=1,
                value=1,
                key="week_text",
                help="Número da semana do semestre em que esta aula ocorreu (ex: 1 a 20)."  # help adicionado
            )
        with col3_t:
            disciplina = st.selectbox(
                "Selecione a Disciplina",
                options=disciplinas,
                key="disc_text",
                help="Disciplina relacionada ao conteúdo deste caderno."  # help adicionado
            )

        st.markdown("##### Conteúdo em Texto")
        conteudo = st.text_area(
            "Cole o conteúdo do caderno/anotações aqui:",
            placeholder="Cole aqui seu texto da sua anotação/caderno aqui...",
            height=300,
            key="conteudo_text",
            help="Copie e cole aqui o texto integral das anotações ou resumo da aula."  # help adicionado
        )

        st.markdown("---")
        submitted = st.form_submit_button("📤 Adicionar no Banco", type="primary")

        if submitted:
            if conteudo.strip() == "":
                st.warning("📌 O conteúdo não pode estar vazio. Cole suas anotações antes de enviar.")
            else:
                dados = {
                    "conteudo": conteudo,
                    "usuario": usuario,
                    "data_upload": str(data_upload),
                    "data_aula": str(data_aula),
                    "semana_aula": int(semana_aula),
                    "disciplina": disciplina
                }
                enviar_n8n(dados)

# ===============================================================
# TAB 2: PDF UPLOAD (Com st.form e lógica corrigida)
# ===============================================================
if 'extracted_text_pdf' not in st.session_state:
    st.session_state.extracted_text_pdf = ""
if 'uploaded_file_pdf_name' not in st.session_state:
    st.session_state.uploaded_file_pdf_name = ""
if 'feedback_message' not in st.session_state:
    st.session_state.feedback_message = None  # Novo estado para feedback

with tab_pdf:
    with st.container(border=True):
        st.subheader("📄 Extrair e Enviar Conteúdo de Arquivo PDF")

        # 1. Parâmetros (Fora do formulário de envio final para manter o estado)
        st.error("Preencher os **parâmetros** abaixo com atenção!")

        col1_p, col2_p, col3_p = st.columns([1, 1, 1])
        with col1_p:
            data_aula = st.date_input("Data da Aula", value=data_upload, key="date_pdf",
                                      help="A data em que o conteúdo foi lecionado.")
        with col2_p:
            semana_aula = st.number_input("Semana da Aula", min_value=1, max_value=20, step=1, value=1, key="week_pdf",
                                          help="Número da semana do semestre em que esta aula ocorreu (ex: 1 a 20).")
        with col3_p:
            disciplina = st.selectbox("Selecione a Disciplina", options=disciplinas, key="disc_pdf",
                                      help="Disciplina relacionada ao conteúdo deste caderno.")

        st.markdown("#### Seleção do Arquivo")


        # 2. Upload do Arquivo (A extração é disparada no 'on_change')
        def handle_pdf_upload():
            """Lida com o upload, extrai o texto e armazena no session_state."""
            uploaded_file = st.session_state.get('file_pdf_uploader')

            # Limpa o feedback anterior ao iniciar a extração ou se o arquivo for removido
            st.session_state.feedback_message = None

            if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_file_pdf_name:
                try:
                    extracted_text = extract_text_from_pdf(uploaded_file)
                    st.session_state.extracted_text_pdf = extracted_text
                    st.session_state.uploaded_file_pdf_name = uploaded_file.name
                    # Armazenar feedback no estado para ser exibido no próximo ciclo de execução
                    st.session_state.feedback_message = {
                        "type": "success",
                        "text": f"✅ Texto extraído de {uploaded_file.name} com sucesso! Verifique a prévia abaixo."
                    }
                except Exception as e:
                    # Se houver erro, limpa o texto e armazena a mensagem de erro
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
            key="file_pdf_uploader",  # Chave para acessar o objeto do uploader
            on_change=handle_pdf_upload
        )

        # 3. Exibição e Confirmação
        extracted_text = st.session_state.extracted_text_pdf

        # Exibir feedback de sucesso/erro da extração
        if st.session_state.feedback_message:
            # Usar um container para a mensagem ser temporária
            if st.session_state.feedback_message["type"] == "success":
                st.success(st.session_state.feedback_message["text"])
            elif st.session_state.feedback_message["type"] == "error":
                st.error(st.session_state.feedback_message["text"])

        if extracted_text:
            st.markdown("---")
            # Exibir prévia do texto extraído para confirmação
            with st.expander(f"✅ Prévia do Conteúdo Extraído de: **{st.session_state.uploaded_file_pdf_name}**"):
                # Limita a prévia para não poluir
                st.markdown(extracted_text[:5000] + (
                    "\n\n*(... Conteúdo cortado na prévia. O texto COMPLETO será enviado para o banco de dados.)*" if len(
                        extracted_text) > 5000 else ""))

            # 4. Formulário de Submissão Final (Botão para envio)
            with st.form("form_pdf_submit", clear_on_submit=False):
                st.markdown("#### Confirmação de Envio")
                st.info(
                    "⚠️ Ao clicar no botão abaixo, o texto extraído será enviado para a fila de processamento da MonitorIA (Supabase/n8n).")

                submitted_pdf = st.form_submit_button("📤 Adicionar no Banco", type="primary")

                if submitted_pdf:
                    if extracted_text.strip() == "":
                        st.error("⚠️ Nenhum texto encontrado para enviar. Por favor, carregue um PDF válido.")
                    else:
                        # Preparar e enviar dados
                        with st.spinner("🚀 Enviando para o Banco de Dados (Supabase/n8n)..."):
                            dados = {
                                "conteudo": extracted_text,  # O texto COMPLETO está aqui
                                "usuario": usuario,
                                "data_upload": str(data_upload),
                                "data_aula": str(data_aula),
                                "semana_aula": int(semana_aula),
                                "disciplina": disciplina,
                            }
                            # Supondo que 'enviar_n8n' é sua função de envio
                            enviar_n8n(dados)
                            # Feedback de sucesso do envio
                            st.success(
                                f"🎉 Conteúdo de '{st.session_state.uploaded_file_pdf_name}' enviado com sucesso para processamento!")

                        # Limpar TODOS os estados, incluindo a mensagem de feedback.
                        st.session_state.extracted_text_pdf = ""
                        st.session_state.uploaded_file_pdf_name = ""
                        st.session_state.feedback_message = None  # Limpa a mensagem após o envio final
                        # REMOÇÃO DO st.rerun() MANTIDA
        elif uploaded_file_obj is not None:
            # Caso em que o uploaded_file_obj não é None, mas extracted_text_pdf é vazio (erro de extração)
            # O feedback_message já deve ter sido setado no on_change se houve erro.
            if st.session_state.extracted_text_pdf == "" and st.session_state.feedback_message and \
                    st.session_state.feedback_message["type"] == "error":
                # A mensagem de erro será exibida no topo do container.
                pass
            elif st.session_state.extracted_text_pdf == "":
                # Se for None, significa que o arquivo foi limpo ou o on_change não disparou corretamente.
                pass