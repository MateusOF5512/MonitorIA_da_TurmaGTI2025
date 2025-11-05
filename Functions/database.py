from supabase import create_client
import streamlit as st
import json
import pandas as pd


SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_data_disciplina(disciplina, semana_aula):
    response = (
        supabase.table("conteudo_aulas")
        .select("conteudo, usuario, semana_aula, data_aula, disciplina")
        .eq("disciplina", disciplina)
        .eq("semana_aula", semana_aula)
        .execute()
    )
    return response.data


def transforma_json(df):
    # Trnasformar os dados para json para facilitar leitura do modelo de LLM
    colunas_para_usar = ["conteudo", "usuario"]
    df = df[[c for c in colunas_para_usar if c in df.columns]]
    conteudos_json = df.to_dict(orient="records")
    dados_json = json.dumps(conteudos_json, ensure_ascii=False, indent=2)

    return dados_json

#####################################################################################################
