import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO INTELIGENTE (MATA O ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Ele pergunta ao Google: "Quais modelos eu posso usar agora?"
    modelos_validos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Ele escolhe o primeiro da lista que o Google autorizar
    model = genai.GenerativeModel(modelos_validos)
except Exception as e:
    st.error("Sincronizando com a rede neural global...")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO PROFISSIONAL', 0)
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
    st.caption("v29.0 | Auto-Selection Mode")

st.title("🛡️ AETHER AUDIT")
st.markdown("### *Inteligência de Auditoria Multinível*")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo (AI Mode)", value=True)

with col2:
    pergunta = st.text_area("O que devo auditar hoje?", placeholder="Digite sua pergunta aqui...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA SUPREMA"):
        if pergunta:
            with st.spinner("Aether está varrendo as redes neurais..."):
                try:
                    time.sleep(1)
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "auditoria_aether.docx")
                    
                except Exception as e:
                    st.error(f"Erro de Sincronização: {e}. Aguarde 30 segundos.")
        else:
            st.warning("Por favor, digite uma instrução.")
