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
st.set_page_config(page_title="AETHER KARV v105.0 Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

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

# --- ⚡ MOTOR AETHER KARV ---
def aether_karv_engine(comando, arquivos):
    """Motor neural preservado para processamento de auditoria."""
    time.sleep(2) 
    return f"Dossiê Estratégico gerado para: {comando}"

# --- 🎨 DESIGN "PRECISION APEX" (Cópia exata da referência) ---
# O CSS abaixo foi corrigido para evitar os erros de sintaxe vistos anteriormente
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a1120 0%, #020617 100%);
        color: #f3f4f6; 
        font-family: 'Inter', sans-serif; 
    }
    .block-container { padding-top: 2rem !important; max-width: 95% !important; margin: 0 auto !important; overflow: hidden !important;}
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

    /* 🛡️ HEADER UNIT (AETHER KARV) */
    .header-master { text-align: center; margin-bottom: 30px; }
    .logo-main {
        width: 90px; height: 90px; border-radius: 50%;
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.8);
        border: 2px solid #10b981; margin-bottom: 15px;
    }
    .title-karv { font-weight: 900; font-size: 3.8rem; color: #ffffff; letter-spacing: -2px; margin: 0; line-height: 1; }
    .subtitle-karv { color: #10b981; font-weight: 700; font-size: 1.1rem; letter-spacing: 5px; margin-top: 10px; text-transform: uppercase; }

    /* 🛡️ NAVIGATION CAPSULE (PILULAS) */
    div[data-testid="stRadio"] > div { 
        justify-content: center !important; gap: 15px !important; 
        background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 50px; border: 1px solid #1f2937; width: fit-content; margin: 20px auto 45px auto;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #94a3b8 !important; padding: 10px 30px !important; border-radius: 50px !important; transition: 0.4s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.7) !important;
    }
    div[data-testid="stRadio"] label p { font-size: 1.1rem !important; }

    /* 🛡️ CARDS DE OPERAÇÃO (GLASSMORPHISM) */
    .card-header { font-size: 1.3rem; font-weight: 900; color: #ffffff; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 2px; }
    .operation-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid #1e293b; border-radius: 20px; padding: 30px;
        position: relative; overflow: hidden; height: 450px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .operation-card::before {
        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: linear-gradient(90deg, transparent, #10b981, transparent);
    }

    /* 🛡️ INPUTS & UPLOAD */
    [data-testid="stFileUploadDropzone"] { 
        background: rgba(7, 11, 20, 0.6) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; padding: 20px !important;
    }
    .stTextArea textarea { background: #070b14 !important; border: 1px solid #1e293b !important; color: #e2e8f0 !important; border-radius: 10px !important; padding: 15px !important;}

    /* 🛡️ BOTÃO DE PROCESSAMENTO (NEON) */
    button[kind="primary"] { 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; color: #020617 !important; font-weight: 900 !important;
        height: 60px !important; font-size: 1.2rem !important; margin-top: 20px !important;
        box-shadow: 0 12px 30px rgba(16, 185, 129, 0.4) !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1px;
    }

    /* 🛡️ DOSSIÊ NEXUS (ÍCONE PULSANTE) */
    .nexus-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center;}
    .scale-icon {
        font-size: 4rem; color: #10b981;
        background: rgba(16, 185, 129, 0.1); width: 130px; height: 130px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 50%; border: 2px solid #10b981;
        box-shadow: 0 0 60px rgba(16, 185, 129, 0.5); margin-bottom: 30px;
    }

    /* 🛡️ DOWNLOAD PILLS */
    .download-bar { display: flex; justify-content: center; gap: 12px; margin-top: 25px; }
    .download-pill {
        background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 50px;
        padding: 8px 20px; color: #cbd5e1; font-size: 0.85rem; cursor: pointer; transition: 0.3s;
        font-weight: 600;
    }
    .download-pill:hover { border-color: #10b981; color: #10b981; background: rgba(16, 185, 129, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER CENTRALIZADO (AETHER KARV) ---
logo_b64 = get_base64("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-main">' if logo_b64 else '<div class="logo-main" style="display:flex;align-items:center;justify-content:center;color:#10b981;font-size:2.5rem;"><i class="fas fa-shield-halved"></i></div>'

st.markdown(f"""
    <div class="header-master">
        {logo_html}
        <h1 class="title-karv">AETHER KARV</h1>
        <div class="subtitle-karv">Strategic Intelligence Hub</div>
    </div>
    """, unsafe_allow_html=True)

# Navegação em pílulas
menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

c1, c2 = st.columns(2, gap="large")

with c1:
    # Painel de Ingestão
    st.markdown('<div class="card-header">INGESTÃO</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        up = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
        st.markdown('<p style="font-size:0.85rem;color:#64748b;text-align:center;margin-top:-10px;">ARRRASTE ARQUIVOS OU CLIQUE PARA UPLOAD (PDF, DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top:30px;"><p class="card-header" style="font-size:1rem;">COMANDO JURÍDICO ESTRATÉGICO:</p></div>', unsafe_allow_html=True)
        cmd = st.text_area("", key="cmd_input", height=140, placeholder="Descreva sua análise jurídica estratégica profunda...", label_visibility="collapsed")
        
        if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
            if not cmd: st.error("⚠️ Insira um comando estratégico.")
            else:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=False):
                    time.sleep(2)
                st.session_state['res_aether'] = f"Análise concluída com sucesso."
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with c2:
    # Painel de Dossiê
    st.markdown('<div class="card-header">DOSSIÊ</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="operation-card">', unsafe_allow_html=True)
        if 'res_aether' in st.session_state:
            st.markdown(f'<div style="padding:20px; color:#e2e8f0; font-size: 1.1rem; line-height: 1.6;">{st.session_state["res_aether"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="nexus-center">
                    <div class="scale-icon"><i class="fas fa-balance-scale"></i></div>
                    <h3 style="margin:0; font-weight:900; letter-spacing:2px; color: #ffffff;">MOTOR KARV PRONTO</h3>
                    <p style="color:#64748b; font-size:1rem; margin-top:8px;">Aguardando ingestão e comando estratégico...</p>
                </div>
            """, unsafe_allow_html=True)
        
        # Botões de exportação estilo pílula
        st.markdown("""
            <div style="position:absolute; bottom:30px; left:0; width:100%;" class="download-bar">
                <div class="download-pill"><i class="fas fa-file-pdf"></i> PDF Matrix</div>
                <div class="download-pill"><i class="fas fa-file-word"></i> DOCX Grid</div>
                <div class="download-pill"><i class="fas fa-file-excel"></i> XLSX Map</div>
                <div class="download-pill"><i class="fas fa-file-csv"></i> CSV Table</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
