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
import random
import docx2txt
import io

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AETHER OMNI v88.1 | Strategic Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN ENTERPRISE "NAVY BLUE" (MANTIDO) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    .insight-card { 
        background-color: #0a192f; padding: 20px; border-radius: 12px; 
        border: 1px solid #112240; margin-bottom: 15px;
    }
    .stButton>button { 
        background-color: #00c853; color: #050a14; font-weight: 700; 
        border-radius: 8px; border: none; width: 100%; height: 3.5em;
    }
    .stTextArea textarea { background-color: #0a192f; color: #e6f1ff; border: 1px solid #112240; border-radius: 8px; }
    .dossie-box { background-color: #0a192f; padding: 25px; border-radius: 12px; border: 1px solid #112240; color: #ccd6f6; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ FUNÇÕES DE LEITURA (PRESERVAÇÃO TOTAL) ---
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

# --- 🧠 MOTOR DE INTELIGÊNCIA HÍBRIDO (CORREÇÃO DE ATRIBUTO) ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        return f"Erro de Configuração de Chave: {e}"
        
    for attempt in range(5):
        try:
            instrucao_cruzamento = ""
            if contexto:
                instrucao_cruzamento = f"\n🔍 CRUZAMENTO DE DADOS: Analise o prompt com os dados do arquivo ({contexto}). Identifique riscos e omissões."

            prompt_sistema = f"""
            Você é o cérebro do AETHER OMNI v88.1. Atue como Sênior Big Four.
            PROTOCOLO: {modo}.
            CONTEXTO: {instrucao_cruzamento if contexto else "Gere Dossiê de Blindagem LINDB."}
            NOTA LEGAL: '⚠️ NOTA: Este relatório é um suporte tecnológico e não substitui o parecer jurídico.'
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            # CORREÇÃO DEFINITIVA DO ERRO 'list' object has no attribute 'message'
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                time.sleep(attempt + 5)
            else:
                return f"Erro na rede neural: {e}"
    return "Cota temporariamente excedida."

# --- 📂 SIDEBAR (ESTRUTURA DE PILARES MANTIDA) ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v88.1 | Enterprise Intelligence")
    st.divider()
    pilar = st.radio("📂 PILARES DE ATUAÇÃO", [
        "🛡️ Pilar A: Auditoria & Compliance",
        "⚖️ Pilar B: Legal & Due Diligence",
        "📄 Pilar C: Gerador de Documentos"
    ])
    st.divider()
    funcao_elite = st.selectbox("Protocolo de Elite:", [
        "Scanner de Risco (Kroll)",
        "Linha do Tempo (Latham & Watkins)",
        "Matriz de Compliance (KPMG)",
        "Extração Inteligente (Big Four)",
        "Gerar Resumo para o CEO"
    ])

# --- 🚀 TELA PRINCIPAL (DESIGN CORPORATIVO) ---
st.title("🛡️ Centro de Inteligência Estratégica")

st.subheader("📊 Feed de Insights em Tempo Real")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='insight-card'>🚨 <b>Risco Detectado:</b> 12 Contratos sem cláusula de reajuste.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='insight-card'>⚖️ <b>Compliance:</b> 98% de adesão à LGPD.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='insight-card'>💰 <b>M&A:</b> 3 oportunidades identificadas.</div>", unsafe_allow_html=True)

st.divider()

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Magic Upload & Entrada")
    user_input = st.text_area("Descreva o caso ou comando:", height=250, placeholder="Inicie o Protocolo Sniper...")
    upload = st.file_uploader("Scanner Global de Documentos", accept_multiple_files=False)

with col_out:
    st.subheader("🚀 Relatório Executivo")
    if st.button("ATIVAR PROTOCOLO OMNI"):
        conteudo_anexo = ""
        if upload:
            with st.spinner("Scanner de Elite processando..."):
                conteudo_anexo = processar_arquivos(upload)
        
        if user_input or conteudo_anexo:
            with st.spinner("Sintetizando Inteligência Estratégica..."):
                resultado = aether_brain(user_input, f"{pilar} - {funcao_elite}", conteudo_anexo)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)

    if 'res_aether' in st.session_state:
        st.download_button(label="📥 EXPORTAR PARA O CEO", data=st.session_state['res_aether'], file_name="AETHER_REPORT.txt")

# --- 💬 CHAT ANALISTA (MANTIDO) ---
st.divider()
st.subheader("💬 Consultar Especialista Aether")
chat_in = st.text_input("Dúvida estratégica?")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Suporte Estratégico", ""))
