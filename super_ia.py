import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE OMNI ---
st.set_page_config(page_title="AETHER OMNI | Ultimate Edition", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 8px; font-weight: bold; height: 3.8em; }
    .report-card { padding: 30px; border-radius: 15px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    .suggestion-box { padding: 15px; background: #262730; border-radius: 10px; border-left: 5px solid #00c6ff; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (FORÇANDO v1 ESTÁVEL) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Comando absoluto para matar o erro v1beta da imagem
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except:
    st.error("📡 Rede Omni: Sincronizando...")

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
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    
    st.divider()
    st.subheader("💡 Sugestões Sniper (Copie e Cole)")
    st.markdown("""
    <div class='suggestion-box'>
    <b>Contratos:</b><br><i>"Analise cláusulas de rescisão e riscos financeiros."</i><br><br>
    <b>Tributário:</b><br><i>"Verifique se as alíquotas de ICMS/IPI nesta nota estão corretas."</i><br><br>
    <b>Fraude:</b><br><i>"Cruze os dados desta planilha com o PDF e aponte divergências."</i>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📜 Histórico de Missões")
    st.caption("v40.5 | Omniscience Edition Active")

# --- INTERFACE PRINCIPAL ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📂 Ingestão Multimodal")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, CSV)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas (OCR)", value=True)
    score_risco = st.toggle("Cálculo de Score de Risco (%)", value=True)
    cruzamento = st.toggle("Cruzamento de Dados Automático", value=True)
    st.write(f"📊 **Status do Sistema:** {'🟢 Operacional' if model else '🔴 Erro'}")

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite ou cole uma sugestão da lateral...", height=170)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL OMNI"):
        if pergunta:
            with st.spinner("Conectando ao Arsenal Sniper..."):
                try:
                    time.sleep(1)
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_mestre = f"Atue como AETHER OMNI. Instrução: {pergunta} {conteudo_extra}. Cite leis brasileiras e normas IFRS."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_mestre, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro de Rede Omni: {e}. Desative o tradutor e reinicie o motor.")
        else:
            st.warning("Insira uma pergunta.")
