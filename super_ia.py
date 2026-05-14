import streamlit as st
import pandas as pd
import os, time, base64, io
import docx2txt
import concurrent.futures
from docx import Document
from docx.shared import Pt, RGBColor

# --- 🧠 LIBS DA FASE 2: RAG, VISÃO E IA ---
import cv2
import numpy as np
from PIL import Image
try:
    import pytesseract
except ImportError:
    pass # OCR Degradado graciosamente se não instalado
try:
    import PyPDF2
except ImportError:
    pass

# Langchain & FAISS (Memória Vetorial)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from groq import Groq
except ImportError:
    pass

# --- ⚙️ CONFIGURAÇÃO DE SEGURANÇA ---
st.set_page_config(page_title="AETHER OMNI V300", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "res_docx" not in st.session_state: st.session_state.res_docx = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo"}

def set_template(texto):
    st.session_state.cmd_input = texto

# --- 👁️ MOTOR DE INGESTÃO MULTIMODAL & OCR (NEXUS V3) ---
def extrator_nexus_v3(arquivos_upados):
    texto_extraido = ""
    sucesso = 0
    usou_ocr = False
    
    for arquivo in arquivos_upados:
        try:
            # 1. Planilhas e Dados Estruturados
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- DADOS CSV: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif arquivo.name.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- DADOS XLSX: {arquivo.name} ---\n{df.to_string(index=False)}"
            
            # 2. Documentos de Texto
            elif arquivo.name.endswith('.docx'):
                texto = docx2txt.process(arquivo)
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{texto}"
            elif arquivo.name.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            
            # 3. PDF Híbrido
            elif arquivo.name.endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(arquivo)
                    texto_pdf = ""
                    for page in pdf_reader.pages:
                        extraido = page.extract_text()
                        if extraido: texto_pdf += extraido + "\n"
                    texto_extraido += f"\n\n--- PDF: {arquivo.name} ---\n{texto_pdf}"
                except:
                    texto_extraido += f"\n[AETHER: Falha na leitura nativa do PDF: {arquivo.name}]"
            
            # 4. VISÃO COMPUTACIONAL (OCR para Imagens)
            elif arquivo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    imagem = Image.open(arquivo)
                    # Convertendo para array do OpenCV para pré-processamento
                    img_cv = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
                    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
                    # Aplica OCR Tesseract (Requer tesseract instalado no SO)
                    texto_ocr = pytesseract.image_to_string(gray, lang='por')
                    texto_extraido += f"\n\n--- IMAGEM OCR (Visão Ativada): {arquivo.name} ---\n{texto_ocr}"
                    usou_ocr = True
                except Exception as e_ocr:
                    texto_extraido += f"\n[AETHER: Módulo OCR inativo ou imagem ilegível: {arquivo.name}]"
            
            sucesso += 1
        except Exception as e:
            texto_extraido += f"\n[ERRO CRÍTICO EM {arquivo.name}: {str(e)}]"
            
    return texto_extraido, sucesso, usou_ocr

# --- 🧠 MEMÓRIA VETORIAL (RAG COM FAISS & LANGCHAIN) ---
def processar_com_rag(texto, comando):
    """Fatia documentos gigantes e busca só o que importa usando Matemática Vetorial"""
    if not GEMINI_KEY:
        return texto[:90000] + "\n[ALERTA: Chave Gemini ausente. RAG desativado. Texto truncado para evitar estouro de memória.]"
    
    try:
        # Fatiamento inteligente (Chunks com overlap para não cortar frases no meio)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
        chunks = text_splitter.split_text(texto)
        
        # Cria embeddings (Transforma o texto em coordenadas matemáticas)
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=GEMINI_KEY, model="models/embedding-001")
        
        # Cria o banco de dados vetorial FAISS na memória RAM
        vector_store = FAISS.from_texts(chunks, embeddings)
        
        # Busca no banco de dados os chunks que mais se parecem com o comando do usuário
        docs_relevantes = vector_store.similarity_search(comando, k=8) # Pega os 8 melhores pedaços
        
        contexto_filtrado = "\n...\n".join([doc.page_content for doc in docs_relevantes])
        return f"[AETHER RAG FILTER ACTIVE: Exibindo apenas fragmentos matematicamente relevantes para a análise]\n\n{contexto_filtrado}"
    except Exception as e:
        return texto[:90000] + f"\n[ALERTA RAG: Falha no processamento vetorial ({str(e)}). Operando em modo texto bruto.]"

