import streamlit as st
from groq import Groq
from typing import Generator
from supabase import create_client
import time
import pandas as pd
import json
from Functions.database import *


# VARIAVEIS PRICIPAIS:

if "mensagem" not in st.session_state:
    st.session_state.mensagem = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = []

# Para armazenar métricas
if "metrics" not in st.session_state:
    st.session_state.metrics = {"input_tokens": 0, "output_tokens": 0, "elapsed": 0}

conta = st.session_state.usuario_logado


# Função para buscar dados
db = get_data()
# Trnasformar os dados para json para facilitar leitura do modelo de LLM
df = pd.DataFrame(db)
colunas_para_usar = ["id", "conteudo", "usuario", "disciplina"]
df = df[df["disciplina"] == "Infraestrutura de Redes"]

df = df[[c for c in colunas_para_usar if c in df.columns]]
conteudos_json = df.to_dict(orient="records")
dados = json.dumps(conteudos_json, ensure_ascii=False, indent=2)

client = Groq(api_key=st.secrets["grok"]["GROK_API"],
              default_headers={"Groq-Model-Version": "latest"})

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

with st.sidebar:

    with st.container(border=True):
        models = {
            "groq/compound-mini": {"name": "Gorq | Compound Mini | 09/2023", "tokens": 8192},
            "groq/compound": {"name": "Gorq | Compound | 09/2023", "tokens": 8192},
            "openai/gpt-oss-20b": {"name": "OpenAI | GPT OSS 20B | 08/2025", "tokens": 65536},
            "openai/gpt-oss-120b": {"name": "OpenAI | GPT OSS 120B | 08/2025", "tokens": 65536},
            "gemma2-9b-it": {"name": "Google | Gemma 2 9B | 09/2023", "tokens": 8192},
            "llama-3.3-70b-versatile": {"name": "Meta | Llama 3.3 70B | 12/2024", "tokens": 32768},
            "meta-llama/llama-4-maverick-17b-128e-instruct": {"name": "Meta | Llama 4 Maverick 17B | 04/2025", "tokens": 8192,},
            "qwen/qwen3-32b": {"name":"Alibaba | Qwen3 32B | 05/2025", "tokens": 16384},
            "deepseek-r1-distill-llama-70b": {"name": "DeepSeek | R1 Llama 70B | 01/2025", "tokens": 4096}
        }

        model_options = st.selectbox(
                "Selecione um Modelo de Linguagem Natural:",
                options=list(models.keys()),
                format_func=lambda x: models[x]["name"],
                index=0
            )

        if st.session_state.selected_model != model_options:
            st.session_state.mensagem = []
            st.session_state.selected_model = model_options
            st.rerun()

        max_tokens_range = models[model_options]["tokens"]

        max_tokens = st.slider("Máximo de Tokens para o Modelo:",
                               min_value=512, max_value=max_tokens_range,
                               value=int(max_tokens_range/2), step=512)

        temperature = st.slider("Selecione a Criatividade do Modelo:",
                               min_value=0.1, max_value=2.0,
                               value=0.4, step=0.2)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown("")
    with col2:
        if st.button("Reiniciar conversa"):
            st.session_state.mensagem = []
            st.session_state.metrics = {"input_tokens": 0, "output_tokens": 0, "elapsed": 0}
            st.rerun()
    with col3:
        st.markdown("")


st.subheader("👨‍🏫 MonitorIA da Turma", divider="rainbow", anchor=False)

for mensagem in st.session_state.mensagem:
    avatar = "👨‍🏫" if mensagem["role"] == "assistant" else "👨‍🎓"
    with st.chat_message("role", avatar=avatar):
        st.markdown(mensagem["content"])

