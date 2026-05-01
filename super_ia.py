import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN SNIPER (MODO ESCURO PROFISSIONAL) ---
st.set_page_config(page_title="AETHER AUDIT | X-Ray Edition", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .diff-box { padding: 15px; border-radius: 10px; background-color: #1a1c24; border-left: 5px solid #ff4b4b; margin-bottom: 10px; }
    .match-box { padding: 15px; border-radius: 10px; background-color: #1a1c24; border-left: 5px solid #00c6ff; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Falha na sincronização Aether.")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO DE CONFRONTO', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT - X-RAY MODE")
st.markdown("##### *Auditoria Comparativa e Detecção de Divergências*")

# MODO DE OPERAÇÃO
modo = st.radio("Selecione o Modo de Missão:", ["Auditoria Simples", "Confronto de Documentos (X-Ray)"], horizontal=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    if modo == "Auditoria Simples":
        arquivo_1 = st.file_uploader("Subir Documento Base", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv", "docx"])
        arquivo_2 = None
    else:
        arquivo_1 = st.file_uploader("📄 Documento A (Original/Petição)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx"])
        arquivo_2 = st.file_uploader("📄 Documento B (Aditivo/Sentença/INSS)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "docx"])

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que a Aether deve confrontar ou analisar?", placeholder="Ex: Compare estes dois contratos e aponte o que mudou no valor e nas multas...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA X-RAY"):
        if pergunta:
            with st.spinner("Realizando varredura comparativa..."):
                try:
                    time.sleep(1)
                    
                    # Preparação dos dados para a IA
                    contexto = f"MODO: {modo}\nINSTRUÇÃO: {pergunta}\n\n"
                    prompt_data = [contexto]
                    
                    if arquivo_1:
                        # Se for imagem, processa como imagem, se não, como texto (simplificado)
                        if arquivo_1.type.startswith("image"):
                            prompt_data.append(Image.open(arquivo_1))
                        else:
                            prompt_data.append(f"DOCUMENTO A: {arquivo_1.name}")

                    if arquivo_2:
                        if arquivo_2.type.startswith("image"):
                            prompt_data.append(Image.open(arquivo_2))
                        else:
                            prompt_data.append(f"DOCUMENTO B: {arquivo_2.name}")

                    # Super Prompt Sniper
                    final_prompt = """
                    Atue como o software AETHER AUDIT no MODO X-RAY.
                    Sua missão é identificar DIVERGÊNCIAS, CONTRADIÇÕES e MUDANÇAS entre os documentos.
                    
                    ESTRUTURA DE RESPOSTA:
                    1. 🚩 ALERTA DE DIVERGÊNCIA: Liste onde os documentos não batem.
                    2. ⚖️ ANÁLISE DE IMPACTO JURÍDICO: O que essa mudança causa de risco?
                    3. 📊 TABELA COMPARATIVA: Coloque lado a lado as diferenças.
                    4. ✅ VEREDITO FINAL: Qual documento é mais favorável ou se há fraude.
                    """
                    prompt_data[0] += final_prompt
                    
                    response = model.generate_content(prompt_data)
                    
                    st.success("Confronto Concluído!")
                    st.markdown("---")
                    st.markdown(response.text)
                    st.download_button("📥 BAIXAR RELATÓRIO DE CONFRONTO", preparar_download(response.text), "confronto_aether.docx")
                    
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}")
        else:
            st.warning("Insira uma instrução para iniciar a missão.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("AETHER AUDIT v37.0 | X-Ray Sniper Edition")
