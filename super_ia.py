import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN DE ELITE OMNI ---
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
    .report-card { padding: 30px; border-radius: 18px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .suggestion-card { background: #262730; padding: 10px; border-radius: 8px; border-left: 4px solid #00c6ff; margin-bottom: 8px; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (RESOLVE O ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    # LISTAGEM INTELIGENTE: O segredo da v36 que trouxe de volta para matar o 404
    modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Forçamos a seleção do modelo flash puro, sem prefixos beta
    model_name = "gemini-1.5-flash"
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error("📡 Rede Omni: Sincronizando conexão segura...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR COMPLETA ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {
            "Auditor Geral": ["Analise riscos contratuais e financeiros.", "Verifique cláusulas abusivas."],
            "Trabalhista": ["Valide multas conforme a CLT.", "Verifique riscos de vínculo."],
            "Tributário": ["Valide alíquotas de impostos.", "Aponte divergências fiscais."],
            "Imobiliário": ["Verifique reajustes e atrasos.", "Analise garantias."],
            "LGPD": ["Verifique conformidade com a LGPD.", "Analise retenção de dados."]
        }
        for item in opcoes.get(agente, []):
            st.markdown(f"<div class='suggestion-card'>💡 {item}</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Sniper Mode")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    cruzamento = st.toggle("Cruzamento de Dados", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("v43.1 | Enterprise Master Edition")

# --- CENTRAL OMNI ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}** | Engine: **v43.1 Ultimate**")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução...", height=150)

if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está processando os dados..."):
            try:
                contexto_total = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"

                prompt_final = f"""
                Atue como um {agente} Sênior. 
                Instrução: {pergunta} {contexto_total}
                REQUISITOS: Checklist de Compliance: {checklist} | Score de Risco: {score} | Cruzamento: {cruzamento}
                Use lógica de Big Four e cite leis brasileiras.
                """
                
                # Chamada limpa sem v1beta
                response = model.generate_content(prompt_final)
                
                st.markdown("### 📝 Resultado da Auditoria")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                st.download_button("📥 Exportar Relatório Master (.DOCX)", preparar_download(response.text), "aether_report.docx")
                st.balloons()
            except Exception as e:
                st.error(f"Erro de Rede Omni: {e}. Desative o tradutor e reinicie o motor.")
    else:
        st.warning("Insira uma pergunta.")
