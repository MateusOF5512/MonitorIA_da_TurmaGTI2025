import streamlit as st
from groq import Groq
from typing import Generator

conta = st.session_state.usuario_logado

st.subheader("👨‍🏫 MonitorIA da Turma", divider="rainbow", anchor=False)

client = Groq(api_key=st.secrets["grok"]["GROK_API"])

if "mensagem" not in st.session_state:
    st.session_state.mensagem = []

for mensagem in st.session_state.mensagem:
    avatar = "👨‍🏫" if mensagem["role"] == "assistant" else "👨‍🎓"
    with st.chat_message("role", avatar=avatar):
        st.markdown(mensagem["content"])

def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


if prompt := st.chat_input("Pergunte algo sobre as aulas do curso de Gestão de TI..."):
    st.session_state.mensagem.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)


    try:
        chat_completion = client.chat.completions.create(
            model="groq/compound-mini",
            messages=[
                         {"role": "system", "content": "Sua resoosta deve ser em apenas um paragrafo"}
                     ] + [
                         {"role": m["role"], "content": m["content"]}
                         for m in st.session_state.mensagem
                     ],
            temperature=0.1,
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




with st.sidebar:
    if st.button("Reiniciar conversa"):
        st.session_state.mensagem = []
        st.rerun()

