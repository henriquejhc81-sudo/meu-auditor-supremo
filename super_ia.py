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

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (FAVICON ANTIGO INSERIDO AQUI) ---
st.set_page_config(page_title="AETHER OMNI v93.3", page_icon="antigo_logo.jpg", layout="wide", initial_sidebar_state="collapsed")

# --- 🎨 DESIGN "SAAS ENTERPRISE" (CORREÇÃO DE BORDAS E LAYOUT) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Playfair+Display:wght@700&display=swap');
    
    /* Fundo Slate Profundo e Fontes */
    .stApp { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* 🛡️ CORREÇÃO DAS BORDAS BRANCAS DO LOGO */
    img[data-testid="stImage"] { border-radius: 25px; box-shadow: 0px 10px 30px rgba(0, 200, 83, 0.15); }
    
    /* Headers e Títulos */
    .header-container { margin-bottom: 30px; }
    .header-subtitle { letter-spacing: 4px; color: #888; font-size: 0.9rem; text-transform: uppercase; margin-top: 10px; font-weight: 600;}
    
    /* Estilização das Abas (Tabs) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #0a192f; border-radius: 8px 8px 0 0; color: #888; border: 1px solid #112240; border-bottom: none; padding: 0 30px; transition: all 0.3s ease; }
    .stTabs [aria-selected="true"] { background-color: #00c853 !important; color: #050a14 !important; font-weight: bold; border-color: #00c853; }
    
    /* Caixas de Texto e Uploads */
    .stTextArea textarea { background-color: #0a192f !important; color: #e6f1ff !important; border: 1px solid #112240 !important; border-radius: 8px; }
    .stTextArea textarea:focus { border-color: #00c853 !important; box-shadow: 0 0 5px rgba(0, 200, 83, 0.5) !important; }
    
    /* Dossiê Box Refinado */
    .dossie-box { background-color: #0a192f; padding: 40px; border-radius: 8px; color: #e6f1ff; line-height: 1.8; white-space: pre-wrap; font-family: 'Inter', sans-serif; border-top: 5px solid #00c853; border: 1px solid #112240; box-shadow: 0px 10px 30px rgba(0,0,0,0.5); }
    
    /* Estilo dos Botões */
    div.stButton > button { background-color: #00c853 !important; color: #050a14 !important; font-weight: 700 !important; border-radius: 8px !important; text-transform: uppercase !important; border: none !important; }
    div.stButton > button:hover { box-shadow: 0 5px 15px rgba(0, 200, 83, 0.3); }
    
    /* Botão de Reset Menor e Discreto */
    button[key="reset_btn"] { background-color: transparent !important; color: #888 !important; font-size: 0.8rem !important; border: 1px solid #112240 !important; width: auto !important; height: auto !important; padding: 5px 15px !important; margin-bottom: -20px; }
    button[key="reset_btn"]:hover { color: #00c853 !important; border-color: #00c853 !important; background-color: rgba(0, 200, 83, 0.1) !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 🛠️ FUNÇÕES TÉCNICAS PRESERVADAS ---
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
        prompt_sys = f"AETHER OMNI v93.3. Master Auditor Harvard. Use Art. 421-A CC. CTX: {contexto_ext} - {contexto}"
        completion = client.chat.completions.create(messages=[{"role": "system", "content": prompt_sys}, {"role": "user", "content": prompt}], model="llama-3.3-70b-versatile", temperature=0.1)
        return completion.choices[0].message.content
    except Exception as e_groq:
        print(f"Groq falhou: {e_groq}. Iniciando Gemini Auto-Healing...")
        if "GOOGLE_API_KEY" in st.secrets:
            try:
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-pro-latest') 
                return model.generate_content(f"MASTER: {prompt}\nCTX: {contexto}").text
            except Exception as e_gemini:
                return f"Erro Crítico. Groq: {e_groq} | Gemini: {e_gemini}"
        return "Erro de conexão segura."

# --- 🚀 HEADER CENTRALIZADO (CORRIGIDO) ---
st.markdown("<div class='header-container'>", unsafe_allow_html=True)

# 1. Botão de Reset limpo e organizado no canto
col_btn, col_vazia = st.columns([1, 10])
with col_btn:
    if st.button("🔄 System Reset", key="reset_btn"):
        st.session_state.clear()
        st.rerun()

# 2. Logo
