import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- DESIGN PREMIUM MASTER ---
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
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA (AUTO-SWITCH DE VERSÃO) ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # MUDANÇA CRÍTICA: Forçamos a versão 1.5 estável sem passar por v1beta
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except Exception as e:
    st.error("📡 Sincronizando Rede Omni...")

def preparar_docx(texto, titulo="RELATÓRIO"):
    doc = Document()
    doc.add_heading(f'AETHER OMNI - {titulo}', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL MASTER) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {"Auditor Geral": ["Riscos financeiros.", "Cláusulas abusivas."], "Trabalhista": ["Multas CLT.", "Vínculo empregatício."]}
        for item in opcoes.get(agente, ["Analise este documento."]):
            st.caption(f"💡 {item}")

    st.divider()
    st.subheader("📂 Ingestão de Dados")
    arquivos = st.file_uploader("Evidências (PDF, Excel, Imagem)", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    gerar_minuta = st.toggle("🤖 Gerar Minuta de Contrato/Petição", value=False)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- INTERFACE CENTRAL ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}** | Engine: **v43.0 Ultimate**")

pergunta = st.text_area("O que o sistema deve analisar ou auditar?", placeholder="Digite sua instrução...", height=150)

if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
    if pergunta:
        with st.spinner(f"O {agente} está operando..."):
            try:
                contexto_total = ""
                if arquivos:
                    for arq in arquivos:
                        if arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nTABELA {arq.name}:\n{df.to_string()}"

                prompt_master = f"""
                Atue como {agente} Sênior. 
                Instrução: {pergunta}
                Contexto: {contexto_total}
                
                FORMATO OBRIGATÓRIO:
                1. RELATÓRIO DE AUDITORIA (Checklist: {checklist}, Score: {score})
                2. {'GERAÇÃO DE MINUTA JURÍDICA: Redija um texto pronto para uso legal corrigindo os erros apontados.' if gerar_minuta else ''}
                """
                
                response = model.generate_content(prompt_master)
                
                st.markdown("### 📝 Resultado da Operação")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                nome_doc = "minuta_juridica.docx" if gerar_minuta else "relatorio_auditoria.docx"
                st.download_button(f"📥 BAIXAR {nome_doc.upper()}", preparar_docx(response.text, "RESULTADO"), nome_doc)
                st.balloons()
            except Exception as e:
                st.error(f"📡 Erro de Rede Omni: {e}. Desative o tradutor e reinicie.")
    else:
        st.warning("Insira uma instrução.")

st.sidebar.caption("v43.0 | Enterprise Master Edition")
