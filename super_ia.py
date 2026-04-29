import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN AETHER ---
st.set_page_config(page_title="AETHER AUDIT", layout="wide")

# --- CONEXÃO DIRETA (ANTI-404) ---
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)
# Comando atualizado para forçar a versão correta na nuvem
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT")
col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo", value=True)

with col2:
    pergunta = st.text_area("O que devo analisar?", height=150)
    if st.button("🚀 INICIAR VARREDURA"):
        if pergunta:
            with st.spinner("Conectando..."):
                try:
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro: {e}. O Google está reiniciando. Aguarde 30 segundos.")
