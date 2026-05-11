import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO DE FUNÇÕES ---
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
st.set_page_config(page_title="AETHER KARV Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

if "res_aether" not in st.session_state:
    st.session_state.res_aether = None

# --- 🎨 DESIGN "CYBER APEX" (FIX DE SINTAXE) ---
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { 
        background: radial-gradient(circle at center, #0a1120 0%, #020617 100%);
        color: #f3f4f6; font-family: 'Inter', sans-serif; 
    }
    .block-container { padding-top: 1rem !important; max-width: 95% !important; margin: 0 auto !important; overflow: hidden !important;}
    [data-testid="stHeader"], [data-testid="stSidebar"] { display: none !important; }

    .header-master { text-align: center; margin-bottom: 25px; }
    .logo-main {
        width: 85px; height: 85px; border-radius: 50%;
        box-shadow: 0 0 45px rgba(16, 185, 129, 0.8);
        border: 2px solid #10b981; margin-bottom: 12px;
    }
    .title-karv { font-weight: 900; font-size: 3.5rem; color: #ffffff; letter-spacing: -2px; margin: 0; line-height: 1; }
    .subtitle-karv { color: #10b981; font-weight: 700; font-size: 1.1rem; letter-spacing: 5px; margin-top: 10px; text-transform: uppercase; }

    div[data-testid="stRadio"] > div { 
        justify-content: center !important; gap: 15px !important; 
        background: rgba(15, 23, 42, 0.7); padding: 10px; border-radius: 50px; border: 1px solid #1f2937; width: fit-content; margin: 15px auto 40px auto;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #94a3b8 !important; padding: 10px 30px !important; border-radius: 50px !important; transition: 0.4s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.7) !important;
    }

    .card-header-text { font-size: 1.2rem; font-weight: 900; color: #ffffff; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 2px; }
    .operation-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid #1e293b; border-radius: 20px; padding: 25px;
        position: relative; overflow: hidden; height: 460px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    }
    .operation-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #10b981; }

    [data-testid="stFileUploadDropzone"] { background: rgba(7, 11, 20, 0.6) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; }
    .stTextArea textarea { background: #070b14 !important; border: 1px solid #1e293b !important; color: #e2e8f0 !important; border-radius: 10px !important; }

    button[kind="primary"] { 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; color: #020617 !important; font-weight: 900 !important;
        height: 60px !important; margin-top: 20px !important; border: none !important;
        text-transform: uppercase; letter-spacing: 1px;
    }

    .nexus-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center;}
    .scale-icon {
        font-size: 4rem; color: #10b981;
        background: rgba(16, 185, 129, 0.1); width: 130px; height: 130px;
        display: flex; align-items: center; justify-content: center;
        border-radius: 50%; border: 2px solid #10b981;
        box-shadow: 0 0 60px rgba(16, 185, 129, 0.5); margin-bottom: 25px;
    }

    .download-pill {
        background: rgba(30, 41, 59, 0.7); border: 1px solid #334155; border-radius: 50px;
        padding: 8px 18px; color: #cbd5e1; font-size: 0.8rem; cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 RENDER DA INTERFACE ---
logo_b64 = get_base64("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-main">' if logo_b64 else '<div class="logo-main" style="display:flex;align-items:center;justify-content:center;color:#10b981;font-size:2.5rem;"><i class="fas fa-shield-halved"></i></div>'

st.markdown(f'<div class="header-master">{logo_html}<h1 class="title-karv">AETHER KARV</h1><div class="subtitle-karv">Strategic Intelligence Hub</div></div>', unsafe_allow_html=True)

menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="card-header-text">INGESTÃO</div>', unsafe_allow_html=True)
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    up = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
    st.markdown('<p style="font-size:0.8rem;color:#64748b;text-align:center;">ARRASTE ARQUIVOS (PDF, DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top:25px;"><p class="card-header-text" style="font-size:0.9rem;">COMANDO JURÍDICO ESTRATÉGICO:</p></div>', unsafe_allow_html=True)
    cmd = st.text_area("", key="cmd_input", height=130, placeholder="Descreva sua análise estratégica profunda...", label_visibility="collapsed")
    
    if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
        if cmd:
            with st.status("🧠 Inicializando Motores Neurais...", expanded=False):
                time.sleep(2)
            st.session_state.res_aether = f"Análise estratégica processada para: {cmd}"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card-header-text">DOSSIÊ</div>', unsafe_allow_html=True)
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    if st.session_state.res_aether:
        st.markdown(f'<div style="padding:15px; color:#e2e8f0; font-size:1.1rem;">{st.session_state.res_aether}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="nexus-center">
                <div class="scale-icon"><i class="fas fa-balance-scale"></i></div>
                <h3 style="margin:0; font-weight:900; color:white;">MOTOR KARV PRONTO</h3>
                <p style="color:#64748b; font-size:0.9rem;">Aguardando ingestão e comando estratégico...</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="position:absolute; bottom:25px; left:0; width:100%; display:flex; justify-content:center; gap:10px;">
            <div class="download-pill">PDF Matrix</div>
            <div class="download-pill">DOCX Grid</div>
            <div class="download-pill">XLSX Map</div>
            <div class="download-pill">CSV Table</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
