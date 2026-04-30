import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN PROFISSIONAL ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO DIRETA (ANTI-404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Forçamos a configuração estável
    genai.configure(api_key=API_KEY)
    # O SEGREDO: Usamos o nome puro do modelo. Isso evita o erro de versão na nuvem.
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Conectando ao Cérebro IA...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.toggle("Extração de Tabelas", value=True)
    
    # Botão de Reboot Discreto
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

with col2:
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", height=150)
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Processando na nuvem..."):
                try:
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "relatorio.docx")
                except Exception as e:
                    st.error(f"Erro técnico: {e}. Aguarde 30 segundos.")
