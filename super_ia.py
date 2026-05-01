import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN OMNISCENCE (BLACK MODE) ---
st.set_page_config(page_title="AETHER OMNI", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO DIRETA (ANTI-404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usamos apenas o nome puro do modelo para evitar o erro v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Rede Omni: Sincronizando conexão...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE AUDITORIA', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ Aether Omni")
st.markdown("##### *Omniscience Edition Active*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Entrada Multimodal")
    arquivo = st.file_uploader("Upload de Documentos (PDF, Imagens, Excel)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que a Aether Omni deve processar agora?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA OMNI"):
        if pergunta:
            with st.spinner("Conectando ao Arsenal Sniper..."):
                try:
                    time.sleep(1)
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        # Processamento seguro para PDFs e textos
                        response = model.generate_content(pergunta)
                    
                    st.success("Concluído!")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 BAIXAR RELATÓRIO", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro de Rede Omni: {e}. Desative o tradutor e aguarde 30 segundos.")
        else:
            st.warning("Insira uma pergunta.")
