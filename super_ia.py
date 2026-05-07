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

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO: CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="AETHER OMNI v88.1 | Enterprise Intelligence", page_icon="🛡️", layout="wide")

# --- 🎨 DESIGN ENTERPRISE "NAVY BLUE" (BASEADO EM BIG FOUR) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Fundo Navy Blue Profundo */
    .main { background-color: #050a14; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Minimalista Estilo Enterprise */
    [data-testid="stSidebar"] { background-color: #02060d; border-right: 1px solid #112240; min-width: 250px !important; }
    
    /* Cards de Insights (Pilar B) */
    .insight-card { 
        background-color: #0a192f; padding: 20px; border-radius: 12px; 
        border: 1px solid #112240; margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .insight-card:hover { border-color: #00c853; transform: scale(1.01); }

    /* Botão "Magic Upload" e Ações de Elite */
    .stButton>button { 
        background-color: #00c853; color: #050a14; font-weight: 700; 
        border-radius: 8px; border: none; width: 100%; transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #64ffda; box-shadow: 0 0 20px rgba(100, 255, 218, 0.3); }

    /* Inputs e Áreas de Texto */
    .stTextArea textarea { background-color: #0a192f; color: #e6f1ff; border: 1px solid #112240; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- ⚙️ FUNÇÕES DE LEITURA (MANTIDAS INTEGRALMENTE) ---
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

# --- 🧠 MOTOR DE INTELIGÊNCIA HÍBRIDO (SNIPER MODE) ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        return f"Erro de Configuração: {e}"
        
    for attempt in range(5):
        try:
            prompt_sistema = f"""
            Você é o cérebro do AETHER OMNI v88.1. 
            PILAR ATUAL: {modo}.
            CONDIÇÃO: Analise o contexto abaixo e aja como um sênior da Deloitte/Kirkland & Ellis.
            CONTEXTO: {contexto}
            
            DIRETRIZ: {modo}. Forneça recomendações estratégicas e justificativa técnica (LINDB).
            NOTA LEGAL: '⚠️ NOTA: Este relatório é um suporte tecnológico e não substitui o parecer jurídico.'
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
    return "Cota temporariamente excedida."

# --- 📂 SIDEBAR: OS 3 PILARES E GESTÃO (ESTRUTURA ADITIVA) ---
with st.sidebar:
    st.image("https://icons8.com", width=60) # Simulando o Logo Aether
    st.title("AETHER OMNI")
    st.caption("v88.1 | Strategic Intelligence")
    st.divider()
    
    # Navegação por Pilares
    pilar = st.radio("📂 PILARES DE ATUAÇÃO", [
        "🛡️ Pilar A: Auditoria & Compliance",
        "⚖️ Pilar B: Legal & Due Diligence",
        "📄 Pilar C: Gerador de Documentos"
    ])
    
    st.divider()
    # Funções Obrigatórias de Elite
    st.subheader("🎯 Ações de Elite")
    funcao_elite = st.selectbox("Selecione o Protocolo:", [
        "Scanner de Risco (Kroll)",
        "Linha do Tempo (Latham & Watkins)",
        "Matriz de Compliance (KPMG)",
        "Extração Inteligente (Big Four)",
        "Gerar Resumo para o CEO"
    ])
    
    st.divider()
    st.info("Pandas, Pillow & Google AI Ativos.")

# --- 🚀 TELA PRINCIPAL (DESIGN ENTERPRISE) ---
st.title("🛡️ Centro de Inteligência Estratégica")

# Pilar B: Painel de Insights em tempo real (Mockup Aditivo)
st.subheader("📊 Feed de Insights em Tempo Real")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("<div class='insight-card'>🚨 <b>Risco Detectado:</b> 12 Contratos sem cláusula de reajuste.</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='insight-card'>⚖️ <b>Compliance:</b> 98% de adesão à LGPD nos novos documentos.</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='insight-card'>💰 <b>M&A:</b> 3 oportunidades identificadas em processos cíveis.</div>", unsafe_allow_html=True)

st.divider()

col_in, col_out = st.columns([1, 1.2])

with col_in:
    st.subheader("📥 Magic Upload & Entrada")
    user_input = st.text_area("Descreva o caso ou cole a tese:", height=200, placeholder="Inicie o Protocolo Sniper...")
    upload = st.file_uploader("Arraste seus documentos aqui (Scanner Global)", accept_multiple_files=False)

with col_out:
    st.subheader("🚀 Relatório Executivo")
    if st.button("ATIVAR PROTOCOLO OMNI"):
        conteudo_anexo = ""
        if upload:
            with st.spinner("Scanner de Elite em andamento..."):
                conteudo_anexo = processar_arquivos(upload)
        
        if user_input or conteudo_anexo:
            with st.spinner("Sintetizando Dossiê de Blindagem..."):
                resultado = aether_brain(user_input, f"{pilar} - {funcao_elite}", conteudo_anexo)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)

    if 'res_aether' in st.session_state:
        st.download_button(label="📥 EXPORTAR PARA O CEO", data=st.session_state['res_aether'], file_name="AETHER_OMNI_CEO_REPORT.txt")

# --- 💬 CHAT ANALISTA (MANTIDO) ---
st.divider()
st.subheader("💬 Consultar Especialista de Plantão")
chat_in = st.text_input("Dúvida estratégica?")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Suporte Estratégico", ""))
