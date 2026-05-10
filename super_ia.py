import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & NOVAS LIBS ---
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

# --- ⚙️ CONFIGURAÇÃO ---
st.set_page_config(page_title="AETHER OMNI v100.0 Ultra Master", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO & FUNÇÕES PRESERVADAS ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

def set_template(text):
    st.session_state.cmd_input = text

# --- 🎨 DESIGN "MINIMALIST MASTER" (Blindado) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 90% !important;}
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* 🛡️ BLINDAGEM DO MENU LATERAL ESQUERDO */
    [data-testid="stSidebar"] { display: none !important; }

    /* 🛡️ EXTERMÍNIO DEFINITIVO DO PONTO VERMELHO NO RADIO */
    div[role="radiogroup"] > div > label > div:first-child { display: none !important; }
    
    div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 15px !important; }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #6b7280 !important;
        padding: 10px 20px !important; border-radius: 8px !important;
        border: 1px solid #1f2937 !important; transition: 0.3s; margin: 0 !important;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: rgba(16, 185, 129, 0.1) !important; border-color: #10b981 !important;
        box-shadow: inset 0 0 10px rgba(16, 185, 129, 0.2) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p { color: #10b981 !important; font-weight: 800 !important; text-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }

    /* ☁️ UPLOADER UNIVERSAL LIMPO */
    [data-testid="stFileUploadDropzone"] { 
        background-color: rgba(17, 24, 39, 0.4) !important; border: 1px dashed #374151 !important; 
        padding: 30px !important; border-radius: 12px !important; transition: 0.3s;
    }
    [data-testid="stFileUploadDropzone"]:hover { border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important;}
    [data-testid="stFileUploadDropzone"] div { color: #9ca3af !important; }
    [data-testid="stFileUploadDropzone"] button { display: none !important; }

    .card-panel { background-color: #0f172a; padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-top: 3px solid #10b981; }
    
    button[kind="primary"] { 
        background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
        border: none !important; border-radius: 8px !important; font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important; text-transform: uppercase; letter-spacing: 1px;
        padding: 15px !important; margin-top: 10px !important;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER SOLDADO (HTML/CSS Direto para não quebrar) ---
logo_b64 = get_base64("logo.png")
logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width: 75px; height: 75px; border-radius: 50%; object-fit: cover;">' if logo_b64 else ''

# Container pai em Flexbox: Alinha tudo perfeitamente na horizontal
header_html = f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px;">
    <div style="display: flex; align-items: center; gap: 20px;">
        {logo_img}
        <div style="display: flex; flex-direction: column;">
            <h1 style="margin: 0; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 2.4rem; color: #ffffff; line-height: 1; letter-spacing: -1px;">AETHER OMNI</h1>
            <span style="color: #10b981; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.85rem; letter-spacing: 3px; margin-top: 4px;">INTELLIGENCE HUB</span>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# Colocamos o menu do Streamlit logo abaixo do cabeçalho, centralizado ou alinhado à esquerda
menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed", horizontal=True)
st.markdown("<br>", unsafe_allow_html=True) 

# --- 🏗️ ÁREA DE TRABALHO ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.2], gap="large")
    
    with col_l:
        # Uploader universal (Limpo)
        up = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=150, placeholder="Descreva sua análise estratégica...")
        
        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            # --- EFEITO DE PROCESSAMENTO NEURAL PARA VENDAS ---
            with st.status("🧠 Inicializando Motores Neurais AETHER...", expanded=True) as status:
                st.write("Ingerindo dados estruturados...")
                time.sleep(1)
                st.write("Executando varredura profunda...")
                time.sleep(1)
                st.write("Compilando Dossiê...")
                time.sleep(1)
                status.update(label="Auditoria Concluída com Sucesso!", state="complete", expanded=False)
            
            # Simulador para teste visual (Substitua pela sua IA real)
            st.session_state['res_aether'] = """
            <h3 style='color: #10b981; margin-top:0;'>Resultado da Auditoria Neural</h3>
            <p style='color: #d1d5db; font-size: 0.95rem; line-height: 1.6;'>
            O processamento estratégico foi finalizado. Foram detectadas anomalias críticas e validações completas na estrutura submetida.
            </p>
            """
            st.rerun() 
            
    with col_r:
        if 'res_aether' in st.session_state:
            # 1. Dossiê
            st.markdown(f"<div class='card-panel'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            
            # 2. Botões Exportar
            st.markdown("<h5 style='color:#10b981; font-size: 0.9rem; margin-top: 10px;'>📥 Exportar Dados (Matrix)</h5>", unsafe_allow_html=True)
            d1, d2, d3, d4 = st.columns(4)
            d1.download_button("☁️ PDF", "mock pdf", file_name="aether.pdf", use_container_width=True)
            d2.download_button("📄 DOCX", "mock docx", file_name="aether.docx", use_container_width=True)
            d3.download_button("📊 XLSX", "mock xlsx", file_name="aether.xlsx", use_container_width=True)
            d4.download_button("📋 CSV", "mock csv", file_name="aether.csv", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3. Gráficos Plotly
            if PLOTLY_READY:
                st.markdown("<h5 style='color:#10b981; font-size: 0.9rem;'>Telemetria Estratégica</h5>", unsafe_allow_html=True)
                pc1, pc2 = st.columns(2)
                with pc1:
                    fig_donut = go.Figure(data=[go.Pie(labels=['Validados', 'Anomalias', 'Avisos', 'Dados Base'], values=[40, 10, 20, 30], hole=.7)])
                    fig_donut.update_traces(marker=dict(colors=['#10b981', '#ef4444', '#f59e0b', '#1f2937']), showlegend=False, textinfo='percent')
                    fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180)
                    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
                with pc2:
                    x_data = list(range(50))
                    y_data = [100 - (i * 2) + np.random.normal(0, 3) for i in x_data]
                    fig_line = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color='#10b981', width=2)))
                    fig_line.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=True, gridcolor='#1f2937'))
                    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        else:
            # Nexus Minimalista
            st.markdown("""
            <div style='border: 1px dashed #1f2937; border-radius: 12px; height: 350px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #374151; background-color: rgba(15, 23, 42, 0.2); margin-top: 10px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>⚖️</div>
                <div style='font-weight: 600; letter-spacing: 1px;'>SISTEMA PRONTO</div>
                <div style='font-size: 0.85rem; margin-top: 5px;'>Aguardando ingestão e comando.</div>
            </div>
            """, unsafe_allow_html=True)
