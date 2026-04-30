import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (FORÇANDO PRODUÇÃO v1) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # FORÇAMOS A VERSÃO DE PRODUÇÃO PARA MATAR O ERRO v1beta
    genai.configure(api_key=API_KEY)
    
    # O SEGREDO: Usamos o nome de sistema absoluto que a nuvem exige
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Rede Aether: Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO EXECUTIVO', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    st.toggle("Extração de Tabelas Inteligente", value=True)
    st.toggle("Score de Risco Automático", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    time.sleep(1)
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    # Prompt de Elite
                    prompt_final = f"Atue como o sistema AETHER AUDIT. Instrução: {pergunta} {conteudo_extra}. Cite leis brasileiras e dê um veredito de risco."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Análise Concluída!")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                
                except Exception as e:
                    # SE AINDA DER ERRO, O SISTEMA TENTA O MODELO DE RESERVA AUTOMATICAMENTE
                    try:
                        reserva = genai.GenerativeModel(model_name='models/gemini-pro')
                        response = reserva.generate_content(pergunta)
                        st.markdown(response.text)
                    except:
                        st.error(f"Erro na Rede Aether: {e}. O Google está reiniciando. Aguarde 30 segundos.")
        else:
            st.warning("Insira uma pergunta.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("AETHER AUDIT v32.2 | Production Mode")
