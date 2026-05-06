import streamlit as st
import pandas as pd
import io
import time
from PIL import Image

# Gestão de dependências críticas
try:
    import google.generativeai as genai
    from docx import Document
    BIBLIOTECAS_OK = True
except ImportError:
    BIBLIOTECAS_OK = False

# --- UI REVOLUTION & DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER OMNI MASTER v75.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Erro Crítico: Dependências ausentes no servidor. Verifique o requirements.txt.")
    st.stop()

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    #MainMenu, footer, header {visibility: hidden;}
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .main { background: radial-gradient(circle at 10% 10%, #0d1117, #080a0d); color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
        transition: 0.3s all;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 198, 255, 0.4); }
    .report-card { padding: 35px; border-radius: 20px; background-color: #1a1c24; border: 1px solid #2d2f39; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .stTextArea textarea { background-color: #11141b !important; border-radius: 12px !important; border: 1px solid #2d323d !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE AUTO-EVOLUÇÃO (EVOLUTION ENGINE) ---
@st.cache_resource
def engine_auto_evolutiva(api_key):
    """Monitora erros e troca de IA/Protocolo automaticamente até estabilizar."""
    genai.configure(api_key=api_key)
    
    # Lista priorizada de Modelos (Evolução Automática)
    mapa_inteligencia = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "models/gemini-1.5-flash",
        "models/gemini-pro"
    ]
    
    for modelo_nome in mapa_inteligencia:
        try:
            m = genai.GenerativeModel(model_name=modelo_nome)
            # Teste de sobrevivência (Ping Neural)
            m.generate_content("ok", generation_config={"max_output_tokens": 1})
            return m, modelo_nome
        except Exception:
            continue # Tenta a próxima IA da lista se a atual falhar
            
    # Última tentativa: Busca dinâmica na API por qualquer modelo vivo
    try:
        modelos_vivos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if modelos_vivos:
            m_emergencia = genai.GenerativeModel(modelos_vivos[0])
            return m_emergencia, f"Emergência: {modelos_vivos[0]}"
    except:
        pass
        
    return None, None

# --- ATIVAÇÃO DO MOTOR COM LOG DE STATUS ---
api_key = st.secrets.get("GOOGLE_API_KEY")
model, model_id = engine_auto_evolutiva(api_key) if api_key else (None, None)

def preparar_exportacao(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (CONTROLE DE INTELIGÊNCIA) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("v75.0 | Auto-Evolution Mode")
    
    if model:
        st.success(f"🔋 IA ATIVA: {model_id}")
    else:
        st.error("🚨 ERRO DE CHAVE: A API não autorizou a conexão.")
        st.info("Verifique se sua chave no Streamlit Secrets está correta.")

    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Compliance Federal", "Trabalhista", "Tributário"])
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    auto_evolve = st.toggle("Evolução Automática (IA)", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    
    if st.button("🔄 FORÇAR AUTO-EVOLUÇÃO"):
        st.cache_resource.clear()
        st.rerun()

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")

col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    pergunta = st.text_area("Instruções Diretas (Sniper Prompt):", placeholder="Digite o comando...", height=250)
    arquivos = st.file_uploader("Upload de Ativos", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    acao = st.selectbox("Comportamento Neural:", ["Auditoria & Conclusão Mestra", "Detecção de Anomalias", "Blindagem LINDB"])

with col_output:
    if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner(f"Processando com {model_id}..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_master = f"Atue como AETHER OMNI ({agente}). MISSÃO: {acao}. INSTRUÇÃO: {pergunta} CONTEXTO: {extra_data}"
                    
                    # Chamada com proteção contra falha em tempo de execução
                    try:
                        response = model.generate_content([prompt_master, *imagens] if imagens else prompt_master)
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                        st.download_button("📥 Exportar (.DOCX)", preparar_exportacao(response.text), "AETHER_REPORT.docx")
                    except:
                        st.warning("IA falhou no processamento. Tentando Evolução em tempo real...")
                        st.cache_resource.clear()
                        st.rerun()
                except Exception as e:
                    st.error(f"Erro Crítico: {e}")
        else:
            st.warning("Aguardando entrada ou conexão com a API.")
