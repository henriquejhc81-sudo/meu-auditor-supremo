import streamlit as st
import pandas as pd
import io
import time
from PIL import Image

# Gestão de dependências críticas
try:
    import google.generativeai as genai
    from docx import Document
    BIBLIOTECAS_OK = True
except ImportError:
    BIBLIOTECAS_OK = False

# --- UI ELITE DESIGN (ULTRA-DARK EVOLUTION) ---
st.set_page_config(page_title="AETHER OMNI ELITE v81.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização para eliminar o "Branco" e focar no Dark Mode Profissional
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fundo Principal Ultra-Dark */
    .stApp { background-color: #05070a !important; color: #e1e1e1 !important; }
    
    /* Títulos e Textos */
    h1, h2, h3, p, span, label { color: #d1d5db !important; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    /* Botão Estilo Elite */
    .stButton>button { 
        width: 100%; background: linear-gradient(135deg, #12151c 0%, #1a1f2b 100%); 
        color: #00c6ff !important; border: 1px solid #2d323d !important; border-radius: 8px; font-weight: 600;
        height: 3.8em; transition: 0.4s all; text-transform: uppercase; letter-spacing: 1.5px;
    }
    .stButton>button:hover { border-color: #00c6ff !important; box-shadow: 0 0 20px rgba(0, 198, 255, 0.2); color: #fff !important; }
    
    /* Cards de Métrica (Luminance Style) */
    .metric-card { 
        background: #0d1117; padding: 25px; border-radius: 12px; 
        border: 1px solid #1e252e; text-align: center;
        box-shadow: inset 0 0 10px rgba(0, 198, 255, 0.05);
    }
    .metric-card b { color: #00c6ff !important; font-size: 1.4em; }
    .metric-card small { color: #7b818f !important; text-transform: uppercase; letter-spacing: 1px; }
    
    /* Inputs Escuros (Fim do Branco) */
    .stTextArea textarea, .stFileUploader section { 
        background-color: #0d1117 !important; 
        border: 1px solid #2d323d !important; 
        color: #e1e1e1 !important;
        border-radius: 10px !important;
    }
    
    /* Customização da Sidebar */
    [data-testid="stSidebar"] { background-color: #080a0d !important; border-right: 1px solid #1e252e; }
    
    /* Resultado da Auditoria */
    .report-card { 
        padding: 40px; border-radius: 15px; background: #0d1117; 
        border: 1px solid #1e252e; box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        line-height: 1.8; color: #d1d5db;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DE INTELIGÊNCIA ---
@st.cache_resource
def evolution_engine(api_key):
    genai.configure(api_key=api_key)
    for model_name in ["gemini-1.5-pro", "gemini-1.5-flash"]:
        try:
            m = genai.GenerativeModel(model_name=model_name)
            m.generate_content("ok", generation_config={"max_output_tokens": 1})
            return m, model_name
        except: continue
    return None, None

api_key = st.secrets.get("GOOGLE_API_KEY")
model, model_id = evolution_engine(api_key) if api_key else (None, None)

def export_docx(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI ELITE REPORT', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR CENTER ---
with st.sidebar:
    st.markdown("<h2 style='color:#00c6ff;'>🛡️ AETHER ELITE</h2>", unsafe_allow_html=True)
    st.caption("Global Intelligence v81.0")
    if model: st.success(f"ONLINE: {model_id}")
    
    st.divider()
    agente = st.selectbox("🎯 Agente", ["E-Discovery (Everlaw)", "Due Diligence (Kira)", "Compliance (OneTrust)", "Finance Audit (DataSnipper)"])
    st.divider()
    st.subheader("⚡ Parâmetros")
    st.toggle("Extração de Dados", value=True)
    st.toggle("Detecção de Anomalias", value=True)
    if st.button("🔄 REINICIAR SISTEMA"):
        st.cache_resource.clear()
        st.rerun()

# --- DASHBOARD: THE COMMAND CENTER ---
st.title("🛡️ AETHER OMNI COMMAND")
st.markdown(f"<p style='color:#7b818f; font-family:JetBrains Mono;'>ORCHESTRATOR ACTIVE // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Estilizadas (Fundo Escuro)
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>ANOMALIA</small><br><b>MONITORANDO</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>PRECISÃO</small><br><b>99.8%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>STATUS</small><br><b>PROTEGIDO</b></div>", unsafe_allow_html=True)

st.divider()

col_a, col_b = st.columns([1, 1.3], gap="large")

with col_a:
    st.subheader("📂 Ingestão de Ativos")
    arquivos = st.file_uploader("Arraste arquivos aqui", accept_multiple_files=True)
    acao = st.selectbox("Estratégia Neural:", ["Auditoria Conclusão Mestra", "Due Diligence Automática", "E-Discovery Profundo"])

with col_b:
    pergunta = st.text_area("Sniper Prompt (Instruções):", placeholder="Defina a missão...", height=220)
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner("Processando..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_elite = f"Atue como AETHER ELITE. Agente: {agente}. MISSÃO: {acao}. INSTRUÇÃO: {pergunta} CONTEXTO: {extra_data}"
                    response = model.generate_content([prompt_elite, *imagens] if imagens else prompt_elite)
                    
                    st.markdown("### 📝 PARECER ELITE")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 EXPORTAR (.DOCX)", export_docx(response.text), "AETHER_REPORT.docx")
                except Exception as e: st.error(f"Erro: {e}")
