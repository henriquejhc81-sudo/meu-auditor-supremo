import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- DESIGN MODERNO ---
st.set_page_config(page_title="PRO Auditor | AI Mode Edition", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; background-color: #4285F4; color: white; border-radius: 20px; font-weight: bold; }
    .report-card { padding: 25px; border-radius: 15px; background-color: #ffffff; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO SEGURA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Conectando ao Cérebro IA...")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('RELATÓRIO DE AUDITORIA - AI MODE', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.title("🌎 Auditor Supremo - Modo IA")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📁 Entrada de Dados")
    arquivo = st.file_uploader("Subir Evidência (PDF/Foto/TXT)", type=["txt", "pdf", "png", "jpg", "jpeg"])
    
    st.divider()
    st.markdown("### 🤖 Configurações do Modo IA")
    # Toggles inspirados no Labs do Google
    deep_search = st.toggle("Query Fan-out (Pesquisa Profunda)", value=True)
    source_citation = st.toggle("Citar Fontes Legais (Links)", value=True)
    audit_mode = st.toggle("Modo Auditoria Corporativa", value=True)

with col2:
    st.subheader("🔍 Central de Comando")
    pergunta = st.text_area("O que o Modo IA deve auditar?", 
                           placeholder="Ex: Faça uma análise profunda deste contrato, cite as leis brasileiras e extraia os valores em tabela...", 
                           height=150)
    
    if st.button("🚀 INICIAR PESQUISA IA"):
        if pergunta:
            with st.spinner("Modo IA: Executando múltiplas pesquisas de profundidade..."):
                try:
                    # Instrução mestre inspirada no comportamento do AI Mode
                    prompt_ai_mode = f"""
                    Atue no MODO IA do Google. Use a técnica de 'Query Fan-out' para explorar todos os subtópicos da instrução: {pergunta}
                    
                    REQUISITOS:
                    1. Identifique riscos jurídicos e éticos.
                    2. Cite artigos de leis brasileiras (ex: Art. 421 do Código Civil).
                    3. Se houver dados, organize-os em uma TABELA.
                    4. Dê um veredito de risco de 0 a 100%.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_ai_mode, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_ai_mode)
                    
                    st.success("Análise Multinível Concluída!")
                    
                    aba_resumo, aba_fontes, aba_docx = st.tabs(["📄 Resumo IA", "🔗 Fontes e Links", "📥 Exportar"])
                    
                    with aba_resumo:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    
                    with aba_fontes:
                        st.info("As fontes e artigos citados estão integrados no Resumo acima conforme as leis brasileiras.")
                    
                    with aba_docx:
                        st.download_button("📥 Baixar Relatório AI Mode (.DOCX)", preparar_download(response.text), "relatorio_aimode.docx")
                
                except Exception as e:
                    st.error(f"Erro no processamento: {e}")
        else:
            st.warning("Insira uma pergunta para ativar a IA.")

st.sidebar.caption("v24.0 | Powered by Google AI Mode Logic")
