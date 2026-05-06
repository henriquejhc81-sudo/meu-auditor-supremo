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
st.set_page_config(page_title="AETHER OMNI MASTER v74.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Erro Crítico: Dependências ausentes (google-generativeai, python-docx).")
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

# --- FUNÇÃO DE AUTO CURA (HEALER ENGINE) ---
@st.cache_resource
def inicializar_motor_healer(api_key):
    """Tenta múltiplos caminhos de conexão para curar erros de rota 404."""
    genai.configure(api_key=api_key)
    
    # Lista de modelos e rotas para tentativa de cura
    estrategias = [
        {"name": "gemini-1.5-flash", "version": "v1"},
        {"name": "models/gemini-1.5-flash", "version": "v1"},
        {"name": "gemini-1.5-pro", "version": "v1"},
        {"name": "gemini-pro", "version": "v1"}
    ]
    
    for est in estrategias:
        try:
            m = genai.GenerativeModel(model_name=est["name"])
            # Teste de pulso
            m.generate_content("pulse", generation_config={"max_output_tokens": 1})
            return m, est["name"]
        except:
            continue
    return None, None

# --- EXECUÇÃO DO MOTOR ---
api_key = st.secrets.get("GOOGLE_API_KEY")
model, model_ativo = inicializar_motor_healer(api_key) if api_key else (None, None)

if model:
    st.sidebar.success(f"💉 Sistema Auto-Curado: {model_ativo}")
else:
    st.error("📡 Falha Crítica: O motor não conseguiu se auto-curar. Verifique a API Key.")

def preparar_exportacao(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL SNIPER) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("v74.0 | Healer & Neural Engine")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Compliance Federal", "Trabalhista", "Tributário"])
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    auto_cura = st.toggle("Ativar Auto-Cura (Healer)", value=True)
    
    if st.button("🔄 Reiniciar e Curar"):
        st.cache_resource.clear()
        st.rerun()

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")

col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    pergunta = st.text_area("Instruções Diretas (Sniper Prompt):", placeholder="Digite o comando...", height=250)
    arquivos = st.file_uploader("Upload de Ativos", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    acao = st.selectbox("Comportamento Neural:", ["Auditoria de Erros & Conclusão Mestra", "Detecção de Anomalias (Deep Learning)", "Blindagem Jurídica (LINDB)"])

with col_output:
    if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner(f"AETHER está processando..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_master = f"Atue como AETHER OMNI ({agente}). MISSÃO: {acao}. INSTRUÇÃO: {pergunta} CONTEXTO: {extra_data}"
                    
                    # TENTATIVA DE RESPOSTA COM TRATAMENTO DE ERRO EM TEMPO REAL
                    try:
                        response = model.generate_content([prompt_master, *imagens] if imagens else prompt_master)
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                        st.download_button("📥 Exportar (.DOCX)", preparar_exportacao(response.text), "AETHER_REPORT.docx")
                    except Exception as e_inner:
                        st.warning("⚠️ Erro súbito detectado. Iniciando Auto-Cura...")
                        st.cache_resource.clear()
                        st.error(f"Erro: {e_inner}. Por favor, tente clicar no botão novamente.")
                except Exception as e:
                    st.error(f"Erro fatal: {e}")
        else:
            st.warning("Aguardando entrada de dados.")
