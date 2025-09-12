import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

@st.cache_data
def load_google_sheet():
    # Autenticação do Google
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)  # Converter a string JSON em um dicionário

    # Autenticar usando as credenciais carregadas
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Carregar a planilha do Google Sheets
    url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet("Página1")

    # Converter os dados da planilha em um DataFrame do Pandas
    data = sheet.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df.index = df.index + 1


    return df


def append_to_google_sheet(df_novo):
    try:
        if df_novo.empty:
            st.warning("O DataFrame está vazio. Nada foi enviado ao Google Sheets.")
            return False

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        creds_json = st.secrets["google"]["credentials_json"]
        creds_dict = json.loads(creds_json)

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
        sheet = client.open_by_url(url).worksheet("Página1")

        # Trata o DataFrame
        df_str = df_novo.fillna("").astype(str)
        valores = df_str.values.tolist()

        sheet.append_rows(valores, value_input_option="USER_ENTERED")

        st.success("Dados adicionados ao Google Sheets com sucesso!")
        return True

    except Exception as e:
        st.error(f"Erro ao adicionar dados ao Google Sheets: {e}")
        return False


def add_row_to_google_sheet(row_data):
    """
    Adiciona uma nova linha ao Google Sheets.

    Parâmetros:
    row_data (list): Lista com os dados em ordem correspondente aos cabeçalhos da planilha.
    """
    # Autenticação (mesmo processo da função load_google_sheet)
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Abrir a planilha e a aba desejada
    url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet("Página1")

    # Adicionar a nova linha ao final da planilha
    sheet.append_row(row_data)

    return True


def update_cell_in_google_sheet(linha, coluna_nome, novo_valor):
    """
    Atualiza uma célula específica no Google Sheets.

    Parâmetros:
    linha (int): número da linha (começa em 1, incluindo cabeçalho).
    coluna_nome (str): nome da coluna conforme aparece no cabeçalho.
    novo_valor: novo valor a ser inserido na célula.
    """
    # Autenticação
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Abrir a planilha e a aba
    url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet("Página1")

    # Buscar o índice da coluna com base no cabeçalho
    headers = sheet.row_values(1)
    if coluna_nome not in headers:
        raise ValueError(f"Coluna '{coluna_nome}' não encontrada.")

    coluna_index = headers.index(coluna_nome) + 1  # gspread começa em 1

    # Atualizar a célula
    sheet.update_cell(linha+1, coluna_index, novo_valor)

    return True

def update_row_in_google_sheet(linha, novos_dados_dict):
    """
    Atualiza uma linha inteira no Google Sheets com base nos nomes das colunas.

    Parâmetros:
    linha (int): número da linha (começa em 1, incluindo cabeçalho).
    novos_dados_dict (dict): dicionário no formato {coluna: novo_valor}
    """
    # Autenticação
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Abrir a planilha e a aba
    url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet("Página1")

    # Pegar os cabeçalhos para localizar as colunas
    headers = sheet.row_values(1)

    for coluna_nome, novo_valor in novos_dados_dict.items():
        if coluna_nome not in headers:
            raise ValueError(f"Coluna '{coluna_nome}' não encontrada.")
        coluna_index = headers.index(coluna_nome) + 1  # gspread começa em 1
        sheet.update_cell(linha + 1, coluna_index, novo_valor)  # +1 porque linha 1 é o cabeçalho

    return True


def delete_row_in_google_sheet(linha):
    """
    Exclui uma linha específica do Google Sheets.

    Parâmetros:
    linha (int): número da linha a ser excluída (começa em 1, incluindo cabeçalho).
                 Normalmente você vai querer pular o cabeçalho (linha 1).
    """
    # Autenticação
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Abrir a planilha e a aba
    url = 'https://docs.google.com/spreadsheets/d/1y0sC7iVh0rXNIbYNzMHiz1S5qiOBY7rJEi3CuBAC4fs/edit?usp=sharing'
    sheet = client.open_by_url(url).worksheet("Página1")

    # Excluir a linha
    sheet.delete_rows(linha+1)

    return True


#########################################################################################################
# FUNÇÕES DE VISUALIZAÇÃO E ATUALIZAÇÃO DO BANCO DE DADOS DO HISTICO DE ATIVIDADES
#########################################################################################################

