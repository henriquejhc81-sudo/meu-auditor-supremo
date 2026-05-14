import streamlit as st
import pandas as pd
import os, time, base64, io, re
import textwrap
import concurrent.futures
from PIL import Image

# --- 🛡️ LIBS TÁTICAS & BLINDAGEM ---
try:
    from groq import Groq
except ImportError:
    pass

try:
    import google.generativeai as genai
except ImportError:
    pass

try:
    from duckduckgo_search import DDGS
    MODULO_INTERNET = True
except ImportError:
    MODULO_INTERNET = False

try:
    import docx2txt
    from docx import Document
    from docx.shared import Pt, RGBColor
except ImportError:
    st.error("⚠️ Biblioteca DOCX ausente.")

try:
    import markdown
    from xhtml2pdf import pisa 
except ImportError:
    pass

try:
    import PyPDF2
except ImportError:
    pass

# --- 👁️ VISÃO COMPUTACIONAL ---
try:
    import cv2
    import numpy as np
    import pytesseract
    MODULO_VISAO = True
except ImportError:
    MODULO_VISAO = False

# --- 🧠 MEMÓRIA VETORIAL / RAG ---
try:
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    MODULO_RAG = True
except ImportError:
    MODULO_RAG = False

# --- ⚙️ SETUP E SEGURANÇA ---
st.set_page_config(page_title="AETHER KARV V312 APEX", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "res_docx" not in st.session_state: st.session_state.res_docx = None
if "res_pdf" not in st.session_state: st.session_state.res_pdf = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}

def set_template(texto):
    st.session_state.cmd_input = texto

# --- 🌐 MÓDULO INTERNET (INVISÍVEL E SILENCIOSO) ---
def buscar_na_internet(query):
    if not MODULO_INTERNET: return ""
    try:
        ddgs = DDGS()
        resultados = list(ddgs.text(query, max_results=3))
        res_str = "\n[AETHER WEB SEARCH INJETADO]:\n"
        for r in resultados:
            res_str += f"- {r['body']}\n"
        return res_str
    except:
        return ""

# --- 👁️ MOTOR DE INGESTÃO (RESGATADO V310 COM .TIFF e .BMP) ---
def extrator_nexus_v3(arquivos_upados):
    texto_extraido = ""
    sucesso = 0
    usou_ocr = False
    
    for arquivo in arquivos_upados:
        try:
            filename = arquivo.name.lower()
            if filename.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- CSV: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- XLSX: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.docx'):
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{docx2txt.process(arquivo)}"
            elif filename.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            elif filename.endswith('.pdf'):
                texto_pdf_nativo = ""
                try:
                    pdf_reader = PyPDF2.PdfReader(arquivo)
                    for page in pdf_reader.pages:
                        extraido = page.extract_text()
                        if extraido: texto_pdf_nativo += extraido + "\n"
                except: pass
                if texto_pdf_nativo.strip(): texto_extraido += f"\n\n--- PDF: {arquivo.name} ---\n{texto_pdf_nativo}"
            
            # RESGATE DA VISÃO AMPLIADA DA V310
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                if MODULO_VISAO:
                    try:
                        imagem_pil = Image.open(arquivo)
                        img = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        denoised = cv2.fastNlMeansDenoising(gray, h=10)
                        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                        
                        tess_config = r'--oem 3 --psm 6 lang=por'
                        texto_ocr = pytesseract.image_to_string(thresh, config=tess_config)
                        
                        if texto_ocr.strip():
                            texto_extraido += f"\n\n--- IMAGEM OCR (Visão Blindada): {arquivo.name} ---\n{texto_ocr}"
                            usou_ocr = True
                        else:
                            texto_extraido += f"\n[AETHER: Nenhum texto detetável na foto: {arquivo.name}]"
                    except Exception as e_ocr:
                        texto_extraido += f"\n[AETHER: Falha na extração OCR: {str(e_ocr)}]"
            sucesso += 1
        except Exception:
            pass
    return texto_extraido, sucesso, usou_ocr

def processar_com_rag(texto, comando):
    if not MODULO_RAG or not GEMINI_KEY: return texto[:90000]
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
        chunks = text_splitter.split_text(texto)
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=GEMINI_KEY, model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embeddings)
        docs_relevantes = vector_store.similarity_search(comando, k=8)
        return "\n...\n".join([doc.page_content for doc in docs_relevantes])
    except:
        return texto[:90000]

