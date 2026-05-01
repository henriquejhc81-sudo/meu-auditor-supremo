import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
st.set_page_config(page_title="AETHER OMNI | Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.5em; 
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO INTELIGENTE (CORREÇÃO DO ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Forçamos o modelo estável diretamente para evitar o erro v1beta na nuvem
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Rede Omni: Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO EXECUTIVO', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.divider()
    with st.expander("🎯 ARSENAL SNIPER", expanded=True):
        st.info("• Inteligência Multimodal\n• Cross-check de Dados\n• Veredito Legal")
    st.divider()
    st.subheader("📜 Histórico de Missões")
    st.caption("v40.3 | Omniscience Edition Active")

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Entrada Multimodal")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, CSV)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    # FUNÇÕES QUE VOCÊ GOSTA (TOGGLES)
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    st.write("📊 **Status:** Operacional")

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA OMNI"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    time.sleep(1)
                    conteudo_extra = ""
                    # Lógica de Excel/CSV (Sniper Mode)
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_final = f"""
                    Atue como o sistema AETHER OMNI. 
                    Instrução: {pergunta} {conteudo_extra}
                    Use lógica de Big Four, cite leis brasileiras e dê o veredito final.
                    Extrair Tabelas: {extrair_tab} | Score de Risco: {score_risco}
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                
                except Exception as e:
                    st.error(f"Erro de Rede Omni: {e}. Desative o tradutor do Chrome e reinicie o motor.")
        else:
            st.warning("Insira uma pergunta.")
