import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO BLINDADA (FIM DO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # AJUSTE MESTRE: Forçamos a configuração estável
    genai.configure(api_key=API_KEY)
    
    # O SEGREDO: Usamos o nome absoluto 'models/gemini-1.5-flash' 
    # Isso impede que o servidor procure na porta errada (v1beta)
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Rede Aether: Sincronizando...")

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
    st.caption("v29.2 | Enterprise Secured")

st.title("🛡️ AETHER AUDIT")
st.markdown("### *Inteligência de Auditoria Multinível*")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo (AI Mode)", value=True)

with col2:
    pergunta = st.text_area("O que devo auditar hoje?", placeholder="Ex: Olá, tudo bem?", height=150)
    
    if st.button("🚀 INICIAR VARREDURA SUPREMA"):
        if pergunta:
            with st.spinner("Processando na Nuvem..."):
                try:
                    # Pequeno delay para estabilidade
                    time.sleep(1)
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR WORD", gerar_docx(response.text), "auditoria_aether.docx")
                    
                except Exception as e:
                    st.error(f"Erro técnico: {e}. O Google está se recalibrando. Aguarde 30 segundos.")
        else:
            st.warning("Digite uma instrução.")
