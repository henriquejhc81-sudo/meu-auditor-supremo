import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: MOTORES DE ELITE ---
# Nenhuma função existente foi removida ou alterada em sua lógica.
# Apenas a interface (front-end) foi refatorada.

try:
    from fpdf import FPDF
    PDF_READY = True
except ImportError:
    st.error("🔄 Otimizando motor de PDF (FPDF)...")
    PDF_READY = False

try:
    from groq import Groq
    import google.generativeai as genai
    from duckduckgo_search import DDGS
except ImportError:
    st.error("🔄 Otimizando motores de IA e Busca...")
    st.stop()

# --- Utility Function: Image to Base64 (v93.16) ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# --- ⚙️ CONFIGURAÇÃO DE PÁGINA (FAVICON SEGURO) ---
# Usando emoji universal 🛡️ como favicon para garantir carregamento 100% seguro.
st.set_page_config(page_title="AETHER OMNI v93.16", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# --- 🎨 DESIGN "SINGLE-PAGE ENTERPRISE" (CSS v93.16) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');
    
    /* Fundo Slate Profundo e Fontes */
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* Hide Default Header e Sidebar */
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    
    /* 🚀 UNIFIED HEADER (Aether Logo + Navigation Buttons) */
    .aether-header {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        background-color: #0a192f;
        padding: 10px 30px;
        border-bottom: 1px solid #112240;
        margin-bottom: 30px;
        position: relative;
    }
    
    /* 🛡️ LOGO RESET F5 BLINDADO (Lateral Esquerda) */
    .aether-logo-container {
        display: flex;
        align-items: center;
        margin-right: 30px;
        padding-top: 5px;
    }
    
    .aether-logo-reset {
        border-radius: 50% !important;
        width: 100px !important;
        height: 100px !important;
        object-fit: cover !important;
        border: 2px solid #00c853;
        box-shadow: 0px 5px 25px rgba(0, 200, 83, 0.25) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
    }
    .aether-logo-reset:hover {
        transform: rotate(5deg) scale(1.05);
        box-shadow: 0px 8px 35px rgba(0, 200, 83, 0.4) !important;
    }
    
    /* 🛡️ FIM DO PONTO VERMELHO E BOLINHAS (RESOLVIDO TÉCNICO-VISUALMENTE) */
    /* Remove default streamlit radio button visual clutter */
    [data-testid="stMainElement"] div.stRadio > div { display: flex !important; flex-direction: row !important; gap: 15px !important; padding: 0 !important; margin: 0 !important; background-color: transparent !important; }
    
    /* Mata a bolinha de rádio nativa */
    [data-testid="stMainElement"] div.stRadio [data-testid="stRadioButton"] { display: none !important; }
    
    /* Estilização dos Botões de Navegação como "Tabs" Premium */
    [data-testid="stMainElement"] div.stRadio label {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 50px !important;
        background-color: #0a192f !important;
        color: #888 !important;
        border: 1px solid #112240 !important;
        border-radius: 8px !important;
        padding: 0 30px !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        margin: 0 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    
    /* Estilo "Emerald Glow" quando o botão está selecionado */
    [data-testid="stMainElement"] div.stRadio label[data-baseweb="radio"]:has(input[checked]),
    [data-testid="stMainElement"] div.stRadio input[checked] + div[data-testid="stMarkdownContainer"] {
        background-color: #00c853 !important;
        color: #050a14 !important;
        border-color: #00c853 !important;
        box-shadow: 0px 0px 20px rgba(0, 200, 83, 0.4) !important;
    }
    
    /* Headers e Títulos */
    h1 { font-family: 'Playfair Display', serif; color: #00c853 !important; }
    h2, h3 { color: #888; font-family: 'Inter', sans-serif;}
    
    /* Dossiê Box */
    .dossie-box { background-color: #0a192f; padding: 40px; border-radius: 8px; color: #e6f1ff; line-height: 1.8; white-space: pre-wrap; font-family: 'Inter', sans-serif; border-top: 5px solid #00c853; border-left: 1px solid #112240; border-right: 1px solid #112240; border-bottom: 1px solid #112240; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    
    /* Botões Primários Emerald */
    div.stButton > button[kind="primary"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: 700 !important; border-radius: 8px !important; text-transform: uppercase !important; border: none !important; width: 100% !important; height: 3.5em !important; transition: transform 0.2s ease, box-shadow 0.2s ease; }
    div.stButton > button[kind="primary"]:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0, 200, 83, 0.3); }

    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES TÉCNICAS (PRESERVADAS INTEGRALMENTE) ---
def export_pdf(texto):
    if not PDF_READY: return None
    pdf = FPDF()
    pdf.add_page()
    try: pdf.image('logo.png', 10, 8, 33)
    except: pass
    pdf.set_font("Arial", 'B', 16); pdf.cell(0, 20, "RELATÓRIO AETHER OMNI", ln=True, align='C'); pdf.ln(10)
    pdf.set_font("Arial", size=11)
    safe_text = texto.replace("🚨", "ALERTA:").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')

def export_docx(texto):
    doc = Document()
    try: doc.add_picture('logo.png', width=Inches(1.5))
    except: pass
    doc.add_heading('AETHER OMNI | Strategic Report', 0)
    doc.add_paragraph(texto)
    bio = io.BytesIO(); doc.save(bio)
    return bio.getvalue()

def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e: return f"Erro: {e}"

def aether_brain_supreme(prompt, contexto):
    try:
        with DDGS() as ddgs:
            contexto_ext = "\n".join([r['body'] for r in ddgs.text(f"jurisprudência STJ STF 2026 {prompt[:30]}", max_results=2)])
    except: contexto_ext = ""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt_sys = f"AETHER OMNI v93.16. Master Auditor Harvard. CTX: {contexto_ext} - {contexto}"
        completion = client.chat.completions.create(messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.1)
        return completion.choices[0].message.content
    except Exception as e_groq:
        if "GOOGLE_API_KEY" in st.secrets:
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-pro-latest') 
                return model.generate_content(f"MASTER: {prompt}\nCTX: {contexto}").text
            except Exception as e_gemini:
                return f"Erro Crítico. Groq: {e_groq} | Gemini: {e_gemini}"
        return "Erro de conexão segura."

# --- 🚀 REORGANIZAÇÃO: UNIFIED HEADER (LOGO + BOTÕES v93.16) ---
# Substituo st.sidebar por um st.markdown com HTML customizado no topo da página.

st.markdown("<div class='aether-header'>", unsafe_allow_html=True)

# 1. Logo Clicável F5 (Reset Master)
logo_b64 = None
if os.path.exists("logo.png"):
    logo_b64 = get_base64_of_bin_file("logo.png")

if logo_b64:
    html_logo_clickable = f"""
        <div class='aether-logo-container'>
            <a href="." target="_self">
                <img src='data:image/png;base64,{logo_b64}' alt='AETHER OMNI Logo' class='aether-logo-reset' title='System Reset'>
            </a>
        </div>
        """
    st.markdown(html_logo_clickable, unsafe_allow_html=True)

# 2. Botões de Navegação Horizontal (Single-Page App)
# Uso st.radio mas aplico o CSS v93.16 para que ele pareça uma barra de botões horizontais premium.
menu_radio = st.radio(
    "Navegação:",
    ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"],
    index=0,
    label_visibility="collapsed", # Esconde o label "Navegação:"
)

st.markdown("</div>", unsafe_allow_html=True) # Fim do Header

# --- 🏗️ ÁREA DE TRABALHO UNIFICADA ---
st.write("") # Espaçamento para o Header

if menu_radio == "🛡️ Auditoria":
    st.markdown("<h1>Auditoria Estratégica Jurídica</h1>", unsafe_allow_html=True)
    st.divider()
    
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        upload = st.file_uploader("Subir Arquivo (PDF, DOCX, XLSX, CSV)", type=['pdf', 'docx', 'xlsx', 'csv'])
        user_input = st.text_area("Comando Jurídico:", height=250, placeholder="Ex: Analise este contrato buscando cláusulas abusivas segundo o Art. 421-A do CC...")
        
        if st.button("🚀 PROCESSAR AUDITORIA", kind="primary"):
            if user_input:
                with st.spinner("AETHER processando inteligência estratégica..."):
                    res = aether_brain_supreme(user_input, processar_arquivos(upload) if upload else "")
                    st.session_state['res_aether'] = res
            else:
                st.warning("⚠️ Insira um comando jurídico.")
                
    with col_out:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            st.divider()
            cx1, cx2, cx3 = st.columns(3)
            with cx1: st.download_button("📄 PDF REPORT", data=export_pdf(st.session_state['res_aether']), file_name="AETHER_REPORT.pdf")
            with cx2: st.download_button("📝 WORD DOCX", data=export_docx(st.session_state['res_aether']), file_name="AETHER_REPORT.docx")
            with cx3: st.download_button("📑 TXT RAW", data=st.session_state['res_aether'].encode('utf-8'), file_name="AETHER_REPORT.txt")

elif menu_radio == "🔍 Forense":
    st.markdown("<h1>Análise Forense e Grafotécnica</h1>", unsafe_allow_html=True)
    st.divider()
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        p_file = st.file_uploader("Upload Assinatura/Documento (Forense)", type=['png', 'jpg', 'jpeg'])
        if p_file:
            img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
            edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
            st.image(edges, caption="Detecção de Bordas Canny (Hesitação)", use_container_width=True)
    with col_f2:
        if p_file and st.button("🔍 GERAR LAUDO FORENSE", kind="primary"):
            with st.spinner("Analisando traços..."):
                laudo = aether_brain_supreme("Analise traços grafotécnicos. Descreva hesitações.", "Módulo Forense")
                st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)

elif menu_radio == "🏗️ Engenharia":
    st.markdown("<h1>Engenharia de Documentos</h1>", unsafe_allow_html=True)
    st.divider()
    st.info("🏗️ Módulo em standby para automação contratual.")