@st.cache_data
def load_historico():
    # Autenticação do Google
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)  # Converter a string JSON em um dicionário

    # Autenticar usando as credenciais carregadas
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Carregar a planilha do Google Sheets
    url = st.secrets["google_sheets"]["url2"]
    sheet_historico_atividades = client.open_by_url(url).worksheet("Página1")

    # Converter os dados da planilha em um DataFrame do Pandas
    data = sheet_historico_atividades.get_all_values()
    headers = data.pop(0)
    df = pd.DataFrame(data, columns=headers)
    df.index = df.index + 1

    df.sort_values(by=['DATA', 'HORARIO'], ascending=[False, False], inplace=True)

    return df

def add_row_historico(row_data):
    # Autenticação do Google
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds_json = st.secrets["google"]["credentials_json"]
    creds_dict = json.loads(creds_json)  # Converter a string JSON em um dicionário

    # Autenticar usando as credenciais carregadas
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    # Carregar a planilha do Google Sheets
    url = st.secrets["google_sheets"]["url2"]
    sheet_historico_atividades = client.open_by_url(url).worksheet("Página1")

    # Adicionar a nova linha ao final da planilha
    sheet_historico_atividades.append_row(row_data)

    return True



@st.dialog("Criar linha nova", width="large")
def add(df):
    novo_id = (pd.to_numeric(df["id_experimento"]).max() + 1)
    conta = st.session_state.usuario_logado
    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    hoje = now.date()
    hora = now.time()

    # =====================
    # SEÇÃO 1 - MATERIAIS
    # =====================
    with st.container(border=True):
        st.subheader("Material usado")
        col1, col2, col3 = st.columns(3)
        with col1:
            id_experimento = st.text_input("**ID do Experimento:**", key="id_experimento", value=novo_id)
        with col2:
            nome_material = st.text_input("**Nome do Material:**", key="nome_material")
        with col3:
            fabricante_material = st.text_input("**Fabricante:**", key="fabricante_material")

        col4, col5, col6 = st.columns(3)
        with col4:
            cor_material = st.text_input("**Cor:**", key="cor_material")
        with col5:
            tipo_material = st.text_input("**Tipo do Material:**", key="tipo_material")
        with col6:
            densidade_material = st.number_input(
                "**Densidade (g/cm³):**", key="densidade_material", min_value=0.0, format="%.2f"
            )

    # =====================
    # SEÇÃO 2 - IMPRESSÃO
    # =====================
    with st.container(border=True):
        st.subheader("Impressão 3D")
        col1, col2, col3 = st.columns(3)
        with col1:
            formato_amostra = st.text_input("**Formato da Amostra:**", key="formato_amostra")
        with col2:
            dimensoes_amostra = st.text_input("**Dimensões (mm):**", key="dimensoes_amostra")
        with col3:
            metodo_impressao = st.text_input("**Método de Impressão:**", key="metodo_impressao")

        col4, col5, col6 = st.columns(3)
        with col4:
            temperatura_impressao = st.number_input("**Temperatura de Impressão (°C):**", key="temperatura_impressao", min_value=0)
        with col5:
            velocidade_impressao = st.number_input("**Velocidade de Impressão (mm/s):**", key="velocidade_impressao", min_value=0)
        with col6:
            data_impressao = st.date_input("**Data de Impressão:**", key="data_impressao", value=hoje, format="DD/MM/YYYY")

    # =====================
    # SEÇÃO 3 - EXPERIMENTO
    # =====================
    with st.container(border=True):
        st.subheader("Experimento")
        col1, col2, col3 = st.columns(3)
        with col1:
            tipo_radiacao = st.text_input("**Tipo de Radiação:**", key="tipo_radiacao")
        with col2:
            dose_radiacao_gy = st.number_input("**Dose (Gy):**", key="dose_radiacao_gy", min_value=0.0, format="%.2f")
        with col3:
            tempo_exposicao_min = st.number_input("**Tempo de Exposição (min):**", key="tempo_exposicao_min", min_value=0)

        col4, col5, col6 = st.columns(3)
        with col4:
            temperatura_ambiente = st.number_input("**Temperatura Ambiente (°C):**", key="temperatura_ambiente", min_value=0)
        with col5:
            umidade_ambiente = st.number_input("**Umidade Ambiente (%):**", key="umidade_ambiente", min_value=0, max_value=100)
        with col6:
            data_ensaio = st.date_input("**Data do Ensaio:**", key="data_ensaio", value=hoje, format="DD/MM/YYYY")

    # =====================
    # SEÇÃO 4 - RESULTADOS
    # =====================
    with st.container(border=True):
        st.subheader("Resultados")
        col1, col2, col3 = st.columns(3)
        with col1:
            resultado_visual = st.text_input("**Resultado Visual:**", key="resultado_visual")
        with col2:
            resultado_mecanico = st.text_input("**Resultado Mecânico:**", key="resultado_mecanico")
        with col3:
            massa_antes_g = st.number_input("**Massa Antes (g):**", key="massa_antes_g",
                                            min_value=0.0, max_value=100.0, format="%.2f", step=0.1)
            massa_antes_g = float(str(massa_antes_g).replace(",", "."))

        col4, col5, col6 = st.columns(3)
        with col4:
            massa_depois_g = st.number_input("**Massa Depois (g):**", key="massa_depois_g", min_value=0.0, format="%.2f")
        with col5:
            resistencia_tracao = st.number_input("**Resistência à Tração (MPa):**", key="resistencia_tracao", min_value=0.0, format="%.2f")
        with col6:
            observacoes = st.text_input("**Observações:**", key="observacoes")

    # =====================
    # SEÇÃO 5 - RESPONSÁVEIS
    # =====================
    with st.container(border=True):
        st.subheader("Responsáveis e Registro")
        col1, col2 = st.columns(2)
        with col1:
            responsavel_experimento = st.text_input("**Responsável pelo Experimento:**", key="responsavel_experimento")
        with col2:
            responsavel_registro = st.text_input("**Responsável pelo Registro:**", key="responsavel_registro", value=conta)

        col3, col4 = st.columns(2)
        with col3:
            horario_registro = st.time_input("**Horário de Registro:**", key="horario_registro", value=hora)
        with col4:
            data_registro = st.date_input("**Data de Registro:**", key="data_registro", value=hoje, format="DD/MM/YYYY")

    col1b, col2b, col3b = st.columns(3)
    with col1b:
        st.markdown('')
    with col2b:
        if st.button("Salvar linha", use_container_width=True):
            st.session_state.add = {
                "id_experimento": id_experimento,
                "nome_material": nome_material,
                "fabricante_material": fabricante_material,
                "cor_material": cor_material,
                "tipo_material": tipo_material,
                "densidade_material": densidade_material,
                "formato_amostra": formato_amostra,
                "dimensoes_amostra": dimensoes_amostra,
                "metodo_impressao": metodo_impressao,
                "temperatura_impressao": temperatura_impressao,
                "velocidade_impressao": velocidade_impressao,
                "data_impressao": data_impressao.strftime("%d/%m/%Y") if hasattr(data_impressao,
                                                                                 "strftime") else data_impressao,
                "tipo_radiacao": tipo_radiacao,
                "dose_radiacao_gy": dose_radiacao_gy,
                "tempo_exposicao_min": tempo_exposicao_min,
                "temperatura_ambiente": temperatura_ambiente,
                "umidade_ambiente": umidade_ambiente,
                "data_ensaio": data_ensaio.strftime("%d/%m/%Y") if hasattr(data_ensaio, "strftime") else data_ensaio,
                "resultado_visual": resultado_visual,
                "resultado_mecanico": resultado_mecanico,
                "massa_antes_g": massa_antes_g,
                "massa_depois_g": massa_depois_g,
                "resistencia_tracao": resistencia_tracao,
                "observacoes": observacoes,
                "responsavel_experimento": responsavel_experimento,
                "responsavel_registro": responsavel_registro,
                "data_registro": data_registro.strftime("%d/%m/%Y") if hasattr(data_registro,
                                                                               "strftime") else data_registro,
                "horario_registro": horario_registro.strftime("%H:%M:%S") if hasattr(horario_registro,
                                                                                     "strftime") else horario_registro
            }
            st.rerun()
    with col3b:
        st.markdown('')


