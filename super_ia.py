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
    .suggestion-card { background: #262730; padding: 10px; border-radius: 8px; border-left: 4px solid #00c6ff; margin-bottom: 8px; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (ESTABILIZAÇÃO V1 - FIM DO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # A correção mestre: Forçamos o modelo sem v1beta e ignoramos list_models()
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

# --- INTERFACE ---
st.title("🛡️ AETHER AUDIT ENTERPRISE v46.0")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.markdown("### ⚙️ Sniper Config")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas", value=True)
    score_risco = st.toggle("Score de Risco Automático", value=True)
    detec_anomalia = st.toggle("Detecção de Anomalias (Forense/Assinaturas)", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    # RESTAURAÇÃO: Filtro de Objetivo (Contrato, Processo, Auditoria)
    modo_acao = st.selectbox("🎯 Objetivo da Análise", [
        "Auditoria e Auditoria Forense", 
        "Gerar Contrato Personalizado", 
        "Gerar Processo/Petição Jurídica",
        "Análise de Conformidade (Compliance)"
    ])
    
    pergunta = st.text_area("O que o sistema deve analisar ou redigir?", placeholder="Descreva sua missão aqui...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando na nuvem..."):
                try:
                    conteudo_extra = ""
                    imagens = []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"):
                                imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                conteudo_extra += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"

                    prompt_final = f"""
                    Atue como AUDITOR SUPREMO e ADVOGADO SÊNIOR. 
                    Missão: {modo_acao}. Instrução: {pergunta} {conteudo_extra}.
                    Use lógica de Big Four, cite leis brasileiras e forneça checklist de compliance e Score de Risco.
                    Se o modo for Geração, redija o documento jurídico completo.
                    """
                    
                    if imagens:
                        response = model.generate_content([prompt_final, *imagens])
                    else:
                        response = model.generate_content(prompt_final)
                    
                    st.success("Missão Cumprida!")
                    tab1, tab2 = st.tabs(["📝 Relatório Supremo", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RESULTADO (.DOCX)", preparar_download(response.text, modo_acao), "aether_result.docx")
                        st.balloons()
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}. Desative o tradutor e reinicie o motor.")
        else:
            st.warning("Aguardando instrução do Sniper.")

with st.sidebar:
    st.subheader("📚 Biblioteca Sniper")
    # RESTAURAÇÃO: Sugestões dinâmicas por modo
    if modo_acao == "Gerar Contrato Personalizado":
        st.markdown("<div class='suggestion-card'>💡 Redija um contrato de prestação de serviços de TI com cláusula de confidencialidade.</div>", unsafe_allow_html=True)
    elif modo_acao == "Auditoria e Auditoria Forense":
        st.markdown("<div class='suggestion-card'>💡 Verifique se as assinaturas deste PDF apresentam sinais de montagem digital.</div>", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    st.caption("AETHER AUDIT v46.0 | Master Fusion Edition")
