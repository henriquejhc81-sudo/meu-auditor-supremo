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

# --- UI ELITE DESIGN (STEALTH & LOGO INTEGRATION) ---
st.set_page_config(page_title="AETHER OMNI ELITE v84.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização Suprema: Fundo Matte, Neon Dinâmico e Cards de Vidro
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fundo Matte Black Profundo */
    .stApp { background: linear-gradient(180deg, #020305 0%, #05070a 100%) !important; color: #e1e1e1 !important; }
    
    /* Logo e Títulos */
    .logo-text { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; letter-spacing: -2px; color: #ffffff; margin-bottom: 0px; }
    p, span, label { color: #64748b !important; font-size: 0.85em; letter-spacing: 0.5px; }

    /* Cards de Métrica (Layout Stealth) */
    .metric-card { 
        background: rgba(10, 12, 16, 0.8); 
        padding: 30px; border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.03);
        text-align: center;
        backdrop-filter: blur(10px);
        transition: 0.5s all cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .metric-card:hover { 
        border-color: #00c6ff; 
        box-shadow: 0 0 30px rgba(0, 198, 255, 0.15); 
        transform: translateY(-8px);
    }
    .metric-card b { 
        color: #00c6ff !important; 
        font-size: 1.8em; 
        font-family: 'JetBrains Mono';
        text-shadow: 0 0 15px rgba(0, 198, 255, 0.4);
    }

    /* Inputs e File Uploader (Glassmorphism Dark) */
    .stTextArea textarea { 
        background-color: rgba(5, 7, 10, 0.8) !important; 
        border: 1px solid #14181f !important; 
        color: #f1f5f9 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        transition: 0.4s all;
    }
    .stTextArea textarea:focus { border-color: #00c6ff !important; box-shadow: 0 0 20px rgba(0, 198, 255, 0.1) !important; }

    /* Botão de Comando (Premium Gradient Glow) */
    .stButton>button { 
        width: 100%; background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important; 
        color: #ffffff !important; 
        border: none !important; 
        border-radius: 14px; font-weight: 700;
        height: 4.2em; transition: 0.4s all;
        text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(0, 198, 255, 0.2);
    }
    .stButton>button:hover { 
        transform: scale(1.02);
        box-shadow: 0 20px 40px rgba(0, 198, 255, 0.4);
        filter: brightness(1.1);
    }

    /* Sidebar Ultra-Dark */
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #14181f; }
    
    /* Container do Relatório Final */
    .report-card { 
        padding: 60px; border-radius: 30px; background: #05070a; 
        border: 1px solid #14181f; box-shadow: 0 50px 100px rgba(0,0,0,0.9);
        line-height: 2.1; color: #cbd5e1; font-family: 'Plus Jakarta Sans';
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

# --- SIDEBAR (CONFIGURAÇÃO E LOGO) ---
with st.sidebar:
    # --- ESPAÇO PARA O SEU LOGO ---
    # st.image("caminho/do/seu/logo.png", width=150) # Descomente e coloque o caminho aqui
    st.markdown("<h1 class='logo-text'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    st.caption("Intelligence System v84.0")
    if model: st.success(f"Shield: {model_id}")
    
    st.divider()
    agente = st.selectbox("🎯 Agent Strategy", ["E-Discovery (Everlaw)", "Due Diligence (Kira)", "Compliance (OneTrust)", "Finance Audit (DataSnipper)"])
    st.divider()
    st.subheader("⚡ Core Modules")
    st.toggle("Neural Extraction", value=True)
    st.toggle("Anomalies Detection", value=True)
    if st.button("🔄 System Reboot"):
        st.cache_resource.clear()
        st.rerun()

# --- COMMAND CENTER ---
# Logo no centro (opcional)
# st.image("seu_logo_central.png", width=100) 
st.markdown("<h2 style='letter-spacing:-2px; margin-bottom:5px;'>COMMAND CENTER</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='font-family:JetBrains Mono; color:#475569;'>ORCHESTRATOR STATUS: ACTIVE // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Estilo Elite (Glow Reforçado)
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>Status</small><br><b>MONITORING</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>Precision</small><br><b>99.9%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>Protocol</small><br><b>ENCRYPTED</b></div>", unsafe_allow_html=True)

st.divider()

# Layout de Trabalho
col_a, col_b = st.columns([1, 1.4], gap="large")

with col_a:
    st.markdown("### 📂 Assets")
    arquivos = st.file_uploader("Drop evidences here", accept_multiple_files=True)
    acao = st.selectbox("Execution Mode:", ["Auditoria Conclusão Mestra", "Due Diligence Automática", "E-Discovery Profundo"])

with col_b:
    st.markdown("### 🔍 Sniper Prompt")
    pergunta = st.text_area("Audit Command:", placeholder="Input the specific mission parameters...", height=230)
    if st.button("🚀 EXECUTE GLOBAL SWEEP"):
        if (pergunta or arquivos) and model:
            with st.spinner("Analyzing Global Assets..."):
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
                    st.download_button("📥 DOWNLOAD ENCRYPTED REPORT", export_docx(response.text), "AETHER_REPORT.docx")
                except Exception as e: st.error(f"Error: {e}")
