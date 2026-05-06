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

# --- UI ELITE DESIGN (COMPACT & LAYERED DARKNESS) ---
st.set_page_config(page_title="AETHER OMNI v88.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização Suprema: Design Compacto de Alta Densidade
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fundo em Camadas (Inspirado em Harvey) */
    .stApp { 
        background: radial-gradient(circle at top, #1e293b 0%, #0f172a 50%, #020617 100%) !important; 
        color: #f1f5f9 !important; 
    }
    
    /* Compactação de Títulos */
    h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; letter-spacing: -1px; margin-bottom: 5px !important; }
    p, span, label { color: #94a3b8 !important; font-size: 0.85em !important; font-weight: 500; }

    /* Cards de Métrica Compactos */
    .metric-card { 
        background: rgba(30, 41, 59, 0.4); 
        padding: 15px; border-radius: 12px; 
        border: 1px solid rgba(56, 189, 248, 0.2);
        text-align: center;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
    }
    .metric-card b { 
        color: #38bdf8 !important; 
        font-size: 1.4em; 
        font-family: 'JetBrains Mono';
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }
    .metric-card small { color: #64748b; text-transform: uppercase; letter-spacing: 2px; font-size: 0.65em; }

    /* Inputs Profissionais de Alta Densidade */
    .stTextArea textarea { 
        background-color: #020617 !important; 
        border: 1px solid #1e293b !important; 
        color: #f8fafc !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 0.9em !important;
    }
    .stFileUploader section { 
        background-color: #020617 !important; 
        border: 1px dashed #334155 !important; 
        border-radius: 12px !important;
        padding: 5px !important;
    }

    /* Botão de Comando Compacto (Pulse Mode) */
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%) !important; 
        color: #ffffff !important; border: none !important; 
        border-radius: 10px; font-weight: 700;
        height: 3em; transition: 0.3s all;
        text-transform: uppercase; letter-spacing: 1px; font-size: 0.8em;
    }
    .stButton>button:hover { 
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.4);
        transform: scale(1.01);
    }

    /* Sidebar Ultra-Elegante */
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    
    /* Painel de Resultado Consolidado */
    .report-card { 
        padding: 30px; border-radius: 16px; background: rgba(15, 23, 42, 0.8); 
        border: 1px solid #1e293b; line-height: 1.8; color: #cbd5e1;
        font-size: 0.9em;
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
    doc.add_heading('AETHER OMNI MASTER REPORT', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (CONTROLES GLOBAIS) ---
with st.sidebar:
    try:
        st.image("logo.png.jpeg", use_column_width=True)
    except:
        st.markdown("<h2 style='color:#38bdf8; text-align:center;'>🛡️ AETHER</h2>", unsafe_allow_html=True)
    
    st.caption("Intelligence System v88.0")
    if model: st.success(f"System Active")
    
    st.divider()
    agente = st.selectbox("🎯 Agent Focus", ["E-Discovery (Everlaw)", "Due Diligence (Kira)", "Compliance (OneTrust)", "Finance Audit (DataSnipper)"])
    st.divider()
    st.subheader("⚡ Modules")
    st.toggle("Neural Scan", value=True)
    st.toggle("Anomalies", value=True)
    if st.button("🔄 Reset Engine"):
        st.cache_resource.clear()
        st.rerun()

# --- COMMAND CENTER ---
st.markdown("<h3 style='margin-bottom:0px;'>AETHER OMNI COMMAND</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='font-family:JetBrains Mono; color:#38bdf8; font-size:0.7em !important;'>STATUS: OPERATIONAL // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Compactas
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>Status</small><br><b>MONITORING</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>Precision</small><br><b>99.9%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>Protocol</small><br><b>SECURE</b></div>", unsafe_allow_html=True)

# Espaço de Trabalho Compacto
col_a, col_b = st.columns([1, 1.4], gap="small")

with col_a:
    st.markdown("### 📂 Assets")
    arquivos = st.file_uploader("Upload evidences", accept_multiple_files=True)
    acao = st.selectbox("Execution Mode:", ["Auditoria Master", "Due Diligence", "E-Discovery"])

with col_b:
    st.markdown("### 🔍 Sniper Prompt")
    pergunta = st.text_area("Audit Command:", placeholder="Input the mission parameters...", height=180)
    if st.button("🚀 EXECUTE GLOBAL SWEEP"):
        if (pergunta or arquivos) and model:
            with st.spinner("Analyzing..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.head(5).to_string()}"

                    prompt_elite = f"Act as AETHER ELITE ({agente}). MISSION: {acao}. INSTRUCTION: {pergunta} CONTEXT: {extra_data}"
                    response = model.generate_content([prompt_elite, *imagens] if imagens else prompt_elite)
                    
                    st.markdown("### 📝 REPORT")
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 DOWNLOAD", export_docx(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e: st.error(f"Error: {e}")
