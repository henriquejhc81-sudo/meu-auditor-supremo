import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO DIRETA (DEFINIÇÃO OBRIGATÓRIA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Definimos o modelo de forma direta e global para evitar o erro 'not defined'
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
with st.sidebar:
    st.title("Painel Aether")
    if st.button("🔄 REINICIAR MOTOR"):
        st.rerun()
    st.caption("v29.1 | Direct Connection Mode")

st.title("🛡️ AETHER AUDIT")
st.markdown("### *Inteligência de Auditoria Multinível*")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo (AI Mode)", value=True)

with col2:
    pergunta = st.text_area("O que devo auditar hoje?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA SUPREMA"):
        if pergunta:
            with st.spinner("Aether está processando..."):
                try:
                    # Pequena pausa para sincronia
                    time.sleep(1)
                    
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        # Chamada direta e simples
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "auditoria_aether.docx")
                    
                except Exception as e:
                    st.error(f"O Google está demorando para responder: {e}. Tente novamente em 30 segundos.")
        else:
            st.warning("Por favor, digite uma instrução.")
