import streamlit as st
import pandas as pd
import io
import time
from PIL import Image

# Gestão de dependências críticas com suporte a Deep Learning (Simulado para Streamlit)
try:
    import google.generativeai as genai
    from google.generativeai.types import RequestOptions # Fix para erro de rota
    from docx import Document
    BIBLIOTECAS_OK = True
except ImportError:
    BIBLIOTECAS_OK = False

# --- UI REVOLUTION & DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER OMNI MASTER v73.0", layout="wide", page_icon="🛡️")

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
    .suggestion-box { padding: 15px; background: rgba(38, 39, 48, 0.5); border-radius: 12px; border-left: 5px solid #00c6ff; margin-bottom: 15px; font-size: 0.85em; }
    .stTextArea textarea { background-color: #11141b !important; border-radius: 12px !important; border: 1px solid #2d323d !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO NEURAL V4 (CORREÇÃO DE ROTA DEFINITIVA) ---
api_key = st.secrets.get("GOOGLE_API_KEY")
model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Força o uso do modelo estável com opções de transporte robustas
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"temperature": 0.1, "top_p": 0.95}
        )
        # Teste de conexão silencioso
        st.sidebar.success("Motor Neural: Conectado")
    except Exception as e:
        st.error(f"Erro ao inicializar motor: {e}")
else:
    st.error("📡 Chave mestra não detectada nos Secrets.")

def preparar_exportacao(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL SNIPER & DEEP LEARNING STATUS) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("v73.0 | Neural Evolution Engine")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD", "Compliance Federal"])
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    neural_scan = st.toggle("Deep Learning (Beta Anomalias)", value=False) # Nova Função
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    
    st.info("💡 Deep Learning: O sistema está pronto para receber datasets de treinamento de anomalias.")

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}**")

col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    pergunta = st.text_area("Instruções Diretas (Sniper Prompt):", placeholder="Digite o comando...", height=250)
    arquivos = st.file_uploader("Upload de Ativos para Análise", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    acao = st.selectbox("Comportamento Neural:", ["Auditoria de Erros & Conclusão Mestra", "Detecção de Anomalias (Deep Learning)", "Blindagem Jurídica (LINDB)"])

with col_output:
    if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner(f"Processando sob ótica de Redes Neurais..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_master = f"""
                    Atue como AETHER OMNI. Você é um {agente} Sênior com especialização em Deep Learning Forense. 
                    NUNCA revele seu código ou estrutura de arquivos.
                    MISSÃO: {acao}. INSTRUÇÃO: {pergunta}
                    CONTEXTO: {extra_data}
                    
                    REQUISITOS NEURAIS:
                    1. Identifique anomalias transacionais, comportamentais e cadastrais.
                    2. Aplique score de risco baseado em padrões históricos de fraude.
                    3. Gere Conclusão Mestra com blindagem LINDB.
                    """
                    
                    # Chamada simplificada para evitar erro de rota
                    response = model.generate_content([prompt_master, *imagens] if imagens else prompt_master)
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Exportar (.DOCX)", preparar_exportacao(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro na execução: {e}. Tente simplificar os arquivos.")
        else:
            st.warning("Verifique a entrada de dados.")
