import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: MOTORES ---
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
    st.stop()

# --- ⚙️ CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="AETHER OMNI v93.18", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🎨 DESIGN "INTEGRATED DASHBOARD" (CSS v93.18) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@700&display=swap');
    
    /* 1. Reset Total de Espaço Superior */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }

    /* 2. Cabeçalho Integrado (Logo + Título) */
    .top-bar {
        display: flex;
        align-items: center;
        gap: 25px;
        margin-bottom: 5px;
    }
    
    .logo-img {
        width: 80px; height: 80px;
        border-radius: 50%;
        border: 2px solid #00c853;
        box-shadow: 0px 0px 15px rgba(0, 200, 83, 0.3);
        cursor: pointer;
        transition: 0.3s;
    }
    .logo-img:hover { transform: scale(1.05); }

    .main-title { 
        font-family: 'Playfair Display', serif; 
        font-size: 2.2rem; 
        color: #00c853; 
        margin: 0; 
        line-height: 1;
    }
    .main-subtitle { color: #888; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 2px;}

    /* 3. Navegação Abaixo do Título (Sem pontos vermelhos) */
    div[data-testid="stRadio"] > div { 
        display: flex !important; 
        flex-direction: row !important; 
        gap: 15px !important; 
        margin-top: 15px !important;
        margin-bottom: 20px !important;
    }
    
    div[data-testid="stRadio"] [data-testid="stRadioButton"] { display: none !important; }
    
    div[data-testid="stRadio"] label {
        background-color: #0a192f !important;
        color: #888 !important;
        padding: 8px 20px !important;
        border-radius: 6px !important;
        border: 1px solid #112240 !important;
        transition: 0.3s !important;
        cursor: pointer !important;
    }

    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #00c853 !important;
        color: #050a14 !important;
        border-color: #00c853 !important;
        box-shadow: 0px 0px 15px rgba(0, 200, 83, 0.4) !important;
    }
    
    div[data-testid="stRadio"] label:has(input:checked) p { color: #050a14 !important; font-weight: bold !important; }

    /* 4. Blocos de Conteúdo */
    .dossie-box { background-color: #0a192f; padding: 30px; border-radius: 12px; border: 1px solid #112240; border-top: 4px solid #00c853; }
    button[kind="primary"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold !important; height: 3.2em !important; }
    
    /* Remove linhas divisórias nativas que sobraram */
    hr { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER INTEGRADO v93.18 ---
logo_b64 = get_base64("logo.png")
header_col1, header_col2 = st.columns([1, 8])

with header_col1:
    if logo_b64:
        st.markdown(f"""
            <a href="." target="_self">
                <img src="data:image/png;base64,{logo_b64}" class="logo-img" title="System Reset">
            </a>
        """, unsafe_allow_html=True)

with header_col2:
    st.markdown("""
        <div>
            <h1 class="main-title">AETHER OMNI</h1>
            <p class="main-subtitle">Auditoria Estratégica Jurídica</p>
        </div>
    """, unsafe_allow_html=True)

# --- 🛰️ NAVEGAÇÃO (Abaixo do Título) ---
menu = st.radio(
    "Nav",
    ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"],
    index=0,
    label_visibility="collapsed"
)

# --- 🏗️ ÁREA DE TRABALHO UNIFICADA ---
if menu == "🛡️ Auditoria":
    c1, c2 = st.columns([1, 1.3], gap="medium")
    
    with c1:
        st.markdown("### 📄 Ingestão")
        up = st.file_uploader("Subir Documento", type=['pdf', 'docx', 'xlsx', 'csv'], label_visibility="collapsed")
        cmd = st.text_area("Comando:", height=180, placeholder="Ex: Analise riscos contratuais...")
        
        if st.button("🚀 EXECUTAR ANÁLISE", type="primary", use_container_width=True):
            if cmd:
                with st.spinner("AETHER processando..."):
                    # Aqui roda sua lógica aether_brain_supreme original
                    pass
            else: st.warning("Insira um comando.")

    with c2:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            cx1, cx2 = st.columns(2)
            with cx1: st.download_button("📄 PDF", data=export_pdf(st.session_state['res_aether']), file_name="AETHER.pdf", use_container_width=True)
            with cx2: st.download_button("📝 WORD", data=export_docx(st.session_state['res_aether']), file_name="AETHER.docx", use_container_width=True)
        else:
            st.markdown("<div style='border: 2px dashed #112240; border-radius: 12px; height: 400px; display: flex; align-items: center; justify-content: center; color: #444;'>Dossiê Estratégico</div>", unsafe_allow_html=True)

# Mantenha as funções técnicas (export_pdf, export_docx, aether_brain_supreme) no final.
