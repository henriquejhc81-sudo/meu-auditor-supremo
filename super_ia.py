import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Nexus OmniCode",
    page_icon="logo.png",
    layout="wide"
)

# Carregar logo
logo = Image.open("logo.png")
st.sidebar.image(logo, width=200)

# Função para gerar Dossiê de Blindagem
def gerar_dossie_blindagem():
    justificativa_tecnica = st.text_area("Justificativa Técnica", height=200)
    fundamentacao_lindb = st.text_area("Fundamentação LINDB", height=200)
    return f"**Justificativa Técnica:**\n{justificativa_tecnica}\n\n**Fundamentação LINDB:**\n{fundamentacao_lindb}"

# Função para gerar Cláusula de Barreira
def gerar_clausula_barreira():
    return "Nota de Apoio à Decisão: Este documento foi gerado por inteligência artificial como ferramenta de suporte técnico. O conteúdo não constitui parecer jurídico vinculante e não substitui a análise, revisão e assinatura de um advogado devidamente habilitado. A responsabilidade pela decisão final cabe exclusivamente ao usuário."

# Função para gerar Ícone do Celular
def gerar_icone_celular():
    return """
    <style>
    /* Ocultar menu superior padrão */
    .main {
        display: block;
    }
    .main .block-container {
        padding-top: 0;
    }
    /* Ocultar rodapé da plataforma */
    .footer {
        display: none;
    }
    </style>
    """

# Página principal
st.title("Nexus OmniCode")
st.write("Bem-vindo ao nosso sistema de apoio técnico!")

# Menu lateral
st.sidebar.title("Menu")
st.sidebar.button("Gerar Dossiê de Blindagem")
st.sidebar.button("Gerar Cláusula de Barreira")
st.sidebar.button("Gerar Ícone do Celular")

# Gerar Dossiê de Blindagem
if st.sidebar.button("Gerar Dossiê de Blindagem"):
    dossie_blindagem = gerar_dossie_blindagem()
    st.write(dossie_blindagem)
    st.write(gerar_clausula_barreira())

# Gerar Cláusula de Barreira
if st.sidebar.button("Gerar Cláusula de Barreira"):
    st.write(gerar_clausula_barreira())

# Gerar Ícone do Celular
if st.sidebar.button("Gerar Ícone do Celular"):
    st.write(gerar_icone_celular())

# Nota de Apoio à Decisão
st.write(gerar_clausula_barreira())