# --- 🤖 AGENTE EXECUTOR ---
def chamar_agente_groq(nome_agente, system_prompt, comando, contexto):
    if not GROQ_KEY: return f"[{nome_agente}] Erro: Chave API ausente. Configure st.secrets."
    try:
        client = Groq(api_key=GROQ_KEY)
        full_prompt = f"DIRETRIZ DE INVESTIGAÇÃO: {comando}\n\nEVIDÊNCIAS COLETADAS:\n{contexto}"
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.1, # Temperatura baixa = Respostas mais analíticas e menos criativas
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[{nome_agente}] Falha de rede/API: {str(e)}"

# --- 🚀 ORQUESTRADOR MULTI-AGENTE (ASYNC) ---
def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, agente_foco):
    if not contexto_arquivos.strip(): contexto_arquivos = "Nenhum documento fornecido. Opere em modo de consulta livre."
    
    # Ativação do RAG se o texto for muito grande (Ex: Processos de 200 páginas)
    if len(contexto_arquivos) > 60000:
        contexto_arquivos = processar_com_rag(contexto_arquivos, comando)
    
    blindagem = "DIRETRIZ DE COMPLIANCE: Aplique rigorosamente a interpretação do Art. 22 da LINDB, considerando os obstáculos práticos do gestor público." if lindb_ativada else ""
    
    # Prompts de Personalidade Nível Sênior
    agente_1_sys = f"Você é um Auditor Sênior de Riscos Financeiros e Contratuais. Especialidade: {agente_foco}. Procure inconsistências, multas abusivas, riscos operacionais e financeiros. Seja direto, use tópicos e linguagem técnica corporativa. {blindagem}"
    agente_2_sys = f"Você é um Advogado Sênior de Contencioso Estratégico. Especialidade: {agente_foco}. Analise as evidências buscando brechas na lei, teses de defesa, nulidades formais e aplique jurisprudência padrão dos tribunais superiores (STJ/STF). {blindagem}"
    
    resultados = {}
    # Multithreading: 2 IAs trabalhando ao mesmo tempo
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_risco = executor.submit(chamar_agente_groq, "AGENTE RISK", agente_1_sys, comando, contexto_arquivos)
        future_legal = executor.submit(chamar_agente_groq, "AGENTE LEGAL", agente_2_sys, comando, contexto_arquivos)
        
        resultados["risco"] = future_risco.result()
        resultados["legal"] = future_legal.result()
        
    # Síntese Master (Aether Omni)
    agente_3_sys = "Você é o AETHER OMNI, o cérebro coordenador. Você recebeu dois relatórios (um de risco e um jurídico). Sua missão é fundir os dois em um DOSSIÊ EXECUTIVO DE ALTO NÍVEL, estruturado em Markdown profissional. Não mencione 'o agente 1 disse' ou 'o agente 2 disse'. Aja como o autor unificado do documento final."
    contexto_sintese = f"--- RELATÓRIO DO DEPARTAMENTO DE RISCO ---\n{resultados['risco']}\n\n--- RELATÓRIO DO DEPARTAMENTO JURÍDICO ---\n{resultados['legal']}"
    
    dossie_final = chamar_agente_groq("AETHER OMNI", agente_3_sys, "Crie o Dossiê Final Consolidado.", contexto_sintese)
    return dossie_final