# --- 🤖 HYDRA ENGINE (MEGA HÍBRIDO GROQ + GEMINI COM ANTI-BLOCK V311) ---
def chamar_agente_hydra(nome_agente, system_prompt, comando, contexto, tentar_internet=False):
    contexto_final = contexto
    if tentar_internet and MODULO_INTERNET:
        contexto_final += buscar_na_internet(comando)
        
    full_prompt = f"DIRETRIZ DE INVESTIGAÇÃO: {comando}\n\nEVIDÊNCIAS COLETADAS:\n{contexto_final}"
    
    # 1º ATAQUE: GROQ (Velocidade Extrema)
    if GROQ_KEY:
        arsenal_groq = ["llama-3.3-70b-versatile", "llama-3.2-90b-text-preview", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        client = Groq(api_key=GROQ_KEY)
        for modelo in arsenal_groq:
            try:
                for tentativa in range(2): 
                    try:
                        completion = client.chat.completions.create(
                            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": full_prompt}],
                            model=modelo, temperature=0.1
                        )
                        return completion.choices[0].message.content, f"GROQ ({modelo.split('-')[1]})"
                    except Exception as e:
                        if "429" in str(e): time.sleep(2) 
                        else: raise e
            except:
                continue 

    # 2º ATAQUE (FALLBACK INVISÍVEL): GOOGLE GEMINI (Resiliência Absoluta)
    if GEMINI_KEY:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            prompt_gemini = f"{system_prompt}\n\n{full_prompt}"
            response = model.generate_content(prompt_gemini)
            return response.text, "GEMINI (1.5 Pro)"
        except Exception as e:
            return f"[{nome_agente}] Hydra Engine Falhou: {str(e)}", "OFFLINE"

    return f"[{nome_agente}] Erro Crítico: Sem chaves API configuradas.", "OFFLINE"

# --- 🚀 ORQUESTRADOR MULTI-AGENTE (RESGATE DO SNIPER FORENSE DA V310) ---
def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, agente_foco):
    if not contexto_arquivos.strip(): contexto_arquivos = "Nenhum documento fornecido. Opere em modo de consulta livre."
    if len(contexto_arquivos) > 60000: contexto_arquivos = processar_com_rag(contexto_arquivos, comando)
    
    blindagem = "DIRETRIZ DE COMPLIANCE: Aplique rigorosamente a interpretação do Art. 22 da LINDB, considerando obstáculos práticos e alertando sobre responsabilização exagerada." if lindb_ativada else ""
    
    # ⚠️ RESGATE V310: PROMPT FORENSE ANTI-AUTOCORREÇÃO DE LETALIDADE MÁXIMA ⚠️
    agente_1_sys = f"Você é um Auditor Forense Investigativo Sênior. Especialidade: {agente_foco}. REGRA DE OURO: PROIBIDO AUTOCORRIGIR O TEXTO. Se o contrato diz 'R$ 150.000.000,00' e o texto diz '(cento e oitenta milhões)', denuncie como fraude material. Identifique paradoxos temporais (datas de leis futuras) e multas absurdas. Apenas analise os dados fornecidos, não crie fraudes genéricas. {blindagem}"
    
    agente_2_sys = f"Você é um Advogado Sênior Sócio de Escritório de Elite. Especialidade: {agente_foco}. Analise buscando nulidades contratuais, furos de competência (como foros internacionais ou taxas de câmbio para contratos locais), violações a leis de licitação e pegadinhas legais. Aponte explicitamente os erros na estrutura jurídica. {blindagem}"
    
    resultados = {}
    motores_usados = set()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_risco = executor.submit(chamar_agente_hydra, "AGENTE RISK", agente_1_sys, comando, contexto_arquivos, True) # Internet ativa para Risco
        f_legal = executor.submit(chamar_agente_hydra, "AGENTE LEGAL", agente_2_sys, comando, contexto_arquivos, False)
        
        resultados["risco"], m1 = f_risco.result()
        resultados["legal"], m2 = f_legal.result()
        motores_usados.add(m1)
        motores_usados.add(m2)
        
    agente_3_sys = "Você é o AETHER OMNI, o cérebro consolidador. Recebeu um relatório forense e um jurídico. Funda os dois em um DOSSIÊ EXECUTIVO em Markdown de luxo. É OBRIGATÓRIO incluir as inconsistências numéricas exatas e paradoxos temporais encontrados pelo auditor forense."
    contexto_sintese = f"--- RELATÓRIO AUDITORIA FORENSE ---\n{resultados['risco']}\n\n--- RELATÓRIO JURÍDICO ---\n{resultados['legal']}"
    
    dossie_final, m3 = chamar_agente_hydra("AETHER OMNI", agente_3_sys, "Crie o Dossiê Final Consolidado, evidenciando as falhas materiais exatas.", contexto_sintese)
    motores_usados.add(m3)
    
    motor_final = " | ".join(list(motores_usados))
    return dossie_final, motor_final

