import streamlit as st
import pandas as pd
from supabase import create_client
from datetime import date
from groq import Groq

# --- Conexão Supabase ---
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Conexão Groq ---
client = Groq(api_key=st.secrets["grok"]["GROK_API"])

# Função para buscar dados apenas da disciplina de Redes
def get_data_redes():
    response = (
        supabase.table("caderno")
        .select("id, conteudo")  # pegando apenas as colunas que interessam
        .eq("disciplina", "Infraestrutura de Redes")
        .execute()
    )
    return response.data

# --- Interface ---
st.subheader("🌐 Infraestrutura de Redes", divider="rainbow", anchor=False)

dados = get_data_redes()

if dados:
    df = pd.DataFrame(dados)
    st.dataframe(df, use_container_width=True)

    # Transformar os conteúdos em um único texto
    conteudos_texto = "\n".join([f"ID {row['id']}: {row['conteudo']}" for row in dados])

    system = """
    O conteduo a seguir é as anotações das aulas da disciplina de Infraestrutura de rede computadores do curso de Gestao da Yecnologia da Infromação,
    Gere um resumo de todo conteúdos a seguir, analise com cuidado todos os conceitos, apresente eles de forma clara e coerente, seu papel é resumir e organizar essas anotações
     para uma facil e rapida a anlise do conteudo, use negrito para reforçar palavras chaves,    """

    if st.button("Gerar Resumo da Disciplina"):
        try:
            # Chamada à IA
            chat_completion = client.chat.completions.create(
                model="groq/compound-mini",
                messages=[
                    {
                        "role": "system",
                        "content": system
                    },
                    {
                        "role": "user",
                        "content": conteudos_texto
                    }
                ],
                temperature=0.2,
                stream=False
            )

            # Captura da resposta
            resposta = chat_completion.choices[0].message.content

            # Exibição no Markdown
            st.subheader("📌 Resumo Gerado pela IA")
            st.markdown(resposta)

        except Exception as e:
            st.error(f"Erro ao gerar resposta: {e}")
else:
    st.info("Nenhum registro encontrado para Infraestrutura de Redes.")
