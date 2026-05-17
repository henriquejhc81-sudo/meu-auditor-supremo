import streamlit as st

# ⚠️ V336 APEX: SEQUÊNCIA DE IGNIÇÃO BLINDADA ⚠️
st.set_page_config(page_title="AETHER KARV V336 APEX", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

import pandas as pd
import os, time, base64, io, re
import textwrap
import unicodedata
import concurrent.futures
import requests
import json
import sqlite3
from datetime import datetime, timedelta
from PIL import Image

# ==========================================
# 🗄️ MÓDULO DE BANCO DE DADOS (V336 APEX)
# ==========================================
def init_db():
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, data_hora TEXT, tipo TEXT, conteudo TEXT)')
    # Cria o usuário admin padrão se não existir
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

def save_dossier(username, tipo, conteudo):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (username, data_hora, tipo, conteudo) VALUES (?, ?, ?, ?)", (username, get_data_hora_br(), tipo, conteudo))
    conn.commit()
    conn.close()

def load_history(username):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("SELECT data_hora, tipo, conteudo FROM history WHERE username = ? ORDER BY id DESC", (username,))
    data = c.fetchall()
    conn.close()
    return data

init_db()

# --- CONTROLE DE SESSÃO E LOGIN ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

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
try:
    import cv2
    import numpy as np
    import pytesseract
    MODULO_VISAO = True
except ImportError: MODULO_VISAO = False
try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    MODULO_RAG = True
except ImportError: MODULO_RAG = False

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

# --- 👁️ MOTOR DE INGESTÃO (NEXUS) ---
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

def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, num_processo_cnj, agente_foco, ativar_redlining, valor_hora):
    dados_tribunal = consultar_datajud(num_processo_cnj, CNJ_API_KEY) if num_processo_cnj else ""
    contexto_final = contexto_arquivos + "\n" + dados_tribunal
    
    tamanho_dados = len(contexto_final) + len(comando)
    horas_humanas_estimadas = max(1.5, tamanho_dados / 4000) 
    faturamento_total = horas_humanas_estimadas * valor_hora
    
    if len(contexto_final) > 60000: contexto_final = processar_com_rag(contexto_final, comando)
    blindagem = "Aplique a LINDB para invalidar responsabilizações injustas." if lindb_ativada else ""
    
    diretriz_redlining = ""
    if ativar_redlining:
        diretriz_redlining = """
        REGRA 3 (REDLINING AUTOMÁTICO): Para cada erro grave, você DEVE gerar a correção exata. 
        Use EXATAMENTE o prefixo: [REDLINING - CLAUSULA SUGERIDA]:
        """
    
    modo_contrato = len(contexto_arquivos.strip()) > 0 or len(comando) > 100 or "Contrato" in agente_foco

    if modo_contrato:
        agente_1_sys = f"Auditor Sênior. Foco: {agente_foco}. Cruze números e denuncie fraudes."
        agente_2_sys = f"Advogado Sócio. Foco: {agente_foco}. Busque nulidades absolutas. {blindagem}"
        agente_3_sys = f"""Você é o AETHER OMNI, IA Jurídica. Crie o DOSSIÊ EXECUTIVO DE AUDITORIA DE CONTRATOS.
        REGRA 1: Inicie com uma Matriz de Risco em Tabela Markdown (barras verticais |).
        | Nível de Risco | Item | Descrição | Ação Imediata |
        |---|---|---|---|
        REGRA 2: Disserte sobre as fraudes.
        {diretriz_redlining}"""
    else:
        agente_1_sys = f"Analista Investigativo. Extraia os dados do DataJud."
        agente_2_sys = f"Estrategista Jurídico de Elite. Avalie a gravidade processual."
        agente_3_sys = f"""Você é o AETHER OMNI. Crie o RELATÓRIO DE INTELIGÊNCIA PROCESSUAL.
        REGRA 1: Inicie com uma Tabela Markdown perfeita com Barras Verticais (|):
        | Tribunal | Polo Ativo (Autor) | Polo Passivo (Réu) | Valor da Causa | Assunto Principal |
        |---|---|---|---|---|
        REGRA 2: Deixe claro se for simulação.
        {diretriz_redlining}"""

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
    
    bloco_fatura = f"""
    
---
### 💰 Fatura Pro-Forma (Timesheet Audit)
* **Tempo Humano Estimado Poupado:** {horas_humanas_estimadas:.1f} horas
* **Valor da Hora Técnica (Informada):** R$ {valor_hora:.2f}
* **Total Sugerido para Cobrança do Cliente:** **R$ {faturamento_total:.2f}**
"""
    dossie_final += bloco_fatura
    return dossie_final, " | ".join(list(motores_usados))

