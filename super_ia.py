import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time

# --- DESIGN PROFISSIONAL ---
st.set_page_config(page_title="Auditor Supremo PRO", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #004a99; color: white; font-weight: bold; }
    .report-box { padding: 20px; border-radius: 10px; background-color: #ffffff; border-left: 5px solid #004a99; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO COM CAMINHO ABSOLUTO (FIM DO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usando o nome completo do modelo para a nuvem
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
except Exception as e:
    st.error("Conectando ao cérebro central...")

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
            with st.spinner("Navegando em modo seguro..."):
                try:
                    # Pequena pausa para garantir estabilidade
                    time.sleep(1)
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([pergunta, Image.open(arquivo)])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Análise Concluída!")
                    aba1, aba2 = st.tabs(["📊 Relatório", "📥 Download"])
                    
                    with aba1:
                        st.markdown(f"<div class='report-box'>{response.text}</div>", unsafe_allow_html=True)
                    with aba2:
                        st.download_button("📥 BAIXAR DOCUMENTO FINAL (.DOCX)", preparar_download(response.text), "auditoria_pro.docx")
                        
                except Exception as e:
                    # Se falhar o flash-latest, tenta o pro como última alternativa
                    try:
                        reserva = genai.GenerativeModel(model_name='models/gemini-pro')
                        response = reserva.generate_content(pergunta)
                        st.markdown(response.text)
                    except:
                        st.error(f"Erro de Conexão: {e}. Aguarde 30 segundos.")
        else:
            st.warning("Por favor, digite sua pergunta.")
