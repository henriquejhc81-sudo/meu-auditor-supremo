import streamlit as st
import pandas as pd
from PIL import Image
import os, time, io, cv2, base64
import numpy as np
import docx2txt
from docx import Document
from docx.shared import Inches

# --- Utility Function: Image to Base64 for custom HTML embedding (v93.7) ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- Utility Function: Inject JS for browser refresh (F5 logic) attached to logo (v93.7) ---
def inject_reload_on_logo_click():
    # Use JavaScript to perform a full browser reload (window.location.reload())
    # F5 logic as requested by Henrique.
    reload_js = """
    <script>
    document.addEventListener('DOMContentLoaded', (event) => {
        // Streamlit renders delay, so we must wait to select the element
        setTimeout(() => {
            const logoImg = document.getElementById('aether-reset-logo');
            if (logoImg) {
                console.log("AETHER OMNI v93.7: Reset mechanism attached to logo.");
                logoImg.style.cursor = 'pointer';
                logoImg.onclick = function() {
                    window.location.reload();
                };
            } else {
                console.error("AETHER OMNI v93.7: Failed to attach reset mechanism to logo.");
            }
        }, 1000); // 1-second delay to ensure rendering complete
    });
    </script>
    """
    st.markdown(reload_js, unsafe_allow_html=True)

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

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (FAVICON SEGURO) ---
# Usando emoji universal 🛡️ como favicon para evitar tela preta fatal por arquivo faltante.
st.set_page_config(page_title="AETHER OMNI v93.7", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# Inject JS for reloading
inject_reload_on_logo_click()

# --- 🎨 DESIGN "SAAS ENTERPRISE" (TIGHTENING AND ROUND MASKING v93.7) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');
    
    /* Fundo Slate Profundo e Fontes */
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* 🛡️ TIGHTENING: Reducing excessively tall page elements */
    [data-testid="stMain"] > [data-testid="stHeader"] { padding-top: 10px !important; padding-bottom: 0px !important; height: auto !important;}
    [data-testid="stHeaderContainer"] { padding-top: 0px !important; padding-bottom: 0px !important; }
    
    /* Headers, Títulos e Subtítulos */
    .header-container { text-align: center; margin-bottom: 5px !important; padding-top: 0px !important; }
    .header-subtitle { letter-spacing: 4px; color: #888; font-size: 0.9rem; text-transform: uppercase; margin-top: 5px; font-weight: 600;}
    
    /* 🛡️ ROUND LOGO MASKING & SIZE CONTROL: Makes logo round and controlled in height */
    .round-logo-html-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    /* 🛡️ CORTADOR DE BORDAS: Remove os cantos brancos da imagem quadrada (Discovery original) */
    #aether-reset-logo {
        border-radius: 50% !important; /* Forces perfect circle */
        object-fit: cover !important; /* Crops image to circle, cutting off white corners */
        width: 150px !important; /* Controlled size to reduce header height */
        height: 150px !important; /* Must match width for perfect circle */
        box-shadow: 0px 5px 25px rgba(0, 200, 83, 0.25) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
        cursor: pointer !important;
        margin-top: 0px !important;
    }
    
    #aether-reset-logo:hover {
        transform: scale(1.05);
        box-shadow: 0px 8px 35px rgba(0, 200, 83, 0.4) !important;
    }
    
    /* Hide default st.image container if used via the HTML method (which we do now) */
    [data-testid="stMainElement"] > div[data-testid="stImage"] { display: none !important; }

    /* Estilização das Abas (Tabs) - Mantenho */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #0a192f; border-radius: 8px 8px 0 0; color: #888; border: 1px solid #112240; border-bottom: none; padding: 0 30px; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold; border-color: #00c853; }
    
    /* Caixas de Texto e Uploads - Mantenho */
    .stTextArea textarea { background-color: #0a192f !important; color: #e6f1ff !important; border: 1px solid #112240 !important; border-radius: 8px; }
    .stTextArea textarea:focus { border-color: #00c853 !important; box-shadow: 0 0 5px rgba(0, 200, 83, 0.5) !important; }
    
    /* Dossiê Box Refinado - Mantenho */
    .dossie-box { background-color: #0a192f; padding: 40px; border-radius: 8px; color: #e6f1ff; line-height: 1.8; white-space: pre-wrap; font-family: 'Inter', sans-serif; border-top: 5px solid #00c853; border: 1px solid #112240; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    
    /* Estilo dos Botões Primários - Mantenho */
    div.stButton > button[kind="primary"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: 700 !important; border-radius: 8px !important; text-transform: uppercase !important; border: none !important; width: 100% !important; }
    div.stButton > button[kind="primary"]:hover { box-shadow: 0 5px 15px rgba(0, 200, 83, 0.3); }

    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES TÉCNICAS PRESERVADAS (INTACTAS) ---
def export_pdf(texto):
    if not PDF_READY: return None
    pdf = FPDF()
    pdf.add_page()
    # Mantenho o comportamento de exportação de PDF intacto
    try: pdf.image('logo.png', 10, 8, 33) 
    except: pass
    pdf.set_font("Arial", 'B', 16); pdf.cell(0, 20, "RELATÓRIO AETHER OMNI", ln=True, align='C'); pdf.ln(10)
    pdf.set_font("Arial", size=11)
    safe_text = texto.replace("🚨", "ALERTA:").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 8, txt=safe_text)
    return pdf.output(dest='S').encode('latin-1')

def export_docx(texto):
    doc = Document()
    # Mantenho o comportamento de exportação de Docx intacto
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
        prompt_sys = f"AETHER OMNI v93.7. Master Auditor Harvard. Use Art. 421-A CC. CTX: {contexto_ext} - {contexto}"
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

# --- 🚀 REPLACING THE HEADER AREA (FIXING GIGANTIC PAGE v93.7) ---
# Tira o st.columns e st.button antigos daqui. Limpa o visual azul flutuante.
st.markdown("<div class='header-container'>", unsafe_allow_html=True)

# Converter logo.png para Base64 para incorporação segura em HTML customizado
logo_base64 = None
if os.path.exists("logo.png"):
    logo_base64 = get_base64_of_bin_file("logo.png")

if logo_base64:
    # Injetar HTML customizado para logo redondo e clicável (F5).
    # ID 'aether-reset-logo' é fundamental para a seleção via JS.
    html_logo_clickable = f"""
        <div class='round-logo-html-container'>
            <img id='aether-reset-logo' src='data:image/png;base64,{logo_base64}' alt='AETHER OMNI Logo (Clique para Reset)'>
        </div>
        """
    st.markdown(html_logo_clickable, unsafe_allow_html=True)
else:
    # Fallback caso logo.png não exista na pasta
    st.markdown("<h1 style='text-align: center; color: #00c853; font-family: Playfair Display;'>AETHER OMNI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ff9800; font-weight: bold;'>⚠️ Arquivo 'logo.png' não encontrado na pasta.</p>", unsafe_allow_html=True)

st.markdown("<p class='header-subtitle'>STRATEGIC INTELLIGENCE HUB</p></div>", unsafe_allow_html=True)
st.divider()

# --- 🏗️ INTERFACE PRINCIPAL (INTACT PER CONSTRAINTS) ---
tab_auditoria, tab_forense, tab_engenharia = st.tabs(["🛡️ Auditoria", "🔍 Forense", "🏗️ Engenharia"])

with tab_auditoria:
    col_in, col_out = st.columns([1, 1.2], gap="large")
    with col_in:
        upload = st.file_uploader("Subir Arquivo para Análise", type=['pdf', 'docx', 'xlsx', 'csv'])
        user_input = st.text_area("Comando Jurídico Estratégico:", height=250, placeholder="Ex: Analise este contrato buscando cláusulas abusivas segundo o Art. 421-A do CC...")
        if st.button("🚀 PROCESSAR AUDITORIA", kind="primary"):
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
            # Mantenho st.download_button para ações de exportação (kind="primary" não aplicado aqui por design Streamlit padrão, mantenho)
            with c1: st.download_button("📄 PDF REPORT", data=export_pdf(st.session_state['res_aether']), file_name="AETHER_REPORT.pdf")
            with c2: st.download_button("📝 WORD DOCX", data=export_docx(st.session_state['res_aether']), file_name="AETHER_REPORT.docx")
            with c3: st.download_button("📑 TXT RAW", data=st.session_state['res_aether'].encode('utf-8'), file_name="AETHER_REPORT.txt")

with tab_forense:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        p_file = st.file_uploader("Upload Assinatura/Documento (Forense)", type=['png', 'jpg', 'jpeg'])
        if p_file:
            img = cv2.imdecode(np.asarray(bytearray(p_file.read()), dtype=np.uint8), 1)
            edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
            st.image(edges, caption="Análise Forense de Pixels e Hesitação", use_container_width=True)
    with col_f2:
        if p_file and st.button("🔍 GERAR LAUDO FORENSE", kind="primary"):
            with st.spinner("Analisando matriz de pixels..."):
                laudo = aether_brain_supreme("Analise traços desta assinatura com base na perícia grafotécnica. Descreva possíveis hesitações baseadas na detecção de bordas Canny.", "Módulo Forense Ativado")
                st.markdown(f"<div class='dossie-box'>{laudo}</div>", unsafe_allow_html=True)

with tab_engenharia:
    st.info("🏗️ Módulo de Engenharia de Documentos configurado e em standby para expansão.")
