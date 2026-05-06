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

# --- UI DESIGN (NEXUS SENTINEL STYLE + LOGO INTEGRATION) ---
st.set_page_config(page_title="AETHER OMNI v85.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Dependências ausentes no servidor. Verifique o requirements.txt.")
    st.stop()

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background-color: #05070a !important; color: #e1e1e1 !important; }
    
    /* BARRA DE STATUS (INSPIRADA NO NEXUS SENTINEL) */
    .status-bar {
        background: rgba(0, 198, 255, 0.05);
        border: 1px solid rgba(0, 198, 255, 0.2);
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8em;
        letter-spacing: 2px;
        color: #00c6ff;
        margin-bottom: 30px;
    }

    /* TÍTULOS E SEÇÕES */
    .section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 700; color: #ffffff; display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }
    
    /* INPUTS DARK */
    .stTextArea textarea { background-color: #0a0c10 !important; border: 1px solid #14181f !important; color: #f1f5f9 !important; border-radius: 12px !important; }
    .stFileUploader section { background-color: #0a0c10 !important; border: 1px dashed #1e293b !important; border-radius: 12px !important; }

    /* BOTÃO ATIVAR (GRADIENTE NEXUS) */
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%) !important;
        color: white !important; border: none !important; border-radius: 10px;
        font-weight: 700; height: 3.8em; text-transform: uppercase; letter-spacing: 1px;
        transition: 0.4s all;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 198, 255, 0.4); }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] { background-color: #010203 !important; border-right: 1px solid #14181f; }
    
    /* CARD DE RESULTADO */
    .report-card { background: #0a0c10; padding: 30px; border-radius: 15px; border: 1px solid #14181f; line-height: 1.8; color: #d1d5db; }
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
    # INTEGRAÇÃO DO LOGO (Conforme imagem do GitHub)
    try:
        st.image("logo.png.jpeg", use_column_width=True)
    except:
        st.markdown("<h1 style='color:white;'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    
    st.caption("v85.0 | Elite Intelligence")
    
    st.divider()
    with st.expander("🚀 Superpoderes Aether", expanded=True):
        st.toggle("Segurança Nativa", value=True)
        st.toggle("Auto-Healing Ativo", value=True)
        st.toggle("Deep Scanning", value=True)
    
    st.divider()
    agente = st.selectbox("🎯 Estratégia", ["E-Discovery", "Due Diligence", "Compliance", "Finance Audit"])
    if st.button("🔄 Reiniciar Motor"):
        st.cache_resource.clear()
        st.rerun()

# --- CONTEÚDO PRINCIPAL (DASHBOARD OMNI) ---
st.markdown("""<div class='status-bar'>AETHER: VIGILANTE | AUTO-HEALING: ATIVO | VARREDURA: LIGADA</div>""", unsafe_allow_html=True)

col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    st.markdown("<div class='section-title'>🕹️ Entrada de Missão</div>", unsafe_allow_html=True)
    pergunta = st.text_area("Instrução ou Sniper Prompt:", height=250, placeholder="Ex: Analise riscos no contrato anexo...")
    
    st.markdown("<div class='section-title'>📂 Ativos Adicionais</div>", unsafe_allow_html=True)
    arquivos = st.file_uploader("Upload evidences", accept_multiple_files=True)

with col_output:
    st.markdown("<div class='section-title'>🚀 Resposta do Sentinel</div>", unsafe_allow_html=True)
    
    if st.button("ATIVAR AETHER OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner("PROCESSANDO VARREDURA GLOBAL..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_elite = f"Atue como AETHER ELITE ({agente}). MISSÃO: Auditoria. INSTRUÇÃO: {pergunta} CONTEXTO: {extra_data}"
                    response = model.generate_content([prompt_elite, *imagens] if imagens else prompt_elite)
                    
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Exportar Relatório (.DOCX)", export_docx(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro na Varredura: {e}")
        else:
            st.warning("Verifique a Chave API e as instruções.")
