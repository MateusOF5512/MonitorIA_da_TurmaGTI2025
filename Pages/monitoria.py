import streamlit as st
from groq import Groq
from typing import Generator
from supabase import create_client

# --- Conexão Supabase ---
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para buscar dados apenas da disciplina de Redes
def get_data():
    response = (
        supabase.table("caderno")
        .select("id, conteudo")
        .execute()
    )
    return response.data

dados = get_data()

conta = st.session_state.usuario_logado

st.subheader("👨‍🏫 MonitorIA da Turma", divider="rainbow", anchor=False)

client = Groq(api_key=st.secrets["grok"]["GROK_API"],
              default_headers={"Groq-Model-Version": "latest"})

if "mensagem" not in st.session_state:
    st.session_state.mensagem = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = []

for mensagem in st.session_state.mensagem:
    avatar = "👨‍🏫" if mensagem["role"] == "assistant" else "👨‍🎓"
    with st.chat_message("role", avatar=avatar):
        st.markdown(mensagem["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

with st.sidebar:

    if st.button("Reiniciar conversa"):
        st.session_state.mensagem = []
        st.rerun()


with st.expander("Configurar MonitorIA"):

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
                           value=int(max_tokens_range/3), step=512)

    temperature = st.slider("Selecione a Criatividade do Modelo:",
                           min_value=0.1, max_value=2.0,
                           value=0.4, step=0.2)


if prompt := st.chat_input("Pergunte algo sobre as aulas do curso de Gestão de TI..."):
    st.session_state.mensagem.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    conteudos_texto = "\n".join([f"ID {row['id']}: {row['conteudo']}" for row in dados])
    system = f"""
    Você é o Monitor da Turma (2° fase) de Gestão da Tecnologia da Informação do IFSC Florianopolis,
    seu papel é apenas auxilar os estudantes tirando duvidas sobre o conteudo dos cadernos e arquivos disponivies,
    sua resposta deve ser em apenas um paragrafo, seja claro e coerente, use negrito para reforçar palavras chaves,
    responda apenas com base nos dados do a seguir, nao gere nenhuma infromação nova que nao esteja 
    no banco de dados: {conteudos_texto} 
    """


    try:
        chat_completion = client.chat.completions.create(
            model=model_options,
            messages=[
                         {"role": "system", "content": system}
                     ] + [
                         {"role": m["role"], "content": m["content"]}
                         for m in st.session_state.mensagem
                     ],
            max_completion_tokens=max_tokens,
            temperature=temperature,
            stream=True,
        )

        with st.chat_message("assistant", avatar='👨‍🏫'):
            chat_responses_generator = generate_chat_responses(chat_completion)
            full_response = st.write_stream(chat_responses_generator)

    except Exception as e:
        st.error(e)

    if isinstance(full_response, str):
        st.session_state.mensagem.append({"role": "assistant", "content": full_response})

    else:
        combined_response = '\n'.join(str(item) for item in full_response)
        st.session_state.mensagem.append({"role": "assistant", "content": combined_response})





