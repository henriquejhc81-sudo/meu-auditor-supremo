import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- DESIGN AETHER (BLACK & NEON) ---
st.set_page_config(page_title="AETHER AUDIT | Intelligence Mode", layout="wide", page_icon="🛡️")

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
    }
    .report-card { padding: 25px; border-radius: 12px; background-color: #1a1c24; border: 1px solid #2d2f39; color: #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA IA (CORREÇÃO DE NUVEM) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # O SEGREDO: Usar o nome puro do modelo sem o prefixo "models/"
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Aether Network: Aguardando conexão...")

# Função de Exportação
def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO DE INTELIGÊNCIA', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE AETHER ---
st.title("🛡️ AETHER AUDIT")
st.markdown("##### *Advanced Compliance & Multimodal Intelligence*")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📂 Central de Evidências")
    arquivo_subido = st.file_uploader("Upload de Documentos ou Imagens", type=["txt", "pdf", "png", "jpg", "jpeg"])
    
    st.divider()
    st.markdown("### ⚙️ Parâmetros de Missão")
    st.toggle("Ativar Modo IA Profundo", value=True)
    st.toggle("Cruzamento de Leis Brasileiras", value=True)

with col2:
    st.subheader("🔍 Painel de Análise")
    pergunta = st.text_area("O que a Aether deve processar?", placeholder="Ex: Analise este contrato...", height=150)
    
    if st.button("🚀 INICIAR VARREDURA AETHER"):
        if pergunta:
            with st.spinner("Conectando ao Cérebro Global..."):
                try:
                    time.sleep(random.uniform(1.0, 2.5))
                    
                    dados_ia = []
                    if arquivo_subido:
                        if arquivo_subido.type.startswith("image"):
                            img = Image.open(arquivo_subido)
                            dados_ia = [img]
                        else:
                            conteudo = arquivo_subido.read().decode("utf-8", errors="ignore")
                            dados_ia = [f"CONTEÚDO: {conteudo}"]

                    # Prompt Estruturado
                    prompt_mestre = f"""
                    Atue como AUDITOR SUPREMO GLOBAL (AETHER AUDIT). 
                    Instrução do Usuário: {pergunta}
                    
                    ESTRUTURA DE RESPOSTA:
                    1. 📝 SUMÁRIO EXECUTIVO
                    2. 🔍 ANÁLISE TÉCNICA E ERROS
                    3. ✅ VEREDITO FINAL
                    """
                    
                    if dados_ia:
                        response = model.generate_content([prompt_mestre, *dados_ia])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Missão Concluída!")
                    tab1, tab2 = st.tabs(["📝 Relatório", "📥 Download"])
                    
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", gerar_docx(response.text), "aether_report.docx")
                        
                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}")
        else:
            st.warning("Insira uma pergunta ou instrução!")

st.sidebar.caption("AETHER AUDIT v26.1 | Cloud Optimized")
