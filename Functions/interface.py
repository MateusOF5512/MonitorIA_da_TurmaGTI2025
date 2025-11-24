import streamlit as st
from datetime import datetime


def criar_rodape():
    """
    Renderiza um rodapé estiloso com espaçamento superior,
    contato para reportar erros e data de atualização.
    """
    # Pega a data de hoje formatada

    # CSS para garantir o espaçamento e o visual
    footer_html = f"""
    <style>
        .footer-container {{
            margin-top: 50px; /* Garante o espaço bom para rolar a página */
            padding-top: 20px;
            padding-bottom: 20px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 14px;
            background-color: transparent;
        }}
        .footer-link {{
            color: #ff4b4b;
            text-decoration: none;
            font-weight: bold;
        }}
        .footer-link:hover {{
            text-decoration: underline;
        }}
    </style>

    <div class="footer-container">
    <p style="font-size: 14px; margin-top: 5px; opacity: 0.8;">
            🛠️ Sistema atualizado: <strong>24/11/2025</strong> - Projeto Final - Metodologia de Projetos 2025.2
    </p>
    <p style="font-size: 14px; margin-top: 5px; opacity: 0.8;">
        Encontrou um erro ou tem uma sugestão? 
        <a class="footer-link" href="https://api.whatsapp.com/send/?phone=5548988098335&text=Ol%C3%A1,%20gostaria%20de%20falar%20sobre%20o%20Caderno%20da%20Turma" target="_blank">Reportar via WhatsApp</a>
    </p>
        
    </div>
    """

    st.markdown(footer_html, unsafe_allow_html=True)