# --- 📄 EXPORTAÇÕES OMNI PARSER ---
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
    is_redlining_mode = False
    
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
            linha_limpa_csv = linha_limpa.replace('"', '')
            separador = '\t' if '\t' in linha_limpa_csv else ','
            cols = [c.strip() for c in linha_limpa_csv.split(separador)]
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
        
        if linha.startswith('#') or linha.startswith('**') or 'CONCLUSÃO' in linha.upper() or 'RECOMENDAÇÕES' in linha.upper() or '---' in linha:
            is_redlining_mode = False 

        if '[REDLINING' in linha.upper(): is_redlining_mode = True 

        if linha.startswith('### '): doc.add_heading(linha.replace('### ', ''), level=3)
        elif linha.startswith('## '): doc.add_heading(linha.replace('## ', ''), level=2)
        elif linha.startswith('# '): doc.add_heading(linha.replace('# ', ''), level=1)
        elif linha.startswith('**') and linha.endswith('**'): 
            p = doc.add_paragraph()
            r = p.add_run(linha.replace('**', ''))
            r.bold = True
            if is_redlining_mode: r.font.color.rgb = RGBColor(0, 102, 204)
        else: 
            p = doc.add_paragraph()
            r = p.add_run(linha.replace('**', ''))
            if is_redlining_mode: r.font.color.rgb = RGBColor(0, 102, 204)

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
        
        pdf.set_font("helvetica", "B", 12)
        pdf.set_text_color(212, 175, 55)
        pdf.cell(0, 8, txt="AETHER KARV - PARECER EXECUTIVO", ln=1, align='C')
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, txt=f"Auditoria Documental: {sanitize_for_pdf(get_data_hora_br())}", ln=1, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(5)
        
        texto_limpo = texto_markdown.replace('**', '').replace('### ', '').replace('## ', '').replace('# ', '')
        texto_seguro = sanitize_for_pdf(texto_limpo)
        is_redlining_mode = False
        table_headers = []
        
        for linha in texto_seguro.split('\n'):
            linha_filtrada = linha.strip()
            if not linha_filtrada: 
                pdf.ln(3); continue

            if re.match(r'^\|[-\s\|]+\|$', linha_filtrada): continue
            
            is_table_line = False
            cols = []
            
            if linha_filtrada.startswith('|') and linha_filtrada.endswith('|'):
                cols = [c.strip() for c in linha_filtrada.split('|')[1:-1]]
                is_table_line = True
            elif ('Nivel de Risco' in linha_filtrada or 'Tribunal' in linha_filtrada or 'Polo Ativo' in linha_filtrada) and (',' in linha_filtrada or '\t' in linha_filtrada):
                linha_limpa_csv = linha_filtrada.replace('"', '')
                sep = '\t' if '\t' in linha_limpa_csv else ','
                cols = [c.strip() for c in linha_limpa_csv.split(sep)]
                if len(cols) >= 3: is_table_line = True
                
            if is_table_line:
                if not table_headers:
                    table_headers = cols
                    continue
                
                pdf.set_font("helvetica", "B", 10)
                pdf.set_text_color(212, 175, 55) 
                
                titulo_card = f"[{table_headers[0] if table_headers else 'Item'}: {cols[0]}]"
                pdf.cell(0, 6, txt=titulo_card, ln=1)
                
                pdf.set_font("helvetica", "", 10)
                pdf.set_text_color(0, 0, 0)
                
                for i in range(1, len(cols)):
                    header_name = table_headers[i] if i < len(table_headers) else f"Coluna {i+1}"
                    texto_card = f"{header_name}: {cols[i]}"
                    pedacos = textwrap.wrap(texto_card, width=95, break_long_words=True)
                    for pedaco in pedacos:
                        pdf.cell(0, 6, txt=pedaco, ln=1)
                pdf.ln(4)
                continue
            else:
                table_headers = []

            if linha_filtrada.startswith('#') or 'CONCLUSAO' in linha_filtrada.upper() or 'RECOMENDACOES' in linha_filtrada.upper() or '---' in linha_filtrada:
                is_redlining_mode = False

            if '[REDLINING' in linha_filtrada.upper():
                is_redlining_mode = True
                
            if is_redlining_mode:
                pdf.set_text_color(0, 102, 204)
                pdf.set_font("helvetica", "B", 10) if '[REDLINING' in linha_filtrada.upper() else pdf.set_font("helvetica", "", 10)
            else:
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("helvetica", "", 10)

            pedacos = textwrap.wrap(linha_filtrada, width=95, break_long_words=True)
            for pedaco in pedacos:
                pdf.cell(0, 6, txt=pedaco, ln=1)
                    
        return bytes(pdf.output())

    except Exception as e:
        emergencia = FPDF()
        emergencia.add_page()
        emergencia.set_font("helvetica", size=10)
        emergencia.cell(0, 6, txt="ERRO PDF: Modo Grafico Falhou. Utilize exportacao DOCX.", ln=1)
        emergencia.cell(0, 6, txt=f"Log: {str(e)[:50]}", ln=1)
        return bytes(emergencia.output())