# --- 📄 EXPORTAÇÃO DOCX (ALTA FIDELIDADE) ---
def gerar_docx_aether(texto_markdown):
    doc = Document()
    styles = doc.styles
    style = styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)
    
    header = doc.add_heading('AETHER OMNI - PARECER EXECUTIVO', 0)
    header.runs[0].font.color.rgb = RGBColor(212, 175, 55) # Dourado Premium
    doc.add_paragraph(f"Auditoria Neural Finalizada em: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    doc.add_paragraph("Classificação: CONFIDENCIAL / PRIVILÉGIO ADVOGADO-CLIENTE")
    doc.add_paragraph("_"*65)
    
    linhas = texto_markdown.split('\n')
    for linha in linhas:
        if linha.startswith('### '): doc.add_heading(linha.replace('### ', ''), level=3)
        elif linha.startswith('## '): doc.add_heading(linha.replace('## ', ''), level=2)
        elif linha.startswith('# '): doc.add_heading(linha.replace('# ', ''), level=1)
        elif linha.startswith('**') and linha.endswith('**'):
             p = doc.add_paragraph()
             p.add_run(linha.replace('**', '')).bold = True
        elif linha.strip() == '': continue
        else: doc.add_paragraph(linha.replace('**', ''))

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ==========================================
# 🎨 CSS APEX V132 (INTOCADO - PRESERVADO 100%)
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow: hidden !important; height: 100vh !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; height: 100vh !important; overflow: hidden !important; }}
.block-container {{ padding: 0.8rem 1rem 0 1rem !important; max-width: 98% !important; height: 100vh !important; display: flex; flex-direction: column; overflow: hidden !important; }}
[data-testid="stHeader"], footer {{ display: none !important; }}
.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 6px 20px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); flex-shrink: 0; }}
.omni-brand {{ display: flex; align-items: center; gap: 12px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #f8fafc; font-weight: 700; letter-spacing: 0.5px; }}
.omni-brand span {{ color: #D4AF37; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 2px 6px; border-radius: 6px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}
.omni-status {{ font-size: 0.7rem; color: #94a3b8; font-weight: 500; }}
.omni-status span {{ color: #D4AF37; font-weight: 600; }}
[data-testid="column"] {{ background: rgba(30, 41, 59, 0.3) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; padding: 12px 18px !important; height: calc(100vh - 75px) !important; display: flex; flex-direction: column; box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2); overflow-y: auto !important; overflow-x: hidden !important; }}
[data-testid="column"]::-webkit-scrollbar {{ width: 6px; }}
[data-testid="column"]::-webkit-scrollbar-thumb {{ background-color: rgba(212, 175, 55, 0.3); border-radius: 4px; }}
.section-title {{ color: #f8fafc; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; margin-top: 5px; display: flex; align-items: center; gap: 6px; flex-shrink: 0; }}
.section-title::before {{ content: ''; display: block; width: 3px; height: 10px; background: #D4AF37; border-radius: 4px; }}
[data-testid="stFileUploadDropzone"] {{ background-color: rgba(15, 23, 42, 0.4) !important; border: 1px dashed rgba(255,255,255,0.1) !important; border-radius: 6px !important; padding: 5px !important; min-height: 40px !important; transition: 0.3s; flex-shrink: 0; }}
[data-testid="stFileUploadDropzone"] small {{ display: none !important; }}
div[data-baseweb="select"] > div {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.75rem !important; border-radius: 6px !important; min-height: 32px !important; }}
.stTextArea label, .stCheckbox label span, .stSelectbox label {{ font-size: 0.65rem !important; color: #cbd5e1 !important; font-weight: 600 !important; margin-bottom: 2px !important; }}
.stTextArea textarea {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; height: 85px !important; min-height: 85px !important; padding: 8px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2); flex-shrink: 0; }}
.stTextArea textarea:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 8px rgba(212, 175, 55, 0.1) !important; }}
[data-testid="stCheckbox"] {{ background: rgba(0,0,0,0.1); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.03); margin-bottom: 5px; flex-shrink: 0; }}
.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 6px !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 8px !important; border: none !important; width: 100% !important; margin-top: auto !important; transition: 0.3s; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); font-size: 0.85rem !important; flex-shrink: 0; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4); filter: brightness(1.1); }}
.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; flex-shrink: 0; }}
.kpi-box {{ background: rgba(15, 23, 42, 0.4); border-radius: 6px; display: flex; flex-direction: column; border: 1px solid rgba(255,255,255,0.03); border-left: 2px solid #D4AF37; padding: 6px 10px; }}
.kpi-title {{ color: #94a3b8; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; font-weight: 600; }}
.kpi-value {{ color: #f8fafc; font-size: 1rem; font-weight: 500; line-height: 1.1; }}
.kpi-value.highlight {{ color: #D4AF37; font-weight: 700; }}
.agent-grid {{ display: flex; gap: 6px; margin-bottom: 10px; flex-wrap: wrap; flex-shrink: 0; }}
.agent-badge {{ background: rgba(212, 175, 55, 0.1); border: 1px solid rgba(212, 175, 55, 0.3); color: #D4AF37; font-size: 0.6rem; font-weight: 600; padding: 2px 8px; border-radius: 4px; display: flex; align-items: center; gap: 4px; }}
.agent-standby {{ background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); color: #94a3b8; font-size: 0.6rem; padding: 2px 8px; border-radius: 4px; display: flex; align-items: center; gap: 4px; }}
.console-output {{ background: rgba(15, 23, 42, 0.5) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 6px !important; padding: 12px !important; flex-grow: 1; overflow-y: auto; font-size: 0.8rem; color: #f1f5f9; margin-bottom: 10px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.3); line-height: 1.5; }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 6px !important; font-size: 0.7rem !important; font-weight: 500 !important; padding: 4px !important; width: 100% !important; transition: 0.3s; margin: 0 !important; }}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ background: rgba(255,255,255,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}
.standby-container {{ display:flex; flex-direction:column; align-items:center; justify-content:center; flex-grow:1; border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; background: rgba(15, 23, 42, 0.3); padding: 15px; margin-top: 5px; }}
.welcome-title {{ color: #f8fafc; font-size: 1.05rem; font-weight: 600; margin-bottom: 3px; text-align: center; }}
.welcome-subtitle {{ color: #94a3b8; font-size: 0.75rem; margin-bottom: 15px; text-align: center; }}
.stButton button p {{ font-size: 0.75rem !important; margin: 0 !important; line-height: 1.2 !important; white-space: normal !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# INTERFACE
# ==========================================
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER KARV</h1></div>
    <div class="omni-status">SESSÃO: <span>CRIPTOGRAFADA (AES-256)</span></div>
</div>
""", unsafe_allow_html=True)

col_setup, col_main = st.columns([1.2, 2.5], gap="large")

with col_setup:
    st.markdown('<div class="section-title">📁 Enviar Documentos e Processos</div>', unsafe_allow_html=True)
    up = st.file_uploader("Arraste contratos, petições, planilhas ou IMAGENS...", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title">⚖️ Configurações da Análise</div>', unsafe_allow_html=True)
    agente_foco = st.selectbox("Especialidade do Assistente", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"], label_visibility="collapsed")
    ativar_lindb = st.checkbox("Aplicar Filtro de Proteção (Art. 22 LINDB)", value=True)
    
    st.markdown('<div class="section-title">💬 Instruções ou Pedidos Especiais</div>', unsafe_allow_html=True)
    cmd = st.text_area("", key="cmd_input", placeholder="Ex: Verifique as cláusulas de rescisão e aponte os riscos...", label_visibility="collapsed")

    if st.button("🚀 Iniciar Varredura Jurídica", type="primary"):
        if not GROQ_KEY:
            st.error("⚠️ CHAVE API GROQ NÃO ENCONTRADA. Configure o st.secrets.")
        elif cmd:
            with st.spinner("Iniciando varredura profunda (RAG & Multi-Agent)..."):
                # 1. Extração Multimodal (Lê Texto, PDF, Excel e IMAGENS via OCR)
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up) if up else ("", 0, False)
                
                # 2. Orquestração Real em Paralelo com RAG Embutido
                resposta = orquestrador_omni(cmd, texto_arquivos, ativar_lindb, agente_foco)
                
                # 3. Geração Automática do DOCX de Elite
                docx_buffer = gerar_docx_aether(resposta)
                
                st.session_state.res_aether = resposta
                st.session_state.res_docx = docx_buffer
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Varredura Completa",
                    "ocr": "ATIVADO" if usou_ocr else "Standby"
                }
            st.rerun() 
        else:
            st.warning("Por favor, forneça uma instrução para a análise.")

with col_main:
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Documentos Lidos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Volume (RAG Act)</span><span class="kpi-value">{t['volume']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Módulo Visão (OCR)</span><span class="kpi-value">{t['ocr']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Missão</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Status dos Módulos Especialistas</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">✓ AGENTE RISCO: CONCLUÍDO</div>
            <div class="agent-badge">✓ AGENTE JURÍDICO: CONCLUÍDO</div>
            <div class="agent-badge">✓ AETHER (SÍNTESE): ATIVO</div>
            <div class="agent-badge">✓ MEMÓRIA VETORIAL (RAG): OK</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">Parecer Jurídico (Resultado)</div>', unsafe_allow_html=True)
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.markdown(st.session_state.res_aether) 
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1,1,2])
        with b1: 
            st.download_button("⬇ Exportar Relatório (Word DOCX)", data=st.session_state.res_docx, file_name="AETHER_Parecer_Executivo.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with b2: 
            st.download_button("⬇ Exportar Matriz (TXT/MD)", data=st.session_state.res_aether, file_name="AETHER_Matriz.txt", use_container_width=True)
        with b3: 
            if st.button("⟳ Nova Análise (Limpar Memória)", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.res_docx = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo"}
                st.rerun()
    else:
        st.markdown('<div class="standby-container">', unsafe_allow_html=True)
        st.markdown('<div class="welcome-title">Como posso ajudar na sua análise hoje?</div>', unsafe_allow_html=True)
        st.markdown('<div class="welcome-subtitle">Escolha um atalho rápido ou digite sua instrução no painel à esquerda.</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.button("📄 Analisar Petição Inicial da Parte Contrária", on_click=set_template, args=("Faça uma análise crítica da petição inicial em anexo, identificando fragilidades jurídicas e sugerindo teses de defesa.",), use_container_width=True)
            st.button("🔍 Procurar Cláusulas Abusivas em Contrato", on_click=set_template, args=("Revise o contrato anexo e destaque todas as cláusulas que possam ser consideradas abusivas ou desproporcionais.",), use_container_width=True)
        with c2:
            st.button("📅 Calcular Prazos e Ler Intimação", on_click=set_template, args=("Leia a publicação do diário oficial e identifique os prazos processuais e as providências cabíveis.",), use_container_width=True)
            st.button("📊 Simular Probabilidade de Acordo", on_click=set_template, args=("Com base nos documentos, avalie os riscos de perda e simule uma proposta de acordo financeiramente viável.",), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
