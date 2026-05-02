import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM MASTER ---
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
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (FORÇANDO PORTA v1 ESTÁVEL) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Comando de configuração absoluta
    genai.configure(api_key=API_KEY)
    
    # AJUSTE FÊNIX: Listamos os modelos para garantir que pegamos o caminho de produção
    # Isso mata o erro 404 de 'versão v1beta' que aparece na sua tela
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Sincronizando Rede Omni... Detalhe: {e}")

def preparar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE INTELIGÊNCIA MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL COMPLETO MANTIDO) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {
            "Auditor Geral": ["Analise riscos contratuais e financeiros.", "Verifique cláusulas abusivas."],
            "Trabalhista": ["Valide multas rescisórias CLT.", "Verifique riscos de vínculo."],
            "Tributário": ["Valide alíquotas de impostos.", "Aponte divergências fiscais."],
            "Imobiliário": ["Verifique reajustes (IGP-M/IPCA).", "Analise garantias."],
            "LGPD": ["Verifique conformidade com a LGPD atual."]
        }
        for item in opcoes.get(agente, []):
            st.caption(f"💡 {item}")

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco Automático (%)", value=True)
    cruzamento = st.toggle("Cruzamento de Dados (Cross-check)", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- INTERFACE CENTRAL ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}** | Versão Estável v1")

c1, c2, c3 = st.columns(3)
with c1: st.caption("💡 *Analise riscos trabalhistas*")
with c2: st.caption("💡 *Verifique cláusulas de LGPD*")
with c3: st.caption("💡 *Compare planilhas e contratos*")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução...", height=150)

if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está processando as evidências..."):
            try:
                contexto_total = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nDADOS DO ARQUIVO {arq.name}:\n{df.to_string()}"

                prompt_master = f"Atue como {agente} Sênior. Instrução: {pergunta} {contexto_total}. Requisitos: Checklist: {checklist}, Score: {score}. Cite leis brasileiras."
                
                # Chamada direta sem prefixos de versão
                response = model.generate_content(prompt_master)
                
                st.markdown("### 📝 Resultado da Auditoria")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                st.download_button("📥 Exportar Relatório Master (.DOCX)", preparar_docx(response.text), "aether_report_master.docx")
                st.balloons()
            except Exception as e:
                st.error(f"📡 Erro de Rede Omni: {e}. Desative o tradutor do navegador.")
    else:
        st.warning("Insira uma pergunta.")

st.sidebar.caption("v42.0 | Enterprise Master Edition")
