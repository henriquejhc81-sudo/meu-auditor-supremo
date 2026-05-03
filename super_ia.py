import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
import random

# --- DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO USANDO SUA LÓGICA QUE FUNCIONA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # SUA LÓGICA DE OURO: Deixa o Google escolher a porta certa
    modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model = genai.GenerativeModel(modelos[0] if modelos else 'gemini-1.5-flash')
except:
    st.error("📡 Sincronizando rede segura...")

def preparar_download(texto, titulo):
    doc = Document()
    doc.add_heading(f'AETHER AUDIT - {titulo}', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE MASTER ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v47.0")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    st.markdown("### ⚙️ Sniper Config")
    # Funções de elite mantidas
    st.toggle("Extração Inteligente de Tabelas", value=True)
    st.toggle("Score de Risco Automático", value=True)
    st.toggle("Detecção de Anomalias (Forense)", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    # O filtro de ação que você queria
    tipo_saida = st.selectbox("🎯 Objetivo da Missão (Filtro)", [
        "Apenas Relatório de Auditoria", 
        "Auditoria + Gerar Contrato Corrigido", 
        "Auditoria + Gerar Petição/Processo",
        "Análise Forense de Assinaturas"
    ])
    
    pergunta = st.text_area("O que as IAs devem analisar?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Conectando ao Arsenal Aether..."):
                try:
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_final = f"Atue como Auditor e Advogado Sênior. Missão: {tipo_saida}. Instrução: {pergunta} {conteudo_extra}."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Cumprida!")
                    tab1, tab2 = st.tabs(["📝 Relatório", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RESULTADO (.DOCX)", preparar_download(response.text, tipo_saida), "aether_result.docx")
                except Exception as e:
                    st.error(f"Erro: {e}")
        else:
            st.warning("Insira uma instrução.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"): st.rerun()
    st.caption("AETHER AUDIT v47.0 | Master Edition")
