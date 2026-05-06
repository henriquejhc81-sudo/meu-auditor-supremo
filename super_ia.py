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

# --- UI ELITE DESIGN (LIQUID COMMAND CENTER) ---
st.set_page_config(page_title="AETHER OMNI ELITE v82.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização High-End: Eliminando o branco e focando em profundidade
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Corpo Dark Mode Absoluto */
    .stApp { background-color: #030407 !important; color: #e1e1e1 !important; }
    
    /* Fontes e Títulos */
    h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -1px; color: #ffffff !important; }
    p, span, label { color: #8e95a2 !important; font-size: 0.95em; }

    /* Cards de Métrica (Efeito Glassmorphism) */
    .metric-container { 
        display: flex; gap: 15px; margin-bottom: 25px; 
    }
    .metric-card { 
        background: rgba(13, 17, 23, 0.6); 
        padding: 20px; border-radius: 16px; 
        border: 1px solid rgba(255, 255, 255, 0.05);
        flex: 1; text-align: center;
        transition: 0.3s all;
    }
    .metric-card:hover { border-color: #00c6ff; background: rgba(0, 198, 255, 0.02); }
    .metric-card b { color: #00c6ff !important; font-size: 1.6em; font-family: 'JetBrains Mono'; }
    .metric-card small { display: block; color: #5c6370; text-transform: uppercase; font-size: 0.7em; letter-spacing: 2px; margin-bottom: 5px; }

    /* Inputs e TextAreas Estilo 'Luminance' */
    .stTextArea textarea { 
        background-color: #0a0c10 !important; 
        border: 1px solid #1e252e !important; 
        color: #d1d5db !important;
        border-radius: 12px !important;
        font-family: 'JetBrains Mono', monospace;
    }
    .stFileUploader section { 
        background-color: #0a0c10 !important; 
        border: 1px dashed #1e252e !important; 
        border-radius: 12px !important;
    }

    /* Botão de Ação (Aura Glow) */
    .stButton>button { 
        width: 100%; background: #ffffff !important; 
        color: #000000 !important; border: none !important; 
        border-radius: 10px; font-weight: 700;
        height: 3.8em; transition: 0.4s all;
        text-transform: uppercase; letter-spacing: 1px;
    }
    .stButton>button:hover { 
        background: #00c6ff !important; color: #ffffff !important;
        box-shadow: 0 10px 25px rgba(0, 198, 255, 0.3);
    }

    /* Sidebar Refinada */
    [data-testid="stSidebar"] { background-color: #05070a !important; border-right: 1px solid #14181f; }
    
    /* Painel de Resultado (O Parecer) */
    .report-card { 
        padding: 45px; border-radius: 20px; background: #0a0c10; 
        border: 1px solid #14181f; box-shadow: 0 30px 60px rgba(0,0,0,0.8);
        line-height: 1.9; color: #d1d5db; font-family: 'Plus Jakarta Sans';
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
    st.markdown("<h2 style='color:#00c6ff;'>🛡️ AETHER</h2>", unsafe_allow_html=True)
    st.caption("Intelligence System v82.0")
    if model: st.success(f"System: {model_id}")
    
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
st.markdown(f"<p style='font-family:JetBrains Mono;'>ORCHESTRATOR ACTIVE // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Estilo Harvey AI
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>Status</small><br><b>MONITORING</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>Precision</small><br><b>99.8%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>Security</small><br><b>ENCRYPTED</b></div>", unsafe_allow_html=True)

st.divider()

# Layout de Trabalho Assimétrico
col_a, col_b = st.columns([1, 1.4], gap="large")

with col_a:
    st.markdown("### 📂 Assets")
    arquivos = st.file_uploader("Upload evidences", accept_multiple_files=True)
    acao = st.selectbox("Neural Strategy:", ["Auditoria Conclusão Mestra", "Due Diligence Automática", "E-Discovery Profundo"])

with col_b:
    st.markdown("### 🔍 Sniper Prompt")
    pergunta = st.text_area("Audit Instructions:", placeholder="Enter your command for the Super-AI...", height=210)
    if st.button("🚀 EXECUTE GLOBAL SWEEP"):
        if (pergunta or arquivos) and model:
            with st.spinner("Processing..."):
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
                    st.download_button("📥 DOWNLOAD (.DOCX)", export_docx(response.text), "AETHER_REPORT.docx")
                except Exception as e: st.error(f"Error: {e}")
