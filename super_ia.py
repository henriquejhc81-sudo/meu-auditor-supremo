import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO ---
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)
# Comando atualizado para evitar o erro 404 de versão
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.6 - Ultra Conectado")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Carregar Arquivo", type=["txt", "pdf", "png", "jpg", "jpeg"])

pergunta = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if pergunta:
        with st.spinner("Consultando inteligência de última geração..."):
            if arquivo and arquivo.type.startswith("image"):
                img = Image.open(arquivo)
                response = model.generate_content([pergunta, img])
            else:
                response = model.generate_content(pergunta)
            
            st.markdown("---")
            st.markdown(response.text)
            st.download_button("📥 BAIXAR EM WORD", preparar_download(response.text), "Auditoria.docx")
    else:
        st.warning("Digite uma pergunta.")
