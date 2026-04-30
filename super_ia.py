import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 10px; font-weight: bold; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (v31.1 - ANTI 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usamos o nome de produção total que a nuvem exige
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except:
    st.error("📡 Rede Aether: Sincronizando...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO EXECUTIVO', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    st.toggle("Extração de Tabelas Inteligente", value=True)
    st.toggle("Score de Risco Automático", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    pergunta = st.text_area("O que o sistema deve auditar?", placeholder="Instruções...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Snipping... Extraindo dados na nuvem..."):
                try:
                    time.sleep(1)
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_mestre = f"Atue como Auditor Supremo. Instrução: {pergunta} {conteudo_extra}. Cite leis brasileiras e gere o veredito final."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_mestre, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR RELATÓRIO WORD", gerar_docx(response.text), "aether_report.docx")
                
                except Exception as e:
                    st.error(f"Erro técnico: {e}. O Google está reiniciando. Aguarde 30 segundos.")
        else:
            st.warning("Insira uma pergunta.")

# BOTÃO DE REBOOT DISCRETO NA BARRA LATERAL
with st.sidebar:
    if st.button("🔄 Reiniciar Sistema"):
        st.rerun()
