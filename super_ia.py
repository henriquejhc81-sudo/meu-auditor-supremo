import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS ---
try:
    from fpdf import FPDF
    PDF_READY = True
except ImportError:
    PDF_READY = False

try:
    from groq import Groq
    import google.generativeai as genai
    from duckduckgo_search import DDGS
except ImportError:
    pass

try:
    import plotly.graph_objects as go
    PLOTLY_READY = True
except ImportError:
    PLOTLY_READY = False

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="AETHER KARV V105.0 Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# Funções de Base64 para Imagens Locais
def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

def set_template(text):
    st.session_state.cmd_input = text

# --- ⚡ MOTOR AETHER KARV (SIMULAÇÃO PRESERVADA) ---
def aether_karv_engine(comando, arquivos):
    """Lógica simulada do motor neural Karv (Fidelidade v104.0)."""
    time.sleep(2) 
    return f"Processamento neural concluído com sucesso."

# --- 🎨 DESIGN "CYBER APEX CONSOLE" (Espelhamento da Imagem Autorizada) ---
# Carregamos as imagens do seu GitHub para usar no CSS
back_b64 = get_base64_image("back.png")
logo_b64 = get_base64_image("logo.png")

# Se o fundo tático existir, aplicamos ele ao background
bg_css = f"background-image: url('data:image/png;base64,{back_b64}'); background-size: cover; background-position: center;" if back_b64 else "background-color: #020617;"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* 1. O AMBIENTE - CORPORATE TITAN DARK MODE */
    .stApp {{
        {bg_css}
        color: #f3f4f6; font-family: 'Inter', sans-serif;
    }}
    .block-container {{ padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 90% !important; margin: 0 auto !important; overflow: hidden !important;}}
    [data-testid="stHeader"], [data-testid="collapsedControl"] {{ display: none !important; }}

    /* 2. MENU CÁPSULAS CENTRALIZADAS (Design do Print) */
    div[role="radiogroup"] > div > label > div:first-child {{ display: none !important; }}
    
    div[data-testid="stRadio"] > div {{ 
        justify-content: center !important; gap: 12px !important; 
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 5px !important; border-radius: 50px !important; border: 1px solid #1e293b !important;
        width: fit-content !important; margin: 0 auto 35px auto !important;
    }}
    div[data-testid="stRadio"] label {{
        background-color: transparent !important; color: #94a3b8 !important; padding: 10px 25px !important; transition: all 0.4s ease; margin: 0 !important; cursor: pointer;
    }}
    div[data-testid="stRadio"] label:has(input:checked) {{
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 800 !important; border-radius: 50px !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }
    div[data-testid="stRadio"] label p {{ font-size: 1rem !important; font-weight: 600 !important; }}

    /* 3. UPLOADER TÁTICO */
    [data-testid="stFileUploadDropzone"] {{ 
        background-color: rgba(7, 11, 20, 0.6) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; transition: 0.3s;
    }}
    [data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important;}}
    [data-testid="stFileUploadDropzone"] p {{ color: #cbd5e1 !important; }}
    
    /* 4. INPUT AREA */
    .stTextArea label, .stTextArea textarea, .stTextInput input, .stTextInput label {{
        font-family: 'Inter', sans-serif !important;
    }}
    .stTextArea textarea {{
        background-color: #070b14 !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; font-size: 0.9rem !important;
    }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }}

    /* 5. PAINÉIS E BOTÕES TÁTICOS (Glassmorphism) */
    .card-label {{ font-size: 1.1rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .operation-card {{
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid #1e293b; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
        position: relative; overflow: hidden;
    }}
    .operation-card::before {{ content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: #10b981; }}
    
    button[kind="primary"] {{ 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3) !important; text-transform: uppercase; letter-spacing: 1px;
        padding: 15px !important; margin-top: 15px !important; border: none !important; font-size: 1rem !important;
    }}
    button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 15px 35px rgba(16, 185, 129, 0.5) !important; filter: brightness(1.1); }}

    /* 6. TÍTULO CENTRALIZADO COM GLOW */
    .header-container {{ text-align: center; margin-bottom: 25px; display: flex; flex-direction: column; align-items: center; }}
    .logo-glow {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 35px rgba(16,185,129,0.8); margin-bottom: 12px; border: 2px solid rgba(16,185,129,0.3); }}
    .karv-title {{ margin: 0; font-weight: 900; font-size: 3rem; color: #ffffff; letter-spacing: -2px; }}
    .karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 1.1rem; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px; }}
    
    /* 7. DOSSIÊ NEXUS (Placeholder) */
    .nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 320px; text-align: center; }}
    .scale-icon {{ font-size: 4rem; color: #10b981; background: rgba(16, 185, 129, 0.1); width: 120px; height: 120px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #10b981; box-shadow: 0 0 50px rgba(16, 185, 129, 0.5); margin-bottom: 20px; }}

    /* 8. DOWNLOAD PILLS */
    .download-bar {{ display: flex; justify-content: center; gap: 8px; margin-top: 20px; }}
    .download-pill {{ background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 50px; padding: 6px 14px; color: #cbd5e1; font-size: 0.8rem; cursor: pointer; transition: 0.3s; font-weight: 600; }}
    .download-pill:hover {{ border-color: #10b981; color: #10b981; background: rgba(16, 185, 129, 0.05); }}
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER CENTRALIZADO (ESTILO CONSOLE APEX) ---
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-glow">' if logo_b64 else '<div class="logo-glow" style="display:flex;align-items:center;justify-content:center;color:#10b981;font-size:2.5rem;"><i class="fas fa-shield-halved"></i></div>'

header_html = f"""
<div class="header-container">
    {logo_html}
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

# Grid de Operação
col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    st.markdown('<div class="card-label">INGESTÃO</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        up = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown('<p style="font-size:0.8rem;color:#64748b;text-align:center;margin-top:-10px;">ARRRASTE ARQUIVOS OU CLIQUE PARA UPLOAD (PDF, DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top:25px;"><p class="card-label" style="font-size:0.9rem;">COMANDO JURÍDICO ESTRATÉGICO:</p></div>', unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=130, placeholder="Descreva sua análise jurídica estratégica profunda...")

        if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
            if cmd:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                    time.sleep(2)
                st.session_state['res_aether'] = f"Processamento neural simulado concluído."
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col_dos:
    st.markdown('<div class="card-label">DOSSIÊ</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        if 'res_aether' in st.session_state:
            st.markdown(f"<div style='color:#e2e8f0; font-size:1.1rem; padding:15px;'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="nexus-center">
                <div class="scale-icon"><i class="fas fa-balance-scale"></i></div>
                <h3 style="margin:0; font-weight:900; color:white; letter-spacing:1px;">MOTOR KARV PRONTO</h3>
                <p style="color:#64748b; font-size:1rem; margin-top:5px;">Aguardando ingestão estratégica...</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="download-bar">
            <div class="download-pill"><i class="fas fa-file-pdf"></i> PDF Matrix</div>
            <div class="download-pill"><i class="fas fa-file-word"></i> DOCX Grid</div>
            <div class="download-pill"><i class="fas fa-file-excel"></i> XLSX Map</div>
            <div class="download-pill"><i class="fas fa-file-csv"></i> CSV Table</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
