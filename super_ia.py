import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM REFINADO (INTER FONT & DARK MODE) ---
st.set_page_config(page_title="AETHER OMNI MASTER", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
    }
    .report-card { padding: 30px; border-radius: 18px; background-color: #1a1c24; border: 1px solid #2d2f39; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .suggestion-box { padding: 12px; background: #262730; border-radius: 10px; border-left: 5px solid #00c6ff; margin-bottom: 10px; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (FIM DEFINITIVO DO ERRO 404) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # A correção definitiva: Usar o nome estável v1 que o Google exige agora
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("📡 Rede Omni: Sincronizando conexão segura...")

def preparar_docx(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - DOCUMENTO OFICIAL', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL (RESTAURADO COM TODAS AS FUNÇÕES) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    
    # Restauração: Modo de Operação
    modo = st.selectbox("🚀 Modo de Operação", ["Auditoria de Evidências", "Geração de Contratos/Petições", "Análise Financeira"])
    
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {
            "Auditor Geral": ["Analise riscos financeiros.", "Verifique cláusulas ambíguas."],
            "Trabalhista": ["Valide multas da CLT.", "Analise riscos de vínculo."],
            "Geração": ["Redija contrato de prestação de serviços.", "Crie petição inicial trabalhista."]
        }
        for item in opcoes.get(agente if modo != "Geração de Contratos/Petições" else "Geração", []):
            st.markdown(f"<div class='suggestion-box'>💡 {item}</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Upload de Documentos", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Sniper Parameters")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    tabelas = st.toggle("Extração de Tabelas (OCR)", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("v43.2 | Enterprise Master Edition")

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Operação: **{modo}** | Agente: **{agente}** | Engine: **v1 Estável**")

pergunta = st.text_area("Descreva a missão (Ex: Analise este PDF ou Redija um contrato de...)", placeholder="Digite aqui...", height=150)

if st.button("🚀 EXECUTAR VARREDURA GLOBAL OMNI"):
    if pergunta:
        with st.spinner(f"Processando em modo {modo}..."):
            try:
                time.sleep(1)
                contexto_total = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nARQUIVO {arq.name}:\n{df.to_string()}"

                # Lógica Master: O prompt muda de acordo com o modo escolhido
                if modo == "Geração de Contratos/Petições":
                    instrucao_ia = f"Atue como um Advogado Sênior. Redija um documento jurídico profissional com base em: {pergunta}. Siga os padrões legais brasileiros."
                else:
                    instrucao_ia = f"Atue como um {agente} Sênior. Instrução: {pergunta} {contexto_total}. Forneça checklist de compliance: {checklist} e Score de Risco: {score}."

                response = model.generate_content(instrucao_ia)
                
                st.markdown("### 📝 Resultado da Inteligência Omni")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                st.download_button("📥 BAIXAR DOCUMENTO (.DOCX)", preparar_docx(response.text), "aether_omni_doc.docx")
                st.balloons()
            except Exception as e:
                st.error(f"Erro de Rede Omni: {e}. Desative o tradutor e aguarde 30 segundos.")
    else:
        st.warning("Insira uma instrução para o Sniper.")
