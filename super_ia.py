import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: IMPORTAÇÕES BLINDADAS ---
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
    st.error("🔄 Otimizando motores de elite no servidor...")
    st.stop()

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (UI/UX PREMIUM) ---
st.set_page_config(
    page_title="AETHER OMNI v93.1", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 🎨 DESIGN "SAAS ENTERPRISE" (CSS CUSTOMIZADO) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* Header Minimalista */
    .header-container { text-align: center; padding-top: 10px; margin-bottom: 0px; }
    .header-title { font-family: 'Playfair Display', serif; color: #00c853; font-size: 3.5rem; margin-top: -10px; }
    .header-subtitle { letter-spacing: 5px; color: #888; font-size: 0.8rem; text-transform: uppercase; margin-top: -15px; }

    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 50px; background-color: #0a192f; border-radius: 8px 8px 0 0; 
        color: #888; border: 1px solid #112240; padding: 0 30px;
    }
    .stTabs [aria-selected="true"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold; }

    /* Relatório Harvard Style */
    .dossie-box {
        background-color: #ffffff; padding: 40px; border-radius: 4px; color: #1a1a1a;
        line-height: 1.8; white-space: pre-wrap; font-family: 'Georgia', serif;
        border-top: 15px solid #85142b; box-shadow: 0px 15px 35px rgba(0,0,0,0.6);
    }
    
    /* Botão Primário Largo */
    div.stButton > button:first-child {
        background-color: #00c853 !important; color: #050a14 !important;
        font-weight: 700 !important; width: 100% !important; height: 3.5em !important;
        border-radius: 8px !important; text-transform: uppercase !important;
    }
    
    /* Reset Button Invisible */
    div.stButton > button[key="reset_trigger"] {
        background: transparent !important; color: transparent !important; border: none !important;
        position: absolute; top: 0; left: 0; width: 100%; height: 100px; z-index: 1000;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES DE EXPORTAÇÃO (CORE PRESERVADO) ---
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

# --- ⚙️ FUNÇÕES TÉCNICAS (INTACTAS) ---
def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e: return f"Erro: {e}"

def aether_brain_supreme(prompt, contexto):
    try:
        with DDGS() as ddgs:
            contexto_ext = "\n".join([r['body'] for r in ddgs.text(f"jurisprudência STJ STF 2024 {prompt[:30]}", max_results=2)])
    except: contexto_ext = ""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt_sys = f"AETHER OMNI v93.1. Master Auditor Harvard. Use Art. 421-A CC. CTX: {contexto_ext} - {contexto}"
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", temperature=0.1
        )
        return completion.choices.message.content
    except:
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro')
            return model.generate_content(f"MASTER: {prompt}\nCTX: {contexto}").text
        return "Erro de conexão segura."

# --- 🚀 HEADER CENTRALIZADO (LOGO RESET FIXED) ---
st.markdown("<div class='header-container'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3) # FIX: Agora com valor explícito
with col2:
    if st.button("🛡️", key="reset_trigger", help="Clique para Reiniciar"):
        st.session_state.clear()
        st.rerun()
st.markdown("<h1 class='header-title'>AETHER</h1><p class='header-subtitle'>STRATEGIC INTELLIGENCE</p></div>", unsafe_allow_html=True)
st.divider()

# --- 🏗️ INTERFACE POR ABAS (TABS) ---
tab_auditoria, tab_forense, tab_engenharia = st.tabs(["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"])

# --- 🛡️ ABA A: AUDITORIA ---
with tab_auditoria:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        st.subheader("📥 Inserção de Dados")
        upload = st.file_uploader("Subir Arquivo", type=['pdf', 'docx', 'xlsx', 'csv'])
        user_input = st.text_area("Descreva o comando jurídico:", height=250)
        if st.button("🚀 PROCESSAR AUDITORIA"):
            with st.spinner("Analisando..."):
                cont = processar_arquivos(upload) if upload else ""
                res = aether_brain_supreme(user_input, cont)
                st.session_state['res_aether'] = res

    with col_out:
        st.subheader("🚀 Relatório de Elite")
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1: st.download_button("📄 PDF", data=export_pdf(st.session_state['res_aether']), file_name="REPORT.pdf")
            with c2: st.download_button("📝 WORD", data=export_docx(st.session_state['res_aether']), file_name="REPORT.docx")
            with c3: st.download_button("📑 TXT", data=st.session_state['res_aether'].encode('utf-8'), file_name="REPORT.txt")

# --- 🔍 ABA B: FORENSE ---
with tab_forense:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        p_file = st.file_uploader("Upload Assinatura", type=['png', 'jpg'])
        if p_file:
            img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
            edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
            st.image(edges, caption="Análise Forense de Pixels", use_container_width=True)
    with col_f2:
        if p_file and st.button("🔍 GERAR LAUDO DE FRAUDE"):
            laudo = aether_brain_supreme("Analise traços desta assinatura. Procure hesitação.", "Forense")
            st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)
