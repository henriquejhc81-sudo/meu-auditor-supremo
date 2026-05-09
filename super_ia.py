import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: IMPORTAÇÕES ---
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

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA ---
st.set_page_config(page_title="AETHER OMNI v89.8 | Strategic Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN "HIGH-END CORPORATE" (HARVARD + NAVY LEGACY) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    
    .dossie-box { 
        background-color: #ffffff; 
        padding: 50px; 
        border-radius: 2px; 
        color: #1a1a1a; 
        line-height: 1.8; 
        white-space: pre-wrap; 
        font-family: 'Georgia', serif; 
        border-top: 15px solid #85142b; 
        box-shadow: 0px 15px 35px rgba(0,0,0,0.6);
        margin: 20px auto;
        max-width: 900px;
    }
    
    .stButton>button { 
        background-color: #00c853; color: #050a14; font-weight: 700; 
        border-radius: 4px; height: 3.5em; text-transform: uppercase; letter-spacing: 1px;
    }
    
    .insight-card { 
        background-color: #0a192f; padding: 15px; border-radius: 8px; 
        border-left: 5px solid #00c853; border: 1px solid #112240; margin-bottom: 10px; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES DE EXPORTAÇÃO (CORREÇÃO DE ENCODING & DESIGN) ---
def gerar_relatorio_pdf(texto):
    if not PDF_READY: return None
    pdf = FPDF()
    pdf.add_page()
    # Tenta carregar logo se existir
    try: pdf.image('logo.png', 10, 8, 33) 
    except: pass
    
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 20, "RELATÓRIO DE AUDITORIA ESTRATÉGICA", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    # Limpeza de interrogações: Substitui emojis por texto seguro para o PDF padrão
    safe_text = texto.replace("🚨", "ALERTA:").replace("⚠️", "NOTA:").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')

def gerar_relatorio_docx(texto):
    doc = Document()
    try: doc.add_picture('logo.png', width=Inches(1.5))
    except: pass
    doc.add_heading('AETHER OMNI | Strategic Intelligence', 0)
    doc.add_paragraph(texto)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- ⚙️ FUNÇÕES TÉCNICAS (PRESERVADAS) ---
def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e: return f"Erro técnico: {e}"

# --- 🧠 MOTOR HÍBRIDO SUPREME V4.8 (MASTER) ---
def aether_brain_supreme(prompt, modo, contexto, strict, double_check):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        instrucao = "🚨 ALERTA DE RISCO CRÍTICO: Atue como Auditor Sênior Harvard. Use escrita defensiva e Art. 421-A CC." if strict else ""
        prompt_sys = f"AETHER OMNI v89.8. {instrucao} MODO: {modo}. CTX: {contexto}"
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", temperature=0.1
        )
        return completion.choices[0].message.content
    except:
        if "GOOGLE_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro')
            res = model.generate_content(f"{modo}: {prompt}\nContexto: {contexto}")
            return res.text
        return "Erro de conexão com as redes neurais."

# --- 📂 INTERFACE ---
with st.sidebar:
    # Área da Logo no Sidebar
    try: st.image("logo.png", width=150)
    except: st.markdown("<h1 style='color: #00c853;'>🛡️ AETHER</h1>", unsafe_allow_html=True)
    
    st.caption("Strategic Intelligence | v89.8")
    st.divider()
    with st.expander("🛠️ PERÍCIA & COMPLIANCE", expanded=True):
        strict_mode = st.toggle("Modo Blindagem Patrimonial", value=True)
        ocr_active = st.toggle("Forense OpenCV", value=True)
    funcao_elite = st.selectbox("Protocolo:", ["Scanner de Risco", "Auto-Minuta", "Laudo Pericial"])

st.title("🏢 Strategic Operations Center")

if MODO_MODERNO:
    aba_ativa = segmented_control(options=["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"], index=0)
else:
    aba_ativa = st.radio("Pilar:", ["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"])

if "Auditoria" in aba_ativa:
    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva o caso/contrato:", height=300)
        upload = st.file_uploader("Documento Base")
    with col_out:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            res = aether_brain_supreme(user_input, funcao_elite, processar_arquivos(upload) if upload else "", strict_mode, False)
            st.session_state['res_aether'] = res
            # Exibição no estilo papel timbrado
            st.markdown(f"<div class='dossie-box'>{res}</div>", unsafe_allow_html=True)

        if 'res_aether' in st.session_state:
            st.divider()
            c1, c2 = st.columns(2)
            with c1: st.download_button("📄 Baixar PDF Profissional", data=gerar_relatorio_pdf(st.session_state['res_aether']), file_name="RELATORIO_AETHER.pdf")
            with c2: st.download_button("📝 Baixar Word (Editável)", data=gerar_relatorio_docx(st.session_state['res_aether']), file_name="RELATORIO_AETHER.docx")

elif "Forense" in aba_ativa:
    st.subheader("🔍 Perícia Grafotécnica Digital")
    p_file = st.file_uploader("Upload Assinatura", type=['png', 'jpg'])
    if p_file and ocr_active:
        img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        st.image(edges, caption="Análise Forense de Traços", use_container_width=True)
        if st.button("GERAR LAUDO DE FRAUDE"):
            laudo = aether_brain_supreme("Analise os traços desta assinatura. Procure por hesitação.", "Laudo Forense", "Assinatura OpenCV", True, False)
            st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)
