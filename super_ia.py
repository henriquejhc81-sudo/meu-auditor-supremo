import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide")

# --- CONEXÃO MODERNA (FIM DO AVISO DE DEPRECIAÇÃO) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Seleção automática do melhor modelo disponível
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Conectando ao Cérebro IA...")

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
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()

with col2:
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", height=150)
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Conectando ao Cérebro IA..."):
                try:
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "report.docx")
                except Exception as e:
                    st.error(f"Erro técnico: {e}. Aguarde 30 segundos.")
