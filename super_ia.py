import streamlit as st
import pandas as pd
import os, time, base64, io, re
import textwrap
import unicodedata
import concurrent.futures
import requests
import json
from datetime import datetime, timedelta
from PIL import Image

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO TOTAL & LIBS TÁTICAS ---
try: from groq import Groq
except ImportError: pass
try: import google.generativeai as genai
except ImportError: pass
try:
    from duckduckgo_search import DDGS
    MODULO_INTERNET = True
except ImportError: MODULO_INTERNET = False
try:
    import docx2txt
    from docx import Document
    from docx.shared import Pt, RGBColor
except ImportError: st.error("⚠️ Biblioteca 'python-docx' ausente.")
try: from fpdf import FPDF
except ImportError: pass
try: import PyPDF2
except ImportError: pass

# --- 👁️ VISÃO COMPUTACIONAL (OCR + OPENCV) ---
try:
    import cv2
    import numpy as np
    import pytesseract
    MODULO_VISAO = True
except ImportError: MODULO_VISAO = False

# --- 🧠 MEMÓRIA VETORIAL / RAG ---
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    MODULO_RAG = True
except ImportError: MODULO_RAG = False

# --- ⚙️ CONFIGURAÇÃO DE SEGURANÇA E UI (LAYOUT AMPLO E SIDEBAR EXPANDIDA) ---
st.set_page_config(page_title="AETHER KARV V327 APEX", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
CNJ_API_KEY = st.secrets.get("CNJ_API_KEY", "DEMO_KEY")

if GEMINI_KEY: genai.configure(api_key=GEMINI_KEY)

def get_data_hora_br():
    fuso_br = datetime.utcnow() - timedelta(hours=3)
    return fuso_br.strftime('%d/%m/%Y às %H:%M:%S')

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def gerar_botao_primario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: linear-gradient(135deg, #B8860B, #D4AF37); color: #020617; border-radius: 6px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); transition: 0.3s;"
    hover_css = "this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 15px rgba(212,175,55,0.4)';"
    out_css = "this.style.transform='translateY(0)'; this.style.boxShadow='0 4px 10px rgba(212,175,55,0.2)';"
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="{css}" onmouseover="{hover_css}" onmouseout="{out_css}">{label}</a>'

def gerar_botao_secundario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: rgba(255,255,255,0.05); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; transition: 0.3s;"
    hover_css = "this.style.background='rgba(212,175,55,0.1)'; this.style.borderColor='#D4AF37'; this.style.color='#fff';"
    out_css = "this.style.background='rgba(255,255,255,0.05)'; this.style.borderColor='rgba(255,255,255,0.15)'; this.style.color='#cbd5e1';"
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="{css}" onmouseover="{hover_css}" onmouseout="{out_css}">{label}</a>'

if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "res_docx" not in st.session_state: st.session_state.res_docx = None
if "res_pdf" not in st.session_state: st.session_state.res_pdf = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}

def set_template(texto): st.session_state.cmd_input = texto

# --- 🌐 MÓDULO INTERNET & CNJ DATAJUD ---
def buscar_na_internet(query):
    if not MODULO_INTERNET: return ""
    try:
        ddgs = DDGS()
        resultados = list(ddgs.text(query, max_results=3))
        res_str = "\n[AETHER WEB SEARCH INJETADO]:\n"
        for r in resultados: res_str += f"- {r['body']}\n"
        return res_str
    except: return ""

def consultar_datajud(numero_processo, api_key):
    if api_key == "DEMO_KEY" or not api_key:
        time.sleep(1.5) 
        return f"""
        [⚠️ ALERTA: MODO DE DEMONSTRAÇÃO ATIVADO (DADOS FICTÍCIOS) ⚠️]
        O sistema está operando sem uma Chave API Oficial. Os dados abaixo são 100% inventados para testar o sistema.
        
        Alvo da Busca (CPF/CNPJ/Processo): {numero_processo}
        
        DADOS DO PROCESSO SIMULADO:
        Tribunal: TRIBUNAL DE TESTES DE SOFTWARE
        Comarca: Foro Central de Demonstração
        Valor da Causa: R$ 10.000,00 (Valor Simulado)
        Data de Ajuizamento: {datetime.now().strftime('%d/%m/%Y')}
        
        QUALIFICAÇÃO DAS PARTES:
        Polo Ativo (Autor): Cliente Fictício S/A
        Polo Passivo (Réu): Empresa vinculada ao Documento {numero_processo}
        
        HISTÓRICO DE MOVIMENTAÇÕES:
        - Hoje: Conclusos para Despacho Simulado.
        - Ontem: Juntada de Petição de Teste.
        """
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search"
    headers = {"Authorization": f"ApiKey {api_key}", "Content-Type": "application/json"}
    payload = {"query": {"match": {"numeroProcesso": numero_processo}}}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200: return f"\n[DATAJUD OFICIAL]:\n{json.dumps(response.json())[:3000]}"
        else: return f"\n[ALERTA DATAJUD]: Status {response.status_code}"
    except Exception as e: return f"\n[ALERTA DATAJUD]: Falha ({str(e)})"

# --- 👁️ MOTOR DE INGESTÃO (NEXUS MULTIMODAL) ---
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
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                if MODULO_VISAO:
                    try:
                        imagem_pil = Image.open(arquivo)
                        img = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        denoised = cv2.fastNlMeansDenoising(gray, h=10)
                        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                        texto_ocr = pytesseract.image_to_string(thresh, config=r'--oem 3 --psm 6 lang=por')
                        if texto_ocr.strip():
                            texto_extraido += f"\n\n--- IMAGEM OCR: {arquivo.name} ---\n{texto_ocr}"
                            usou_ocr = True
                    except: pass
            sucesso += 1
        except: pass
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
    except: return texto[:90000]

# --- 🤖 HYDRA ENGINE ---
def chamar_agente_hydra(nome_agente, system_prompt, comando, contexto, tentar_internet=False):
    contexto_final = contexto
    if tentar_internet and MODULO_INTERNET:
        contexto_final += buscar_na_internet(comando)
        
    full_prompt = f"DIRETRIZ DE INVESTIGAÇÃO: {comando}\n\nEVIDÊNCIAS COLETADAS:\n{contexto_final}"
    
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
            except: continue 

    if GEMINI_KEY:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            prompt_gemini = f"{system_prompt}\n\n{full_prompt}"
            response = model.generate_content(prompt_gemini)
            return response.text, "GEMINI (1.5 Pro)"
        except Exception as e:
            return f"[{nome_agente}] Hydra Engine Falhou: {str(e)}", "OFFLINE"

    return f"[{nome_agente}] Erro Crítico: Sem chaves API configuradas.", "OFFLINE"

# --- 🚀 ORQUESTRADOR MULTI-AGENTE ---
def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, num_processo_cnj, agente_foco):
    tem_arquivos = len(contexto_arquivos.strip()) > 0
    dados_tribunal = consultar_datajud(num_processo_cnj, CNJ_API_KEY) if num_processo_cnj else ""
    contexto_final = contexto_arquivos + "\n" + dados_tribunal
    
    if len(contexto_final) > 60000: contexto_final = processar_com_rag(contexto_final, comando)
    blindagem = "Aplique a LINDB para invalidar responsabilizações injustas." if lindb_ativada else ""
    
    if tem_arquivos:
        agente_1_sys = f"Auditor Sênior. Foco: {agente_foco}. Cruze números com extenso e denuncie fraudes. Analise dados do DataJud se houver."
        agente_2_sys = f"Advogado Sócio. Foco: {agente_foco}. Busque nulidades absolutas e avalie jurisdição. {blindagem}"
        agente_3_sys = """Você é o AETHER OMNI, IA Jurídica. Crie o DOSSIÊ EXECUTIVO DE AUDITORIA.
        REGRA 1: Inicie com uma Matriz de Risco em Tabela Markdown (barras verticais |).
        | Nível de Risco | Item | Descrição | Ação Imediata |
        |---|---|---|---|
        Após a tabela, disserte profundamente sobre as fraudes, contratos e detalhes do processo."""
    else:
        agente_1_sys = f"Analista Investigativo. Extraia os dados do extrato DataJud. Deixe claro se for uma simulação."
        agente_2_sys = f"Estrategista Jurídico de Elite. Avalie a gravidade processual."
        agente_3_sys = """Você é o AETHER OMNI, IA de Inteligência Processual.
        Crie o RELATÓRIO DE INTELIGÊNCIA PROCESSUAL com base apenas no extrato judicial fornecido.
        REGRA 1: Inicie com uma Tabela Markdown perfeita com Barras Verticais (|):
        | Tribunal | Polo Ativo (Autor) | Polo Passivo (Réu) | Valor da Causa | Assunto Principal |
        |---|---|---|---|---|
        REGRA 2: Se os dados contiverem [MODO SIMULAÇÃO], deixe claro no texto que é uma demonstração do Aether."""

    resultados = {}
    motores_usados = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_risco = executor.submit(chamar_agente_hydra, "AGENTE RISK", agente_1_sys, comando, contexto_final, True)
        f_legal = executor.submit(chamar_agente_hydra, "AGENTE LEGAL", agente_2_sys, comando, contexto_final, False)
        resultados["risco"], m1 = f_risco.result()
        resultados["legal"], m2 = f_legal.result()
        motores_usados.add(m1)
        motores_usados.add(m2)
        
    contexto_sintese = f"--- PARTE 1 ---\n{resultados['risco']}\n\n--- PARTE 2 ---\n{resultados['legal']}"
    dossie_final, m3 = chamar_agente_hydra("AETHER OMNI", agente_3_sys, "Crie o Dossiê Final. Use Tabela Markdown com barras verticais (|).", contexto_sintese)
    motores_usados.add(m3)
    
    return dossie_final, " | ".join(list(motores_usados))

