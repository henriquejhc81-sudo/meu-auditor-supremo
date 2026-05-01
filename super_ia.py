import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE DESIGN ---
st.set_page_config(page_title="AETHER AUDIT | Supreme", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .history-item { font-size: 12px; padding: 8px; border-bottom: 1px solid #333; color: #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAR HISTÓRICO ---
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- CONEXÃO BLINDADA v37.3 (FIM DO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usando o nome completo do modelo para a nuvem
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash-latest')
except Exception as e:
    st.error("📡 Rede Aether: Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO OFICIAL', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Painel Aether")
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.divider()
    with st.expander("🎯 ARSENAL SNIPER (Comandos)"):
        st.info("Copie e cole abaixo:")
        st.code("Aether, faça uma auditoria snip deste contrato e procure cláusulas abusivas ou erros de datas.")
        st.code("Compare estes dois documentos e crie uma tabela de divergências entre os valores citados.")
    st.divider()
    st.subheader("📜 Histórico de Missões")
    if not st.session_state.historico:
        st.caption("Nenhuma missão registrada.")
    for item in reversed(st.session_state.historico):
        st.markdown(f"<div class='history-item'>⏱️ {item['data']}<br>{item['resumo']}</div>", unsafe_allow_html=True)

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ AETHER AUDIT - SUPREME")
modo = st.radio("Selecione o Modo de Missão:", ["Auditoria Simples", "Confronto X-Ray"], horizontal=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo_1 = st.file_uploader("Documento A", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx"])
    arquivo_2 = None
    if modo == "Confronto X-Ray":
        arquivo_2 = st.file_uploader("Documento B", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx"])

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que a Aether deve confrontar, analisar ou auditar?", 
                           placeholder="Cole aqui seu comando do Arsenal...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA"):
        if pergunta:
            with st.spinner("Processando em modo Sniper..."):
                try:
                    time.sleep(1)
                    # Preparação de conteúdo
                    prompt_lista = [pergunta]
                    if arquivo_1:
                        if arquivo_1.type.startswith("image"): prompt_lista.append(Image.open(arquivo_1))
                        else: prompt_lista.append(f"Ref A: {arquivo_1.name}")
                    if arquivo_2:
                        if arquivo_2.type.startswith("image"): prompt_lista.append(Image.open(arquivo_2))
                        else: prompt_lista.append(f"Ref B: {arquivo_2.name}")

                    response = model.generate_content(prompt_lista)
                    
                    # Salvar histórico
                    data_atual = datetime.now().strftime("%H:%M")
                    st.session_state.historico.append({"data": data_atual, "resumo": pergunta[:30] + "..."})
                    
                    st.success("Missão Concluída!")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Baixar Relatório", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro de Conexão: {e}. Tente novamente.")
        else:
            st.warning("Insira uma instrução.")

st.sidebar.caption("v37.3 | Supreme Mode Active")
