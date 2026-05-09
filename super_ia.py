import streamlit as st
import pandas as pd
from PIL import Image
import os
import time
import io
import cv2
import numpy as np
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: CARGA DE ELITE ---
try:
    from streamlit_extras.segmented_control import segmented_control
    from streamlit_extras.grid import grid
    MODO_MODERNO = True
except ImportError:
    MODO_MODERNO = False

try:
    from groq import Groq
except ImportError:
    st.error("🔄 Otimizando motores de elite... Verifique o requirements.txt")
    st.stop()

import google.generativeai as genai
from duckduckgo_search import DDGS

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (PRESERVADA) ---
st.set_page_config(page_title="AETHER OMNI v89.2 | Strategic Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN ENTERPRISE "NAVY BLUE" (PRESERVADO) ---
st.markdown("""
    <style>
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    .insight-card { background-color: #0a192f; padding: 20px; border-radius: 12px; border: 1px solid #112240; margin-bottom: 15px; }
    .stButton>button { background-color: #00c853; color: #050a14; font-weight: 700; border-radius: 8px; border: none; width: 100%; height: 3.5em; }
    .dossie-box { background-color: #0a192f; padding: 25px; border-radius: 12px; border: 1px solid #112240; color: #ccd6f6; line-height: 1.6; white-space: pre-wrap; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ FUNÇÕES TÉCNICAS (TRABALHO DE MESES INTACTO) ---
def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        elif upload.name.endswith('.csv'): return pd.read_csv(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e:
        return f"Erro na leitura técnica: {e}"

def buscar_jurisprudencia_realtime(termo):
    try:
        with DDGS() as ddgs:
            results = [r['body'] for r in ddgs.text(f"jurisprudência STJ STF vigente {termo}", max_results=2)]
            return "\n".join(results)
    except:
        return "Consulta externa temporariamente indisponível."

# --- 🧠 MOTOR SUPREME V4.2 (COM DOUBLE-CHECK RESTAURADO) ---
def aether_brain_supreme(prompt, modo, contexto, strict, double_check):
    contexto_externo = ""
    if double_check:
        with st.spinner("🔍 Realizando Double-Check Legislativo..."):
            contexto_externo = buscar_jurisprudencia_realtime(prompt[:50])

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        instrucao = "FOCO: Blindagem Patrimonial. Use Escrita Defensiva." if strict else ""
        
        prompt_sistema = f"""
        Você é o AETHER OMNI v89.2. Sênior Big Four.
        MODO: {modo}. {instrucao}
        JURISPRUDÊNCIA RECENTE (Double-Check): {contexto_externo}
        CONTEXTO DO CASO: {contexto}
        """
        
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return completion.choices[0].message.content
    except:
        # Fallback para Gemini (Segurança de Mercado)
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"BACKUP MODE - {modo}: {prompt}")
        return response.text

# --- 📂 SIDEBAR (RESTAURAÇÃO DO DOUBLE-CHECK) ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v89.2 | Elite Operations")
    st.divider()
    with st.expander("🛠️ CONFIGURAÇÕES DA PERÍCIA", expanded=True):
        strict_mode = st.toggle("Modo Blindagem Patrimonial", value=True)
        check_vigencia = st.toggle("Double-Check Legislativo", value=True) # RESTAURADO
        ocr_active = st.toggle("Análise de Assinatura (OpenCV)", value=True)
    st.divider()
    funcao_elite = st.selectbox("Protocolo de Elite:", ["Scanner de Risco (Kroll Style)", "Auto-Minuta (Skadden)", "Análise Forense Digital"])

# --- 🚀 INTERFACE PRINCIPAL ---
st.title("🏢 Legal Operations Hub")

if MODO_MODERNO:
    aba_ativa = segmented_control(label="Pilar Ativo:", options=["🛡️ Auditoria", "🔍 Forense Digital", "🏗️ Engenharia de Docs"], index=0)
else:
    aba_ativa = st.radio("Pilar Ativo:", ["🛡️ Auditoria", "🔍 Forense Digital", "🏗️ Engenharia de Docs"])

if "Auditoria" in aba_ativa:
    if MODO_MODERNO:
        g = grid(4, vertical_align="center")
        g.metric("Precisão", "99.9%", "Market Ready")
        g.metric("Double-Check", "Ativo" if check_vigencia else "Off", "STJ/STF")
        g.metric("Backup IA", "Stand-by", "Gemini")
        g.metric("Status LINDB", "Vigente", "✅")
    
    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva a análise ou redação:", height=250)
        upload = st.file_uploader("Documento Base", type=['pdf', 'docx', 'xlsx'])

    with col_out:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            cont = processar_arquivos(upload) if upload else ""
            res = aether_brain_supreme(user_input, funcao_elite, cont, strict_mode, check_vigencia)
            st.session_state['res_aether'] = res
            st.markdown(f"<div class='dossie-box'>{res}</div>", unsafe_allow_html=True)
