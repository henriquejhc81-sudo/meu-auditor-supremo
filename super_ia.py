import streamlit as st
import pandas as pd
import io
import time
from PIL import Image

# Gestão de dependências
try:
    import google.generativeai as genai
    from docx import Document
    BIBLIOTECAS_OK = True
except ImportError:
    BIBLIOTECAS_OK = False

# --- UI DESIGN (THE SENTINEL MASTER EVOLUTION) ---
st.set_page_config(page_title="AETHER OMNI v86.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes. Verifique o requirements.txt.")
    st.stop()

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #020408 !important; color: #e1e1e1 !important; }
    
    /* BARRA DE STATUS PREMIUM */
    .status-bar {
        background: linear-gradient(90deg, rgba(0, 198, 255, 0.05) 0%, rgba(0, 114, 255, 0.1) 100%);
        border: 1px solid rgba(0, 198, 255, 0.3);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85em;
        letter-spacing: 3px;
        color: #00c6ff;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.1);
        margin-bottom: 40px;
    }

    /* CARDS DE CONTEÚDO (ESTILO NEXUS) */
    .sentinel-card {
        background: rgba(10, 15, 25, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        margin-bottom: 25px;
    }

    .section-title { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        font-weight: 700; 
        color: #ffffff; 
        display: flex; 
        align-items: center; 
        gap: 12px; 
        margin-bottom: 20px; 
        font-size: 1.2em;
    }
    
    /* INPUTS HIGH-TECH */
    .stTextArea textarea { 
        background-color: #05070a !important; 
        border: 1px solid #1c2331 !important; 
        color: #f1f5f9 !important; 
        border-radius: 15px !important;
        font-family: 'Inter', sans-serif;
    }
    .stFileUploader section { 
        background-color: #05070a !important; 
        border: 1px dashed #2c3e50 !important; 
        border-radius: 15px !important;
    }

    /* BOTÃO ATIVAR (ULTRA GRADIENTE) */
    .stButton>button {
        width: 100%; 
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important; 
        border: none !important; 
        border-radius: 15px;
        font-weight: 700; 
        height: 4.2em; 
        text-transform: uppercase; 
        letter-spacing: 2px;
        transition: 0.5s all cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 10px 25px rgba(0, 198, 255, 0.3);
    }
    .stButton>button:hover { 
        transform: scale(1.03) translateY(-3px); 
        box-shadow: 0 15px 35px rgba(0, 198, 255, 0.5);
    }
    
    /* SIDEBAR NEXUS STYLE */
    [data-testid="stSidebar"] { 
        background-color: #010204 !important; 
        border-right: 1px solid rgba(0, 198, 255, 0.1); 
    }
    
    /* PARECER FINAL */
    .report-card { 
        background: #05070a; 
        padding: 40px; 
        border-radius: 20px; 
        border: 1px solid #1c2331; 
        line-height: 1.9; 
        color: #cbd5e1;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.5);
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

# --- SIDEBAR (LOGO E CONTROLES) ---
with st.sidebar:
    try:
        st.image("logo.png.jpeg", use_column_width=True)
    except:
        st.markdown("<h1 style='color:#00c6ff; text-align:center;'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    
    st.caption("v86.0 | Sentinel Master Intelligence")
    
    st.divider()
    with st.expander("🚀 Operações Especiais", expanded=True):
        st.toggle("Auto-Healing Pro", value=True)
        st.toggle("Neural Scan", value=True)
        st.toggle("Privacy Shield", value=True)
    
    st.divider()
    agente = st.selectbox("🎯 Intelligence Agente", ["E-Discovery", "Due Diligence", "Compliance", "Finance Audit"])
    if st.button("🔄 Reboot System"):
        st.cache_resource.clear()
        st.rerun()

# --- CONTEÚDO PRINCIPAL (DASHBOARD OMNI) ---
st.markdown("""<div class='status-bar'>AETHER: VIGILANTE | AUTO-HEALING: ATIVO | VARREDURA: LIGADA</div>""", unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("<div class='sentinel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🕹️ Entrada de Missão</div>", unsafe_allow_html=True)
    pergunta = st.text_area("Descreva o objetivo da auditoria ou instrução sniper:", height=300, placeholder="Ex: Analise o contrato anexo e aponte riscos cambiais...")
    
    st.markdown("<div class='section-title'>📂 Ativos de Dados</div>", unsafe_allow_html=True)
    arquivos = st.file_uploader("Upload evidences", accept_multiple_files=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_output:
    st.markdown("<div class='sentinel-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🚀 Resposta do Sentinel</div>", unsafe_allow_html=True)
    
    if st.button("ATIVAR VARREDURA GLOBAL"):
        if (pergunta or arquivos) and model:
            with st.spinner("PROCESSANDO DADOS NEURAIS..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_elite = f"Act as AETHER ELITE ({agente}). MISSION: Audit. INSTRUCTION: {pergunta} CONTEXT: {extra_data}"
                    response = model.generate_content([prompt_elite, *imagens] if imagens else prompt_elite)
                    
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 DOWNLOAD REPORT (.DOCX)", export_docx(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro na Missão: {e}")
        else:
            st.warning("Aguardando entrada de dados para iniciar varredura.")
    st.markdown("</div>", unsafe_allow_html=True)
