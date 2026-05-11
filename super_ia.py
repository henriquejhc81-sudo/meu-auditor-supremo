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

# --- ⚙️ CONFIGURAÇÃO ---
st.set_page_config(page_title="AETHER KARV v102.0 Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

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

# --- ⚡ MOTOR AETHER KARV (AQUI ENTRA SUA LÓGICA DE BACKEND) ---
def aether_karv_engine(comando, arquivos):
    """
    Insira aqui a lógica de IA que você estruturou (Groq/Gemini, Langchain, extração de texto).
    O retorno desta função será exibido no Dossiê Estratégico.
    """
    # Exemplo de processamento para manter a interface funcionando
    time.sleep(2) 
    return f"""
    <h3 style='color: #10b981; margin-top:0; font-weight: 800;'>Resultado da Auditoria Neural</h3>
    <p style='color: #d1d5db; font-size: 0.95rem; line-height: 1.7;'>
    Processamento executado com sucesso.<br><br>
    <strong>Comando Detectado:</strong> <em>{comando}</em><br>
    <strong>Volume de Dados:</strong> {len(arquivos) if arquivos else 0} documento(s) na matriz.<br><br>
    Análise concluída. Integração do motor validada.
    </p>
    """

# --- 🎨 DESIGN "APEX KARV" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp { background-color: #030712; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 92% !important;}
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Blindagem Lateral */
    [data-testid="stSidebar"] { display: none !important; }

    /* Extermínio do ponto vermelho */
    div[role="radiogroup"] > div > label > div:first-child { display: none !important; }
    
    div[data-testid="stRadio"] > div { flex-direction: row !important; gap: 15px !important; }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #6b7280 !important;
        padding: 10px 22px !important; border-radius: 8px !important;
        border: 1px solid #1f2937 !important; transition: all 0.4s ease; margin: 0 !important;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label:hover {
        border-color: #374151 !important; color: #9ca3af !important; background-color: rgba(31, 41, 55, 0.3) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: rgba(16, 185, 129, 0.08) !important; border-color: #10b981 !important;
        box-shadow: inset 0 0 12px rgba(16, 185, 129, 0.15) !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) p { color: #10b981 !important; font-weight: 800 !important; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }

    /* Uploader Premium */
    [data-testid="stFileUploadDropzone"] { 
        background-color: rgba(17, 24, 39, 0.4) !important; border: 1px dashed #374151 !important; 
        padding: 30px !important; border-radius: 12px !important; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    [data-testid="stFileUploadDropzone"]:hover { 
        border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.1) !important; transform: translateY(-2px);
    }
    [data-testid="stFileUploadDropzone"] div { color: #9ca3af !important; }
    [data-testid="stFileUploadDropzone"] button { display: none !important; }

    /* Painéis e Botões */
    .card-panel { background-color: #0f172a; padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-top: 3px solid #10b981; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    
    button[kind="primary"] { 
        background: linear-gradient(90deg, #059669 0%, #10b981 100%) !important;
        border: none !important; border-radius: 8px !important; font-weight: 800 !important; color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2) !important; text-transform: uppercase; letter-spacing: 1.5px;
        padding: 16px !important; margin-top: 10px !important; transition: all 0.4s ease !important;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4) !important; transform: translateY(-1px); }

    .karv-title {
        margin: 0; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 2.6rem; line-height: 1; letter-spacing: -1.5px;
        background: linear-gradient(135deg, #ffffff 0%, #a7f3d0 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    @keyframes sutil-pulse {
        0% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 5px rgba(16, 185, 129, 0.2)); }
        50% { transform: scale(1.05); opacity: 1; filter: drop-shadow(0 0 15px rgba(16, 185, 129, 0.6)); }
        100% { transform: scale(1); opacity: 0.8; filter: drop-shadow(0 0 5px rgba(16, 185, 129, 0.2)); }
    }
    .nexus-icon { display: inline-block; animation: sutil-pulse 3s infinite ease-in-out; color: #10b981; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER SOLDADO ---
logo_b64 = get_base64("logo.png")
logo_img = f'<img src="data:image/png;base64,{logo_b64}" style="width: 75px; height: 75px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 20px rgba(16,185,129,0.2);">' if logo_b64 else ''

header_html = f"""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 45px;">
    <div style="display: flex; align-items: center; gap: 22px;">
        {logo_img}
        <div style="display: flex; flex-direction: column;">
            <h1 class="karv-title">AETHER KARV</h1>
            <span style="color: #10b981; font-family: 'Inter', sans-serif; font-weight: 700; font-size: 0.85rem; letter-spacing: 4px; margin-top: 4px; opacity: 0.9;">INTELLIGENCE HUB</span>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed", horizontal=True)
st.markdown("<br>", unsafe_allow_html=True) 

# --- 🏗️ ÁREA DE TRABALHO ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.25], gap="large")
    
    with col_l:
        up_files = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=160, placeholder="Descreva sua análise estratégica profunda para o motor Karv...")

        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            if not cmd:
                st.error("⚠️ Insira um comando estratégico antes de processar.")
            else:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=True) as status:
                    st.write("Ingerindo dados e alocando tensores...")
                    
                    # Chamada do backend preservado
                    resultado_final = aether_karv_engine(comando=cmd, arquivos=up_files)
                    
                    st.write("Compilando Dossiê Estratégico...")
                    status.update(label="Auditoria Concluída com Sucesso!", state="complete", expanded=False)
                
                st.session_state['res_aether'] = resultado_final
                st.rerun() 
            
    with col_r:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='card-panel'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            
            st.markdown("<h5 style='color:#10b981; font-size: 0.85rem; margin-top: 15px; letter-spacing: 1px; text-transform: uppercase;'>📥 Exportar Dados (Matrix)</h5>", unsafe_allow_html=True)
            d1, d2, d3, d4 = st.columns(4)
            d1.download_button("☁️ PDF", "mock pdf", file_name="aether_karv.pdf", use_container_width=True)
            d2.download_button("📄 DOCX", "mock docx", file_name="aether_karv.docx", use_container_width=True)
            d3.download_button("📊 XLSX", "mock xlsx", file_name="aether_karv.xlsx", use_container_width=True)
            d4.download_button("📋 CSV", "mock csv", file_name="aether_karv.csv", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if PLOTLY_READY:
                st.markdown("<h5 style='color:#10b981; font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase;'>Telemetria Estratégica</h5>", unsafe_allow_html=True)
                pc1, pc2 = st.columns(2)
                with pc1:
                    fig_donut = go.Figure(data=[go.Pie(labels=['Validados', 'Anomalias', 'Avisos', 'Dados Base'], values=[55, 5, 10, 30], hole=.72)])
                    fig_donut.update_traces(marker=dict(colors=['#10b981', '#ef4444', '#f59e0b', '#1f2937']), showlegend=False, textinfo='percent', hoverinfo='label+percent')
                    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=190)
                    st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
                with pc2:
                    x_data = list(range(50))
                    y_data = [100 - (i * 2) + np.random.normal(0, 2) for i in x_data]
                    fig_line = go.Figure(data=go.Scatter(x=x_data, y=y_data, line=dict(color='#10b981', width=2.5), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)'))
                    fig_line.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=190, xaxis=dict(showgrid=False, visible=False), yaxis=dict(showgrid=True, gridcolor='#1f2937', zeroline=False))
                    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        else:
            st.markdown("""
            <div style='border: 1px dashed #374151; border-radius: 12px; height: 380px; display: flex; flex-direction: column; align-items: center; justify-content: center; color: #4b5563; background: linear-gradient(180deg, rgba(15,23,42,0.1) 0%, rgba(3,7,18,0.4) 100%); margin-top: 5px; box-shadow: inset 0 0 30px rgba(0,0,0,0.5);'>
                <div class="nexus-icon" style='font-size: 3rem; margin-bottom: 15px;'>⚖️</div>
                <div style='font-family: "Inter", sans-serif; font-weight: 700; font-size: 1.1rem; letter-spacing: 2px; color: #e5e7eb;'>MOTOR KARV PRONTO</div>
                <div style='font-size: 0.85rem; margin-top: 8px; opacity: 0.7;'>Aguardando ingestão e comando.</div>
            </div>
            """, unsafe_allow_html=True)