# --- 📄 EXPORTAÇÕES DE ALTO PADRÃO ---
def gerar_docx_aether(texto_markdown):
    doc = Document()
    font = doc.styles['Normal'].font
    font.name = 'Arial'; font.size = Pt(10)
    
    header = doc.add_heading('AETHER KARV - PARECER EXECUTIVO', 0)
    header.runs[0].font.color.rgb = RGBColor(212, 175, 55) 
    doc.add_paragraph(f"Auditoria Finalizada em: {get_data_hora_br()}")
    doc.add_paragraph("Classificação: CONFIDENCIAL / PRIVILÉGIO ADVOGADO-CLIENTE")
    doc.add_paragraph("_"*65)
    
    in_table = False
    table = None
    
    for linha in texto_markdown.split('\n'):
        linha_limpa = linha.strip()
        if not linha_limpa: continue

        is_table_line = False
        cols = []
        
        if linha_limpa.startswith('|') and linha_limpa.endswith('|'):
            if re.match(r'^\|[-\s\|]+\|$', linha_limpa): continue 
            cols = [c.strip() for c in linha_limpa.split('|')[1:-1]]
            is_table_line = True
        elif ('Nível de Risco' in linha_limpa or 'Tribunal' in linha_limpa or 'Polo Ativo' in linha_limpa) and (',' in linha_limpa or '\t' in linha_limpa):
            separador = '\t' if '\t' in linha_limpa else ','
            cols = [c.strip() for c in linha_limpa.split(separador)]
            if len(cols) >= 3: is_table_line = True

        if is_table_line:
            if not in_table:
                table = doc.add_table(rows=1, cols=len(cols))
                table.style = 'Table Grid'
                hdr_cells = table.rows[0].cells
                for i, col in enumerate(cols):
                    if i < len(hdr_cells):
                        hdr_cells[i].text = col.replace('**', '')
                        hdr_cells[i].paragraphs[0].runs[0].bold = True 
                in_table = True
            else:
                row_cells = table.add_row().cells
                for i, col in enumerate(cols):
                    if i < len(row_cells): row_cells[i].text = col.replace('**', '')
            continue

        in_table = False
        if linha.startswith('### '): doc.add_heading(linha.replace('### ', ''), level=3)
        elif linha.startswith('## '): doc.add_heading(linha.replace('## ', ''), level=2)
        elif linha.startswith('# '): doc.add_heading(linha.replace('# ', ''), level=1)
        elif linha.startswith('**') and linha.endswith('**'): doc.add_paragraph().add_run(linha.replace('**', '')).bold = True
        else: doc.add_paragraph(linha.replace('**', ''))

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def sanitize_for_pdf(texto):
    return unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')

