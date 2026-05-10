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
    pass # Removido o st.stop() temporariamente para você testar a interface mesmo sem as chaves

try:
    import plotly.graph_objects as go
    PLOTLY_READY = True
except ImportError:
    PLOTLY_READY = False

# --- ⚙️ CONFIGURAÇÃO ---
st.set_page_config(page_title="AETHER OMNI v98.0 Ultra", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

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

# --- 🎨 DESIGN "CORPORATE TITAN V2" (Alinhamento Horizontal) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 95% !important;}
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* 🛡️ HEADER UNIT - Otimizado */
    .logo-final {
        width: 70px; height: 70px; border-radius: 50%;
        border: 2px solid #10b981; box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        cursor: pointer; transition: 0.4s; margin-top: 5px;
    }
    .logo-final:hover { transform: scale(1.05); box-shadow: 0 0 25px rgba(16, 185, 129, 0.5); }
    
    .title-text { font-weight: 900; font-size: 2.2rem; color: #ffffff; letter-spacing: -1px; line-height: 1; margin: 0; }
    .subtitle-text { color: #10b981; font-weight: 700; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 2px; }

    /* 🛡️ MENU UNIFICADO COM O CABEÇALHO */
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
    div[data-testid="stRadio"] label:has(input:checked) p { color: #10b981 !important; font-weight: 800 !important; text-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }

    /* 🛡️ INTAKE MATRIX (Estilo Mockup) */
    .intake-matrix { display: flex; gap: 8px; margin-bottom: 15px; }
    .intake-slot {
        flex: 1; background: linear-gradient(180deg, #1f2937 0%, #111827 100%); 
        border: 1px solid #374151; border-radius: 8px; padding: 12px 5px; 
        text-align: center; font-size: 0.7rem; color: #9ca3af; transition: 0.3s;
    }
    .intake-slot:hover { border-color: #4b5563; background: linear-gradient(180deg, #374151 0%, #1f2937 100%); }
    .intake-slot span { display: block; font-weight: 900; color: #e5e7eb; margin-bottom: 4px; font-size: 1rem;}
    
    [data-testid="stFileUploadDropzone"] { background-color: rgba(17, 24, 39, 0.5) !important; border: 1px dashed #374151 !important; padding: 15px !important; border-radius: 10px !important;}
    [data-testid="stFileUploadDropzone"] div { color: #9ca3af !important; }
    [data-testid="stFileUploadDropzone"] button { display: none !important; }

    .card-panel { background-color: #0f172a; padding: 25px; border-radius: 12px; border: 1px solid #1e293b; border-top: 3px solid #10b981; }
    
    button[kind="primary"] { 
        background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
        border: none !important; border-radius: 8px !important; font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important; text-transform: uppercase; letter-spacing: 1px;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 4px 20px rgba(16, 185, 129, 0.4) !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER UNIFICADO ---
logo_b64 = get_base64("logo.png")
c_logo, c_title, c_menu = st.columns([0.5, 2.5, 7], gap="small")

with c_logo:
    if logo_b64:
        st.markdown(f'<a href="." target="_self"><img src="data:image/png;base64,{logo_b64}" class="logo-final"></a>', unsafe_allow_html=True)
with c_title:
    st.markdown('<div style="margin-top: 15px;"><h1 class="title-text">AETHER OMNI</h1><p class="subtitle-text">Intelligence Hub</p></div>', unsafe_allow_html=True)
with c_menu:
    menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed", horizontal=True)

st.markdown("<hr style='border-color: #1f2937; margin-top: 5px; margin-bottom: 25px;'>", unsafe_allow_html=True)

# --- 🏗️ ÁREA DE TRABALHO ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.2], gap="large")
    
    with col_l:
        st.markdown("<h4 style='color: #10b981; margin-bottom: 15px;'>#### ☁️ Ingestão</h4>", unsafe_allow_html=True)
        
        # File Intake Matrix Refinada
        st.markdown("""
        <div class="intake-matrix">
            <div class="intake-slot"><span>☁️</span>PDF Matrix</div>
            <div class="intake-slot"><span>📄</span>DOCX Grid</div>
            <div class="intake-slot"><span>📊</span>XLSX Map</div>
            <div class="intake-slot"><span>📋</span>CSV Table</div>
        </div>
        """, unsafe_allow_html=True)
        
        up = st.file_uploader("", type=['pdf', 'docx', 'xlsx', 'csv'], label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=110, placeholder="Descreva sua análise jurídica estratégica...")
        
        # Templates
        st.markdown("<span style='color: #10b981; font-weight: bold; font-size: 0.85rem;'>#### AI Strategy Templates:</span>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        t1.button("📑 Risk Matrix", use_container_width=True, on_click=set_template, args=("Analise a matriz de riscos contratuais.",))
        t2.button("🔍 Forensic", use_container_width=True, on_click=set_template, args=("Compile evidências forenses e anomalias.",))
        t3.button("⚖️ Compliance", use_container_width=True, on_click=set_template, args=("Verifique a conformidade regulatória.",))
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            # Lógica aether_brain_supreme...
            pass
            
    with col_r:
        st.markdown("<h4 style='color: #10b981; margin-bottom: 15px;'>#### Dossiê Estratégico</h4>", unsafe_allow_html=True)
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='card-panel'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
        else:
            # Container do Mockup de Gráficos (Plotly)
            st.markdown("<div style='text-align: center; color: #9ca3af; margin-bottom: 20px;'>Aguardando Processamento Neural...</div>", unsafe_allow_html=True)
            
            if PLOTLY_READY:
                # Simulando os gráficos da imagem 2
                pc1, pc2 = st.columns(2)
                with pc1:
                    # Gráfico Rosca Simulado
                    fig_donut = go.Figure(data=[go.Pie(labels=['PDF', 'DOCX', 'XLSX', 'CSV'], values=[30, 20, 20, 30], hole=.7)])
                    fig_donut.update_traces(marker=dict(colors=['#1f2937', '#374151', '#10b981', '#059669']), showlegend=False, textinfo='percent')
                    fig_donut.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200)
                    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
                    st.markdown("<p style='text-align: center; color: #6b7280; font-size: 0.8rem;'>File composition wheel</p>", unsafe_allow_html=True)
                
                with pc2:
                    # Gráfico de Linha Simulado (Burndown)
                    x_data = list(range(100))
                    y_data = [200 - (i * 2) + np.random.normal(0, 5) for i in x_data]
                    fig_line = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color='#10b981', width=2)))
                    fig_line.update_layout(margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=True, gridcolor='#1f2937'))
                    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
                    st.markdown("<p style='text-align: center; color: #6b7280; font-size: 0.8rem;'>Potential Insights Burndown</p>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='border: 1px solid #1e293b; border-radius: 15px; height: 300px; display: flex; align-items: center; justify-content: center; color: #374151; background-color: #0f172a;'>Instale o Plotly para ver o painel neural.</div>", unsafe_allow_html=True)
