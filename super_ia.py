import streamlit as st
import pandas as pd
from PIL import Image
try:
    from groq import Groq
except ImportError:
    st.error("🔄 Instalando pacotes de elite... Por favor, aguarde 30 segundos e atualize a página.")
    st.stop()
import google.generativeai as genai
from duckduckgo_search import DDGS
import time
import random
import docx2txt
import io

# --- CONFIGURAÇÃO DA PÁGINA (ESTRUTURA ORIGINAL MANTIDA) ---
st.set_page_config(page_title="AETHER OMNI v88.0", page_icon="🛡️", layout="wide")

# --- DESIGN ELITE TECH (IDENTIDADE AETHER - AZUL NOITE E VERDE ESMERALDA) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    .main { background-color: #0a192f; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Sora', sans-serif; color: #e6f1ff; font-weight: 700; }
    .stTextArea textarea { background-color: #112240; color: #e6f1ff; border: 1px solid #233554; border-radius: 8px; }
    
    /* Botão Verde Esmeralda conforme o Logo */
    .stButton>button { 
        background-color: #00c853; 
        color: #0a192f; font-weight: 700; border-radius: 8px; 
        border: none; padding: 0.6rem 2rem; transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover { background-color: #64ffda; transform: translateY(-1px); }
    
    [data-testid="stSidebar"] { background-color: #020c1b; border-right: 1px solid #233554; }
    .status-box { 
        padding: 1rem; border-radius: 8px; background: #112240; 
        border: 1px solid #64ffda; color: #64ffda;
        margin-bottom: 20px; font-size: 0.9rem;
    }
    .dossie-box { 
        background-color: #112240; padding: 25px; border-radius: 8px; 
        border: 1px solid #233554; box-shadow: 0 10px 30px -15px rgba(2, 12, 27, 0.7);
        line-height: 1.6; color: #ccd6f6;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE LEITURA (PRESERVANDO FUNÇÕES DE DOCX/PANDAS) ---
def processar_arquivos(upload):
    conteudo = ""
    try:
        if upload.name.endswith('.docx'):
            conteudo = docx2txt.process(upload)
        elif upload.name.endswith('.xlsx') or upload.name.endswith('.xls'):
            df = pd.read_excel(upload)
            conteudo = df.to_string()
        elif upload.name.endswith('.csv'):
            df = pd.read_csv(upload)
            conteudo = df.to_string()
        else:
            conteudo = upload.read().decode("utf-8")
    except Exception as e:
        st.error(f"Erro ao ler arquivo: {e}")
    return conteudo

# --- MOTOR DE INTELIGÊNCIA ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "Erro: Configure sua GROQ_API_KEY nos Secrets do Streamlit!"
        
    for attempt in range(5):
        try:
            prompt_sistema = f"""
            Você é o AETHER OMNI v88.0. Missão: {modo}. Contexto: {contexto}.
            Gere o DOSSIÊ DE BLINDAGEM técnica com base na LINDB.
            
            NOTA LEGAL OBRIGATÓRIA AO FINAL:
            '⚠️ NOTA: Este relatório é um suporte tecnológico à decisão e análise técnica. Não substitui o parecer jurídico de um advogado.'
            """
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            return completion.choices.message.content
        except Exception as e:
            if "429" in str(e):
                time.sleep(attempt + 5)
            else:
                return f"Erro na rede neural Aether: {e}"
    return "Aguardando liberação de cota..."

# --- INTERFACE ESTRUTURADA ---
with st.sidebar:
    st.title("🛡️ AETHER OMNI")
    st.caption("v88.0 | Elite Intelligence")
    st.divider()
    modo = st.selectbox("🎯 Ação Estratégica", [
        "Auditoria Técnica + LINDB", 
        "Dossiê de Blindagem", 
        "Análise Forense de Dados"
    ])
    st.info("Sistemas de Imagem (Pillow) e Planilhas (Pandas) Integrados.")

st.title("🛡️ Centro de Inteligência Aether")
st.markdown("<div class='status-box'>PROTOCOLO DE BLINDAGEM ATIVO | MOTOR HÍBRIDO (GROQ/GOOGLE)</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Entrada de Dados")
    user_input = st.text_area("Descreva o caso ou cole o conteúdo:", height=200)
    upload = st.file_uploader("Documentos (docx, xlsx, csv, txt, py)", type=['docx', 'xlsx', 'xls', 'csv', 'txt', 'py'])

with col2:
    st.subheader("Dossiê de Auditoria")
    if st.button("INICIAR ANÁLISE ESTRATÉGICA"):
        conteudo_total = ""
        if upload:
            with st.spinner("Lendo e integrando dados do arquivo..."):
                conteudo_total = processar_arquivos(upload)
        
        if user_input or conteudo_total:
            with st.spinner("Sintetizando inteligência de elite..."):
                resultado = aether_brain(user_input, modo, conteudo_total)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)
        else:
            st.warning("Aguardando dados para processar.")

    if 'res_aether' in st.session_state:
        st.download_button(label="📥 EXPORTAR DOSSIÊ", data=st.session_state['res_aether'], file_name="aether_report_v88.txt")

# --- CONSULTA ANALISTA (RODAPÉ) ---
st.divider()
st.subheader("💬 Consultar Analista Aether")
chat_in = st.text_input("Refinar análise ou tirar dúvida:")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Ajuste de Auditoria", ""))
