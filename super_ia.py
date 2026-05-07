import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random
import docx2txt

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aether Omni | Elite Intelligence", page_icon="🛡️", layout="wide")

# --- DESIGN ELITE TECH (IDENTIDADE AETHER) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');

    /* Fundo Azul Noite Profundo */
    .main { background-color: #0a192f; color: #e6f1ff; font-family: 'Inter', sans-serif; }
    
    /* Cabeçalhos e Títulos */
    h1, h2, h3 { font-family: 'Sora', sans-serif; color: #e6f1ff; font-weight: 700; }
    
    /* Estilo dos Cards (Hierarquia Visual) */
    .stTextArea textarea { background-color: #112240; color: #e6f1ff; border: 1px solid #233554; border-radius: 8px; }
    
    /* Botão Principal Verde Esmeralda (Pixel Perfect) */
    .stButton>button { 
        background-color: #00c853; /* Verde Esmeralda do Logo */
        color: #0a192f; font-weight: 700; border-radius: 8px; 
        border: none; padding: 0.6rem 2rem; transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover { background-color: #64ffda; transform: translateY(-1px); box-shadow: 0 6px 12px rgba(100, 255, 218, 0.2); }
    
    /* Sidebar Minimalista */
    [data-testid="stSidebar"] { background-color: #020c1b; border-right: 1px solid #233554; }
    
    /* Status Box Elegante (Sem Neon) */
    .status-box { 
        padding: 1rem; border-radius: 8px; background: #112240; 
        border: 1px solid #64ffda; color: #64ffda;
        margin-bottom: 20px; font-size: 0.9rem;
    }
    
    /* Dossiê de Blindagem (Estética de Auditoria) */
    .dossie-box { 
        background-color: #112240; padding: 25px; border-radius: 8px; 
        border: 1px solid #233554; box-shadow: 0 10px 30px -15px rgba(2, 12, 27, 0.7);
        line-height: 1.6; color: #ccd6f6;
    }

    /* Ajuste de Swithes e Toggles */
    .stCheckbox label { color: #8892b0; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO PARA LER ARQUIVOS ---
def ler_arquivo(uploaded_file):
    try:
        if uploaded_file.name.endswith('.docx'):
            return docx2txt.process(uploaded_file)
        elif uploaded_file.name.endswith('.txt') or uploaded_file.name.endswith('.py'):
            return uploaded_file.read().decode("utf-8")
        else:
            return "Formato não suportado."
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"

# --- MOTOR ANTI-LOCK E AUTO-HEALING ---
def aether_brain(prompt, modo, contexto):
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "Erro: Configure sua GROQ_API_KEY nos Secrets!"
        
    for attempt in range(5):
        try:
            prompt_sistema = f"""
            Você é o Aether Omni Sentinel. Missão: {modo}.
            CONTEXTO DO DOCUMENTO: {contexto}
            
            DIRETRIZ: Gere um 'DOSSIÊ DE BLINDAGEM' com Justificativa Técnica e base na LINDB.
            
            NOTA LEGAL OBRIGATÓRIA AO FINAL:
            '⚠️ NOTA: Este relatório é um suporte tecnológico à decisão e análise técnica. Não substitui o parecer jurídico de um advogado ou autoridade competente.'
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
                return f"Erro no sistema: {e}"
    return "Cota de API excedida."

# --- BARRA LATERAL (ESTILO MINIMALISTA) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("v5.6 | Auditoria de Elite")
    
    st.divider()
    with st.expander("⚙️ Parâmetros de Inteligência", expanded=True):
        st.toggle("Análise Forense", value=True)
        st.toggle("Risco Compliance", value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Ação Estratégica", [
        "Auditoria Técnica + LINDB",
        "Dossiê de Blindagem",
        "Compliance & Risco"
    ])

# --- ÁREA PRINCIPAL ---
st.title("🛡️ Centro de Inteligência Aether")
st.markdown("<div class='status-box'>SISTEMA OPERACIONAL | PROTOCOLO DE BLINDAGEM ATIVO</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Entrada de Dados")
    user_input = st.text_area("Descreva o caso para análise:", height=200, placeholder="Insira aqui os detalhes técnicos ou jurídicos...")
    upload = st.file_uploader("Upload de Documentos (docx, txt, py)", type=['docx', 'txt', 'py'])

with col2:
    st.subheader("Dossiê de Auditoria")
    if st.button("INICIAR ANÁLISE ESTRATÉGICA"):
        conteudo_arquivo = ""
        if upload:
            with st.spinner("Decodificando documento..."):
                conteudo_arquivo = ler_arquivo(upload)
        
        if user_input or conteudo_arquivo:
            with st.spinner("Aether processando dados sob protocolo LINDB..."):
                resultado = aether_brain(user_input, modo, conteudo_arquivo)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)
        else:
            st.warning("Aguardando entrada de dados para iniciar.")

    if 'res_aether' in st.session_state:
        st.divider()
        st.download_button(label="📥 EXPORTAR DOSSIÊ (PDF/TXT)", data=st.session_state['res_aether'], file_name="aether_intelligence_report.txt")

# --- CHAT ANALISTA (RODAPÉ) ---
st.divider()
st.subheader("💬 Consultar Analista Aether")
chat_in = st.text_input("Refinar análise ou solicitar esclarecimentos:")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Ajuste de Auditoria", ""))
