import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import io
import cv2
import numpy as np
import docx2txt
from docx import Document

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: IMPORTAÇÕES BLINDADAS ---
try:
    from fpdf import FPDF
    PDF_READY = True
except ImportError:
    PDF_READY = False

try:
    from streamlit_extras.segmented_control import segmented_control
    from streamlit_extras.grid import grid
    MODO_MODERNO = True
except ImportError:
    MODO_MODERNO = False

try:
    from groq import Groq
except ImportError:
    st.error("🔄 Aguardando deploy do requirements.txt...")
    st.stop()

import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (ESTILO HARVARD) ---
st.set_page_config(page_title="AETHER OMNI v89.5 | Strategic Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN ELITE "HARVARD NAVY" (PRESERVADO) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    h1, h2, h3 { font-family: 'Playfair Display', serif; color: #ffffff; }
    .insight-card { background-color: #0a192f; padding: 20px; border-radius: 8px; border-left: 5px solid #00c853; border: 1px solid #112240; margin-bottom: 15px; }
    .stButton>button { background-color: #00c853; color: #050a14; font-weight: 700; border-radius: 4px; width: 100%; height: 3.8em; text-transform: uppercase; }
    .dossie-box { background-color: #ffffff; padding: 40px; border-radius: 4px; color: #1a1a1a; line-height: 1.8; white-space: pre-wrap; font-family: 'Georgia', serif; border-top: 10px solid #85142b; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES DE EXPORTAÇÃO ---
def export_pdf(text):
    if not PDF_READY: return None
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        return pdf.output(dest='S').encode('latin-1')
    except: return None

def export_docx(text):
    doc = Document()
    doc.add_heading('AETHER OMNI - Relatório Oficial', 0)
    doc.add_paragraph(text)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- ⚙️ FUNÇÕES TÉCNICAS PRESERVADAS ---
def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        elif upload.name.endswith('.csv'): return pd.read_csv(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e: return f"Erro: {e}"

def buscar_jurisprudencia(termo):
    try:
        with DDGS() as ddgs:
            return "\n".join([r['body'] for r in ddgs.text(f"STJ STF jurisprudência {termo}", max_results=2)])
    except: return ""

# --- 🧠 MOTOR SUPREME V4.5 (BLINDADO CONTRA ERRO DE CHAVE) ---
def aether_brain_supreme(prompt, modo, contexto, strict, double_check):
    contexto_ext = buscar_jurisprudencia(prompt[:50]) if double_check else ""
    
    # Tentativa 1: Groq (Principal)
    if "GROQ_API_KEY" in st.secrets:
        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            instrucao = "ATUAÇÃO: Auditor Harvard. Se Blindagem ON, inicie com '🚨 ALERTA DE RISCO CRÍTICO'." if strict else ""
            prompt_sys = f"Você é o AETHER OMNI v89.5. {instrucao} MODO: {modo}. REF: {contexto_ext} CTX: {contexto}"
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            st.warning(f"Motor Groq em espera. Acionando Backup...")

    # Tentativa 2: Gemini (Backup)
    if "GOOGLE_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro')
            res = model.generate_content(f"MODO AUDITORIA: {prompt}\nCONTEXTO: {contexto}")
            return res.text
        except Exception as e:
            return "🛡️ Erro: Ambas as chaves de IA (Groq/Google) falharam. Verifique seus Secrets."
    
    return "🛡️ Erro Crítico: Nenhuma Chave de API (GROQ ou GOOGLE) foi encontrada nos Secrets."

# --- 📂 INTERFACE ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #00c853;'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    st.caption("Strategic Intelligence | v89.5")
    st.divider()
    with st.expander("🛠️ PERÍCIA & COMPLIANCE", expanded=True):
        strict_mode = st.toggle("Modo Blindagem Patrimonial", value=True)
        check_vigencia = st.toggle("Double-Check Legislativo", value=True)
        ocr_active = st.toggle("Forense OpenCV", value=True)
    st.divider()
    funcao_elite = st.selectbox("Protocolo:", ["Scanner de Risco", "Auto-Minuta", "Due Diligence"])

st.title("🏢 Harvard Strategic Operations")

if MODO_MODERNO:
    aba_ativa = segmented_control(options=["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0)
else:
    aba_ativa = st.radio("Selecione:", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"])

if "Auditoria" in aba_ativa:
    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva o caso/contrato:", height=300)
        upload = st.file_uploader("Documento Base")

    with col_out:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            with st.spinner("Analisando com motor híbrido..."):
                cont = processar_arquivos(upload) if upload else ""
                res = aether_brain_supreme(user_input, funcao_elite, cont, strict_mode, check_vigencia)
                st.session_state['res_aether'] = res
                st.markdown(f"<div class='dossie-box'>{res}</div>", unsafe_allow_html=True)

        if 'res_aether' in st.session_state:
            st.divider()
            c1, c2, c3 = st.columns(3)
            if PDF_READY:
                with c1: st.download_button("📄 Baixar PDF", data=export_pdf(st.session_state['res_aether']), file_name="RELATORIO_AETHER.pdf")
            with c2: st.download_button("📝 Baixar Word", data=export_docx(st.session_state['res_aether']), file_name="RELATORIO_AETHER.docx")
            with c3: st.download_button("📑 Baixar TXT", data=st.session_state['res_aether'], file_name="RELATORIO_AETHER.txt")

elif "Forense" in aba_ativa:
    st.subheader("🔍 Perícia Forense (OpenCV)")
    p_file = st.file_uploader("Upload Assinatura", type=['png', 'jpg', 'jpeg'])
    if p_file and ocr_active:
        img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        st.image(edges, caption="Análise Forense de Traços", use_container_width=True)