def gerar_pdf_aether(texto_markdown):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("helvetica", size=10)
        
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 10, txt="AETHER KARV - PARECER EXECUTIVO", ln=1, align='C')
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 8, txt=f"Gerado em: {sanitize_for_pdf(get_data_hora_br())}", ln=1, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        texto_limpo = texto_markdown.replace('**', '').replace('### ', '').replace('## ', '').replace('# ', '')
        texto_seguro = sanitize_for_pdf(texto_limpo)
        
        for linha in texto_seguro.split('\n'):
            linha_filtrada = linha.strip()
            if not linha_filtrada: 
                pdf.ln(3); continue

            if re.match(r'^\|[-\s\|]+\|$', linha_filtrada): continue
            
            if linha_filtrada.startswith('|') and linha_filtrada.endswith('|'):
                cols = [c.strip() for c in linha_filtrada.split('|')[1:-1]]
                linha_filtrada = "  |  ".join(cols)
            elif ('Nivel de Risco' in linha_filtrada or 'Tribunal' in linha_filtrada) and (',' in linha_filtrada or '\t' in linha_filtrada):
                sep = '\t' if '\t' in linha_filtrada else ','
                cols = [c.strip() for c in linha_filtrada.split(sep)]
                linha_filtrada = "  |  ".join(cols)

            pedacos = textwrap.wrap(linha_filtrada, width=85, break_long_words=True)
            for pedaco in pedacos:
                pdf.cell(0, 6, txt=pedaco, ln=1)
                    
        return bytes(pdf.output())

    except Exception as e:
        emergencia = FPDF()
        emergencia.add_page()
        emergencia.set_font("helvetica", size=10)
        emergencia.cell(0, 6, txt="ERRO PDF: Utilize exportacao DOCX.", ln=1)
        emergencia.cell(0, 6, txt=f"Log: {str(e)[:50]}", ln=1)
        return bytes(emergencia.output())

