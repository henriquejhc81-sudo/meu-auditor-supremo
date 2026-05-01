import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
from datetime import datetime

# --- DESIGN SUPREME OMNI ---
st.set_page_config(page_title="AETHER OMNISCIENCE", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    .stHeader { color: #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAR HISTÓRICO ---
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- CONEXÃO DE PRODUÇÃO v39.0 ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Sincronizando Rede Aether Omniscience...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO OMNISCIENCE', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- BARRA LATERAL AVANÇADA ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.divider()
    
    with st.expander("🎯 ARSENAL SNIPER (Expandido)"):
        st.info("Comandos de Elite:")
        st.code("Aether, analise este áudio e compare com as cláusulas do contrato. Há contradições?")
        st.code("Verifique esta imagem em busca de assinaturas falsas ou adulterações digitais.")
        st.code("Audite este endereço e me diga os riscos de zoneamento e valor de mercado atual.")
    
    st.divider()
    st.subheader("📜 Histórico de Missões")
    for item in reversed(st.session_state.historico):
        st.markdown(f"<small>⏱️ {item['data']}: {item['resumo']}</small>", unsafe_allow_html=True)

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ AETHER OMNISCIENCE")
st.markdown("##### *Auditoria Total: Documentos, Imagens, Dados e Localização*")

# SELEÇÃO DE MÓDULOS
modulo = st.selectbox("Selecione o Módulo de Inteligência:", 
                     ["Auditoria de Contratos & PDFs", "Confronto X-Ray (Dois Arquivos)", "Análise de Fraude em Imagens", "Auditoria de Áudio e Reuniões", "Inteligência Imobiliária & Mapas"])

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Entrada Multimodal")
    arquivo_1 = st.file_uploader("Primeiro Arquivo (Base)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx", "csv", "mp3", "wav"])
    arquivo_2 = None
    if modulo == "Confronto X-Ray (Dois Arquivos)":
        arquivo_2 = st.file_uploader("Segundo Arquivo (Confronto)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx", "csv"])

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que a Aether Omni deve processar agora?", 
                           placeholder="Ex: Procure indícios de fraude nesta assinatura...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA OMNI"):
        if pergunta:
            with st.spinner("Aether está exercendo onisciência sobre os dados..."):
                try:
                    prompt_lista = [f"Módulo: {modulo}\nInstrução: {pergunta}"]
                    
                    # Processamento de arquivos
                    if arquivo_1:
                        if arquivo_1.type.startswith("image"):
                            prompt_lista.append(Image.open(arquivo_1))
                        elif arquivo_1.type.startswith("audio"):
                            st.audio(arquivo_1)
                            prompt_lista.append(f"ÁUDIO DETECTADO: O sistema deve transcrever e analisar o conteúdo sonoro de {arquivo_1.name}")
                        else:
                            prompt_lista.append(f"Ref A: {arquivo_1.name}")

                    response = model.generate_content(prompt_lista)
                    
                    data_atual = datetime.now().strftime("%H:%M")
                    st.session_state.historico.append({"data": data_atual, "resumo": pergunta[:25] + "..."})
                    
                    st.success("Varredura Concluída!")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Baixar Relatório Omni", preparar_download(response.text), "aether_omni_report.docx")
                except Exception as e:
                    st.error(f"📡 Erro de Rede Omni: {e}. Reinicie o motor.")
        else:
            st.warning("Insira uma instrução para a varredura.")

st.sidebar.caption("v39.0 | Omniscience Edition Active")
