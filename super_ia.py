import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM (DARK MODE CORPORATIVO) ---
st.set_page_config(page_title="AETHER AUDIT | Global Enterprise", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); color: white; border-radius: 10px; font-weight: bold; height: 3.5em; }
    .metric-card { background-color: #1a1c24; padding: 20px; border-radius: 15px; border: 1px solid #2d2f39; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("📡 Falha na sincronização com a rede Aether.")

def gerar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER AUDIT - RELATÓRIO EXECUTIVO', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- DASHBOARD AETHER ---
st.title("🛡️ AETHER AUDIT ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Compliance*")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<div class='metric-card'>🕵️‍♂️ Modo: <b>Investigação Profunda</b></div>", unsafe_allow_html=True)
    st.divider()
    
    st.subheader("📂 Ingestão de Dados")
    arquivo = st.file_uploader("Subir Evidências (PDF, Imagem, Excel, TXT)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    
    st.divider()
    st.subheader("⚙️ Módulos de Auditoria")
    extrair_tabelas = st.toggle("Extração Inteligente de Tabelas", value=True)
    validacao_lei = st.toggle("Validação Regulatória (Brasil/Global)", value=True)
    score_risco = st.toggle("Cálculo de Score de Risco (%)", value=True)

with col2:
    st.subheader("🔍 Central de Inteligência")
    pergunta = st.text_area("O que o sistema deve auditar?", 
                           placeholder="Ex: Compare os valores deste contrato com a tabela anexa e aponte riscos...", height=150)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL"):
        if pergunta:
            with st.spinner("Aether está processando nos servidores de alta performance..."):
                try:
                    conteudo_extra = ""
                    # Lógica para ler Excel se for enviado
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        st.write("📊 Amostra dos dados detectados:", df.head(3))
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_global = f"""
                    Atue como o software AETHER AUDIT. Use lógica de auditoria de elite (Big Four).
                    Instrução: {pergunta} {conteudo_extra}
                    
                    REQUISITOS OBRIGATÓRIOS:
                    1. 📄 CITE ARTIGOS DE LEIS reais para cada erro encontrado.
                    2. 📊 EXTRAIA VALORES EM TABELA formatada se houver dados numéricos.
                    3. ⚖️ SCORE DE RISCO: Dê um veredito de 0 a 100%.
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_global, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_global)
                    
                    st.success("Auditoria Concluída com Sucesso!")
                    
                    aba_analise, aba_word = st.tabs(["📝 Relatório Inteligente", "📥 Exportação Profissional"])
                    
                    with aba_analise:
                        st.markdown(response.text)
                    
                    with aba_word:
                        st.download_button("📥 BAIXAR RELATÓRIO OFICIAL (.DOCX)", gerar_docx(response.text), "aether_report.docx")
                        st.info("Relatório gerado em formato editável de auditoria.")

                except Exception as e:
                    st.error(f"Erro na Rede Aether: {e}")
        else:
            st.warning("Insira uma instrução para ativar o sistema.")

st.sidebar.caption("AETHER AUDIT v31.0 | Global Enterprise Solution 2026")
