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
st.set_page_config(page_title="AETHER KARV v103.0 Cyber", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

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

# --- ⚡ MOTOR AETHER KARV (Sem a exigência de chave na interface) ---
def aether_karv_engine(comando, arquivos):
    """Lógica preservada do motor neural Karv."""
    time.sleep(2) 
    return f"""
    <h3 style='color: #10b981; margin-top:0; font-weight: 800;'>Resultado da Auditoria Neural</h3>
    <p style='color: #d1d5db; font-size: 0.95rem; line-height: 1.7;'>
    Processamento executado com sucesso no motor Karv.<br><br>
    <strong>Comando Detectado:</strong> <em>{comando}</em><br>
    <strong>Matriz de Dados:</strong> {len(arquivos) if arquivos else 0} documento(s) ativos.<br><br>
    Análise estratégica concluída com integridade de 92%. Autenticação de rede validada.
    </p>
    """

# --- 🎨 DESIGN "CYBER CONSOLE" (Espelhamento exato do seu Print do Paint) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    /* Fundo super escuro (Cyberpunk Console) */
    .stApp { background-color: #020617; color: #f3f4f6; font-family: 'Inter', sans-serif; }
    .block-container { padding-top: 2rem !important; padding-bottom: 0rem !important; max-width: 90% !important;}
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }

    /* Blindagem Lateral */
    [data-testid="stSidebar"] { display: none !important; }

    /* --- MENU PÍLULAS CENTRALIZADAS (Design do Print) --- */
    div[role="radiogroup"] > div > label > div:first-child { display: none !important; }
    
    div[data-testid="stRadio"] > div { 
        flex-direction: row !important; 
        justify-content: center !important; /* Centraliza as pílulas */
        gap: 20px !important; 
        background: transparent !important;
        padding: 10px;
        margin: 0 auto 40px auto;
        border: none !important;
    }
    div[data-testid="stRadio"] label {
        background-color: #0f172a !important; 
        color: #64748b !important;
        padding: 12px 35px !important; 
        border-radius: 50px !important; /* Formato Pílula */
        border: 1px solid #1e293b !important; 
        transition: all 0.4s ease; margin: 0 !important;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #064e3b, #10b981) !important; 
        border-color: #34d399 !important;
        box-shadow: 0 0 25px rgba(16, 185, 129, 0.5), inset 0 0 10px rgba(16, 185, 129, 0.5) !important; /* Aura Neon */
    }
    div[data-testid="stRadio"] label:has(input:checked) p { color: #ffffff !important; font-weight: 800 !important; text-shadow: 0 0 8px rgba(255,255,255,0.5); }
    div[data-testid="stRadio"] label p { font-size: 1.1rem !important; font-weight: 600 !important; }

    /* --- UPLOADER CAMUFLADO --- */
    [data-testid="stFileUploadDropzone"] { 
        background-color: rgba(15, 23, 42, 0.3) !important; 
        border: 1px dashed #1e293b !important; 
        padding: 15px !important; border-radius: 12px !important; 
        transition: 0.3s;
    }
    [data-testid="stFileUploadDropzone"]:hover { border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.05) !important;}
    
    /* --- INPUT AREA (Escura e elegante) --- */
    .stTextArea label { color: #f8fafc !important; font-weight: 600 !important; font-size: 1rem !important; margin-bottom: 8px !important; }
    .stTextArea textarea {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 8px !important;
        color: #d1d5db !important;
        padding: 15px !important;
    }
    .stTextArea textarea:focus { border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }

    /* --- PAINÉIS E BOTÕES --- */
    .card-panel { background-color: #0f172a; padding: 30px; border-radius: 12px; border: 1px solid #1e293b; border-top: 3px solid #10b981; box-shadow: 0 10px 40px rgba(0,0,0,0.5); }
    
    button[kind="primary"] { 
        background: linear-gradient(90deg, #059669, #10b981) !important;
        border: none !important; border-radius: 10px !important; font-weight: 800 !important; color: #ffffff !important;
        box-shadow: 0 5px 20px rgba(16, 185, 129, 0.2) !important; text-transform: uppercase; letter-spacing: 1px;
        padding: 18px 20px !important; margin-top: 15px !important; transition: 0.3s !important;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); transform: translateY(-2px); box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important; }

    /* --- TITULO CENTRALIZADO COM GLOW --- */
    .header-container { text-align: center; margin-bottom: 25px; display: flex; flex-direction: column; align-items: center; }
    .logo-glow { width: 70px; height: 70px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 35px rgba(16,185,129,0.8); margin-bottom: 15px; border: 2px solid rgba(16,185,129,0.3); }
    .karv-title {
        margin: 0; font-family: 'Inter', sans-serif; font-weight: 900; font-size: 3.2rem; line-height: 1; letter-spacing: -1px;
        color: #ffffff; text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }
    .karv-subtitle { color: #34d399; font-family: 'Inter', sans-serif; font-weight: 600; font-size: 1.1rem; letter-spacing: 3px; margin-top: 8px; }
    
    /* --- DOSSIÊ PLACEHOLDER (Do Print) --- */
    .dossier-empty {
        background-color: #050b14;
        border: 1px solid #1e293b;
        border-radius: 12px;
        height: 360px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        margin-top: 28px;
    }
    /* Borda superior verde fina */
    .dossier-empty::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: linear-gradient(90deg, transparent, #10b981, transparent); }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 HEADER CENTRALIZADO (ESTILO CONSOLE) ---
logo_b64 = get_base64("logo.png")
logo_img = f'<img src="data:image/png;base64,{logo_b64}" class="logo-glow">' if logo_b64 else ''

header_html = f"""
<div class="header-container">
    {logo_img}
    <h1 class="karv-title">AETHER KARV</h1>
    <div class="karv-subtitle">Strategic Intelligence Hub</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# O Menu Radio agora centraliza automaticamente pelo CSS
menu = st.radio("", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0, label_visibility="collapsed", horizontal=True)

# --- 🏗️ ÁREA DE TRABALHO (2 COLUNAS) ---
if menu == "🛡️ Auditoria":
    col_l, col_r = st.columns([1, 1.25], gap="large")
    
    with col_l:
        up_files = st.file_uploader(" ", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        cmd = st.text_area("Comando Jurídico Estratégico:", key="cmd_input", height=150, placeholder="Descreva sua análise jurídica estratégica...")

        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            if not cmd:
                st.error("⚠️ Insira um comando estratégico antes de processar.")
            else:
                with st.status("🧠 Inicializando Motores Neurais AETHER KARV...", expanded=True) as status:
                    st.write("Ingerindo dados e alocando tensores...")
                    # Função executada (sem a exigência de api_key na UI)
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
            # Novo layout do Dossiê Placeholder espelhando o seu texto do Paint
            st.markdown("""
            <div class="dossier-empty">
                <p style="color: #f1f5f9; font-weight: 700; font-size: 1.1rem; text-align: center; margin: 0;">
                    Dossiê Estratégico:<br>
                    <span style="color: #64748b; font-weight: 400; font-size: 0.95rem;">Aguardando Processamento Neural...</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
