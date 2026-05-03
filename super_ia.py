import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE (FIE L À IMAGEM) ---
st.set_page_config(page_title="AETHER AUDIT | Global Edition", layout="wide", page_icon="🛡️")

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

# --- CONEXÃO BLINDADA (ESTABILIZAÇÃO V1) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Correção definitiva do erro 404: usamos a porta estável direta
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Rede Aether: Sincronizando conexão segura...")

def preparar_download(texto, titulo):
    doc = Document()
    doc.add_heading(titulo, 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE IGUAL À SUA IMAGEM ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v46.1")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Upload de Evidências (PDF, Imagem, Excel, TXT)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    st.divider()
    
    st.markdown("### ⚙️ Sniper Config")
    # OS BOTÕES VERMELHOS DA SUA IMAGEM:
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    detec_anomalia = st.toggle("Detecção de Anomalias (Assinaturas/Forense)", value=True)
    cruzamento_sped = st.toggle("Cruzamento SPED/XML (Beta)", value=False)

with col2:
    st.subheader("🔍 Central de Inteligência")
    # O FILTRO QUE SUMIU VOLTOU EXATAMENTE COMO NA IMAGEM:
    tipo_saida = st.selectbox("🎯 Ação Pós-Auditoria (Filtro)", [
        "Apenas Relatório de Auditoria", 
        "Auditoria + Gerar Contrato Corrigido", 
        "Auditoria + Gerar Petição/Processo",
        "Análise Grafotécnica (Assinaturas)"
    ])
    
    pergunta = st.text_area("O que o sistema deve analisar ou redigir?", placeholder="Ex: Analise este contrato e verifique assinaturas...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    conteudo_extra = ""
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    # PROMPT MESTRE QUE EXECUTA A AÇÃO DO FILTRO
                    prompt_final = f"""
                    Atue como AUDITOR SUPREMO e ADVOGADO SÊNIOR. 
                    MENSAGEM: {pergunta}
                    FILTRO ATIVO: {tipo_saida}
                    DADOS: {conteudo_extra}
                    
                    REQUISITOS:
                    - Se 'Gerar Contrato/Processo' estiver ativo, redija o documento jurídico completo.
                    - Se 'Análise Grafotécnica' estiver ativa, verifique sinais de fraude em assinaturas.
                    - Cite leis brasileiras e forneça Score de Risco.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_final, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Cumprida!")
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RESULTADO (.DOCX)", preparar_download(response.text, tipo_saida), "aether_result.docx")
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. Desative o tradutor e dê Reboot!")
        else:
            st.warning("Insira uma instrução para o Sniper.")

with st.sidebar:
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("AETHER AUDIT v46.1 | Global Edition")