# --- 📄 EXPORTAÇÕES (RESGATE DA QUALIDADE V310) ---
def gerar_docx_aether(texto_markdown):
    doc = Document()
    styles = doc.styles
    font = styles['Normal'].font
    font.name = 'Arial'
    font.size = Pt(11)
    
    header = doc.add_heading('AETHER KARV - PARECER EXECUTIVO', 0)
    header.runs[0].font.color.rgb = RGBColor(212, 175, 55) 
    doc.add_paragraph(f"Auditoria Neural Finalizada em: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    doc.add_paragraph("Classificação: CONFIDENCIAL / PRIVILÉGIO ADVOGADO-CLIENTE")
    doc.add_paragraph("_"*65)
    
    for linha in texto_markdown.split('\n'):
        if linha.startswith('### '): doc.add_heading(linha.replace('### ', ''), level=3)
        elif linha.startswith('## '): doc.add_heading(linha.replace('## ', ''), level=2)
        elif linha.startswith('# '): doc.add_heading(linha.replace('# ', ''), level=1)
        elif linha.startswith('**') and linha.endswith('**'): doc.add_paragraph().add_run(linha.replace('**', '')).bold = True
        elif linha.strip() == '': continue
        else: doc.add_paragraph(linha.replace('**', ''))

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def gerar_pdf_aether(texto_markdown):
    try:
        texto_sanitizado = texto_markdown.replace('______________________________________', '<hr>')
        html_content = markdown.markdown(texto_sanitizado, extras=['tables', 'fenced-code-blocks'])
        
        # RESGATE DO TIMBRE CONFIDENCIAL DA V310
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{ size: a4; margin: 2cm; }}
                body {{ font-family: Arial, sans-serif; font-size: 10pt; color: #000; line-height: 1.4; }}
                .cabecalho {{ text-align: center; margin-bottom: 15px; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }}
                .cabecalho h1 {{ color: #D4AF37; font-size: 14pt; margin: 0; }}
                .cabecalho p {{ color: #7f8c8d; font-size: 8pt; margin: 2px 0; }}
                h1, h2, h3 {{ color: #D4AF37; margin-top: 15px; margin-bottom: 5px; }}
                h1 {{ font-size: 12pt; text-transform: uppercase; }}
                h2 {{ font-size: 11pt; }}
                h3 {{ font-size: 10pt; }}
                p, li {{ margin-bottom: 5px; text-align: justify; }}
                strong {{ font-weight: bold; color: #000; }}
            </style>
        </head>
        <body>
            <div class="cabecalho">
                <h1>AETHER KARV - PARECER EXECUTIVO</h1>
                <p>Auditoria Neural: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                <p>CONFIDENCIAL / PRIVILÉGIO ADVOGADO-CLIENTE</p>
            </div>
            {html_content}
        </body>
        </html>
        """
        
        buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html_template.encode("UTF-8")), dest=buffer, encoding='UTF-8')
        
        if pisa_status.err: raise Exception("Falha na renderização do HTML")
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        return f"ERRO CRÍTICO NO MOTOR DE PDF.\n\nUtilize exportação DOCX (Word).\n\nErro: {str(e)}".encode('utf-8')

# ==========================================
# 🎨 CSS APEX V312 (RESGATE DO DESIGN V310 ZERO SCROLL COMPLETO)
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

[data-testid="column"] {{ background: rgba(30, 41, 59, 0.3) !important; backdrop-filter: blur(16px) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 12px !important; padding: 12px 18px !important; height: calc(100vh - 75px) !important; display: flex; flex-direction: column; box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2); overflow: hidden !important; }}

div[data-testid="stVerticalBlockBorderWrapper"] {{ background: rgba(15, 23, 42, 0.3) !important; border-radius: 6px !important; border: 1px solid rgba(255,255,255,0.05) !important; box-shadow: inset 0 2px 10px rgba(0,0,0,0.3) !important; padding: 10px !important; margin-bottom: 10px; }}

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

.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 6px !important; font-size: 0.7rem !important; font-weight: 500 !important; padding: 4px !important; width: 100% !important; transition: 0.3s; margin: 0 !important; }}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ background: rgba(255,255,255,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}

.standby-container {{ display:flex; flex-direction:column; align-items:center; justify-content:center; flex-grow:1; border: 1px dashed rgba(255,255,255,0.1); border-radius: 8px; background: rgba(15, 23, 42, 0.3); padding: 15px; margin-top: 5px; }}
.welcome-title {{ color: #f8fafc; font-size: 1.05rem; font-weight: 600; margin-bottom: 3px; text-align: center; }}
.welcome-subtitle {{ color: #94a3b8; font-size: 0.75rem; margin-bottom: 15px; text-align: center; }}
.stButton button p {{ font-size: 0.7rem !important; margin: 0 !important; line-height: 1.2 !important; white-space: normal !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER KARV</h1><span>V312 APEX HYDRA</span></div>
    <div class="omni-status">SESSÃO: <span>CRIPTOGRAFADA</span> | NÚCLEO: <span>MULTI-LLM</span></div>
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
        if not GROQ_KEY and not GEMINI_KEY:
            st.error("⚠️ ERRO CRÍTICO: Nenhuma chave API configurada no st.secrets.")
        elif cmd:
            with st.spinner("Motor Hydra Ativado. Processando Multi-Agentes..."):
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up) if up else ("", 0, False)
                
                resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, ativar_lindb, agente_foco)
                
                docx_buffer = gerar_docx_aether(resposta)
                pdf_data = gerar_pdf_aether(resposta)
                
                st.session_state.res_aether = resposta
                st.session_state.res_docx = docx_buffer
                st.session_state.res_pdf = pdf_data
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Varredura Completa",
                    "ocr": "ATIVADO" if usou_ocr else ("Standby" if MODULO_VISAO else "OFFLINE"),
                    "motor": motor_usado
                }
            st.rerun() 
        else:
            st.warning("Por favor, forneça uma instrução para a análise.")

with col_main:
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Documentos Lidos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Motor IA Ativo</span><span class="kpi-value" style="color:#D4AF37;">{t['motor']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Módulo Visão (OCR)</span><span class="kpi-value">{t['ocr']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Missão</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Status dos Módulos Especialistas</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown(f"""
        <div class="agent-grid">
            <div class="agent-badge">✓ AGENTE FORENSE: CONCLUÍDO</div>
            <div class="agent-badge">✓ AGENTE JURÍDICO: CONCLUÍDO</div>
            <div class="agent-badge">✓ AETHER (SÍNTESE): ATIVO</div>
            <div class="agent-badge">✓ MEMÓRIA (RAG): {'OK' if MODULO_RAG else 'OFFLINE'}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">Ações e Exportação</div>', unsafe_allow_html=True)
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1: st.download_button("📄 Word (DOCX)", data=st.session_state.res_docx, file_name="AETHER_Parecer.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with b2: st.download_button("📕 PDF Blindado", data=st.session_state.res_pdf, file_name="AETHER_Parecer.pdf", mime="application/pdf", use_container_width=True)
        with b3: st.download_button("📝 Texto (TXT)", data=st.session_state.res_aether, file_name="AETHER_Parecer.txt", mime="text/plain", use_container_width=True)
        with b4: st.download_button("📊 Matriz (MD)", data=st.session_state.res_aether, file_name="AETHER_Parecer.md", mime="text/markdown", use_container_width=True)
        with b5: 
            if st.button("⟳ Nova Análise", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.res_docx = None
                st.session_state.res_pdf = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}
                st.rerun()

        st.markdown('<div class="section-title" style="margin-top:10px;">Parecer Jurídico (Resultado)</div>', unsafe_allow_html=True)
        
        with st.container(height=350):
            st.markdown(st.session_state.res_aether)
            
        with st.expander("📋 Copiar Parecer (Código Fonte)"):
            st.code(st.session_state.res_aether, language="markdown")
            
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
            st.button("🌐 Pesquisar Jurisprudência Atual", on_click=set_template, args=("Busque as decisões mais recentes sobre este tema na internet.",), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
