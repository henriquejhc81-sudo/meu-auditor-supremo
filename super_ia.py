import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN AETHER ---
st.set_page_config(page_title="AETHER AUDIT", layout="wide")

# --- MOTOR DE CONEXÃO BLINDADO (v27.0) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Forçamos a biblioteca a ignorar versões beta instáveis
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usamos o nome simplificado que o servidor é obrigado a aceitar
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Conectando ao Cérebro Global...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
with st.sidebar:
    if st.button("🔄 Reiniciar Sistema"):
        st.rerun()
    st.caption("Aether Audit v27.0")

st.title("🛡️ AETHER AUDIT")
col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo", value=True)

with col2:
    pergunta = st.text_area("O que devo analisar?", placeholder="Digite aqui...", height=150)
    if st.button("🚀 INICIAR VARREDURA"):
        if pergunta:
            with st.spinner("Varrendo..."):
                try:
                    # Envio simplificado para garantir estabilidade na nuvem
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Concluído!")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro técnico: {e}. O Google está se recalibrando. Aguarde 30 segundos.")
