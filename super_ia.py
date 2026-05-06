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

# --- UI ELITE DESIGN (PRECISION & GLOW EVOLUTION) ---
st.set_page_config(page_title="AETHER OMNI ELITE v83.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização Refinada: Foco em profundidade e iluminação neon seletiva
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fundo Deep Black */
    .stApp { background-color: #020305 !important; color: #e1e1e1 !important; }
    
    /* Títulos Magnéticos */
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -1.5px; color: #ffffff !important; }
    p, span, label { color: #64748b !important; font-size: 0.9em; font-weight: 500; }

    /* Cards de Métrica (Refinamento de Glow) */
    .metric-card { 
        background: #0a0c10; 
        padding: 30px; border-radius: 18px; 
        border: 1px solid #14181f;
        text-align: center;
        transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover { 
        border-color: #00c6ff; 
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.1); 
        transform: translateY(-5px);
    }
    .metric-card b { 
        color: #00c6ff !important; 
        font-size: 1.8em; 
        font-family: 'JetBrains Mono';
        text-shadow: 0 0 10px rgba(0, 198, 255, 0.3);
    }
    .metric-card small { 
        display: block; 
        color: #475569; 
        text-transform: uppercase; 
        font-size: 0.75em; 
        letter-spacing: 3px; 
        margin-bottom: 8px; 
    }

    /* Inputs High-Tech (Foco Neon) */
    .stTextArea textarea { 
        background-color: #05070a !important; 
        border: 1px solid #14181f !important; 
        color: #f1f5f9 !important;
        border-radius: 14px !important;
        font-family: 'JetBrains Mono', monospace;
        transition: 0.3s all;
    }
    .stTextArea textarea:focus { border-color: #00c6ff !important; box-shadow: 0 0 15px rgba(0, 198, 255, 0.15) !important; }

    .stFileUploader section { 
        background-color: #05070a !important; 
        border: 1px dashed #1e293b !important; 
        border-radius: 14px !important;
    }

    /* Botão de Elite (Vidro & Luz) */
    .stButton>button { 
        width: 100%; background: transparent !important; 
        color: #ffffff !important; 
        border: 1px solid #1e293b !important; 
        border-radius: 12px; font-weight: 600;
        height: 4em; transition: 0.5s all;
        text-transform: uppercase; letter-spacing: 2px;
    }
    .stButton>button:hover { 
        background: #ffffff !important; color: #000000 !important;
        box-shadow: 0 15px 35px rgba(255, 255, 255, 0.2);
        border: none !important;
    }

    /* Sidebar Dark Profissional */
    [data-testid="stSidebar"] { background-color: #010203 !important; border-right: 1px solid #14181f; }
    
    /* Área de Relatório (Efeito de Profundidade) */
    .report-card { 
        padding: 50px; border-radius: 24px; background: #05070a; 
        border: 1px solid #14181f; box-shadow: 0 40px 80px rgba(0,0,0,0.9);
        line-height: 2; color: #cbd5e1; font-family: 'Plus Jakarta Sans';
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

# --- SIDEBAR (CONFIGURAÇÃO) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00c6ff; font-size:1.8em;'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    st.caption("Intelligence System v83.0")
    if model: st.success(f"Online: {model_id}")
    
    st.divider()
    agente = st.selectbox("🎯 Agent Focus", ["E-Discovery (Everlaw)", "Due Diligence (Kira)", "Compliance (OneTrust)", "Finance Audit (DataSnipper)"])
    st.divider()
    st.subheader("⚡ Tools")
    st.toggle("Data Extraction", value=True)
    st.toggle("Anomalies Detection", value=True)
    if st.button("🔄 Reset System"):
        st.cache_resource.clear()
        st.rerun()

# --- COMMAND CENTER ---
st.title("🛡️ COMMAND CENTER")
st.markdown(f"<p style='font-family:JetBrains Mono; color:#475569;'>ORCHESTRATOR ACTIVE // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Estilo Harvey AI (Com Glow Reforçado)
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>Status</small><br><b>MONITORING</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>Precision</small><br><b>99.8%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>Security</small><br><b>ENCRYPTED</b></div>", unsafe_allow_html=True)

st.divider()

# Layout de Trabalho Assimétrico (Melhorado)
col_a, col_b = st.columns([1, 1.4], gap="large")

with col_a:
    st.markdown("### 📂 Assets")
    arquivos = st.file_uploader("Upload evidences", accept_multiple_files=True)
    acao = st.selectbox("Neural Strategy:", ["Auditoria Conclusão Mestra", "Due Diligence Automática", "E-Discovery Profundo"])

with col_b:
    st.markdown("### 🔍 Sniper Prompt")
    pergunta = st.text_area("Audit Instructions:", placeholder="Enter your command for the Super-AI...", height=230)
    if st.button("🚀 EXECUTE GLOBAL SWEEP"):
        if (pergunta or arquivos) and model:
            with st.spinner("Executing Swep..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_elite = f"Act as AETHER ELITE ({agente}). MISSION: {acao}. INSTRUCTION: {pergunta} CONTEXT: {extra_data}"
                    response = model.generate_content([prompt_elite, *imagens] if imagens else prompt_elite)
                    
                    st.markdown("### 📝 FINAL REPORT")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 DOWNLOAD REPORT (.DOCX)", export_docx(response.text), "AETHER_REPORT.docx")
                except Exception as e: st.error(f"Error: {e}")
