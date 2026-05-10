import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: MOTORES DE ELITE ---
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
    st.error("🔄 Otimizando motores no servidor...")
    st.stop()

# --- ⚙️ CONFIGURAÇÃO MASTER ---
st.set_page_config(page_title="AETHER OMNI v93.15", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

def get_base64(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# --- 🎨 DESIGN "ULTRA-CLEAN ENTERPRISE" (CSS v93.15) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    /* Customização da Sidebar */
    [data-testid="stSidebar"] { background-color: #050a14 !important; border-right: 1px solid #112240 !important; }
    
    .sidebar-logo {
        display: block; margin-left: auto; margin-right: auto;
        width: 130px; border-radius: 50%; border: 2px solid #00c853;
        box-shadow: 0px 0px 25px rgba(0, 200, 83, 0.3);
        transition: 0.4s ease; cursor: pointer;
    }

    /* 🛡️ FIM TOTAL DO PONTO VERMELHO E BOLINHAS */
    div[data-testid="stRadio"] > div { background-color: transparent !important; gap: 10px; }
    div[data-testid="stRadio"] [data-testid="stRadioButton"] { display: none !important; } /* Mata a bolinha */
    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"]::before { display: none !important; } /* Mata o ponto */
    
    div[data-testid="stRadio"] label {
        background-color: #0a192f !important;
        border: 1px solid #112240 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        width: 100% !important;
        transition: 0.3s;
        display: flex !important;
        align-items: center !important;
    }

    div[data-testid="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-weight: 600 !important; color: #888 !important; margin: 0 !important; font-size: 1rem !important;
    }

    /* Estilo ATIVO (O que você selecionou) */
    div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #00c853 !important;
        border-color: #00c853 !important;
        box-shadow: 0px 0px 20px rgba(0, 200, 83, 0.4) !important;
    }
    
    div[data-testid="stRadio"] label:has(input:checked) p { color: #050a14 !important; }

    /* UI Central */
    .dossie-box { background-color: #0a192f; padding: 40px; border-radius: 15px; border: 1px solid #112240; border-top: 5px solid #00c853; }
    button[kind="primary"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: 800 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES TÉCNICAS (REVISÃO COMPLETA) ---
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
        else: return upload.read().decode("utf-8", errors="ignore")
    except Exception as e: return f"Erro no processamento: {e}"

def aether_brain_supreme(prompt, contexto):
    try:
        with DDGS() as ddgs:
            contexto_ext = "\n".join([r['body'] for r in ddgs.text(f"jurisprudência STJ STF 2026 {prompt[:30]}", max_results=2)])
    except: contexto_ext = ""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt_sys = f"AETHER OMNI v93.15. Master Auditor Harvard. CTX: {contexto_ext} - {contexto}"
        completion = client.chat.completions.create(messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.1)
        return completion.choices[0].message.content
    except Exception as e:
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro-latest') 
            return model.generate_content(f"MASTER: {prompt}\nCTX: {contexto}").text
        return f"Erro nos motores: {e}"

# --- 🚀 SIDEBAR ---
with st.sidebar:
    logo_b64 = get_base64("logo.png")
    if logo_b64:
        st.markdown(f"""
            <div style="text-align: center; padding-top: 20px;">
                <a href="." target="_self">
                    <img src="data:image/png;base64,{logo_b64}" class="sidebar-logo" title="System Reset">
                </a>
                <div style="color: #00c853; font-weight: bold; font-size: 0.8rem; margin-top: 15px; letter-spacing: 3px;">AETHER OMNI v93.15</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    menu = st.radio("Menu", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], label_visibility="collapsed")
    st.markdown("<div style='position: fixed; bottom: 20px; width: 220px; text-align: center; color: #00c853; font-size: 0.7rem;'>ONLINE | ENCRYPTED</div>", unsafe_allow_html=True)

# --- 🏗️ ÁREA PRINCIPAL ---
if menu == "🛡️ Auditoria":
    st.markdown("<h1>Auditoria Estratégica</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        up = st.file_uploader("Subir Documento", type=['pdf', 'docx', 'xlsx', 'csv'])
        cmd = st.text_area("Comando Jurídico:", height=200, placeholder="Ex: Analise riscos de compliance...")
        if st.button("🚀 EXECUTAR ANÁLISE", type="primary", use_container_width=True):
            if cmd:
                with st.spinner("AETHER processando..."):
                    res = aether_brain_supreme(cmd, processar_arquivos(up) if up else "")
                    st.session_state['res_aether'] = res
            else: st.warning("Insira um comando.")
    with c2:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            st.divider()
            cx1, cx2 = st.columns(2)
            with cx1: st.download_button("📄 PDF REPORT", data=export_pdf(st.session_state['res_aether']), file_name="AETHER_REPORT.pdf", use_container_width=True)
            with cx2: st.download_button("📝 WORD DOCX", data=export_docx(st.session_state['res_aether']), file_name="AETHER_REPORT.docx", use_container_width=True)

elif menu == "🔍 Forense":
    st.markdown("<h1>Análise Forense</h1>", unsafe_allow_html=True)
    f_file = st.file_uploader("Upload Assinatura/Documento", type=['png', 'jpg', 'jpeg'])
    if f_file:
        img = cv2.imdecode(np.asarray(bytearray(f_file.read()), dtype=np.uint8), 1)
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        st.image(edges, caption="Detecção de Hesitação Grafotécnica (Bordas Canny)", use_container_width=True)

elif menu == "🏗️ Engenharia":
    st.markdown("<h1>Engenharia de Documentos</h1>")
    st.info("Módulo configurado para expansão de templates contratuais.")
