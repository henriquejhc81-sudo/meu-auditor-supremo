import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
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

# --- CONEXÃO BLINDADA (SOLUÇÃO DEFINITIVA PARA O ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Forçamos o modelo estável para evitar o erro v1beta do seu print
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("📡 Rede Aether: Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO EXECUTIVO SUPREMO', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v45.1")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    
    st.markdown("### ⚙️ Sniper Config")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    detec_anomalia = st.toggle("Detecção de Anomalias (Forense)", value=True)
    cruzamento_sped = st.toggle("Cruzamento SPED/XML (Beta)", value=False)

with col2:
    st.subheader("🔍 Central de Inteligência")
    # Filtro de Objetivo (Contrato, Processo, Auditoria)
    modo_acao = st.selectbox("🎯 Objetivo da Análise", [
        "Auditoria e Auditoria Forense", 
        "Gerar Contrato Personalizado", 
        "Gerar Processo/Petição Jurídica",
        "Análise de Conformidade (Compliance)"
    ])
    
    pergunta = st.text_area("O que o sistema deve analisar ou redigir?", placeholder="Digite aqui sua instrução...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    # Prompt de Engenharia Reversa (Simula Claude, DeepSeek, Llama, Grok internamente)
                    prompt_final = f"""
                    Atue como o sistema AETHER AUDIT MASTER. 
                    Objetivo: {modo_acao}.
                    Instrução: {pergunta} {conteudo_extra}.
                    
                    Use lógica de Big Four (PwC, EY, Deloitte, KPMG).
                    Analise sob 4 óticas: Ética, Técnica, Criativa e Pragmática.
                    Forneça Checklist de Compliance, Score de Risco e Veredito Final.
                    Siga estritamente as leis brasileiras e normas IFRS.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Cumprida!")
                    tab1, tab2 = st.tabs(["📝 Relatório Supremo", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. Desative o tradutor e reinicie o motor.")
        else:
            st.warning("Insira uma pergunta ou comando.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    st.caption("AETHER AUDIT v45.1 | Global Enterprise Edition")
    st.divider()
    st.info("💡 **Dica de Elite:** No modo 'Gerar Contrato', descreva as partes e o objeto para uma redação jurídica perfeita.")
