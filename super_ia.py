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
st.set_page_config(page_title="AETHER OMNI v99.0 Master", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO & FUNÇÕES PRESERVADAS ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""

# Função preservada (ativa no backend para os templates de IA)
def set_template(text):
    st.session_state.cmd_input = text

# --- 🎨 DESIGN "MINIMALIST MASTER" (Limpeza Visual Extrema) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 90% !important;}
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* 🛡️ HEADER UNIT - Limpo (Sem borda oval) */
    .logo-final {
        width: 75px; height: 75px; border-radius: 50%;
        cursor: pointer; transition: 0.4s; margin-top: 0px;
    }
    .logo-final:hover { transform: scale(1.02); filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.4)); }
    
    .title-text { font-weight: 900; font-size: 2.2rem; color: #ffffff; letter-spacing: -1px; line-height: 1; margin: 0; }
    .subtitle-text { color: #10b981; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 2px; }

    /* 🛡️ MENU UNIFICADO */
    div[role="radiogroup"] label > div:first-child { display: none !important; } 
    div[data-testid="stRadio"] [data-testid="stRadioButton"] div[class*="st-"] { display: none !important; }
    div[data-testid="stRadio"] label svg { display: none !important; }
    div[data-testid="stRadio"] input { display: none !important; }
    
    div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 10px !important; margin-top: 10px !important;}
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #6b7280 !important;
        padding: 8px 16px !important; border-radius: 8px !important;
        border: 1px solid #1f2937 !important; transition: 0.3s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: rgba(16, 185, 129, 0.1) !important; border-color: #10b981 !important;
        box-shadow: inset 0 0 10px rgba(16, 185, 129, 0.2) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p { color: #10b981 !important; font-weight: 800 !important; }

    /* ☁️ UPLOADER LIMPO */
    [data-testid="stFileUploadDropzone"] { background-color: rgba(17, 24, 39, 0.3) !important; border: 1px dashed #374151 !important; padding: 25px !important; border-radius: 10px !important; transition: 0.3s;}
    [data-testid="stFileUploadDropzone"]:hover { border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important;}
    [data-testid="stFileUploadDropzone"] div { color: #9ca3af !important; }
    [data-testid="stFileUploadDropzone"] button { display: none !important; }

    .card-panel { background-color: #0f172a; padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-top: 3px solid #10b981; margin-bottom: 20px;}
    
    button[kind="primary"] { 
        background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
        border: none !important; border-radius: 8px !important; font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important; text-transform: uppercase; letter-spacing: 1px;
        padding: 12px !important;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important; }
    
    /* Botões Secundários (Download) */
    button[kind="secondary"] {
        border: 1px solid #374151 !important; background-color: rgba(17, 24, 39, 0.5) !important; color: #9ca3af !important;
        border-radius: 6px !important; transition: 0.3s;
    }
    button[kind="secondary"]:hover { border-color: #10b981 !important; color: #10b981 !important; background-color: #0f172a !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER UNIFICADO ---
logo_b64 = get_base64("logo.png")
c_logo, c_title, c_menu = st.columns([0.5, 2.5, 7], gap="small")

with c_logo:
    if logo_b64:
        st.markdown(f'<a href="." target="_self"><img src="data:image/png;base64,{logo_b64}" class="logo-final"></a>', unsafe_allow_html=True)
with c_title:
    st.markdown('<div style="margin-top: 12px;"><h1 class="title-text">AETHER OMNI</h1><p class="subtitle-text">Intelligence Hub</p></div>', unsafe_allow_html=True)
with c_menu:
    menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed", horizontal=True)

st.markdown("<br>", unsafe_allow_html=True) 

# --- 🏗️ ÁREA DE TRABALHO ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.2], gap="large")
    
    with col_l:
        # Uploader universal (Aceita qualquer arquivo, inclusive vídeos)
        up = st.file_uploader("", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=150, placeholder="Descreva sua análise jurídica estratégica...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            # Lógica aether_brain_supreme...
            # st.session_state['res_aether'] = "Relatório Dossiê Exemplo gerado!" # Descomente para testar a aparição
            pass
            
    with col_r:
        if 'res_aether' in st.session_state:
            # 1. Exibe o Dossiê
            st.markdown(f"<div class='card-panel'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            
            # 2. Exibe os Botões de Download Matrix APENAS após gerar o relatório
            st.markdown("<h5 style='color:#10b981; font-size: 0.9rem; margin-top: 10px;'>📥 Exportar Dossiê Matrix</h5>", unsafe_allow_html=True)
            d1, d2, d3, d4 = st.columns(4)
            d1.download_button("☁️ PDF", "dados mock pdf", file_name="aether_dossie.pdf", use_container_width=True)
            d2.download_button("📄 DOCX", "dados mock docx", file_name="aether_dossie.docx", use_container_width=True)
            d3.download_button("📊 XLSX", "dados mock xlsx", file_name="aether_dossie.xlsx", use_container_width=True)
            d4.download_button("📋 CSV", "dados mock csv", file_name="aether_dossie.csv", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3. Exibe os Gráficos de Inteligência APENAS no relatório gerado
            if PLOTLY_READY:
                st.markdown("<h5 style='color:#10b981; font-size: 0.9rem;'>Métricas de Inteligência Estratégica</h5>", unsafe_allow_html=True)
                pc1, pc2 = st.columns(2)
                with pc1:
                    fig_donut = go.Figure(data=[go.Pie(labels=['Arquivos Base', 'Insights Gerados', 'Anomalias', 'Validações'], values=[30, 40, 10, 20], hole=.7)])
                    fig_donut.update_traces(marker=dict(colors=['#1f2937', '#10b981', '#059669', '#374151']), showlegend=False, textinfo='percent')
                    fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180)
                    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
                with pc2:
                    x_data = list(range(50))
                    y_data = [100 - (i * 2) + np.random.normal(0, 3) for i in x_data]
                    fig_line = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color='#10b981', width=2)))
                    fig_line.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=180, xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=True, gridcolor='#1f2937'))
                    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        else:
            # Estado Inicial Clean/Minimalista
            st.markdown("""
            <div style='height: 300px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #4b5563; border: 1px dashed #1f2937; border-radius: 12px; background-color: rgba(15, 23, 42, 0.2);'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>⚖️</div>
                <div style='font-weight: 600; letter-spacing: 1px;'>SISTEMA PRONTO</div>
                <div style='font-size: 0.85rem; margin-top: 5px;'>Aguardando ingestão de dados e comando.</div>
            </div>
            """, unsafe_allow_html=True)
