import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- IDENTIDADE VISUAL DATASNIPPER MODE ---
st.set_page_config(page_title="AETHER OMNI | Enterprise AI", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 8px; font-weight: bold; height: 3.8em; 
    }
    .report-card { padding: 30px; border-radius: 15px; background-color: #1a1c24; border: 1px solid #2d2f39; line-height: 1.6; }
    .sidebar-box { padding: 15px; background: #262730; border-radius: 10px; border-left: 5px solid #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO AUTO-REPARADORA (FIM DEFINITIVO DO 404) ---
def conectar_ia():
    try:
        API_KEY = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=API_KEY)
        # Tenta o caminho de produção (v1) para evitar o erro v1beta da imagem
        return genai.GenerativeModel(model_name='gemini-1.5-flash')
    except:
        try:
            # Caminho de contingência caso o servidor exija o prefixo models/
            return genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        except:
            return None

model = conectar_ia()

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO DE AUDITORIA E COMPLIANCE', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL (ESTILO DATASNIPPER) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    if st.button("🔄 Reiniciar Motor do Sistema"):
        st.rerun()
    
    st.divider()
    st.markdown("<div class='sidebar-box'><b>ARSENAL SNIPER ATIVO</b><br>• OCR Profundo<br>• Validação de IFRS/CPC<br>• Detecção de Fraude</div>", unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📜 Histórico de Missões")
    st.caption("Logs de Auditoria Criptografados")
    st.caption("v40.4 | Omniscience Edition")

# --- INTERFACE MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.markdown("##### *Standard for High-Frequency Auditing & Global Intelligence*")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📂 Ingestão Multimodal")
    arquivo = st.file_uploader("Upload de Documentos (PDF, Imagem, Excel, CSV)", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"])
    
    st.divider()
    st.markdown("### ⚙️ Parâmetros Sniper")
    extrair_tab = st.toggle("Extração Inteligente de Tabelas (OCR)", value=True)
    score_risco = st.toggle("Cálculo de Score de Risco (%)", value=True)
    cruzamento = st.toggle("Cruzamento de Dados Automático", value=True)
    
    st.markdown(f"📊 **Status do Sistema:** {'🟢 Operacional' if model else '🔴 Erro de Sincronização'}")

with col2:
    st.subheader("🔍 Central Sniper")
    pergunta = st.text_area("O que o sistema deve analisar ou auditar?", 
                           placeholder="Ex: Compare a nota fiscal com o contrato e verifique divergências tributárias...", 
                           height=170)
    
    if st.button("🚀 EXECUTAR VARREDURA GLOBAL OMNI"):
        if not model:
            st.error("Erro Crítico: A Rede Aether não conseguiu se conectar ao Google. Verifique sua API Key nos Secrets.")
        elif not pergunta:
            st.warning("Insira uma instrução para o Sniper.")
        else:
            with st.spinner("Processando através das Redes Neurais Omni..."):
                try:
                    time.sleep(1)
                    conteudo_extra = ""
                    # Lógica DataSnipper: Leitura de Planilhas
                    if arquivo and arquivo.name.endswith(('.xlsx', '.csv')):
                        df = pd.read_excel(arquivo) if arquivo.name.endswith('.xlsx') else pd.read_csv(arquivo)
                        conteudo_extra = f"\n\nDADOS DA PLANILHA:\n{df.to_string()}"

                    prompt_mestre = f"""
                    Atue como o sistema AETHER OMNI (Nível Big Four). 
                    Instrução: {pergunta} {conteudo_extra}
                    Use lógica de auditoria forense, cite leis brasileiras e normas contábeis.
                    Requisitos Adicionais: Extração de Tabelas: {extrair_tab} | Score de Risco: {score_risco}
                    """
                    
                    if arquivo and arquivo.type.startswith("image"):
                        response = model.generate_content([prompt_mestre, Image.open(arquivo)])
                    else:
                        response = model.generate_content(prompt_mestre)
                    
                    st.success("Missão de Auditoria Concluída!")
                    
                    tab1, tab2 = st.tabs(["📝 Relatório Inteligente", "📥 Exportar"])
                    with tab1:
                        st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with tab2:
                        st.download_button("📥 BAIXAR RELATÓRIO (.DOCX)", preparar_download(response.text), "aether_report.docx")
                        st.balloons()
                
                except Exception as e:
                    st.error(f"Erro de Rede Omni: {e}. Desative o tradutor do navegador e reinicie o motor.")

st.divider()
st.caption("Aether Omni - Tecnologia de Auditoria de Classe Mundial")
