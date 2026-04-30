import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
import random

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

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
        transition: 0.3s; 
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00c6ff; }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .metric-box { padding: 15px; border-radius: 10px; background: #262730; text-align: center; border: 1px solid #444; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (ANTI 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Aether Network: Sincronizando conexão...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO EXECUTIVO', 0)
    for linha in texto.split('\n'):
        if linha.strip():
            doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE AETHER AUDIT ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-box'>📊 Nível de Varredura: <b>Ultra Deep</b></div>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    
    st.divider()
    st.subheader("⚙️ Parâmetros de Missão")
    st.toggle("Extração de Tabelas Inteligente", value=True)
    st.toggle("Score de Risco Automático", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", 
                           placeholder="Descreva a tarefa ou as cláusulas que deseja processar...", 
                           height=180)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether Audit está processando..."):
                try:
                    time.sleep(random.uniform(1.0, 2.0))
                    
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        try:
                            df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                            conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"
                        except:
                            conteudo_extra = "\n(Erro ao ler os dados da planilha)"

                    prompt_mestre = f"""
                    Atue como o sistema AETHER AUDIT.
                    Instrução: {pergunta} {conteudo_extra}
                    ESTRUTURA: Sumário, Análise Técnica (com leis) e Veredito.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([prompt_mestre, img])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Análise Concluída com Sucesso!")
                    
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportação Profissional"])
                    
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.download_button(
                            label="📥 BAIXAR RELATÓRIO OFICIAL (.DOCX)",
                            data=preparar_download(response.text),
                            file_name="aether_report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}")
        else:
            st.warning("Aguardando entrada de dados.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("AETHER AUDIT v31.3")
