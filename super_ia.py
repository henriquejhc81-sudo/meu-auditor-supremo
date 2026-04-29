import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- CONFIGURAÇÃO SUPREMA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Configure sua GOOGLE_API_KEY nos Secrets do Streamlit.")

# FUNÇÃO VACINA: Tenta achar o modelo certo na nuvem
def conectar_ia():
    for nome in ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']:
        try:
            m = genai.GenerativeModel(nome)
            # Teste rápido de conexão
            return m
        except:
            continue
    return genai.GenerativeModel('gemini-pro')

model = conectar_ia()

def preparar_download(texto_final):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA - RELATÓRIO', 0)
    for linha in texto_final.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.0 - Cloud Edition")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Subir Arquivo/Foto", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.success("🔒 Sistema Online")

# LÓGICA
input_data = []
if arquivo:
    if arquivo.type.startswith("image"):
        img = Image.open(arquivo)
        st.image(img, width=300)
        input_data = [img]
    else:
        texto = arquivo.read().decode("utf-8", errors="ignore")
        input_data = [f"CONTEÚDO: {texto}"]

comando = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if comando:
        with st.spinner("Analisando..."):
            try:
                prompt = f"Atue como um Auditor Supremo. Analise e corrija: {comando}"
                
                if input_data:
                    response = model.generate_content([prompt, *input_data])
                else:
                    response = model.generate_content(prompt)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 BAIXAR EM WORD",
                    data=preparar_download(response.text),
                    file_name="Auditoria.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                st.error(f"Erro: {e}")
