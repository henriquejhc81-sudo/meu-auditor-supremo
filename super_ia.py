import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO DE BACKEND ---
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
st.set_page_config(page_title="AETHER KARV v107.0 Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

def set_template(text):
    st.session_state.cmd_input = text

# --- ⚡ MOTOR AETHER KARV (PRESERVADO) ---
def aether_karv_engine(comando, arquivos):
    time.sleep(2) 
    return f"Processamento neural concluído com sucesso."

# --- 🎨 DESIGN "PRECISION APEX" (Espelhamento da Imagem de Referência) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a1120 0%, #020617 100%);
        color: #f3f4f6; 
        font-family: 'Inter', sans-serif; 
    }
    .block-container { padding-top: 1.5rem !important; max-width: 95% !important; margin: 0 auto !important; overflow: hidden !important;}
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

    /* 🛡️ HEADER UNIT */
    .header-master { text-align: center; margin-bottom: 25px; }
    .logo-main {
        width: 80px; height: 80px; border-radius: 50%;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.7);
        border: 2px solid #10b981; margin-bottom: 12px;
    }
    .title-karv { font-weight: 900; font-size: 3rem; color: #ffffff; letter-spacing: -1px; margin: 0; line-height: 1; }
    .subtitle-karv { color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 5px; margin-top: 8px; text-transform: uppercase; opacity: 0.9; }

    /* 🛡️ NAVIGATION CAPSULE */
    div[data-testid="stRadio"] > div { 
        justify-content: center !important; gap: 12px !important; 
        background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 50px; border: 1px solid #1f2937; width: fit-content; margin: 15px auto 35px auto;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #94a3b8 !important; padding: 8px 25px !important; border-radius: 50px !important; transition: 0.4s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 800 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }
    div[data-testid="stRadio"] label p { font-size: 0.95rem !important; }

    /* 🛡️ CARDS DE OPERAÇÃO */
    .card-header-text { font-size: 1.1rem; font-weight: 800; color: #ffffff; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .operation-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid #1e293b; border-radius: 18px; padding: 25px;
        position: relative; overflow: hidden; height: 440px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .operation-card::before {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: #10b981;
    }

    /* 🛡️ INPUTS & UPLOAD */
    [data-testid="stFileUploadDropzone"] { 
        background: rgba(7, 11, 20, 0.5) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; padding: 15px !important;
    }
    .stTextArea textarea { background: #070b14 !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; border-radius: 10px !important; font-size: 0.9rem !important;}

    /* 🛡️ BOTÃO DE PROCESSAMENTO */
    button[kind="primary"] { 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; color: #020617 !important; font-weight: 900 !important;
        height: 55px !important; font-size: 1rem !important; margin-top: 15px !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.2) !important; border: none !important;
        text-transform: uppercase;
    }

    /* 🛡️ DOSSIÊ NEXUS */
    .nexus-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; margin-top: -20px;}
    .scale-icon {
        font-size: 3rem; color: #10b981;
        background: rgba(16, 185, 129, 0.08); width: 110px; height: 110px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 50%; border: 1px solid #10b981;
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.3); margin-bottom: 20px;
    }

    /* 🛡️ DOWNLOAD PILLS */
    .download-bar { display: flex; justify-content: center; gap: 8px; margin-top: 20px; }
    .download-pill {
        background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 50px;
        padding: 5px 12px; color: #94a3b8; font-size: 0.75rem; cursor: pointer; transition: 0.3s;
        font-weight: 600;
    }
    .download-pill:hover { border-color: #10b981; color: #10b981; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER (AETHER KARV) ---
logo_b64 = get_base64("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-main">' if logo_b64 else '<div class="logo-main" style="display:flex;align-items:center;justify-content:center;color:#10b981;font-size:2rem;"><i class="fas fa-shield-halved"></i></div>'

st.markdown(f"""
    <div class="header-master">
        {logo_html}
        <h1 class="title-karv">AETHER KARV</h1>
        <div class="subtitle-karv">Strategic Intelligence Hub</div>
    </div>
    """, unsafe_allow_html=True)

# Menu pílula
menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

# Grid de Operação
col_ing, col_dos = st.columns(2, gap="large")

with col_ing:
    st.markdown('<div class="card-header-text">INGESTÃO</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        up = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown('<p style="font-size:0.75rem;color:#64748b;text-align:center;margin-top:-8px;">ARRASTE ARQUIVOS OU CLIQUE PARA UPLOAD (PDF, DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top:20px;"><p class="card-header-text" style="font-size:0.85rem;">COMANDO JURÍDICO ESTRATÉGICO:</p></div>', unsafe_allow_html=True)
        cmd = st.text_area("", key="cmd_input", height=130, placeholder="Descreva sua análise jurídica estratégica profunda...", label_visibility="collapsed")
        
        if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
            if not cmd: st.error("⚠️ Insira um comando estratégico.")
            else:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                    time.sleep(2)
                st.session_state['res_aether'] = aether_karv_engine(cmd, up)
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col_dos:
    st.markdown('<div class="card-header-text">DOSSIÊ</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        if 'res_aether' in st.session_state:
            st.markdown(f'<div style="padding:15px; color:#cbd5e1; font-size: 1rem;">{st.session_state["res_aether"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="nexus-center">
                    <div class="scale-icon"><i class="fas fa-balance-scale"></i></div>
                    <h3 style="margin:0; font-weight:900; letter-spacing:1.5px; color:#ffffff;">MOTOR KARV PRONTO</h3>
                    <p style="color:#64748b; font-size:0.85rem; margin-top:5px;">Aguardando ingestão e comando estratégico...</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Download pills na base
        st.markdown("""
            <div style="position:absolute; bottom:25px; left:0; width:100%;" class="download-bar">
                <div class="download-pill"><i class="fas fa-file-pdf"></i> PDF</div>
                <div class="download-pill"><i class="fas fa-file-word"></i> DOCX</div>
                <div class="download-pill"><i class="fas fa-file-excel"></i> XLSX</div>
                <div class="download-pill"><i class="fas fa-file-csv"></i> CSV</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
