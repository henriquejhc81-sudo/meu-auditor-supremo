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
    from streamlit_extras.segmented_control import segmented_control
    MODO_MODERNO = True
except ImportError:
    MODO_MODERNO = False

try:
    from groq import Groq
except ImportError:
    st.error("🔄 Otimizando motores de elite no servidor...")
    st.stop()

import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (CLEAN & RESPONSIVE) ---
st.set_page_config(
    page_title="AETHER OMNI v92.4", 
    page_icon="🛡️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 🎨 DESIGN "PLATINUM SUPREME" (FIXED) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    
    /* Centralização de Logo e Título Único */
    .header-box { text-align: center; padding: 20px; position: relative; }
    .header-box h1 { font-family: 'Playfair Display', serif; color: #00c853; font-size: calc(2.2em + 1.5vw); margin: 0; }
    .header-box p { color: #888; letter-spacing: 5px; font-size: 0.8em; text-transform: uppercase; margin-top: -5px; }

    /* Relatório Harvard (DNA do Projeto) */
    .dossie-box {
        background-color: #ffffff; padding: 40px; border-radius: 2px; color: #1a1a1a;
        line-height: 1.8; white-space: pre-wrap; font-family: 'Georgia', serif;
        border-top: 15px solid #85142b; box-shadow: 0px 15px 35px rgba(0,0,0,0.6);
        margin: 20px auto; width: 95%; max-width: 900px;
    }

    /* Reset Invisível sobre o Logo */
    div.stButton > button[key="reset_supreme"] {
        background: transparent !important; color: transparent !important; border: none !important;
        position: absolute; top: 0; left: 0; width: 100%; height: 160px; z-index: 1000;
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

# --- 🧠 MOTOR SUPREME V5.7 (HÍBRIDO & DOUBLE-CHECK) ---
def aether_brain_supreme(prompt, contexto):
    try:
        with DDGS() as ddgs:
            contexto_ext = "\n".join([r['body'] for r in ddgs.text(f"jurisprudência STJ STF 2024 {prompt[:30]}", max_results=2)])
    except: contexto_ext = ""
    
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt_sys = f"AETHER OMNI v92.4. Master Auditor Harvard. Use Art. 421-A CC. CTX: {contexto_ext} - {contexto}"
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", temperature=0.1
        )
        return completion.choices[0].message.content
    except:
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro')
            return model.generate_content(f"MASTER: {prompt}\nCTX: {contexto}").text
        return "Erro de conexão segura."

# --- 🚀 HEADER CENTRALIZADO (LOGO + RESET FIXED) ---
st.markdown("<div class='header-box'>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3) # Definido 3 colunas explicitamente para evitar TypeError
with col2:
    if st.button(" ", key="reset_supreme", help="Clique no logo para reiniciar"):
        st.session_state.clear()
        st.rerun()
    try: st.image("logo.png", width=140)
    except: pass 
st.markdown("<h1>AETHER</h1><p>STRATEGIC INTELLIGENCE | v92.4</p></div>", unsafe_allow_html=True)

# --- 🏗️ INTERFACE ---
if MODO_MODERNO:
    try: aba_ativa = segmented_control(options=["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0)
    except: aba_ativa = st.radio("Módulo:", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], horizontal=True)
else:
    aba_ativa = st.radio("Módulo:", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], horizontal=True)

st.divider()

if "Auditoria" in aba_ativa:
    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva o caso ou comando de elite:", height=300)
        upload = st.file_uploader("Upload de Documentos")
        if st.button("EXECUTAR INTELIGÊNCIA AETHER"):
            with st.spinner("Analisando..."):
                res = aether_brain_supreme(user_input, processar_arquivos(upload) if upload else "")
                st.session_state['res_aether'] = res

    with col_out:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1: st.download_button("📄 PDF", data=export_pdf(st.session_state['res_aether']), file_name="REPORT.pdf")
            with c2: st.download_button("📝 WORD", data=export_docx(st.session_state['res_aether']), file_name="REPORT.docx")
            with c3: st.download_button("📑 TXT", data=st.session_state['res_aether'].encode('utf-8'), file_name="REPORT.txt")

elif "Forense" in aba_ativa:
    st.subheader("🔍 Perícia Grafotécnica (OpenCV)")
    p_file = st.file_uploader("Upload de Amostra", type=['png', 'jpg'])
    if p_file:
        img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        st.image(edges, caption="Análise Forense de Pixels", use_container_width=True)
        if st.button("GERAR LAUDO PERICIAL"):
            laudo = aether_brain_supreme("Analise os traços desta assinatura. Procure por hesitação.", "Forense")
            st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)
