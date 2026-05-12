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

# --- ⚙️ CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="AETHER KARV V106.1 Apex", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# Funções de Base64 para Imagens Locais
def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state:
    st.session_state.cmd_input = ""
if "res_aether" not in st.session_state:
    st.session_state.res_aether = None
if "telemetria" not in st.session_state:
    st.session_state.telemetria = None

def set_template(text):
    st.session_state.cmd_input = text

# --- ⚡ EXTRATOR NEXUS (LEITURA DE ARQUIVOS) ---
def extrator_nexus(arquivos_upados):
    """Extrai texto e dados reais dos arquivos injetados."""
    texto_extraido = ""
    sucesso = 0
    for arquivo in arquivos_upados:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- MATRIZ CSV: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- MATRIZ XLSX: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.docx'):
                texto = docx2txt.process(arquivo)
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{texto}"
            elif arquivo.name.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            sucesso += 1
        except Exception as e:
            texto_extraido += f"\n[ERRO DE LEITURA EM {arquivo.name}: {str(e)}]"
    return texto_extraido, sucesso

# --- ⚡ MOTOR AETHER KARV EVOLUÍDO (INTEGRAÇÃO GROQ) ---
def aether_karv_engine(comando, contexto_arquivos):
    """Motor neural Karv atualizado para chamadas reais."""
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando.]"
    
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER KARV, um sistema de auditoria avançada.\nComando Jurídico: {comando}\nDados Injetados: {contexto_arquivos}"
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", 
                temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(2.5) 
        return f"**AUDITORIA SINTÉTICA (MODO OFFLINE):**\nO sistema processou o comando `{comando[:20]}...` com sucesso. Para processamento neural real, ative a chave de API Groq no ambiente."

# --- 🎨 DESIGN "CYBER APEX CONSOLE" ---
back_apex_b64 = get_base64_image("back_apex.png")
logo_b64 = get_base64_image("logo.png")

bg_css = f"background-image: url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    .stApp {{
        {bg_css}
        color: #f3f4f6; font-family: 'Inter', sans-serif;
    }}
    .block-container {{ padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 90% !important; margin: 0 auto !important; overflow: hidden !important;}}
    [data-testid="stHeader"], [data-testid="collapsedControl"] {{ display: none !important; }}

    /* 2. MENU CÁPSULAS - EMOJIS NATIVOS */
    div[role="radiogroup"] > div > label > div:first-child {{ display: none !important; }}
    
    div[data-testid="stRadio"] > div {{ 
        justify-content: center !important; gap: 12px !important; 
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 5px !important; border-radius: 50px !important; border: 1px solid #1e293b !important;
        width: fit-content !important; margin: 0 auto 15px auto !important;
    }}
    div[data-testid="stRadio"] label {{
        background-color: transparent !important; color: #94a3b8 !important; padding: 10px 25px !important; transition: all 0.4s ease; margin: 0 !important; cursor: pointer;
    }}
    div[data-testid="stRadio"] label:has(input:checked) {{
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        color: #020617 !important; font-weight: 800 !important; border-radius: 50px !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }}
    div[data-testid="stRadio"] label p {{ font-size: 1.05rem !important; font-weight: 700 !important; white-space: nowrap; }}

    /* 3. UPLOADER TÁTICO - CSS HACK AGRESSIVO */
    [data-testid="stFileUploadDropzone"] {{ 
        background-color: transparent !important; 
        border: 2px dashed rgba(16, 185, 129, 0.4) !important; 
        border-radius: 12px !important; transition: 0.3s;
        min-height: 100px !important; display: flex !important; justify-content: center !important; align-items: center !important;
    }}
    [data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16, 185, 129, 0.1) !important;}}
    
    [data-testid="stFileUploadDropzone"] div {{ display: none !important; }}
    
    [data-testid="stFileUploadDropzone"]::before {{
        content: '☁️ ARRASTE ARQUIVOS OU CLIQUE (PDF, DOCX, XLSX, CSV)';
        color: #cbd5e1; font-weight: 600; font-size: 0.9rem; font-family: 'Inter', sans-serif;
        position: absolute; pointer-events: none;
    }}
    
    /* 4. INPUT AREA */
    .stTextArea label {{ font-size: 0.85rem; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
    .stTextArea textarea {{
        background-color: rgba(7, 11, 20, 0.8) !important; border: 1px solid #1e293b !important; color: #cbd5e1 !important; font-size: 0.9rem !important; border-radius: 10px;
    }}
    .stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16, 185, 129, 0.2) !important; }}

    /* 5. PAINÉIS (TRANSPARENTES) */
    .operation-card {{
        background: transparent !important; border: none !important; padding: 15px; 
    }}
    
    button[kind="primary"] {{ 
        background: linear-gradient(90deg, #10b981, #34d399) !important;
        border-radius: 50px !important; font-weight: 900 !important; color: #020617 !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3) !important; text-transform: uppercase; letter-spacing: 1px;
        padding: 15px !important; margin-top: 15px !important; border: none !important; font-size: 1rem !important;
    }}
    button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 15px 35px rgba(16, 185, 129, 0.5) !important; filter: brightness(1.1); }}

    /* 6. TÍTULO CENTRALIZADO */
    .header-container {{ text-align: center; margin-bottom: 10px; display: flex; flex-direction: column; align-items: center; }}
    .logo-glow {{ width: 80px; height: 80px; border-radius: 50%; object-fit: cover; box-shadow: 0 0 35px rgba(16,185,129,0.8); margin-bottom: 8px; border: 2px solid rgba(16,185,129,0.3); }}
    .karv-title {{ margin: 0; font-weight: 900; font-size: 2.8rem; color: #ffffff; letter-spacing: -2px; line-height: 1; }}
    .karv-subtitle {{ color: #10b981; font-weight: 700; font-size: 1rem; letter-spacing: 4px; text-transform: uppercase; margin-top: 5px; }}
    
    /* 7. DOSSIÊ NEXUS */
    .nexus-center {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 320px; text-align: center; }}
    .scale-icon {{ font-size: 4rem; color: #10b981; background: rgba(16, 185, 129, 0.1); width: 120px; height: 120px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid #10b981; box-shadow: 0 0 50px rgba(16, 185, 129, 0.5); margin-bottom: 20px; }}

    /* 8. DOWNLOAD PILLS */
    .download-bar {{ display: flex; justify-content: center; gap: 8px; margin-top: 20px; }}
    .download-pill {{ background: rgba(30, 41, 59, 0.7); border: 1px solid #33
