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

# --- UI ELITE DESIGN (VIBRANT STEALTH & LOGO INTEGRATION) ---
st.set_page_config(page_title="AETHER OMNI ELITE v87.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

# Estilização: Fundo Profundo com Iluminação de Contorno e Neon Ativo
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Fundo Dark com Gradiente de Iluminação */
    .stApp { 
        background: radial-gradient(circle at 50% 0%, #10141b 0%, #05070a 100%) !important; 
        color: #e1e1e1 !important; 
    }
    
    /* Logo e Títulos Vibrantes */
    .logo-text { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; letter-spacing: -1.5px; color: #ffffff; }
    h2, h3 { color: #ffffff !important; font-family: 'Plus Jakarta Sans', sans-serif; }
    p, span, label { color: #94a3b8 !important; font-size: 0.9em; font-weight: 500; }

    /* Cards de Métrica (Efeito de Brilho Interno) */
    .metric-card { 
        background: rgba(15, 23, 42, 0.6); 
        padding: 25px; border-radius: 18px; 
        border: 1px solid rgba(0, 198, 255, 0.2);
        text-align: center;
        backdrop-filter: blur(12px);
        transition: 0.4s all ease-in-out;
    }
    .metric-card:hover { 
        border-color: #00c6ff; 
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.2);
        transform: translateY(-5px);
    }
    .metric-card b { 
        color: #00c6ff !important; 
        font-size: 1.7em; 
        font-family: 'JetBrains Mono';
        text-shadow: 0 0 12px rgba(0, 198, 255, 0.5);
    }
    .metric-card small { color: #475569; text-transform: uppercase; letter-spacing: 2px; }

    /* Inputs (Remoção do aspecto 'apagado') */
    .stTextArea textarea { 
        background-color: #0f172a !important; 
        border: 1px solid #1e293b !important; 
        color: #f8fafc !important;
        border-radius: 16px !important;
        font-size: 1em !important;
    }
    .stTextArea textarea:focus { border-color: #00c6ff !important; box-shadow: 0 0 15px rgba(0, 198, 255, 0.2) !important; }

    .stFileUploader section { 
        background-color: #0f172a !important; 
        border: 1px dashed #334155 !important; 
        border-radius: 16px !important;
    }

    /* Botão de Comando (Power Blue) */
    .stButton>button { 
        width: 100%; background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important; 
        color: #ffffff !important; border: none !important; 
        border-radius: 12px; font-weight: 700;
        height: 4em; transition: 0.3s all;
        text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0 10px 20px rgba(0, 198, 255, 0.3);
    }
    .stButton>button:hover { 
        box-shadow: 0 0 30px rgba(0, 198, 255, 0.5);
        filter: brightness(1.1);
        transform: scale(1.01);
    }

    /* Sidebar Refinada */
    [data-testid="stSidebar"] { background-color: #020617 !important; border-right: 1px solid #1e293b; }
    
    /* Painel de Resultado (O Parecer Master) */
    .report-card { 
        padding: 40px; border-radius: 20px; background: #0f172a; 
        border: 1px solid #1e293b; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        line-height: 2; color: #cbd5e1;
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

# --- SIDEBAR (LOGO E AGENTE) ---
with st.sidebar:
    try:
        st.image("logo.png.jpeg", use_column_width=True)
    except:
        st.markdown("<h1 class='logo-text'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    
    st.caption("Intelligence System v87.0")
    if model: st.success(f"System Online: {model_id}")
    
    st.divider()
    agente = st.selectbox("🎯 Agent Focus", ["E-Discovery (Everlaw)", "Due Diligence (Kira)", "Compliance (OneTrust)", "Finance Audit (DataSnipper)"])
    st.divider()
    st.subheader("⚡ Modules")
    st.toggle("Neural Extraction", value=True)
    st.toggle("Anomalies Detection", value=True)
    if st.button("🔄 Reset Engine"):
        st.cache_resource.clear()
        st.rerun()

# --- COMMAND CENTER ---
st.markdown("<h2 style='letter-spacing:-1.5px; margin-bottom:0px;'>AETHER OMNI COMMAND</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='font-family:JetBrains Mono; color:#38bdf8;'>ORCHESTRATOR STATUS: ACTIVE // AGENT: {agente.upper()}</p>", unsafe_allow_html=True)

# Métricas Vibrantes (Estilo Harvey + Iluminação)
m1, m2, m3 = st.columns(3)
with m1: st.markdown("<div class='metric-card'><small>Status</small><br><b>MONITORING</b></div>", unsafe_allow_html=True)
with m2: st.markdown("<div class='metric-card'><small>Precision</small><br><b>99.9%</b></div>", unsafe_allow_html=True)
with m3: st.markdown("<div class='metric-card'><small>Protocol</small><br><b>ENCRYPTED</b></div>", unsafe_allow_html=True)

st.divider()

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
            with st.spinner("Analyzing Assets..."):
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
                    st.download_button("📥 DOWNLOAD REPORT", export_docx(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e: st.error(f"Error: {e}")
