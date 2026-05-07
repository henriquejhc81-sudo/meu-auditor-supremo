import streamlit as st
import pandas as pd
from PIL import Image
try:
    from groq import Groq
except ImportError:
    st.error("🔄 Otimizando pacotes... Por favor, aguarde e atualize a página.")
    st.stop()
import google.generativeai as genai
from duckduckgo_search import DDGS
import time
import random
import docx2txt
import io

# --- CONFIGURAÇÃO DA PÁGINA (PRESERVAÇÃO TOTAL MANTIDA) ---
st.set_page_config(page_title="AETHER OMNI v88.1", page_icon="🛡️", layout="wide")

# --- DESIGN ELITE TECH (MANTIDO) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #0a192f; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Sora', sans-serif; color: #e6f1ff; font-weight: 700; }
    .stTextArea textarea { background-color: #112240; color: #e6f1ff; border: 1px solid #233554; border-radius: 8px; }
    .stButton>button { 
        background-color: #00c853; 
        color: #0a192f; font-weight: 700; border-radius: 8px; 
        border: none; padding: 0.6rem 2rem; transition: all 0.3s ease;
    }
    .status-box { padding: 1rem; border-radius: 8px; background: #112240; border: 1px solid #64ffda; color: #64ffda; margin-bottom: 20px; }
    .dossie-box { background-color: #112240; padding: 25px; border-radius: 8px; border: 1px solid #233554; line-height: 1.6; color: #ccd6f6; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE LEITURA (MANTIDA) ---
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
        st.error(f"Erro na leitura: {e}")
    return conteudo

# --- MOTOR DE INTELIGÊNCIA HÍBRIDO (CORREÇÃO DO ERRO DE LISTA) ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        return f"Erro de Configuração: {e}"
        
    for attempt in range(5):
        try:
            instrucao_cruzamento = ""
            if contexto:
                instrucao_cruzamento = f"\n🔍 PROTOCOLO DE CRUZAMENTO: Analise o prompt abaixo em conjunto com os dados extraídos do arquivo anexo ({contexto})."

            prompt_sistema = f"""
            Você é o AETHER OMNI v88.1. Missão: {modo}.
            DIRETRIZ: {instrucao_cruzamento if contexto else "Gere um DOSSIÊ DE BLINDAGEM técnica (LINDB)."}
            ⚠️ NOTA LEGAL OBRIGATÓRIA: 'Este relatório é um suporte tecnológico à decisão e não substitui o parecer jurídico.'
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            # CORREÇÃO AQUI: Acesso direto ao conteúdo da mensagem
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                time.sleep(attempt + 5)
            else:
                return f"Erro na rede neural: {e}"
    return "Cota temporariamente excedida."

# --- INTERFACE ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v88.1 | Elite Intelligence")
    st.divider()
    modo = st.selectbox("🎯 Ação Estratégica", [
        "Auditoria Técnica + LINDB", 
        "Dossiê de Blindagem", 
        "Cruzamento de Dados e Auditoria Comparativa"
    ])

st.title("🛡️ Centro de Inteligência Aether")
st.markdown("<div class='status-box'>PROTOCOLO DE BLINDAGEM ATIVO | MOTOR HÍBRIDO | CRUZAMENTO DE DADOS ATIVO</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Entrada de Dados")
    user_input = st.text_area("Descreva o caso ou solicite a análise:", height=200)
    upload = st.file_uploader("Subir arquivo para cruzamento", type=['docx', 'xlsx', 'xls', 'csv', 'txt', 'py'])

with col2:
    st.subheader("Dossiê de Auditoria")
    if st.button("INICIAR ANÁLISE ESTRATÉGICA"):
        conteudo_anexo = ""
        if upload:
            with st.spinner("Sincronizando dados..."):
                conteudo_anexo = processar_arquivos(upload)
        
        if user_input or conteudo_anexo:
            with st.spinner("Gerando blindagem..."):
                resultado = aether_brain(user_input, modo, conteudo_anexo)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)

    if 'res_aether' in st.session_state:
        st.download_button(label="📥 EXPORTAR DOSSIÊ", data=st.session_state['res_aether'], file_name="aether_audit.txt")

# --- CONSULTA ANALISTA ---
st.divider()
st.subheader("💬 Consultar Analista Aether")
chat_in = st.text_input("Dúvida?")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Suporte", ""))
