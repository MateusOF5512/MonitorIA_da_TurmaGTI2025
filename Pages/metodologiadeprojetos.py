import streamlit as st
from supabase import create_client, Client

SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_todos():
    response = supabase.table('todos').select("*").execute()
    return response.data

def add_todos(task):
    supabase.table('todos').insert({'task': task}).execute()


st.subheader("🎯 Metodologia de Projetos", divider="rainbow", anchor=False)

task =  st.text_input("Adicione uma Tarefa:")

if st.button("Adicionar Task"):
    if task:
        add_todos(task)
        st.success("Tarefa Adicionada!")
    else:
        st.error("Adicione uma Tarefa")


st.markdown("### Lista de Tarefas:")

todos = get_todos()
if todos:
    for todo in todos:
        st.write(f"- {todo['task']}")
else:
    st.write("Sem tarefa ainda")

