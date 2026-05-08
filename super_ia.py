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
st.set_page_config(page_title="AETHER OMNI v88.2 | Strategic Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN ENTERPRISE "NAVY BLUE" (MANTIDO) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; }
    .insight-card { background-color: #0a192f; padding: 20px; border-radius: 12px; border: 1px solid #112240; margin-bottom: 15px; }
    .stButton>button { background-color: #00c853; color: #050a14; font-weight: 700; border-radius: 8px; border: none; width: 100%; height: 3.5em; }
    .stTextArea textarea { background-color: #0a192f; color: #e6f1ff; border: 1px solid #112240; border-radius: 8px; }
    .dossie-box { background-color: #0a192f; padding: 25px; border-radius: 12px; border: 1px solid #112240; color: #ccd6f6; line-height: 1.6; white-space: pre-wrap; }
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

# --- 🧠 MOTOR DE INTELIGÊNCIA HÍBRIDO (MÉTODO ADITIVO - PILAR C) ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        return f"Erro de Configuração: {e}"
        
    for attempt in range(5):
        try:
            # LÓGICA DE GERAÇÃO DE DOCUMENTOS (NOVA FUNÇÃO PILAR C)
            instrucao_documento = ""
            if "Gerador de Documentos" in modo:
                instrucao_documento = "MISSÃO: Gere uma MINUTA DE ADITIVO CONTRATUAL ou DOCUMENTO FORMAL. Use linguagem jurídica de alto nível, cite cláusulas padrão e fundamente na LINDB e Código Civil."
            
            prompt_sistema = f"""
            Você é o AETHER OMNI v88.2. Atue como Sênior Big Four / Skadden Arps.
            MODO: {modo}.
            {instrucao_documento}
            CONTEXTO: {contexto if contexto else "Análise Estratégica Geral."}
            NOTA LEGAL: '⚠️ NOTA: Este documento é uma minuta de suporte tecnológico e não substitui a revisão por um advogado.'
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            return completion.choices.message.content
        except Exception as e:
            if "429" in str(e): time.sleep(attempt + 5)
            else: return f"Erro na rede neural: {e}"
    return "Cota excedida."

# --- 📂 SIDEBAR (PILARES MANTIDOS) ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v88.2 | Elite Intelligence")
    st.divider()
    pilar = st.radio("📂 PILARES DE ATUAÇÃO", [
        "🛡️ Pilar A: Auditoria & Compliance",
        "⚖️ Pilar B: Legal & Due Diligence",
        "📄 Pilar C: Gerador de Documentos" # FOCO DESTA ATUALIZAÇÃO
    ])
    st.divider()
    funcao_elite = st.selectbox("Protocolo de Elite:", [
        "Scanner de Risco (Kroll)",
        "Auto-Minuta de Aditivo (Skadden)", # NOVA FUNÇÃO
        "Matriz de Compliance (KPMG)",
        "Gerar Resumo para o CEO"
    ])

# --- 🚀 TELA PRINCIPAL ---
st.title("🛡️ Centro de Inteligência Estratégica")

st.subheader("📊 Feed de Insights em Tempo Real")
c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='insight-card'>🚨 <b>Risco:</b> Divergência detectada no contrato M&A.</div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='insight-card'>⚖️ <b>Sugerido:</b> Gerar Aditivo de Redução de Multa.</div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='insight-card'>📄 <b>Pilar C:</b> Pronto para redigir minuta formal.</div>", unsafe_allow_html=True)

st.divider()

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Magic Upload & Comando")
    user_input = st.text_area("Descreva o que deseja redigir ou analisar:", height=250, placeholder="Ex: Gere o aditivo para reduzir a multa para R$ 100k...")
    upload = st.file_uploader("Subir contrato base", accept_multiple_files=False)

with col_out:
    st.subheader("🚀 Entrega de Elite")
    if st.button("ATIVAR PROTOCOLO OMNI"):
        conteudo_anexo = ""
        if upload:
            with st.spinner("Lendo contrato base..."):
                conteudo_anexo = processar_arquivos(upload)
        
        if user_input or conteudo_anexo:
            with st.spinner("Gerando documento de blindagem..."):
                resultado = aether_brain(user_input, f"{pilar} - {funcao_elite}", conteudo_anexo)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)

    if 'res_aether' in st.session_state:
        st.download_button(label="📥 EXPORTAR DOCUMENTO / ADITIVO", data=st.session_state['res_aether'], file_name="AETHER_DOC_FINAL.txt")

st.divider()
st.subheader("💬 Consultar Especialista Aether")
chat_in = st.text_input("Ajustar termos do documento?")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Suporte Documental", ""))
