import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM INTERNACIONAL ---
st.set_page_config(page_title="AETHER OMNI", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none;
    }
    .report-card { padding: 30px; border-radius: 18px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .suggestion-card { background: #262730; padding: 15px; border-radius: 10px; border-left: 4px solid #00c6ff; margin-bottom: 10px; font-size: 0.9em; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO ESTÁVEL V1 (FIM DO 404 V1BETA) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE MESTRE: Usamos gemini-1.5-flash na porta de produção estável v1
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔄 Sincronizando conexão estável para amanhã...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL (ARSENAL SNIPER) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    ativar_biblioteca = st.toggle("📂 Biblioteca de Perguntas", value=False)
    if ativar_biblioteca:
        st.subheader("📋 Sugestões (Copie e Cole)")
        opcoes = {
            "Auditor Geral": ["Analise riscos contratuais e financeiros.", "Verifique cláusulas abusivas ou ambíguas."],
            "Trabalhista": ["Valide multas rescisórias conforme a CLT.", "Verifique riscos de vínculo empregatício."],
            "Tributário": ["Valide alíquotas de impostos neste documento.", "Aponte possíveis divergências fiscais."],
            "Imobiliário": ["Verifique reajustes (IGP-M/IPCA) e atrasos.", "Analise garantias e multas contratuais."],
            "LGPD": ["Verifique se o tratamento de dados cumpre a lei.", "Analise a política de retenção de dados."]
        }
        for item in opcoes.get(agente, []):
            st.markdown(f"<div class='suggestion-card'>{item}</div>", unsafe_allow_html=True)

    st.divider()
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- CENTRAL OMNI ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Operando como: **{agente}** | Conexão Estável v1")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução...", height=150)

if st.button("🚀 INICIAR VARREDURA OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está varrendo as evidências..."):
            try:
                time.sleep(1)
                contexto_extra = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_extra += f"\n\nDADOS DO ARQUIVO {arq.name}:\n{df.to_string()}"

                prompt_final = f"Atue como {agente} Sênior. Analise: {pergunta} {contexto_extra}. Dê o Score de Risco e Checklist de Compliance."
                response = model.generate_content(prompt_final)
                
                st.success("Análise Concluída!")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                st.download_button("📥 BAIXAR RELATÓRIO WORD", preparar_download(response.text), "aether_report.docx")
                st.balloons()
            except Exception as e:
                st.error(f"Erro técnico: {e}. O motor será recalibrado.")
    else:
        st.warning("Insira uma instrução.")
