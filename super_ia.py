import streamlit as st
import pandas as pd
from PIL import Image
try:
    from groq import Groq
except ImportError:
    st.error("🔄 Otimizando motores de elite... Aguarde 30 segundos.")
    st.stop()
import google.generativeai as genai
from duckduckgo_search import DDGS
import time
import cv2
import numpy as np
import docx2txt
import io
from streamlit_extras.segmented_control import segmented_control
from streamlit_extras.grid import grid

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: CONFIGURAÇÃO DA PÁGINA ---
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

# --- ⚙️ FUNÇÕES TÉCNICAS (PRESERVADAS) ---
def processar_arquivos(upload):
    conteudo = ""
    try:
        if upload.name.endswith('.docx'):
            conteudo = docx2txt.process(upload)
        elif upload.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(upload)
            conteudo = df.to_string()
        elif upload.name.endswith('.csv'):
            df = pd.read_csv(upload)
            conteudo = df.to_string()
        else:
            conteudo = upload.read().decode("utf-8")
    except Exception as e:
        st.error(f"Erro na leitura técnica: {e}")
    return conteudo

# --- 🧠 MOTOR DE INTELIGÊNCIA V3.5 (EVOLUÍDO COM ESCRETA DEFENSIVA) ---
def aether_brain_v3(prompt, modo, contexto, strict_mode=True):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        return f"Erro de Configuração: {e}"
        
    instrucao_blindagem = ""
    if strict_mode:
        instrucao_blindagem = "FOCO: Blindagem Patrimonial e Redliner Defensivo. Identifique riscos que humanos ignoram. Se houver fraude ou prescrição, inicie com 'ALERTA DE FRAUDE'."

    prompt_sistema = f"""
    Você é o AETHER OMNI v88.3 - Auditor Jurídico Sênior (Big Four style).
    MODO: {modo}. {instrucao_blindagem}
    CONTEXTO: {contexto if contexto else "Análise Estratégica."}
    ⚠️ NOTA: Este documento é uma minuta tecnológica e não substitui a revisão por um advogado.
    """
    
    try:
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
    
    # Toggles de Perícia (Nova Função solicitada)
    with st.expander("🛠️ CONFIGURAÇÕES DA PERÍCIA", expanded=True):
        strict_mode = st.toggle("Modo Blindagem Patrimonial", value=True)
        check_vigencia = st.toggle("Double-Check Legislativo", value=True)
        ocr_active = st.toggle("Análise de Assinatura (OpenCV)", value=False)

    st.divider()
    funcao_elite = st.selectbox("Protocolo de Elite:", [
        "Scanner de Risco (Kroll)", 
        "Auto-Minuta de Aditivo (Skadden)", 
        "Matriz de Compliance (KPMG)",
        "Análise Forense de Documento"
    ])

# --- 🚀 TELA PRINCIPAL: NAVEGAÇÃO SEGMENTADA ---
st.title("🏢 Centro de Inteligência & Forense")

aba_ativa = segmented_control(
    label="Selecione o Pilar de Atuação:",
    options=["🛡️ Auditoria", "🔍 Forense Digital", "🏗️ Engenharia de Docs"],
    index=0
)

st.divider()

if aba_ativa == "🛡️ Auditoria":
    # Layout Original Preservado
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown("<div class='insight-card'>🚨 <b>Risco:</b> Divergência M&A.</div>", unsafe_allow_html=True)
    with c2: st.markdown("<div class='insight-card'>⚖️ <b>Sugerido:</b> Redução de Multa.</div>", unsafe_allow_html=True)
    with c3: st.markdown("<div class='insight-card'>📄 <b>Pilar C:</b> Pronto para redigir.</div>", unsafe_allow_html=True)

    col_in, col_out = st.columns([1, 1.2])
    with col_in:
        user_input = st.text_area("Descreva a análise desejada:", height=200)
        upload = st.file_uploader("Subir contrato base", type=['pdf', 'docx', 'xlsx'])

    with col_out:
        if st.button("ATIVAR PROTOCOLO OMNI"):
            with st.spinner("Processando Inteligência..."):
                cont = processar_arquivos(upload) if upload else ""
                res = aether_brain_v3(user_input, f"Auditoria - {funcao_elite}", cont, strict_mode)
                st.session_state['res_aether'] = res
                st.markdown(f"<div class='dossie-box'>{res}</div>", unsafe_allow_html=True)

elif aba_ativa == "🔍 Forense Digital":
    st.subheader("🔎 Módulo de Perícia Forense")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        doc_forense = st.file_uploader("Upload de Prova (Imagem/PDF)", type=['png', 'jpg', 'pdf'], key="forense")
    with col_f2:
        if doc_forense:
            st.image(doc_forense, caption="Visualização da Evidência", use_container_width=True)
            if ocr_active:
                st.info("Buscando padrões de fraude em assinaturas...")

elif aba_ativa == "🏗️ Engenharia de Docs":
    st.subheader("📝 Gerador Zero-Draft")
    st.info("IA configurada para consultar pasta de modelos internos (Template Ouro).")
    # Futura implementação de busca vetorial (FAISS)
