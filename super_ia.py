import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
st.set_page_config(page_title="AETHER AUDIT | Intelligence Mode", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; 
        border-radius: 8px; 
        border: none; 
        font-weight: bold; 
        height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .metric-box { padding: 15px; border-radius: 10px; background: #262730; text-align: center; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (v25.3 - AUTO-DETECÇÃO) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # Ele busca na sua conta qual modelo está vivo no servidor agora
    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Filtra para usar o gemini-1.5-flash se ele existir na lista, senão pega o primeiro
    modelo_escolhido = next((m for m in modelos_disponiveis if 'gemini-1.5-flash' in m), modelos_disponiveis)
    model = genai.GenerativeModel(modelo_escolhido)
except Exception as e:
    st.error(f"📡 Aether Network: Sincronizando conexão...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE AETHER AUDIT ---
st.title("🛡️ AETHER AUDIT")
st.markdown("##### *Advanced Compliance & Multimodal Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-box'>📊 Nível de Varredura: <b>Ultra Deep</b></div>", unsafe_allow_html=True)
    st.divider()
    st.subheader("📂 Central de Evidências")
    arquivo = st.file_uploader("Upload de Documentos ou Imagens", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.divider()
    st.subheader("⚙️ Parâmetros de Missão")
    st.toggle("Ativar Modo IA Profundo", value=True)
    st.toggle("Cruzamento de Leis Brasileiras", value=True)

with col2:
    st.subheader("🔍 Painel de Análise")
    pergunta = st.text_area("O que a Aether deve processar?", placeholder="Instruções...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA AETHER"):
        if pergunta:
            with st.spinner("Aether Audit está processando..."):
                try:
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([pergunta, img])
                    else:
                        response = model.generate_content(pergunta)
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Relatório", "📥 Exportação"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. O Google está reiniciando os modelos. Aguarde 30 segundos.")
        else:
            st.warning("Aguardando entrada de dados.")
