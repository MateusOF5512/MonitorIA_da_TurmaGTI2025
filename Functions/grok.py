import streamlit as st
from groq import Groq


client = Groq(api_key=st.secrets["grok"]["GROK_API"])

def chat_completion_disciplina(dados):

    system = f"""
    Você é um assistente acadêmico especializado em compilar e organizar anotações de aulas do curso de Gestão da Tecnologia da Informação, especificamente da disciplina de Infraestrutura de Redes de Computadores. 

    O conteúdo a seguir está no formato JSON e representa as anotações de diferentes alunos de uma mesma aula. Seu papel é:

    1. **Analisar cuidadosamente todas as anotações** presentes no JSON.
    2. **Gerar um resumo consolidado** que combine todas as anotações de forma clara, coerente e didática.
    3. Sempre que possível, cite **a origem da informação** em *itálico* indicando o caderno/usuário que fez a anotação.
    4. Use **negrito** para destacar palavras-chave, conceitos importantes ou termos essenciais.
    5. Organize o resumo seguindo exatamente os seguintes segmentos:
       - **(Indique o tema principal da aula)**.
       - **Objetivos de Aprendizado**: Resuma os objetivos que os alunos deveriam alcançar com a aula.
       - **Conteúdo do Dia**: Aborde os principais tópicos, conceitos e detalhes importantes presentes nas anotações.
       - **Conclusão do Aprendizado**: Síntese final do que os alunos devem ter compreendido.
    6. Não invente informações que não estejam presentes nas anotações.
    7. Mantenha um tom didático e estruturado, facilitando uma leitura rápida e eficiente.
    """

    chat_completion = client.chat.completions.create(
        model='openai/gpt-oss-120b',
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": dados
            }
        ],
        temperature=0.1,
        stream=False
    )

    # Captura da resposta
    resposta = chat_completion.choices[0].message.content

    return resposta


def criar_questoes_com_groq(resposta_ia, disciplina):
    prompt_perguntas = """
    Você é uma IA educacional especializada em gerar perguntas de múltipla escolha a partir de resumos de aulas da graduação em Gestão de Tcnologia da Informação.

    Com base no resumo da aula fornecido, elabore 4 perguntas com nível de complexidade médio, voltadas para a fixação e compreensão dos principais conceitos apresentados no texto. 
    As perguntas devem exigir atenção do aluno, evitando respostas óbvias, mas ainda rápidas de responder.

    Regras:
    1. Todas as perguntas devem ser diretamente relacionadas ao conteúdo do resumo.
    2. Cada pergunta deve conter exatamente 3 opções de resposta (A, B e C).
    3. Apenas uma opção deve estar correta.
    4. A resposta deve seguir estritamente o formato JSON abaixo.
    5. Não adicione texto explicativo, introdução ou comentários fora da estrutura.

    A resposta deve ser **EXATAMENTE** neste formato JSON:

    [
        {
            "pergunta": "1️⃣ [Texto da pergunta aqui]",
            "opcoes": [
                "A) [Opção A]",
                "B) [Opção B]",
                "C) [Opção C]"
            ],
            "resposta_correta": "[Letra e texto exato da alternativa correta]"
        },
        {
            "pergunta": "2️⃣ [Texto da pergunta aqui]",
            "opcoes": [
                "A) [Opção A]",
                "B) [Opção B]",
                "C) [Opção C]"
            ],
            "resposta_correta": "[Letra e texto exato da alternativa correta]"
        },
        {
            "pergunta": "3️⃣ [Texto da pergunta aqui]",
            "opcoes": [
                "A) [Opção A]",
                "B) [Opção B]",
                "C) [Opção C]"
            ],
            "resposta_correta": "[Letra e texto exato da alternativa correta]"
        },
        {
            "pergunta": "4️⃣ [Texto da pergunta aqui]",
            "opcoes": [
                "A) [Opção A]",
                "B) [Opção B]",
                "C) [Opção C]"
            ],
            "resposta_correta": "[Letra e texto exato da alternativa correta]"
        }
    ]
    """

    chat_completion = client.chat.completions.create(
        model='openai/gpt-oss-20b',
        messages=[
            {
                "role": "system",
                "content": prompt_perguntas
            },
            {
                "role": "user",
                "content": resposta_ia
            }
        ],
        temperature=0.3,
        stream=False
    )

    # Captura da resposta
    resposta = chat_completion.choices[0].message.content

    return resposta