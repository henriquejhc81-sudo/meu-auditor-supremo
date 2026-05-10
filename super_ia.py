import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO ---
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

# --- ⚙️ CONFIGURAÇÃO ---
st.set_page_config(page_title="AETHER OMNI v97.0 Ultra", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO PARA TEMPLATES DE IA ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

def set_template(text):
    st.session_state.cmd_input = text

# --- 🎨 DESIGN "CORPORATE TITAN" (CSS v97.0 Ultra - NUCLEAR RED DOT FIX) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    [data-testid="stHeader"] { display: none !important; }
    
    /* Remove a pequena seta do sidebar no canto superior esquerdo */
    [data-testid="collapsedControl"] { display: none !important; }

    /* 🛡️ HEADER UNIT */
    .brand-unit { display: flex; align-items: center; gap: 18px; margin-bottom: -5px; }
    .logo-final {
        width: 80px; height: 80px; border-radius: 50%;
        border: 2px solid #10b981; box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
        cursor: pointer; transition: 0.4s;
    }
    .logo-final:hover { transform: scale(1.05); box-shadow: 0 0 35px rgba(16, 185, 129, 0.4); }
    
    .title-text { 
        font-weight: 900; font-size: 2.5rem; 
        color: #ffffff; letter-spacing: -1px; line-height: 1; margin: 0;
    }
    .subtitle-text { 
        color: #10b981; font-weight: 700; font-size: 0.8rem; 
        text-transform: uppercase; letter-spacing: 3px; margin-top: 4px;
    }

    /* 🛡️ EXTERMÍNIO ABSOLUTO DA BOLINHA DO RADIO (NUCLEAR CSS) */
    div[role="radiogroup"] label > div:first-child { display: none !important; } /* Alvo direto na bolinha */
    div[data-testid="stRadio"] [data-testid="stRadioButton"] div[class*="st-"] { display: none !important; }
    div[data-testid="stRadio"] label svg { display: none !important; }
    div[data-testid="stRadio"] input { display: none !important; }
    
    div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 10px !important; margin-top: 15px !important; }
    div[data-testid="stRadio"] label {
        background-color: #111827 !important; color: #6b7280 !important;
        padding: 10px 20px !important; border-radius: 10px !important;
        border: 1px solid #1f2937 !important; transition: 0.3s;
        justify-content: center;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #10b981 !important; border-color: #10b981 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.3) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p { color: #022c22 !important; font-weight: 800 !important; }

    /* 🛡️ INTAKE MATRIX & UI ELEMENTS */
    .intake-matrix {
        display: flex; gap: 10px; margin-bottom: 5px;
    }
    .intake-slot {
        flex: 1; background-color: #111827; border: 1px solid #1f2937; 
        border-radius: 8px; padding: 10px; text-align: center; font-size: 0.75rem; color: #9ca3af;
    }
    .intake-slot span { display: block; font-weight: bold; color: #d1d5db; margin-bottom: 2px; font-size: 0.9rem;}
    
    /* Ocultar a interface feia do uploader nativo e deixar só a área clicável/arrastável */
    [data-testid="stFileUploadDropzone"] { background-color: transparent !important; border: 1px dashed #1f2937 !important; padding: 10px !important; }
    [data-testid="stFileUploadDropzone"] div { color: #6b7280 !important; font-size: 0.8rem !important; }
    [data-testid="stFileUploadDropzone"] button { display: none !important; } /* Esconde o botão 'Browse files' nativo para ficar mais limpo */

    .card-panel { 
        background-color: #0f172a; padding: 30px; border-radius: 15px; 
        border: 1px solid #1e293b; border-top: 4px solid #10b981;
    }
    
    /* 🛡️ DOSSIER PLACEHOLDER AVANÇADO */
    .dossier-wait {
        border: 1px solid #1e293b; border-radius: 15px; height: 500px; 
        background: linear-gradient(145deg, #0f172a 0%, #030712 100%);
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        position: relative; overflow: hidden;
    }
    .dossier-wait::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background-image: linear-gradient(#10b981 1px, transparent 1px), linear-gradient(90deg, #10b981 1px, transparent 1px);
        background-size: 20px 20px; opacity: 0.03; pointer-events: none;
    }
    .wait-title { color: #10b981; font-weight: 700; letter-spacing: 1px; margin-bottom: 10px; z-index: 1;}
    .wait-sub { color: #4b5563; font-size: 0.9rem; z-index: 1;}
    .metrics-mockup { display: flex; gap: 20px; margin-top: 30px; z-index: 1; opacity: 0.5; }
    .metric-box { width: 80px; height: 60px; background-color: #111827; border-radius: 5px; border: 1px solid #1f2937; }

    /* 🛡️ BOTÕES APRIMORADOS */
    button[kind="primary"] { 
        background: linear-gradient(to right, #10b981, #059669) !important;
        border: none !important; border-radius: 10px !important; font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important;
        transition: 0.3s;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER ---
logo_b64 = get_base64("logo.png")
st.markdown('<div class="brand-unit">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 10])
with c1:
    if logo_b64:
        st.markdown(f'<a href="." target="_self"><img src="data:image/png;base64,{logo_b64}" class="logo-final"></a>', unsafe_allow_html=True)
with c2:
    st.markdown('<div><h1 class="title-text">AETHER OMNI</h1><p class="subtitle-text">Strategic Intelligence Hub</p></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- 🛰️ MENU ---
menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed")

st.write("") # Spacer

# --- 🏗️ ÁREA DE TRABALHO ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.3], gap="large")
    
    with col_l:
        st.markdown("#### 📥 File Intake Matrix")
        
        # UI Visual Mockup para Ingestão
        st.markdown("""
        <div class="intake-matrix">
            <div class="intake-slot"><span>PDF</span>Matrix</div>
            <div class="intake-slot"><span>DOCX</span>Grid</div>
            <div class="intake-slot" style="border-bottom: 2px solid #f59e0b;"><span>XLSX</span>Waiting</div>
            <div class="intake-slot" style="border-bottom: 2px solid #10b981;"><span>CSV</span>Ready</div>
        </div>
        """, unsafe_allow_html=True)
        
        # O uploader agora fica mais sutil abaixo da matriz
        up = st.file_uploader("", type=['pdf', 'docx', 'xlsx', 'csv'], label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=130, placeholder="Descreva sua análise jurídica estratégica...")
        
        # --- NOVOS TEMPLATES DE IA ---
        st.markdown("<span style='color: #10b981; font-weight: bold; font-size: 0.85rem;'>⚡ AI Strategy Templates:</span>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        t1.button("📑 Risk Matrix", use_container_width=True, on_click=set_template, args=("Por favor, analise a matriz de riscos contratuais deste documento, destacando cláusulas de quebra e penalidades.",))
        t2.button("🔍 Forensic Data", use_container_width=True, on_click=set_template, args=("Compile as evidências forenses presentes nos dados, focando em anomalias financeiras e desvios de padrão.",))
        t3.button("⚖️ Compliance", use_container_width=True, on_click=set_template, args=("Verifique a conformidade regulatória deste arquivo com base nas normas jurídicas vigentes aplicáveis.",))
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚖️ PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
            # Lógica aether_brain_supreme...
            pass
            
    with col_r:
        st.markdown("#### 🧠 Dossiê Estratégico")
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='card-panel'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
        else:
            # Novo Placeholder de Dossiê Avançado
            st.markdown("""
            <div class='dossier-wait'>
                <div class='wait-title'>Aguardando Processamento Neural...</div>
                <div class='wait-sub'>O AETHER OMNI está pronto para gerar Relatórios Estratégicos.</div>
                <div class='metrics-mockup'>
                    <div class='metric-box'></div>
                    <div class='metric-box' style='border-radius: 50%; width: 60px;'></div>
                    <div class='metric-box'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