if prompt := st.chat_input("Pergunte algo sobre as aulas do curso de Gestão de TI..."):
    st.session_state.mensagem.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    conteudos_texto = dados
    system = f"""
    Você é o Monitor da Turma, um assistente acadêmico experiente que fornece informações a turma de Gestão de TI sobre os cadernos e anotações das aulas, paciente e altamente didático do curso de Gestão da Tecnologia da Informação do IFSC Florianópolis. 
    Seu papel é **auxiliar os estudantes exclusivamente com base nos dados fornecidos abaixo** (cadernos/arquivos do banco). Siga estas instruções estritas:
    
    0. Entenda seu papel como Monitor da Turma, responda de froma clara e educada, se apresente se necessário.
    1. Responda sempre em **português** e em **apenas um ou dois parágrafos** de forma clara, objetiva e didática.
    2. Use **negrito** (Markdown `**texto**`) para destacar palavras-chave e conceitos essenciais.
    3. **Baseie sua resposta unicamente** nas informações contidas em `conteudos_texto`. **Não** gere, suponha ou invente fatos que não estejam no banco de dados.
    4. Analise cuidadosamente os registros disponíveis; se a resposta vier da síntese de vários registros, sintetize-os / resuma e **cite os IDs usados** ao final do parágrafo no formato: `[IDs: ID1, ID2; usuário: NOME (se disponível); disciplina: NOME (se disponível); data: AAAA-MM-DD (se disponível)]`, use ITALICO para destacar as referncias, sempre citas as referencias no final da resposta ou depois de uma explicação.
    4.1 Se sua resposta final nao tiver disponivel no conteudos_texto não gere referencias, fale "Sem referencias no material disponível" em negrito, analise com cuidado se sua resposta tem referencia ou nao e informe com exatidao ao usuario
    5. Sempre que possível, extraia e apresente — dentro do mesmo parágrafo — as **referências** indicando de qual conteúdo a resposta foi gerada: **ID do registro**, **autor/usuário** que gerou o caderno (se existir), **disciplina** e **data da aula**. Se algum metadado estiver ausente, indique explicitamente `(metadado não disponível)`.
    6. Se os dados forem insuficientes para fornecer uma resposta completa, responda em um parágrafo dizendo claramente que **não há informação suficiente** e sugira quais informações ou quais IDs/arquivos adicionais são necessários.
    7. Se houver entradas conflitantes nos dados, aponte a contradição e cite os IDs conflitantes.
    8. Evite jargões desnecessários; priorize uma explicação passo-a-passo simples e acionável quando útil.
    9. Mantenha um tom acolhedor, respeitoso e voltado ao aprendizado do aluno.

    Dados a serem usados (não altere): {conteudos_texto}
    """

    try:
        start_time = time.time()

        chat_completion = client.chat.completions.create(
            model=model_options,
            messages=[{"role": "system", "content": system}] + st.session_state.mensagem,
            max_completion_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        with st.chat_message("assistant", avatar='👨‍🏫'):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

        elapsed = time.time() - start_time


        # --- Estimativa de tokens (simples e incluindo o texto do sistema) ---
        # 1 token ≈ 4 caracteres em média (estimativa usada pela OpenAI)
        def estimar_tokens(texto):
            return len(texto) / 4  # aproximação leve, sem depender de tiktoken


        # Soma de todos os textos do usuário e do sistema
        entrada_total = system + " ".join(m["content"] for m in st.session_state.mensagem)

        input_tokens = int(estimar_tokens(entrada_total))
        output_tokens = int(estimar_tokens(full_response))

        st.session_state.metrics = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "elapsed": elapsed
        }

    except Exception as e:
        st.error(e)

    try:
        if isinstance(full_response, str):
            st.session_state.mensagem.append({"role": "assistant", "content": full_response})
        else:
            combined_response = '\n'.join(str(item) for item in full_response)
            st.session_state.mensagem.append({"role": "assistant", "content": combined_response})

    except:
        st.error("Maxímo de Tokens desse Modelo alcançado! Teste daqui a pouco.")

    col1, col2, col3 =  st.columns(3)
    with col1:
        st.write(f"🔹 Tokens de Entrada: **{st.session_state.metrics['input_tokens']}**")
    with col2:
        st.write(f"🔹 Tokens de Saída: **{st.session_state.metrics['output_tokens']}**")
    with col3:
        st.write(f"⏱️ Tempo de Resposta: **{st.session_state.metrics['elapsed']:.2f}s**")

# --- Exibir métricas no sidebar ---

