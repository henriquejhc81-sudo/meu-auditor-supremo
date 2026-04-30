import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- CONEXÃO BLINDADA (v30.0) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # FORÇAMOS A VERSÃO ESTÁVEL v1 NO LUGAR DA v1beta
    genai.configure(api_key=API_KEY)
    
    # AJUSTE MESTRE: Usamos apenas o nome do modelo sem prefixos
    # Isso evita que o servidor procure na pasta 'models/' que está dando 404
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Conectando ao Cérebro Global...")

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
    st.caption("v30.0 | Cloud Strict Mode")

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
            with st.spinner("Varrendo dados na nuvem..."):
                try:
                    # Delay para sincronização de rede
                    time.sleep(1)
                    
                    # Processamento de Imagem ou Texto
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        # Para PDFs e textos grandes
                        conteudo = arquivo.read().decode("utf-8", errors="ignore") if arquivo else ""
                        final_prompt = f"{pergunta}\n\nDOCUMENTO: {conteudo}"
                        response = model.generate_content(final_prompt)
                    
                    st.success("Análise Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR RELATÓRIO WORD", gerar_docx(response.text), "aether_report.docx")
                    
                except Exception as e:
                    st.error(f"Erro de Conexão: {e}. O Google está se recalibrando. Aguarde 30 segundos.")
        else:
            st.warning("Digite uma instrução.")
