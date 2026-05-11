import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ BIBLIOTECAS PRESERVADAS ---
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

# --- ⚙️ CONFIGURAÇÃO DE ELITE ---
st.set_page_config(page_title="AETHER KARV Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

if "res_aether" not in st.session_state:
    st.session_state.res_aether = None

# --- 🎨 DESIGN "PRECISION APEX" (FIX DE SINTAXE) ---
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

    .header-master { text-align: center; margin-bottom: 20px; }
    .logo-main {
        width: 80px; height: 80px; border-radius: 50%;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.7);
        border: 2px solid #10b981; margin-bottom: 10px;
    }
    .title-karv { font-weight: 900; font-size: 3.2rem; color: #ffffff; letter-spacing: -1px; margin: 0; }
    .subtitle-karv { color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; }

    div[data-testid="stRadio"] > div { 
        justify-content: center !important; gap: 12px !important; 
        background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 50px; border: 1px solid #1f2937; width: fit-content; margin: 15px auto 30px auto;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #94a3b8 !important; padding: 8px 25px !important; border-radius: 50px !important; transition: 0.4s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 800 !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }

    .operation-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid #1e293b; border-radius: 18px; padding: 20px;
        position: relative; height: 440px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .operation-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: #10b981; }

    [data-testid="stFileUploadDropzone"] { background: rgba(7, 11, 20, 0.5) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; }
    .stTextArea textarea { background: #070b14 !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; border-radius: 10px !important; }

    button[kind="primary"] { 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; color: #020617 !important; font-weight: 900 !important;
        height: 50px !important; margin-top: 10px !important; border: none !important;
    }

    .nexus-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; }
    .scale-icon {
        font-size: 2.5rem; color: #10b981; background: rgba(16, 185, 129, 0.08); 
        width: 100px; height: 100px; display: flex; align-items: center; justify-content: center;
        border-radius: 50%; border: 1px solid #10b981; box-shadow: 0 0 40px rgba(16, 185, 129, 0.3); margin-bottom: 15px;
    }

    .download-pill {
        background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 50px;
        padding: 5px 12px; color: #94a3b8; font-size: 0.75rem; cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 INTERFACE MASTER ---
logo_b64 = get_base64("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-main">' if logo_b64 else '<div class="logo-main"></div>'

st.markdown(f'<div class="header-master">{logo_html}<h1 class="title-karv">AETHER KARV</h1><div class="subtitle-karv">Strategic Intelligence Hub</div></div>', unsafe_allow_html=True)

menu = st.radio("", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<p style="font-weight:800; margin-bottom:10px;">INGESTÃO</p>', unsafe_allow_html=True)
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
    st.markdown('<p style="font-size:0.7rem;color:#64748b;text-align:center;">ARRASTE ARQUIVOS (PDF, DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
    
    cmd = st.text_area("COMANDO JURÍDICO ESTRATÉGICO:", height=130, placeholder="Descreva sua análise estratégica...", label_visibility="visible")
    
    if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
        if cmd:
            with st.status("🧠 Processando...", expanded=False):
                time.sleep(2)
            st.session_state.res_aether = "Análise concluída com sucesso."
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<p style="font-weight:800; margin-bottom:10px;">DOSSIÊ</p>', unsafe_allow_html=True)
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    if st.session_state.res_aether:
        st.write(st.session_state.res_aether)
    else:
        st.markdown('<div class="nexus-center"><div class="scale-icon"><i class="fas fa-balance-scale"></i></div><h3 style="color:white; margin:0;">MOTOR KARV PRONTO</h3><p style="color:#64748b; font-size:0.8rem;">Aguardando ingestão estratégica...</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="position:absolute; bottom:20px; left:0; width:100%; display:flex; justify-content:center; gap:8px;"><div class="download-pill">PDF</div><div class="download-pill">DOCX</div><div class="download-pill">XLSX</div><div class="download-pill">CSV</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
