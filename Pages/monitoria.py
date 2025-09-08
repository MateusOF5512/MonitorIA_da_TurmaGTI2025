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


if prompt := st.chat_input("Pergunte algo sobre as aulas do curso de Gestão de TI..."):
    st.session_state.mensagem.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    conteudos_texto = "\n".join([f"ID {row['id']}: {row['conteudo']}" for row in dados])
    system = f"""
    Você é o **Monitor da Turma** (2ª fase) do curso de Gestão da Tecnologia da Informação do IFSC Florianópolis.  
    Seu papel é **apenas auxiliar os estudantes** respondendo dúvidas sobre os conteúdos dos cadernos e arquivos fornecidos.  
    
    1 - Regras importantes:
    - Responda **sempre em apenas um parágrafo**.  
    - Seja **claro, direto, coerente e prestativo**.  
    - Use **negrito** para destacar **conceitos, termos técnicos ou pontos principais**.  
    - **Nunca** invente ou complemente com informações externas.  
    - Baseie sua resposta **exclusivamente** nos dados a seguir conteudos_texto: 
    {conteudos_texto}"""


    try:
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                         {"role": "system", "content": system}
                     ] + [
                         {"role": m["role"], "content": m["content"]}
                         for m in st.session_state.mensagem
                     ],
            temperature=0.2,
            top_p= 0.95,
            stream=True,
            reasoning_format="raw",
            reasoning_effort="medium",
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