@st.dialog("Criar Linhas com Planilha", width="large")
def add_planilha():
    df_csv = 0

    uploaded_files = st.file_uploader(
        "Escolha um arquivos CSV compativel:",
        type="csv",
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.markdown(f"### 📄 Arquivo: {uploaded_file.name}")

            try:
                # Lê o CSV diretamente como DataFrame
                df_csv = pd.read_csv(uploaded_file)
                st.dataframe(df_csv)

            except Exception as e:
                st.error(f"Erro ao ler o arquivo {uploaded_file.name}: {e}")

    if st.button("Criar com Planilha"):
        st.session_state.add_planilha = df_csv
        st.rerun()

@st.dialog("Atualizar Informação", width="large")
def upt(df):

    shape = df.shape[0]
    linha = st.number_input('Digite o INDEX da informação que deseja atualizar:',
                            min_value=1, max_value=shape, value=1, step=1, key=10)

    df = df.reset_index(drop=False)
    linha_df = df.loc[[linha - 1]]  # colchetes duplos mantém o formato de DataFrame

    st.dataframe(linha_df, hide_index=True)
    st.markdown('')

    col1, col2 = st.columns([1, 1])
    with col1:
        colunas = df.columns.tolist()
        coluna = st.selectbox("Selecione a COLUNA da informação que deseja atualizar:",
                              options=colunas, index=2)
    with col2:
        dado_exemplo = df.loc[linha-1, coluna]
        dado = st.text_input('Digite a NOVA INFORMAÇÃO que substituirá o dado atual:', dado_exemplo)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('')
    with col2:
        if st.button("Salvar Dados", use_container_width=True):
            st.session_state.upt = {"linha": linha,
                                    "coluna": coluna,
                                    "dado": dado}
            st.rerun()
    with col3:
        st.markdown('')



@st.dialog("Atualizar linha", width="large")
def upt_linha(df):

    shape = df.shape[0]
    linha = st.number_input('Digite o INDEX da informação que deseja atualizar:',
                            min_value=1, max_value=shape, value=1, step=1)

    df = df.reset_index(drop=False)
    linha_df = df.loc[[linha - 1]]  # colchetes duplos mantém o formato de DataFrame

    st.dataframe(linha_df, hide_index=True)
    st.markdown('')

    col1, col2 = st.columns(2)
    with col1:
        autor_exemplo = df.loc[linha - 1, 'AUTOR']
        autor = st.text_input('Digite para atualizar o AUTOR:', autor_exemplo)
    with col2:
        material_exemplo = df.loc[linha - 1, 'MATERIAL']
        material = st.text_input('Digite para atualizar o MATERIAL:', material_exemplo)


    col1, col2 = st.columns(2)
    with col1:
        metodo_exemplo = df.loc[linha - 1, 'METODO']
        metodo = st.text_input('Digite para atualizar o METODO:', metodo_exemplo)
    with col2:
        experimento_exemplo = df.loc[linha - 1, 'EXPERIMENTO']
        experimento = st.text_input('Digite para atualizar o EXPERIMENTO:', experimento_exemplo)


    col1, col2 = st.columns(2)
    with col1:
        data_exemplo = df.loc[linha - 1, 'DATA']
        data = st.text_input('Digite para atualizar a DATA:', data_exemplo)

    with col2:
        valor_exemplo = df.loc[linha - 1, 'VALOR']
        try:
            valor_exemplo_int = int(valor_exemplo)
        except (ValueError, TypeError):
            valor_exemplo_int = 1  # ou algum valor seguro como padrão
        valor = st.number_input('Digite para atualizar o VALOR:',
                                min_value=0, max_value=1000, value=valor_exemplo_int, step=1)

    st.markdown('---')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('')
    with col2:
        if st.button("Salvar Atualização", use_container_width=True):
            st.session_state.upt_linha = {"data": data,
                                    "autor": autor,
                                    "material": material,
                                    "metodo": metodo,
                                    "experimento": experimento,
                                    "valor": valor, }
            st.rerun()
    with col3:
        st.markdown('')



@st.dialog("Deletar linha", width="large")
def delete_row(df):

    shape = df.shape[0]
    linha = st.number_input('Digite o INDEX da informação que deseja atualizar:',
                            min_value=1, max_value=shape, value=1, step=1)

    df = df.reset_index(drop=False)
    linha_df = df.loc[[linha - 1]]  # colchetes duplos mantém o formato de DataFrame

    st.dataframe(linha_df, hide_index=True)
    st.markdown('')

    st.markdown('---')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('')
    with col2:
        if st.button("Salvar", use_container_width=True, key=20):
            st.session_state.delete_row = {"linha": linha}
            st.rerun()
    with col3:
        st.markdown('')