# ==========================================
# 🎨 CSS APEX V336 (WORKSPACE DESIGN)
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow-x: hidden !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
[data-testid="stHeader"], footer {{ display: none !important; }}

[data-testid="stSidebar"] {{ background: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(212, 175, 55, 0.2) !important; padding-top: 20px; }}
[data-testid="stSidebarContent"] {{ padding: 0 15px; }}

.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 10px 20px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); }}
.omni-brand {{ display: flex; align-items: center; gap: 12px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.2rem; color: #f8fafc; font-weight: 700; letter-spacing: 0.5px; }}
.omni-brand span {{ color: #D4AF37; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 2px 6px; border-radius: 6px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}

.section-title {{ color: #f8fafc; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 8px; margin-top: 15px; display: flex; align-items: center; gap: 6px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 4px; }}
.section-title::before {{ content: ''; display: block; width: 3px; height: 12px; background: #D4AF37; border-radius: 4px; }}

div[data-baseweb="select"] > div {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; }}
.stTextArea label, .stCheckbox label span, .stTextInput label, .stNumberInput label {{ font-size: 0.7rem !important; color: #cbd5e1 !important; font-weight: 600 !important; }}
.stTextArea textarea, .stTextInput input, .stNumberInput input, input[type="password"] {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2); }}
.stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus, input[type="password"]:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 8px rgba(212, 175, 55, 0.1) !important; }}

.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 6px !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 10px !important; border: none !important; width: 100% !important; transition: 0.3s; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); margin-top: 15px; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4); }}

.stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 6px !important; font-weight: 600 !important; transition: 0.3s; }}
.stButton > button[kind="secondary"]:hover {{ background: rgba(212,175,55,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}

.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px; }}
.kpi-box {{ background: rgba(30, 41, 59, 0.4); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); border-left: 3px solid #D4AF37; padding: 12px 15px; backdrop-filter: blur(10px); }}
.kpi-title {{ color: #94a3b8; font-size: 0.60rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; display:block; margin-bottom: 4px; }}
.kpi-value {{ color: #f8fafc; font-size: 1.1rem; font-weight: 600; line-height: 1.2; display:block; }}
.kpi-value.highlight {{ color: #D4AF37; font-weight: 700; }}

[data-testid="stTabs"] button {{ padding: 10px 20px !important; font-weight: 600 !important; color: #94a3b8 !important; border-bottom: 2px solid transparent !important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; background: rgba(212, 175, 55, 0.05) !important; border-radius: 6px 6px 0 0; }}

.standby-container {{ display:flex; flex-direction:column; align-items:center; justify-content:center; height: 60vh; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; background: rgba(30, 41, 59, 0.2); padding: 20px; }}
.welcome-title {{ color: #f8fafc; font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; text-align: center; }}
.welcome-subtitle {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; text-align: center; max-width: 600px; }}

.login-box {{ background: rgba(30, 41, 59, 0.6); padding: 40px; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5); max-width: 400px; margin: 100px auto; text-align: center; backdrop-filter: blur(10px); }}
.login-title {{ color: #f8fafc; font-size: 1.8rem; font-weight: 700; margin-bottom: 5px; }}
.login-subtitle {{ color: #D4AF37; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }}

.stProgress > div > div > div > div {{ background-color: #D4AF37 !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# 🔐 MURALHA DE GELO (TELA DE LOGIN)
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">AETHER KARV</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">ENTERPRISE EDITION V336</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 20px;'>Acesso Restrito ao Cofre de Dados</p>", unsafe_allow_html=True)
    
    login_user = st.text_input("Usuário", placeholder="Digite seu usuário...")
    login_pass = st.text_input("Senha", type="password", placeholder="Digite sua senha...")
    
    if st.button("🔐 AUTENTICAR ACESSO", type="primary"):
        conn = sqlite3.connect('aether_fortknox.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (login_user, login_pass))
        user = c.fetchone()
        conn.close()
        
        if user:
            st.session_state.logged_in = True
            st.session_state.username = login_user
            st.toast("Autenticação Suprema Confirmada.", icon="✅")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Credenciais Inválidas. Acesso Negado.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# INTERFACE PRINCIPAL (SÓ APARECE SE LOGADO)
# ==========================================
else:
    with st.sidebar:
        st.markdown(f'<div class="omni-brand" style="margin-bottom: 20px;"><h1>AETHER KARV</h1><span>V336 DATABASE LOGGED: {st.session_state.username.upper()}</span></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">📁 Base de Conhecimento</div>', unsafe_allow_html=True)
        up = st.file_uploader("Contratos, petições ou imagens...", accept_multiple_files=True, label_visibility="collapsed")
        
        st.markdown('<div class="section-title">⚖️ Motor Jurídico</div>', unsafe_allow_html=True)
        agente_foco = st.selectbox("Especialidade", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"], label_visibility="collapsed")
        
        ativar_redlining = st.checkbox("Ativar Redlining (Reescrita Ativa)", value=False)
        ativar_lindb = st.checkbox("Filtro de Proteção (Art. 22 LINDB)", value=True)
        
        st.markdown('<div class="section-title">🏛️ DataJud (CNJ)</div>', unsafe_allow_html=True)
        if CNJ_API_KEY == "DEMO_KEY":
            st.warning("⚠️ Modo Simulação Ativado.")
        num_processo_input = st.text_input("Nº do Processo / CNPJ", placeholder="Insira para extração...", label_visibility="collapsed")

        st.markdown('<div class="section-title">💰 Faturamento (Timesheet)</div>', unsafe_allow_html=True)
        valor_hora = st.number_input("Valor da sua Hora Técnica (R$)", min_value=50.0, max_value=5000.0, value=350.0, step=50.0)

        st.markdown('<div class="section-title">💬 Comando Direto</div>', unsafe_allow_html=True)
        cmd = st.text_area("", key="cmd_input", placeholder="Instruções ou cole o contrato aqui...", label_visibility="collapsed")

        if st.button("🚀 INICIAR AUDITORIA OMNI", type="primary"):
            if not GROQ_KEY and not GEMINI_KEY:
                st.error("⚠️ ERRO: Chaves API não configuradas.")
                st.toast("Falha: Chaves API ausentes.", icon="❌")
            elif cmd or up or num_processo_input:
                st.toast("Iniciando Motor Hydra...", icon="🔥")
                progress_bar = st.progress(5, text="Iniciando Córtex de Ingestão...")
                time.sleep(0.5)
                
                progress_bar.progress(20, text="Extraindo dados...")
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up) if up else ("", 0, False)
                
                progress_bar.progress(40, text="Consultando bases e estruturando RAG...")
                resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, ativar_lindb, num_processo_input, agente_foco, ativar_redlining, valor_hora)
                
                progress_bar.progress(75, text="Gravando no Banco de Dados (Fort Knox)...")
                # ⚠️ V336: SALVAMENTO AUTOMÁTICO NO BANCO ⚠️
                tipo_doc = "Parecer de Contrato" if "Contrato" in agente_foco else "Inteligência Processual"
                save_dossier(st.session_state.username, tipo_doc, resposta)
                
                docx_buffer = gerar_docx_aether(resposta)
                pdf_data = gerar_pdf_aether(resposta)
                
                progress_bar.progress(100, text="Auditoria Salva com Sucesso!")
                st.toast("Dossiê Executivo Salvo no Banco!", icon="✅")
                time.sleep(0.5)
                progress_bar.empty()
                
                st.session_state.res_aether = resposta
                st.session_state.res_docx = docx_buffer.getvalue()
                st.session_state.res_pdf = pdf_data
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": get_data_hora_br().split("às ")[1], 
                    "risco": "Gravado na Nuvem",
                    "ocr": "Online" if usou_ocr else ("Standby" if MODULO_VISAO else "Offline"),
                    "motor": motor_usado
                }
                st.rerun() 
            else:
                st.warning("Forneça um documento, processo ou comando.")
                
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 LOGOUT", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.res_aether = None
            st.rerun()

    # --- ÁREA PRINCIPAL (WORKSPACE) ---
    st.markdown(f"""
    <div class="omni-topbar">
        <div style="font-weight: 600; color: #f8fafc; font-size: 0.9rem;">DASHBOARD ANALÍTICO</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Status de Conexão: <span style="color: #22c55e;">BANCO DE DADOS ATIVO</span></div>
    </div>
    """, unsafe_allow_html=True)

    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box" title="Volume de contratos e peças inseridos no sistema."><span class="kpi-title">Documentos Digeridos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box" title="Modelo de IA de Elite que processou os dados."><span class="kpi-title">Nó de Processamento</span><span class="kpi-value highlight">{t['motor']}</span></div>
        <div class="kpi-box" title="Status do sistema de leitura visual para PDFs escaneados."><span class="kpi-title">Módulo de Visão</span><span class="kpi-value">{t['ocr']}</span></div>
        <div class="kpi-box" title="Andamento atual do orquestrador Omni."><span class="kpi-title">Status da Operação</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ⚠️ V336: ADICIONADA A 4ª ABA PARA O BANCO DE DADOS ⚠️
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dossiê Executivo", "📥 Central de Exportação", "🕵️‍♂️ Código Raw", "🗄️ Histórico Salvo (Nuvem)"])
    
    with tab1:
        if st.session_state.res_aether:
            st.markdown('<div style="background: rgba(15,23,42,0.5); padding: 25px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px;">', unsafe_allow_html=True)
            st.markdown(st.session_state.res_aether)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="standby-container">', unsafe_allow_html=True)
            st.markdown('<div class="welcome-title">O Workspace do Aether Karv está Online.</div>', unsafe_allow_html=True)
            st.markdown('<div class="welcome-subtitle">Injete documentos ou verifique o seu Histórico Salvo na aba ao lado.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        if st.session_state.res_aether:
            st.write("Selecione o formato para baixar o relatório blindado gerado pelo Aether Karv:")
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.markdown(gerar_botao_primario(st.session_state.res_docx, "AETHER_Parecer.docx", "📄 Download WORD", "application/octet-stream"), unsafe_allow_html=True)
            with c2: st.markdown(gerar_botao_primario(st.session_state.res_pdf, "AETHER_Parecer.pdf", "📕 Download PDF", "application/octet-stream"), unsafe_allow_html=True)
            with c3: st.markdown(gerar_botao_secundario(st.session_state.res_aether.encode('utf-8'), "AETHER_Parecer.txt", "📝 Download TXT", "application/octet-stream"), unsafe_allow_html=True)
            with c4: st.markdown(gerar_botao_secundario(st.session_state.res_aether.encode('utf-8'), "AETHER_Parecer.md", "📊 Download MD", "application/octet-stream"), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⟳ Limpar Workspace (Nova Análise)", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.res_docx = None
                st.session_state.res_pdf = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}
                st.rerun()
        else:
            st.info("Gere uma análise para habilitar a exportação.")
            
    with tab3:
        if st.session_state.res_aether:
            st.code(st.session_state.res_aether, language="markdown")
        else:
            st.info("Nenhum código raw na memória.")
            
    with tab4:
        st.write(f"Bem-vindo ao Cofre, **{st.session_state.username.upper()}**. Aqui estão as suas análises antigas salvas no banco de dados.")
        historico = load_history(st.session_state.username)
        
        if len(historico) == 0:
            st.warning("O seu cofre de dados está vazio. Inicie uma nova auditoria para salvá-la.")
        else:
            for idx, (data_hora, tipo, conteudo) in enumerate(historico):
                with st.expander(f"📁 {tipo} | 🕒 {data_hora}"):
                    st.markdown(conteudo)
                    # Dá a opção de baixar os relatórios antigos puxados do banco!
                    st.markdown(gerar_botao_secundario(conteudo.encode('utf-8'), f"Backup_Aether_{idx}.md", "Baixar Backup (MD)", "application/octet-stream"), unsafe_allow_html=True)
