import streamlit as st
import pandas as pd
from PIL import Image
import os

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: IMPORTAÇÃO BLINDADA ---
try:
    from streamlit_extras.segmented_control import segmented_control
    MODO_MODERNO = True
except ImportError:
    MODO_MODERNO = False

try:
    from groq import Groq
except ImportError:
    st.error("🔄 Aguardando instalação das dependências de elite no servidor...")
    st.stop()

import google.generativeai as genai
from duckduckgo_search import DDGS
import time
import cv2
import numpy as np
import docx2txt
import io

# --- 🛡️ CONFIGURAÇÃO DE PÁGINA (MANTIDA) ---
st.set_page_config(page_title="AETHER OMNI v88.3 | Legal Ops Hub", page_icon="🛡️", layout="wide")

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

# --- ⚙️ FUNÇÕES TÉCNICAS (PRESERVADAS DE MESES DE TRABALHO) ---
def processar_arquivos(upload):
    try:
        if upload.name.endswith('.docx'): return docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')): return pd.read_excel(upload).to_string()
        elif upload.name.endswith('.csv'): return pd.read_csv(upload).to_string()
        else: return upload.read().decode("utf-8")
    except Exception as e:
        return f"Erro na leitura técnica: {e}"

# --- 🧠 MOTOR DE INTELIGÊNCIA V3.5 ---
def aether_brain_v3(prompt, modo, contexto, strict_mode=True):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        instrucao_blindagem = "FOCO: Blindagem Patrimonial. Se houver fraude, inicie com 'ALERTA'." if strict_mode else ""
        
        prompt_sistema = f"Você é o AETHER OMNI v88.3. MODO: {modo}. {instrucao_blindagem}"
        
        completion = client.chat.completions.create(
            messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na rede neural: {e}"

# --- 📂 SIDEBAR EVOLUÍDA ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v88.3 | Legal Operations Hub")
    st.divider()
    
    with st.expander("🛠️ CONFIGURAÇÕES DA PERÍCIA", expanded=True):
        strict_mode = st.toggle("Modo Blindagem Patrimonial", value=True)
        ocr_active = st.toggle("Análise de Assinatura (OpenCV)", value=False)

    st.divider()
    funcao_elite = st.selectbox("Protocolo de Elite:", ["Scanner de Risco (Kroll)", "Auto-Minuta (Skadden)", "Matriz de Compliance (KPMG)"])

# --- 🚀 TELA PRINCIPAL: NAVEGAÇÃO SEGMENTADA (EVOLUÇÃO) ---
st.title("🏢 Centro de Inteligência & Forense")

if MODO_MODERNO:
    aba_ativa = segmented_control(
        label="Selecione o Pilar de Atuação:",
        options=["🛡️ Auditoria", "🔍 Forense Digital", "🏗️ Engenharia de Docs"],
        index=0
    )
else:
    aba_ativa = st.radio("Pilar de Atuação (Modo Recuperação):", ["🛡️ Auditoria", "🔍 Forense Digital", "🏗️ Engenharia de Docs"])

st.divider()

# --- 🛡️ MÓDULO DE AUDITORIA (TRABALHO PRESERVADO) ---
if "Auditoria" in aba_ativa:
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='insight-card'>🚨 <b>Risco:</b> Divergência M&A.</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='insight-card'>⚖️ <b>Sugerido:</b> Redução de Multa.</div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='insight-card'>📄 <b>Status:</b> Pronto para redigir.</div>", unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva a análise:", height=200)
        upload = st.file_uploader("Subir contrato base", type=['pdf', 'docx', 'xlsx'])

    with col_out:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            with st.spinner("Processando..."):
                cont = processar_arquivos(upload) if upload else ""
                res = aether_brain_v3(user_input, funcao_elite, cont, strict_mode)
                st.session_state['res_aether'] = res
                st.markdown(f"<div class='dossie-box'>{res}</div>", unsafe_allow_html=True)

# --- 🔍 MÓDULO FORENSE (NOVO CORE) ---
elif "Forense" in aba_ativa:
    st.subheader("🔎 Módulo de Perícia Forense")
    doc_forense = st.file_uploader("Upload de Prova", type=['png', 'jpg', 'pdf'])
    if doc_forense:
        st.image(doc_forense, caption="Evidência", width=400)
        if ocr_active:
            st.warning("Motor OpenCV aguardando comando de análise de pixels...")

# --- 🏗️ MÓDULO ENGENHARIA (FUTURO) ---
elif "Engenharia" in aba_ativa:
    st.subheader("📝 Gerador Zero-Draft")
    st.info("Módulo pronto para receber a biblioteca FAISS e seus Modelos Ouro.")
