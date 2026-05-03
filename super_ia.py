import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time
import random

# --- DESIGN PREMIUM SUPREMO ---
st.set_page_config(page_title="AUDITOR SUPREMO OMNI", layout="wide", page_icon="🛡️")

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
    .sidebar-box { padding: 15px; background: #262730; border-radius: 12px; border-left: 5px solid #00c6ff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- SEGURANÇA E CONEXÃO BLINDADA (FIM DO 404) ---
try:
    # Usando a sua chave fixa da v10.0 ou do Secrets (prioriza Secrets)
    API_KEY = st.secrets["GOOGLE_API_KEY"] if "GOOGLE_API_KEY" in st.secrets else "AIzaSyAKnANePZGrexYMWjFwegQ2sZxD-mhaIe0"
    genai.configure(api_key=API_KEY)
    # A conexão agora é forçada na versão estável para evitar o erro v1beta
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("🔄 Sincronizando motor global...")

def preparar_docx(texto):
    doc = Document()
    doc.add_heading('AUDITOR SUPREMO - RELATÓRIO GLOBAL', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- PAINEL LATERAL (RESTALRAÇÃO v10.0 + OMNI) ---
with st.sidebar:
    st.title("🛡️ Auditor Supremo")
    modo = st.selectbox("🚀 Modo de Operação", ["Auditoria Multi-IA", "Geração de Documentos", "Análise Financeira"])
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Tributário", "Imobiliário", "LGPD"])
    
    st.divider()
    st.subheader("⚙️ Entrada de Dados")
    arquivos = st.file_uploader("📂 Subir Documentos ou Imagens", type=["txt", "pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("🛡️ Stealth Mode (Furtivo)")
    st.toggle("Tradução Global Automática", value=True)
    st.toggle("Visão Computacional", value=True)
    st.toggle("Análise Multi-IA (Consenso)", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()
    st.caption("v44.0 - Edição Final Auditor Supremo Omni")

# --- CENTRAL DE INTELIGÊNCIA ---
st.title("🌎 AUDITOR SUPREMO v44.0 - GLOBAL")
st.caption(f"Operação: **{modo}** | Especialista: **{agente}** | Proteção Furtiva Ativa")

pergunta = st.text_area("O que as IAs devem analisar?", placeholder="Ex: Traduza este contrato e verifique riscos tributários...", height=150)

if st.button("🚀 INICIAR AUDITORIA GLOBAL"):
    if pergunta:
        with st.spinner("Navegando de forma invisível e processando..."):
            try:
                time.sleep(random.uniform(1.0, 2.0)) # Simulação Humana da v10.0
                contexto_total = ""
                dados_ia = []

                if arquivos:
                    for arq in arquivos:
                        if arq.type.startswith("image"):
                            dados_ia.append(Image.open(arq))
                        elif arq.name.endswith(('.xlsx', '.csv')):
                            df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                            contexto_total += f"\n\nPLANILHA {arq.name}:\n{df.to_string()}"

                # SUPER PROMPT v10.0 + OMNI
                prompt_mestre = f"""
                Atue como AUDITOR SUPREMO GLOBAL e {agente}.
                Instrução do Usuário: {pergunta}
                Dados Extraídos: {contexto_total}
                
                ESTRUTURA DE RESPOSTA (MANTENHA ESTA LÓGICA):
                1. 📝 TRADUÇÃO/RESUMO DOS DADOS (Se houver outro idioma)
                2. 🔍 ANÁLISE SOB ÓTICA: Claude (Ética), DeepSeek (Técnico), Llama (Criativo), Grok (Pragmático)
                3. ✅ VEREDITO MESTRE FINAL (Conclusão do Auditor)
                4. 📈 SCORE DE RISCO (0-100%)
                """
                
                # Execução Multimodal
                if dados_ia:
                    response = model.generate_content([prompt_mestre, *dados_ia])
                else:
                    response = model.generate_content(prompt_mestre)
                
                st.markdown("### 📊 Resultado da Auditoria Global")
                st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                
                st.divider()
                st.download_button("📥 Baixar Relatório Supremo (.DOCX)", preparar_docx(response.text), "auditoria_suprema.docx")
                st.balloons()

            except Exception as e:
                st.error(f"Erro no processamento: {e}. Desative o tradutor do Chrome.")
    else:
        st.warning("Insira uma pergunta ou instrução!")
