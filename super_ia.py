import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM REFINADO (INTER FONT & DARK MODE) ---
st.set_page_config(page_title="AETHER OMNI MASTER", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
    }
    .report-card { padding: 30px; border-radius: 18px; background-color: #1a1c24; border: 1px solid #2d2f39; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .suggestion-box { padding: 15px; background: #262730; border-radius: 12px; border-left: 5px solid #00c6ff; margin-bottom: 15px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO ESTÁVEL V1 (FIM DO 404 V1BETA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Conexão via porta estável de produção
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔄 Conexão instável. Reinicie o motor na lateral.")

def preparar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE INTELIGÊNCIA MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL SNIPER COMPLETO) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {
            "Auditor Geral": ["Analise riscos contratuais e financeiros.", "Verifique cláusulas abusivas ou ambíguas."],
            "Trabalhista": ["Valide multas rescisórias conforme a CLT.", "Verifique riscos de vínculo empregatício."],
            "Tributário": ["Valide alíquotas de impostos neste documento.", "Aponte possíveis divergências fiscais."],
            "Imobiliário": ["Verifique reajustes (IGP-M/IPCA) e atrasos.", "Analise garantias e multas contratuais."],
            "LGPD": ["Verifique se o tratamento de dados cumpre a lei.", "Analise a política de retenção de dados."]
        }
        for item in opcoes.get(agente, []):
            st.caption(f"💡 {item}")

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências (PDF, Excel, Imagens)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco Automático (%)", value=True)
    cruzamento = st.toggle("Cruzamento de Dados (Cross-check)", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Agente: **{agente}** | Status: **Operacional** | Versão Estável v1")

# Sugestões rápidas visuais
c1, c2, c3 = st.columns(3)
with c1: st.caption("💡 *Analise riscos trabalhistas*")
with c2: st.caption("💡 *Verifique cláusulas de LGPD*")
with c3: st.caption("💡 *Compare planilhas e contratos*")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução...", height=150)

if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está processando as evidências..."):
            try:
                time.sleep(1)
                contexto_total = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nDADOS DO ARQUIVO {arq.name}:\n{df.to_string()}"

                prompt_master = f"""
                Atue como um {agente} Sênior (Nível Big Four). 
                Instrução: {pergunta}
                Contexto Adicional: {contexto_total}
                
                REQUISITOS OBRIGATÓRIOS:
                1. 📝 RESUMO EXECUTIVO DA MISSÃO.
                2. ✅ CHECKLIST DE COMPLIANCE: {checklist}.
                3. 📊 SCORE DE RISCO (0-100%): {score}.
                4. ⚖️ SUGESTÃO DE REDAÇÃO JURÍDICA/CORREÇÃO.
                Use linguagem técnica e cite leis brasileiras vigentes.
                """
                
                response = model.generate_content(prompt_master)
                
                st.markdown("### 📝 Resultado da Auditoria")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                st.download_button("📥 Exportar Relatório Master (.DOCX)", preparar_download(response.text), "aether_report_master.docx")
                st.balloons()
            except Exception as e:
                st.error(f"📡 Erro de Rede Omni: {e}. Desative o tradutor do navegador.")
    else:
        st.warning("Aguardando instrução do auditor.")

st.sidebar.caption("v41.0 | Enterprise Master Edition")
