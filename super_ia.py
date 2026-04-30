import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO DIRETA (DEFINIÇÃO OBRIGATÓRIA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Definimos o modelo de forma direta e global
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro na conexão inicial: {e}")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
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
    arquivo = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()

with col2:
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Conectando ao Cérebro IA..."):
                try:
                    time.sleep(1)
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR EM WORD", gerar_docx(response.text), "report.docx")
                except Exception as e:
                    st.error(f"Erro técnico: {e}. Desative o tradutor do Chrome e tente novamente.")
        else:
            st.warning("Insira uma pergunta.")
