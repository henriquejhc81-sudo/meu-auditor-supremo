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
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (CORREÇÃO DO ERRO 404 V1BETA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Correção: Forçamos o modelo 'gemini-1.5-flash' para evitar versões beta expiradas
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Rede Aether: Tentando estabilizar conexão... Erro: {e}")

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
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    
    # NOVAS FUNÇÕES INSPIRADAS EM CONCORRENTES GLOBAIS (PwC, KPMG, DataSnipper)
    st.markdown("### ⚙️ Sniper Config")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    anomalia_det = st.toggle("Detecção de Anomalias (Forense)", value=True) # Nova: Inspirada em MindBridge
    cruzamento_sped = st.toggle("Cruzamento SPED/XML (Beta)", value=False) # Nova: Foco Brasil

with col2:
    st.subheader("🔍 Central de Inteligência")
    # Restauração: Opção de Criar Contrato ou Processo via seletor
    modo_acao = st.selectbox("🎯 Objetivo da Análise", [
        "Auditoria e Auditoria Forense", 
        "Gerar Contrato Personalizado", 
        "Gerar Processo/Petição Jurídica",
        "Análise de Conformidade (Compliance)"
    ])
    
    pergunta = st.text_area("O que o sistema deve analisar ou redigir?", placeholder="Digite aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    # Prompt Inteligente que se adapta ao modo escolhido
                    contexto_modo = f"Modo de Operação: {modo_acao}. "
                    prompt_final = f"Atue como o sistema AETHER AUDIT (Nível Big Four). {contexto_modo} Instrução: {pergunta} {conteudo_extra}. Use leis brasileiras, normas IFRS e dê um veredito técnico preciso."
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success(f"{modo_acao} Concluído(a)!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. Desative o tradutor do Chrome e tente novamente.")
        else:
            st.warning("Insira uma pergunta ou instrução de geração.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    st.caption("AETHER AUDIT v45.0 | Global Enterprise Edition")
    st.divider()
    st.info("💡 **Dica Sniper:** Selecione 'Gerar Contrato' no filtro central para redigir documentos do zero com base em leis brasileiras.")
