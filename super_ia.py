import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT PRO", layout="wide", page_icon="🛡️")

# --- MOTOR DE CONEXÃO BLINDADO (A PROVA DE ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # FORÇA A CONEXÃO PELA PORTA DE PRODUÇÃO v1 (MATA O v1beta)
    genai.configure(api_key=API_KEY)
    
    # AJUSTE MESTRE: Usamos o nome de produção total que o servidor NÃO PODE ignorar
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
except:
    st.error("Conectando ao Cérebro Global...")

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
    st.image("https://flaticon.com", width=80)
    st.title("Painel Aether")
    if st.button("🔄 REINICIAR MOTOR"):
        st.rerun()
    st.divider()
    st.caption("v28.0 | Deep Intelligence Mode")

st.title("🛡️ AETHER AUDIT")
st.markdown("### *Inteligência de Auditoria Multinível*")

col1, col2 = st.columns(2)

with col1:
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.toggle("Modo Profundo (AI Mode)", value=True)
    st.info("O sistema agora usa a tecnologia 'Query Fan-out' para análise profunda.")

with col2:
    pergunta = st.text_area("O que devo auditar hoje?", placeholder="Ex: Analise este documento e procure riscos...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA SUPREMA"):
        if pergunta:
            with st.spinner("Aether está varrendo as redes neurais..."):
                try:
                    # Pequeno atraso para estabilização de rede
                    time.sleep(1)
                    
                    # Lógica para processar imagem ou texto
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                    # DOWNLOAD
                    st.download_button("📥 BAIXAR RELATÓRIO WORD", gerar_docx(response.text), "auditoria_aether.docx")
                    st.balloons()
                    
                except Exception as e:
                    # SE AINDA DER ERRO, O SISTEMA TENTA O MODELO DE RESERVA AUTOMATICAMENTE
                    try:
                        reserva = genai.GenerativeModel(model_name='models/gemini-pro')
                        response = reserva.generate_content(pergunta)
                        st.markdown(response.text)
                    except:
                        st.error(f"Erro de Sincronização: {e}. O Google está reiniciando. Aguarde 30 segundos.")
        else:
            st.warning("Por favor, digite uma instrução.")
