import streamlit as st
import pandas as pd
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO DE BIBLIOTECAS ---
try:
    import google.generativeai as genai
    GEMINI_READY = True
except ImportError:
    GEMINI_READY = False

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE MICROSOFT LEVEL ---
st.set_page_config(page_title="AETHER KARV Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

if "res_aether" not in st.session_state:
    st.session_state.res_aether = None

# --- ⚡ MOTOR NEURAL AETHER KARV (O CÉREBRO) ---
def extrair_texto(arquivos):
    """Lê e extrai os dados reais dos arquivos enviados."""
    texto_completo = ""
    for arq in arquivos:
        extensao = arq.name.split('.')[-1].lower()
        texto_completo += f"\n--- INÍCIO DO DOCUMENTO: {arq.name} ---\n"
        try:
            if extensao == 'docx':
                texto_completo += docx2txt.process(arq)
            elif extensao == 'csv':
                df = pd.read_csv(arq)
                texto_completo += df.to_string()
            elif extensao in ['xlsx', 'xls']:
                df = pd.read_excel(arq)
                texto_completo += df.to_string()
            elif extensao == 'pdf':
                texto_completo += "[Aviso: Leitura de PDF requer biblioteca PyPDF2. Texto simulado/vazio no momento.]"
            else:
                texto_completo += f"[Formato {extensao} não suportado para extração nativa de texto]"
        except Exception as e:
            texto_completo += f"[Erro ao ler {arq.name}: {str(e)}]"
        texto_completo += f"\n--- FIM DO DOCUMENTO: {arq.name} ---\n"
    return texto_completo

def aether_karv_engine(comando, arquivos, api_key):
    """Conecta ao Google Gemini e processa a estratégia."""
    if not GEMINI_READY:
        return "Erro: Biblioteca google-generativeai não encontrada no servidor."
    
    try:
        # 1. Configura a Chave de Ignição
        genai.configure(api_key=api_key)
        
        # 2. Prepara o Motor (Usando o Gemini Flash pela velocidade e contexto longo)
        modelo = genai.GenerativeModel('gemini-1.5-flash')
        
        # 3. Extrai os dados da matriz (arquivos)
        contexto_documentos = extrair_texto(arquivos) if arquivos else "Nenhum documento anexado."
        
        # 4. Forja o Prompt Estratégico
        prompt_mestre = f"""
        Você é o AETHER KARV, uma IA de Inteligência Estratégica e Auditoria de Elite.
        Comporte-se com um tom corporativo, extremamente técnico, cirúrgico e analítico.
        
        COMANDO DO USUÁRIO:
        {comando}
        
        DADOS DE ENTRADA (MATRIZ DE DOCUMENTOS):
        {contexto_documentos}
        
        Sintetize a resposta em formato de Dossiê Estratégico (use markdown, tópicos e negrito para destacar anomalias ou insights críticos).
        """
        
        # 5. Executa o disparo neural
        resposta = modelo.generate_content(prompt_mestre)
        return resposta.text

    except Exception as e:
        return f"**⚠️ Falha no Motor Neural:** {str(e)}\n\nVerifique se a sua Chave de API é válida e se há cota disponível."

# --- 🎨 DESIGN "CYBER APEX" (Fidelidade Absoluta) ---
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

    /* HEADER GLOW */
    .header-master { text-align: center; margin-bottom: 20px; }
    .logo-main {
        width: 85px; height: 85px; border-radius: 50%;
        box-shadow: 0 0 40px rgba(16, 185, 129, 0.7);
        border: 2px solid #10b981; margin-bottom: 10px;
    }
    .title-karv { font-weight: 900; font-size: 3.2rem; color: #ffffff; letter-spacing: -2px; margin: 0; line-height: 1; }
    .subtitle-karv { color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 5px; text-transform: uppercase; margin-top: 5px; }

    /* NAVIGATION CAPSULE */
    div[data-testid="stRadio"] > div { 
        justify-content: center !important; gap: 12px !important; 
        background: rgba(15, 23, 42, 0.6); padding: 8px; border-radius: 50px; border: 1px solid #1f2937; width: fit-content; margin: 15px auto 35px auto;
    }
    div[data-testid="stRadio"] label {
        background-color: transparent !important; color: #94a3b8 !important; padding: 10px 25px !important; border-radius: 50px !important; transition: 0.4s;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 900 !important; box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }

    /* OPERATION CARDS */
    .card-label { font-size: 1.1rem; font-weight: 900; color: #ffffff; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }
    .operation-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid #1e293b; border-radius: 18px; padding: 25px;
        position: relative; height: 500px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        overflow-y: auto;
    }
    .operation-card::-webkit-scrollbar { width: 8px; }
    .operation-card::-webkit-scrollbar-track { background: transparent; }
    .operation-card::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 4px; }
    .operation-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px; background: #10b981; }

    /* INPUTS & TEXTAREA */
    [data-testid="stFileUploadDropzone"] { background: rgba(7, 11, 20, 0.5) !important; border: 1px dashed #334155 !important; border-radius: 12px !important; padding: 10px !important; }
    .stTextArea textarea, .stTextInput input { background: #070b14 !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; border-radius: 10px !important; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }
    .stTextInput label { color: #64748b !important; font-size: 0.8rem !important; font-weight: 600 !important; }

    /* BUTTON NEON */
    button[kind="primary"] { 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; color: #020617 !important; font-weight: 900 !important;
        height: 55px !important; margin-top: 15px !important; border: none !important; text-transform: uppercase;
        transition: 0.3s;
    }
    button[kind="primary"]:hover { filter: brightness(1.2); box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4) !important; transform: scale(1.02); }

    /* DOSSIÊ NEXUS */
    .nexus-center { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; }
    .scale-icon {
        font-size: 3rem; color: #10b981; background: rgba(16, 185, 129, 0.1); 
        width: 110px; height: 110px; display: flex; align-items: center; justify-content: center;
        border-radius: 50%; border: 2px solid #10b981; box-shadow: 0 0 45px rgba(16, 185, 129, 0.3); margin-bottom: 20px;
    }

    /* DOWNLOAD PILLS */
    .download-bar { display: flex; justify-content: center; gap: 8px; margin-top: 20px; padding-bottom: 10px; }
    .download-pill {
        background: rgba(30, 41, 59, 0.5); border: 1px solid #334155; border-radius: 50px;
        padding: 6px 14px; color: #94a3b8; font-size: 0.75rem; font-weight: 600; cursor: pointer; transition: 0.3s;
    }
    .download-pill:hover { border-color: #10b981; color: #10b981; }
    </style>
    """, unsafe_allow_html=True)

# --- 🚀 RENDERIZAÇÃO DA INTERFACE ---
logo_b64 = get_base64("logo.png")
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="logo-main">' if logo_b64 else '<div class="logo-main" style="display:flex;align-items:center;justify-content:center;color:#10b981;font-size:2rem;"><i class="fas fa-shield-halved"></i></div>'

st.markdown(f"""
    <div class="header-master">
        {logo_html}
        <h1 class="title-karv">AETHER KARV</h1>
        <div class="subtitle-karv">Strategic Intelligence Hub</div>
    </div>
""", unsafe_allow_html=True)

menu = st.radio("Menu", ["AUDITORIA", "FORENSE", "ENGENHARIA"], index=0, label_visibility="collapsed", horizontal=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="card-label">INGESTÃO</div>', unsafe_allow_html=True)
    st.markdown('<div class="operation-card">', unsafe_allow_html=True)
    up = st.file_uploader("Upload", accept_multiple_files=True, label_visibility="collapsed")
    st.markdown('<p style="font-size:0.75rem;color:#64748b;text-align:center;margin-top:-10px;">ARRASTE ARQUIVOS (DOCX, XLSX, CSV)</p>', unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top:10px;"><p class="card-label" style="font-size:0.85rem;">COMANDO JURÍDICO ESTRATÉGICO:</p></div>', unsafe_allow_html=True)
    cmd = st.text_area("Comando", key="cmd_input", height=90, placeholder="Descreva sua análise jurídica estratégica...", label_visibility="collapsed")
    
    api_key_input = st.text_input("🔑 CHAVE DE IGNIÇÃO (GEMINI API KEY):", type="password", placeholder="Insira sua API Key do Google Gemini...")
    
    if st.button("🚀 PROCESSAR AUDITORIA NEURAL", type="primary", use_container_width=True):
        if not api_key_input:
            st.error("⚠️ Atenção: A Chave de Ignição (API Key) é obrigatória para acessar os motores do Google Gemini.")
        elif not cmd:
            st.warning("⚠️ Forneça um comando estratégico para a IA.")
        else:
            with st.status("🧠 Inicializando Motores Neurais e Ingerindo Dados...", expanded=False):
                resultado_final = aether_karv_engine(comando=cmd, arquivos=up
