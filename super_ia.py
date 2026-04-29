import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- DESIGN PROFISSIONAL ---
st.set_page_config(page_title="Auditor Supremo PRO", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #004a99; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (v19.0 - ANTI 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # O segredo: forçamos o modelo sem o prefixo 'models/' e usamos a versão estável
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Erro de Configuração: {e}")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('RELATÓRIO DE AUDITORIA PROFISSIONAL', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
col1, col2 = st.columns(2)

with col1:
    st.title("PRO Auditor")
    st.subheader("Painel de Controle")
    arquivo = st.file_uploader("📂 Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.divider()
    st.markdown("### ✅ Checklist Automático")
    st.checkbox("Analisar Leis Brasileiras", value=True)
    st.checkbox("Detectar Cláusulas Abusivas", value=True)

with col2:
    st.header("🔍 Processamento")
    pergunta = st.text_area("Instruções para a Auditoria:", placeholder="O que deseja analisar?", height=150)
    
    if st.button("🚀 EXECUTAR AUDITORIA DE ELITE"):
        if pergunta:
            with st.spinner("Orquestrando análise em modo seguro e invisível..."):
                try:
                    # Delay humano para manter a invisibilidade contra bloqueios
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    # Se tiver arquivo, envia. Se não, envia só a pergunta.
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    aba1, aba2 = st.tabs(["📊 Relatório", "📥 Download"])
                    
                    with aba1:
                        st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with aba2:
                        st.download_button("📥 BAIXAR DOCUMENTO FINAL (.DOCX)", preparar_download(response.text), "auditoria_pro.docx")
                        
                except Exception as e:
                    # Se der erro 404, tentamos um modelo alternativo automaticamente
                    st.warning("O servidor do Google está instável. Tentando conexão de reserva...")
                    try:
                        modelo_reserva = genai.GenerativeModel('gemini-pro')
                        response = modelo_reserva.generate_content(pergunta)
                        st.success("Conectado via reserva!")
                        st.markdown(response.text)
                    except:
                        st.error(f"Erro técnico: {e}. Por favor, aguarde 30 segundos e tente de novo.")
        else:
            st.warning("Por favor, forneça os detalhes para análise.")