# ==========================================
# 🎨 CSS APEX V327 (WORKSPACE DESIGN)
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow-x: hidden !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
[data-testid="stHeader"], footer {{ display: none !important; }}

/* SIDEBAR STYLING */
[data-testid="stSidebar"] {{ background: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(212, 175, 55, 0.2) !important; padding-top: 20px; }}
[data-testid="stSidebarContent"] {{ padding: 0 15px; }}

.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 10px 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); }}
.omni-brand {{ display: flex; align-items: center; gap: 12px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.2rem; color: #f8fafc; font-weight: 700; letter-spacing: 0.5px; }}
.omni-brand span {{ color: #D4AF37; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 2px 6px; border-radius: 6px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}

.section-title {{ color: #f8fafc; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; margin-top: 15px; display: flex; align-items: center; gap: 6px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }}
.section-title::before {{ content: ''; display: block; width: 3px; height: 12px; background: #D4AF37; border-radius: 4px; }}

div[data-baseweb="select"] > div {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; }}
.stTextArea label, .stCheckbox label span, .stTextInput label {{ font-size: 0.7rem !important; color: #cbd5e1 !important; font-weight: 600 !important; }}
.stTextArea textarea, .stTextInput input {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; }}
.stTextArea textarea:focus, .stTextInput input:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 8px rgba(212, 175, 55, 0.1) !important; }}

.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 6px !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 10px !important; border: none !important; width: 100% !important; transition: 0.3s; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); margin-top: 15px; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4); }}

/* MAIN CONTENT AREA */
.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px; }}
.kpi-box {{ background: rgba(30, 41, 59, 0.4); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); border-left: 3px solid #D4AF37; padding: 12px 15px; backdrop-filter: blur(10px); }}
.kpi-title {{ color: #94a3b8; font-size: 0.60rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; display:block; margin-bottom: 4px; }}
.kpi-value {{ color: #f8fafc; font-size: 1.1rem; font-weight: 600; line-height: 1.2; display:block; }}
.kpi-value.highlight {{ color: #D4AF37; font-weight: 700; }}

/* TABS STYLING */
[data-testid="stTabs"] button {{ padding: 10px 20px !important; font-weight: 600 !important; color: #94a3b8 !important; border-bottom: 2px solid transparent !important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; background: rgba(212, 175, 55, 0.05) !important; border-radius: 6px 6px 0 0; }}

.standby-container {{ display:flex; flex-direction:column; align-items:center; justify-content:center; height: 60vh; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; background: rgba(30, 41, 59, 0.2); padding: 20px; }}
.welcome-title {{ color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; text-align: center; }}
.welcome-subtitle {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; text-align: center; max-width: 600px; }}

.stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 6px !important; font-weight: 600 !important; transition: 0.3s; }}
.stButton > button[kind="secondary"]:hover {{ background: rgba(212,175,55,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# INTERFACE PRINCIPAL (SIDEBAR WORKSPACE)
# ==========================================

with st.sidebar:
    st.markdown('<div class="omni-brand" style="margin-bottom: 20px;"><h1>AETHER KARV</h1><span>V327 SUPREME</span></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">📁 Base de Conhecimento</div>', unsafe_allow_html=True)
    up = st.file_uploader("Contratos, petições ou imagens...", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title">⚖️ Motor Jurídico</div>', unsafe_allow_html=True)
    agente_foco = st.selectbox("Especialidade", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"], label_visibility="collapsed")
    ativar_lindb = st.checkbox("Filtro de Proteção (Art. 22 LINDB)", value=True)
    
    st.markdown('<div class="section-title">🏛️ DataJud (CNJ)</div>', unsafe_allow_html=True)
    if CNJ_API_KEY == "DEMO_KEY":
        st.warning("⚠️ Modo Simulação: Dados gerados serão fictícios (Mockup).")
    num_processo_input = st.text_input("Nº do Processo / CNPJ", placeholder="Insira para extração...", label_visibility="collapsed")

    st.markdown('<div class="section-title">💬 Comando Direto</div>', unsafe_allow_html=True)
    cmd = st.text_area("", key="cmd_input", placeholder="Instruções para a IA...", label_visibility="collapsed")

    if st.button("🚀 INICIAR AUDITORIA OMNI", type="primary"):
        if not GROQ_KEY and not GEMINI_KEY:
            st.error("⚠️ ERRO: Chaves API não configuradas.")
        elif cmd or up or num_processo_input:
            with st.spinner("Processando pipeline de dados..."):
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up) if up else ("", 0, False)
                resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, ativar_lindb, num_processo_input, agente_foco)
                
                docx_buffer = gerar_docx_aether(resposta)
                pdf_data = gerar_pdf_aether(resposta)
                
                st.session_state.res_aether = resposta
                st.session_state.res_docx = docx_buffer.getvalue()
                st.session_state.res_pdf = pdf_data
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": get_data_hora_br().split("às ")[1], 
                    "risco": "Missão Cumprida",
                    "ocr": "Online" if usou_ocr else ("Standby" if MODULO_VISAO else "Offline"),
                    "motor": motor_usado
                }
            st.rerun() 
        else:
            st.warning("Forneça um documento, processo ou comando.")

# --- ÁREA PRINCIPAL (WORKSPACE) ---
st.markdown(f"""
<div class="omni-topbar">
    <div style="font-weight: 600; color: #f8fafc; font-size: 0.9rem;">DASHBOARD ANALÍTICO</div>
    <div style="font-size: 0.75rem; color: #94a3b8;">Status de Conexão: <span style="color: #22c55e;">ESTÁVEL</span></div>
</div>
""", unsafe_allow_html=True)

t = st.session_state.telemetria
st.markdown(f"""
<div class="custom-kpi-grid">
    <div class="kpi-box"><span class="kpi-title">Documentos Digeridos</span><span class="kpi-value">{t['arquivos']}</span></div>
    <div class="kpi-box"><span class="kpi-title">Nó de Processamento</span><span class="kpi-value highlight">{t['motor']}</span></div>
    <div class="kpi-box"><span class="kpi-title">Módulo de Visão</span><span class="kpi-value">{t['ocr']}</span></div>
    <div class="kpi-box"><span class="kpi-title">Status da Operação</span><span class="kpi-value highlight">{t['risco']}</span></div>
</div>
""", unsafe_allow_html=True)

if st.session_state.res_aether:
    # SISTEMA DE ABAS (TABS) PARA ORGANIZAÇÃO SUPREMA
    tab1, tab2, tab3 = st.tabs(["📊 Dossiê Executivo", "📥 Central de Exportação", "🕵️‍♂️ Código Raw"])
    
    with tab1:
        st.markdown('<div style="background: rgba(15,23,42,0.5); padding: 25px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px;">', unsafe_allow_html=True)
        st.markdown(st.session_state.res_aether)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab2:
        st.write("Selecione o formato para baixar o relatório blindado gerado pelo Aether Karv:")
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(gerar_botao_primario(st.session_state.res_docx, "AETHER_Parecer.docx", "📄 Download WORD", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"), unsafe_allow_html=True)
        with c2: st.markdown(gerar_botao_primario(st.session_state.res_pdf, "AETHER_Parecer.pdf", "📕 Download PDF", "application/pdf"), unsafe_allow_html=True)
        with c3: st.markdown(gerar_botao_secundario(st.session_state.res_aether.encode('utf-8'), "AETHER_Parecer.txt", "📝 Download TXT", "text/plain"), unsafe_allow_html=True)
        with c4: st.markdown(gerar_botao_secundario(st.session_state.res_aether.encode('utf-8'), "AETHER_Parecer.md", "📊 Download MD", "text/markdown"), unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⟳ Limpar Workspace (Nova Análise)", use_container_width=True):
            st.session_state.res_aether = None
            st.session_state.res_docx = None
            st.session_state.res_pdf = None
            st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}
            st.rerun()
            
    with tab3:
        st.write("Visualização nativa em Markdown gerada pelos motores da Inteligência Artificial.")
        st.code(st.session_state.res_aether, language="markdown")
        
else:
    st.markdown('<div class="standby-container">', unsafe_allow_html=True)
    st.markdown('<div class="welcome-title">O Workspace do Aether Karv está Online.</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-subtitle">Utilize a barra de ferramentas à esquerda para injetar documentos, conectar-se ao DataJud ou inserir instruções paramétricas para a Inteligência Artificial.</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📄 Simular Análise de Risco de Contrato", use_container_width=True): set_template("Faça uma due diligence deste documento e aponte cláusulas abusivas.")
    with col_b:
        if st.button("🏛️ Simular Diagnóstico Processual", use_container_width=True): set_template("Analise as movimentações judiciais e sugira a melhor estratégia de defesa.")
    st.markdown('</div>', unsafe_allow_html=True)
