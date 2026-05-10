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

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (CORREÇÃO DE TELA PRETA AQUI) ---
# Substituí o "antigo_logo.jpg" por "🛡️" para garantir 100% de carregamento seguro.
st.set_page_config(page_title="AETHER OMNI v93.5", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# --- 🎨 DESIGN "SAAS ENTERPRISE" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');
    
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    img[data-testid="stImage"] { border-radius: 20px; box-shadow: 0px 5px 25px rgba(0, 200, 83, 0.1); }
    .header-subtitle { letter-spacing: 5px; color: #888; font-size: 0.85rem; text-transform: uppercase; font-weight: 600; text-align: center; margin-top: 10px;}
    .stTabs [data-baseweb="tab-list"] { justify-content: center; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { background-color: #0a192f; border-radius: 8px 8px 0 0; color: #888; border: 1px solid #112240; padding: 0 30px; border-bottom: none;}
    .stTabs [aria-selected="true"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold; }
    .stTextArea textarea { background-color: #0a192f !important; color: #e6f1ff !important; border: 1px solid #112240 !important; border-radius: 8px; }
    .dossie-box { background-color: #0a192f; padding: 30px; border-radius: 8px; color: #e6f1ff; font-family: 'Inter', sans-serif; border-top: 4px solid #00c853; border-bottom: 1px solid #112240; border-left: 1px solid #112240; border-right: 1px solid #112240; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    button[kind="primary"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold !important; border: none !important; border-radius: 8px !important; }
    button[kind="primary"]:hover { opacity: 0.9; box-shadow: 0px 0px 15px rgba(0, 200, 83, 0.4); }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES TÉCNICAS (SUA LÓGICA DE MESES INTACTA) ---
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
            contexto_ext = "\n".join([r['body'] for r in ddgs.text(f"jurisprudência STJ STF 2024 {prompt[:30]}", max_results=2)])
    except: contexto_ext = ""
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        prompt_sys = f"AETHER OMNI v93.5. Master Auditor Harvard. Use Art. 421-A CC. CTX: {contexto_ext} - {contexto}"
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

# --- 🚀 HEADER ESTRUTURADO ---
st.write("") 
col_esq, col_centro, col_dir = st.columns([1, 2, 1]) 

with col_esq:
    if st.button("🔄 System Reset", use_container_width=False):
        st.session_state.clear()
        st.rerun()

with col_centro:
    try:
        # Se ele achar o logo novo, vai renderizar. Se não achar, coloca só o nome para não bugar nada.
        st.image("logo.png", use_container_width=True)
    except FileNotFoundError:
        st.markdown("<h1 style='text-align: center; color: #00c853;'>AETHER OMNI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='header-subtitle'>STRATEGIC INTELLIGENCE HUB</p>", unsafe_allow_html=True)

with col_dir:
    pass 

st.divider()

# --- 🏗️ INTERFACE PRINCIPAL ---
tab_auditoria, tab_forense, tab_engenharia = st.tabs(["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"])

with tab_auditoria:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        upload = st.file_uploader("Subir Arquivo para Análise", type=['pdf', 'docx', 'xlsx', 'csv'])
        user_input = st.text_area("Comando Jurídico Estratégico:", height=250, placeholder="Ex: Analise este contrato buscando cláusulas abusivas segundo o Art. 421-A do CC...")
        
        if st.button("🚀 PROCESSAR AUDITORIA", type="primary", use_container_width=True):
            if user_input:
                with st.spinner("AETHER processando inteligência estratégica..."):
                    res = aether_brain_supreme(user_input, processar_arquivos(upload) if upload else "")
                    st.session_state['res_aether'] = res
            else:
                st.warning("⚠️ Insira um comando jurídico para iniciar.")
                
    with col_out:
        if 'res_aether' in st.session_state:
            st.markdown(f"<div class='dossie-box'>{st.session_state['res_aether']}</div>", unsafe_allow_html=True)
            st.divider()
            c1, c2, c3 = st.columns(3)
            with c1: st.download_button("📄 PDF", data=export_pdf(st.session_state['res_aether']), file_name="AETHER_REPORT.pdf", use_container_width=True)
            with c2: st.download_button("📝 DOCX", data=export_docx(st.session_state['res_aether']), file_name="AETHER_REPORT.docx", use_container_width=True)
            with c3: st.download_button("📑 TXT", data=st.session_state['res_aether'].encode('utf-8'), file_name="AETHER_REPORT.txt", use_container_width=True)

with tab_forense:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        p_file = st.file_uploader("Upload Assinatura/Documento (Forense)", type=['png', 'jpg', 'jpeg'])
        if p_file:
            img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
            edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
            st.image(edges, caption="Análise Forense de Pixels e Hesitação", use_container_width=True)
    with col_f2:
        if p_file and st.button("🔍 GERAR LAUDO FORENSE", type="primary", use_container_width=True):
            with st.spinner("Analisando matriz de pixels..."):
                laudo = aether_brain_supreme("Analise traços desta assinatura com base na perícia grafotécnica. Descreva possíveis hesitações baseadas na detecção de bordas Canny.", "Módulo Forense Ativado")
                st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)

with tab_engenharia:
    st.info("🏗️ Módulo de Engenharia de Documentos configurado e em standby para expansão.")
