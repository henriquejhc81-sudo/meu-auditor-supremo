import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- DESIGN DE ELITE (AETHER BLACK THEME) ---
st.set_page_config(page_title="AETHER AUDIT | Intelligence Mode", layout="wide", page_icon="🛡️")

# Estilização Profissional via CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; 
        border-radius: 8px; 
        border: none; 
        font-weight: bold; 
        height: 3.5em; 
        transition: 0.3s; 
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00c6ff; }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    .metric-box { padding: 15px; border-radius: 10px; background: #262730; text-align: center; border: 1px solid #444; }
    [data-testid="stSidebar"] { background-color: #1a1c24; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # Seleção automática de modelo estável
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"📡 Aether Network: Erro de Sincronização. Verifique os Secrets.")

# Função para criar o documento Word profissional
def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        if linha.strip():
            doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE AETHER AUDIT ---
st.title("🛡️ AETHER AUDIT")
st.markdown("##### *Advanced Compliance & Multimodal Intelligence*")

# Estrutura de Colunas (Corrigida)
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='metric-box'>📊 Nível de Varredura: <b>Ultra Deep</b></div>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("📂 Central de Evidências")
    arquivo = st.file_uploader("Upload de Documentos ou Imagens", type=["txt", "pdf", "png", "jpg", "jpeg"])
    
    st.divider()
    st.subheader("⚙️ Parâmetros de Missão")
    ai_mode = st.toggle("Ativar Modo IA Profundo", value=True)
    legal_check = st.toggle("Cruzamento de Leis Brasileiras", value=True)
    risk_meter = st.toggle("Cálculo de Score de Risco", value=True)

with col2:
    st.subheader("🔍 Painel de Análise")
    pergunta = st.text_area("O que a Aether deve processar?", 
                           placeholder="Ex: Analise as cláusulas deste contrato e verifique riscos de conformidade...", 
                           height=180)
    
    if st.button("🚀 INICIAR VARREDURA AETHER"):
        if pergunta:
            with st.spinner("Aether Audit está processando nos servidores de alta performance..."):
                try:
                    # Delay furtivo para evitar bloqueios
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    # Prompt Estruturado de Elite
                    prompt_mestre = f"""
                    Atue como o sistema AETHER AUDIT, a IA de auditoria mais avançada do mercado.
                    Instrução: {pergunta}
                    
                    ESTRUTURA OBRIGATÓRIA DA RESPOSTA:
                    1. 📝 SUMÁRIO EXECUTIVO: Resumo do documento.
                    2. ⚖️ ANÁLISE TÉCNICA: Liste erros, abusos e cite leis brasileiras aplicáveis.
                    3. 📊 SCORE DE RISCO: Dê uma nota de 0 a 100 para o perigo deste documento.
                    4. ✅ TEXTO CORRIGIDO: Forneça a versão revisada e segura do texto.
                    """
                    
                    # Processamento Multimodal (Texto + Imagem)
                    if arquivo and arquivo.type.startswith("image"):
                        img = Image.open(arquivo)
                        response = model.generate_content([prompt_mestre, img])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Missão Concluída: Dados Processados.")
                    
                    # Abas de Organização
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportação Profissional"])
                    
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.download_button(
                            label="📥 BAIXAR RELATÓRIO AETHER (.DOCX)",
                            data=preparar_download(response.text),
                            file_name="aether_report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        st.info("Documento formatado e pronto para uso oficial.")
                        st.balloons()
                
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}")
        else:
            st.warning("Aguardando entrada de dados para iniciar varredura.")

st.sidebar.caption("AETHER AUDIT v25.1 | Enterprise Solution")
