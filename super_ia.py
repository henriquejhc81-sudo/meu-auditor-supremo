import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM REFINADO ---
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
    .suggestion-card { background: #262730; padding: 15px; border-radius: 10px; border-left: 4px solid #00c6ff; margin-bottom: 10px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA v1 (FIM DO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except:
    st.error("🔄 Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    # CORREÇÃO DO ERRO: Nome da variável unificado
    ativar_biblioteca = st.toggle("📂 Abrir Biblioteca de Perguntas", value=False)
    
    if ativar_biblioteca:
        st.subheader("📋 Sugestões Sniper")
        if agente == "Auditor Geral":
            st.markdown("<div class='suggestion-card'><b>Geral:</b> Analise este contrato e aponte os 5 principais riscos financeiros e jurídicos.</div>", unsafe_allow_html=True)
            st.markdown("<div class='suggestion-card'><b>Geral:</b> Verifique se há cláusulas abusivas ou ambíguas neste documento.</div>", unsafe_allow_html=True)
        elif agente == "Trabalhista":
            st.markdown("<div class='suggestion-card'><b>Trabalhista:</b> Verifique se as multas rescisórias estão de acordo com a CLT.</div>", unsafe_allow_html=True)
            st.markdown("<div class='suggestion-card'><b>Trabalhista:</b> Analise riscos de vínculo empregatício neste contrato.</div>", unsafe_allow_html=True)
        elif agente == "Tributário":
            st.markdown("<div class='suggestion-card'><b>Tributário:</b> Valide as alíquotas de impostos citadas nesta nota ou contrato.</div>", unsafe_allow_html=True)
        elif agente == "Imobiliário":
            st.markdown("<div class='suggestion-card'><b>Imobiliário:</b> Verifique cláusulas de reajuste e penalidades por atraso.</div>", unsafe_allow_html=True)
        elif agente == "LGPD":
            st.markdown("<div class='suggestion-card'><b>LGPD:</b> Verifique se o tratamento de dados cumpre a LGPD atual.</div>", unsafe_allow_html=True)
        st.caption("Selecione o texto acima para copiar.")

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- CORPO CENTRAL ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}**")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução ou use a biblioteca da lateral...", height=150)

if st.button("🚀 INICIAR VARREDURA OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está processando os dados..."):
            try:
                time.sleep(1)
                contexto_arquivos = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_arquivos += f"\n\nDADOS DO ARQUIVO {arq.name}:\n{df.to_string()}"

                prompt_final = f"Atue como um {agente} Sênior. Sua missão: {pergunta} {contexto_arquivos}. Forneça checklist de compliance e score de risco."
                
                response = model.generate_content(prompt_final)
                
                st.markdown("### 📝 Resultado da Auditoria")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                st.download_button("📥 Exportar para Word", preparar_download(response.text), "aether_report.docx")
                st.balloons()
                
            except Exception as e:
                st.error(f"Erro de Rede Omni: {e}. Desative o tradutor do navegador.")
    else:
        st.warning("Insira uma pergunta.")

st.sidebar.caption("v40.9 | Final Enterprise Edition")
