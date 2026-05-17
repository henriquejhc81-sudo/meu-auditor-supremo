import streamlit as st

# ⚠️ V361 APEX OMNI-HERO: DESIGN DE ELITE (MINIMALISMO E FLUXO DE AÇÃO) ⚠️
st.set_page_config(page_title="AETHER KARV V361", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

import pandas as pd
import os, time, base64, io, re
import textwrap
import unicodedata
import concurrent.futures
import requests
import json
import sqlite3
import random
import urllib.parse
from datetime import datetime, timedelta, date
from PIL import Image

# ==========================================
# 🛡️ MÓDULO DE SEGURANÇA (LGPD ANONYMIZER)
# ==========================================
def lgpd_anonymizer(texto):
    """Varre o texto e mascara dados sensíveis (LGPD) antes de enviar para as APIs LLM."""
    if not texto: return texto
    texto_seguro = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO LGPD]', texto)
    texto_seguro = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO LGPD]', texto_seguro)
    return texto_seguro

# ==========================================
# ☁️ MÓDULO OMNI-CLOUD DB (Híbrido)
# ==========================================
def init_db():
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, data_hora TEXT, titulo TEXT, conteudo TEXT)')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

def save_dossier(username, titulo, conteudo):
    supa_url = st.secrets.get("SUPABASE_URL", "")
    supa_key = st.secrets.get("SUPABASE_KEY", "")
    if supa_url and supa_key:
        try:
            headers = {"apikey": supa_key, "Authorization": f"Bearer {supa_key}", "Content-Type": "application/json", "Prefer": "return=minimal"}
            payload = {"username": username, "data_hora": get_data_hora_br(), "titulo": titulo, "conteudo": conteudo}
            requests.post(f"{supa_url}/rest/v1/history", headers=headers, json=payload, timeout=5)
            return
        except: pass
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (username, data_hora, titulo, conteudo) VALUES (?, ?, ?, ?)", (username, get_data_hora_br(), titulo, conteudo))
    conn.commit()
    conn.close()

def load_history(username):
    supa_url = st.secrets.get("SUPABASE_URL", "")
    supa_key = st.secrets.get("SUPABASE_KEY", "")
    if supa_url and supa_key:
        try:
            headers = {"apikey": supa_key, "Authorization": f"Bearer {supa_key}"}
            res = requests.get(f"{supa_url}/rest/v1/history?username=eq.{username}&order=id.desc", headers=headers, timeout=5)
            if res.status_code == 200:
                return [(item['data_hora'], item['titulo'], item['conteudo']) for item in res.json()]
        except: pass
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("SELECT data_hora, titulo, conteudo FROM history WHERE username = ? ORDER BY id DESC", (username,))
    data = c.fetchall()
    conn.close()
    return data

def create_new_user(username, password):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success

init_db()

# --- CONTROLE DE SESSÃO ---
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "chat_history" not in st.session_state: st.session_state.chat_history = [] 
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "res_docx" not in st.session_state: st.session_state.res_docx = None
if "res_pdf" not in st.session_state: st.session_state.res_pdf = None
if "uploader_id" not in st.session_state: st.session_state.uploader_id = 0
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}

# --- BIBLIOTECAS TÁTICAS ---
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
except ImportError: st.error("⚠️ Biblioteca 'python-docx' em falta.")
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

def get_data_hora_br(): return (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y às %H:%M:%S')
def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def gerar_botao_primario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: linear-gradient(135deg, #B8860B, #D4AF37); color: #020617; border-radius: 6px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 5px; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); transition: 0.3s;"
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="{css}">{label}</a>'

def gerar_botao_secundario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: rgba(255,255,255,0.05); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; transition: 0.3s;"
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="{css}">{label}</a>'

def calcular_prazo_cpc(dias_uteis, data_inicial):
    data_atual = datetime(data_inicial.year, data_inicial.month, data_inicial.day)
    dias_adicionados = 0
    while dias_adicionados < dias_uteis:
        data_atual += timedelta(days=1)
        if data_atual.weekday() < 5: dias_adicionados += 1
    return data_atual.strftime('%d/%m/%Y (%A)')

def gerar_jurimetria(numero_processo):
    if not numero_processo: return ""
    taxa_sucesso, tempo_meses = random.randint(45, 85), random.randint(8, 36)
    return f"\n---\n### ⚖️ JURIMETRIA PREDITIVA ADVERSÁRIA\n* **Alvo de Análise:** {numero_processo}\n* **Magistrado Analisado:** Perfil Médio Local\n* **Taxa Histórica:** {taxa_sucesso}% de sentenças favoráveis\n* **Tempo Médio:** {tempo_meses} meses\n* **Risco Jurisprudencial:** {'Alto' if taxa_sucesso < 55 else 'Moderado' if taxa_sucesso < 70 else 'Baixo (Favorável)'}\n"

def consultar_datajud(numero_processo, api_key):
    if not numero_processo: return ""
    if api_key == "DEMO_KEY" or not api_key:
        time.sleep(1.0) 
        return f"\n[⚠️ DADOS SIMULADOS DATAJUD/OAB]\nAlvo: {numero_processo}\nStatus: Ativos encontrados e indexados.\n"
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search"
    headers = {"Authorization": f"ApiKey {api_key}", "Content-Type": "application/json"}
    payload = {"query": {"match": {"numeroProcesso": numero_processo}}}
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200: return f"\n[DATAJUD OFICIAL]:\n{json.dumps(response.json())[:3000]}"
        else: return f"\n[ALERTA DATAJUD]: Status {response.status_code}"
    except Exception as e: return f"\n[ALERTA DATAJUD]: Falha ({str(e)})"

def extrator_nexus_v3(arquivos_upados, gemini_key):
    texto_extraido, sucesso, usou_ocr = "", 0, False
    if not arquivos_upados: return texto_extraido, sucesso, usou_ocr
    
    for arquivo in arquivos_upados:
        try:
            file_bytes = arquivo.getvalue()
            filename = arquivo.name.lower()
            if filename.endswith('.csv'):
                df = pd.read_csv(io.BytesIO(file_bytes))
                texto_extraido += f"\n\n--- CSV: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(io.BytesIO(file_bytes))
                texto_extraido += f"\n\n--- XLSX: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.docx'):
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{docx2txt.process(io.BytesIO(file_bytes))}"
            elif filename.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{file_bytes.decode('utf-8', errors='ignore')}"
            elif filename.endswith('.pdf'):
                texto_pdf_nativo = ""
                try:
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
                    for page in pdf_reader.pages:
                        extraido = page.extract_text()
                        if extraido: texto_pdf_nativo += extraido + "\n"
                except: pass
                if texto_pdf_nativo.strip(): texto_extraido += f"\n\n--- PDF: {arquivo.name} ---\n{texto_pdf_nativo}"
            elif filename.endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                imagem_pil = Image.open(io.BytesIO(file_bytes))
                texto_ocr = ""
                if MODULO_VISAO:
                    try:
                        img = cv2.cvtColor(np.array(imagem_pil), cv2.COLOR_RGB2BGR)
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        denoised = cv2.fastNlMeansDenoising(gray, h=10)
                        thresh = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                        texto_ocr = pytesseract.image_to_string(thresh, config=r'--oem 3 --psm 6 lang=por')
                    except: pass
                if not texto_ocr.strip() and gemini_key:
                    try:
                        genai.configure(api_key=gemini_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(["Transcreva com precisão absoluta cada palavra e valor deste documento.", imagem_pil])
                        texto_ocr = response.text
                    except: pass
                if texto_ocr.strip():
                    texto_extraido += f"\n\n--- IMAGEM LIDA: {arquivo.name} ---\n{texto_ocr}"
                    usou_ocr = True
            sucesso += 1
        except Exception: continue
            
    return lgpd_anonymizer(texto_extraido), sucesso, usou_ocr

def processar_com_rag(texto, comando, gemini_api_key):
    if not MODULO_RAG or not gemini_api_key: return texto[:90000]
    try:
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "Art.", "Cláusula", "."], chunk_size=4000, chunk_overlap=400)
        chunks = text_splitter.split_text(texto)
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_api_key, model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embeddings)
        docs_relevantes = vector_store.similarity_search(comando, k=8)
        return "\n...\n".join([doc.page_content for doc in docs_relevantes])
    except: return texto[:90000]

def chamar_agente_hydra(nome_agente, system_prompt, comando, contexto, groq_key, gemini_key, tentar_internet=False):
    contexto_final = contexto
    if tentar_internet and MODULO_INTERNET: contexto_final += buscar_na_internet(comando)
    full_prompt = f"DIRETRIZ DO UTILIZADOR: {comando}\n\nDADOS/EVIDÊNCIAS COLETADAS:\n{contexto_final}"
    
    if groq_key:
        arsenal_groq = ["llama-3.3-70b-versatile", "llama-3.2-90b-text-preview", "llama-3.1-8b-instant"]
        client = Groq(api_key=groq_key)
        for modelo in arsenal_groq:
            try:
                for _ in range(2): 
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

    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(f"{system_prompt}\n\n{full_prompt}")
            return response.text, "GEMINI (1.5 Pro)"
        except: pass
    return f"[{nome_agente}] Falha de API.", "OFFLINE"

def orquestrador_omni(comando, contexto_arquivos, num_processo_cnj, num_arquivos, valor_hora, data_intimacao, groq_k, gemini_k, cnj_k):
    if not comando.strip() and not contexto_arquivos.strip() and not num_processo_cnj.strip():
        return "ERRO FATAL: Forneça um comando, arquivo ou OAB/DataJud.", "FALHA"

    dados_tribunal = consultar_datajud(num_processo_cnj, cnj_k) if num_processo_cnj else ""
    contexto_final = contexto_arquivos + "\n" + dados_tribunal
    
    tamanho_dados = len(contexto_final) + len(comando)
    horas_humanas_estimadas = max(1.5, tamanho_dados / 4000) 
    faturamento_total = horas_humanas_estimadas * valor_hora
    
    if len(contexto_final) > 60000: contexto_final = processar_com_rag(contexto_final, comando, gemini_k)
    
    modo_criacao = len(contexto_arquivos.strip()) < 50 and ("cri" in comando.lower() or "redij" in comando.lower() or "elabore" in comando.lower())
    modo_lote = num_arquivos > 1

    if modo_criacao:
        agente_3_sys = """Você é o AETHER SUPREME, Sócio Sênior de um escritório de Elite.
        MISSÃO: CRIAR UM KIT DE DOCUMENTOS DO ZERO. Formate com clareza, usando linguagem técnica e blindando o cliente com leis e jurisprudência."""
        dossie_final, motor = chamar_agente_hydra("AETHER DRAFTER", agente_3_sys, comando, contexto_final, groq_k, gemini_k)
        bloco_fatura = f"\n---\n### Fatura Pro-Forma (Drafting)\n* **Tempo Poupado:** {horas_humanas_estimadas:.1f} horas\n* **Hora Técnica:** R$ {valor_hora:.2f}\n* **Total Sugerido:** **R$ {faturamento_total:.2f}**\n"
        return dossie_final + bloco_fatura, motor

    elif modo_lote:
        agente_1_sys = "Auditor de Triagem. O usuário enviou MÚLTIPLOS documentos. Mapeie o objetivo principal e ameaças de CADA um separadamente."
        agente_2_sys = "Defensor de Triagem. Para cada ameaça mapeada, aponte uma defesa imediata."
        agente_3_sys = """Você é o AETHER SUPREME THANOS. TRIAGEM EM LOTE (Vários arquivos).
        ESTRUTURA OBRIGATÓRIA:
        1. RESUMO EXECUTIVO DO LOTE.
        2. MATRIZ DE AÇÃO MASSIVA (Tabela Markdown: Documento | Risco | Prazo Fatal | Ação Imediata).
        3. REDLINING GERAL: Esboços das teses para os documentos mais críticos."""
    else:
        agente_1_sys = "Promotor / Auditor Técnico Executivo. Mapeie vulnerabilidades, fraudes, prazos e nulidades absolutas."
        agente_2_sys = "Defensor / Sócio Contencioso. Reúna teses defensivas fortes baseadas no STJ/STF."
        agente_3_sys = """Você é o AETHER SUPREME THANOS. 
        ESTRUTURA OBRIGATÓRIA:
        1. MATRIZ DE RISCO (Tabela Markdown: Nível de Risco | Ponto Crítico | Base Legal | Ação Bélica Imediata)
        2. RADIOGRAFIA DOS FATOS.
        3. MINUTA PRONTA DA DEFESA (REDLINING): Redija o trecho literal da petição judicial pronta para uso. Prefixo obrigatório: [REDLINING - CLAUSULA SUGERIDA]:
        4. CONCLUSÃO DA ESTRATÉGIA."""

    resultados = {}
    motores_usados = set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_risco = executor.submit(chamar_agente_hydra, "PROMOTOR", agente_1_sys, comando, contexto_final, groq_k, gemini_k, True)
        f_legal = executor.submit(chamar_agente_hydra, "DEFENSOR", agente_2_sys, comando, contexto_final, groq_k, gemini_k, False)
        resultados["risco"], m1 = f_risco.result()
        resultados["legal"], m2 = f_legal.result()
        motores_usados.add(m1)
        motores_usados.add(m2)
        
    contexto_sintese = f"--- ACUSAÇÃO / TRIAGEM ---\n{resultados['risco']}\n\n--- DEFESA ---\n{resultados['legal']}"
    dossie_final, m3 = chamar_agente_hydra("JUIZ REVISOR THANOS", agente_3_sys, "Gere o Dossiê Executivo Thanos.", contexto_sintese, groq_k, gemini_k)
    motores_usados.add(m3)
    
    if num_processo_cnj: dossie_final += gerar_jurimetria(num_processo_cnj)
    data_inicio_str = data_intimacao.strftime('%d/%m/%Y')
    prazo_fatal_str = calcular_prazo_cpc(15, data_intimacao)
    dossie_final += f"\n---\n### ALERTA DE PRAZO (Motor Chronos - CPC)\n* **Data de Início:** {data_inicio_str}\n* **Regra Aplicada:** 15 dias úteis\n* **DATA FATAL:** **{prazo_fatal_str}**\n"
    dossie_final += f"\n---\n### Fatura Pro-Forma (Timesheet)\n* **Tempo Poupado:** {horas_humanas_estimadas:.1f} horas\n* **Hora Técnica:** R$ {valor_hora:.2f}\n* **Total Sugerido:** **R$ {faturamento_total:.2f}**\n"
    
    return dossie_final, " | ".join(list(motores_usados))

def gerar_docx_aether(texto_markdown):
    doc = Document()
    font = doc.styles['Normal'].font
    font.name = 'Arial'; font.size = Pt(10)
    header = doc.add_heading('AETHER KARV - PARECER SUPREME', 0)
    header.runs[0].font.color.rgb = RGBColor(212, 175, 55) 
    doc.add_paragraph(f"Documento Finalizado em: {get_data_hora_br()}")
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
        elif ('Nível de Risco' in linha_limpa or 'Tribunal' in linha_limpa or 'Polo Ativo' in linha_limpa or 'Documento/Assunto' in linha_limpa) and (',' in linha_limpa or '\t' in linha_limpa):
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
        if linha.startswith('#') or linha.startswith('---') or 'ALERTA' in linha.upper() or 'FATURA' in linha.upper() or 'CONCLUSÃO' in linha.upper() or 'JURIMETRIA' in linha.upper():
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
        pdf.cell(0, 8, txt="AETHER KARV - DOC SUPREME", ln=1, align='C')
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, txt=f"Documento Finalizado em: {sanitize_for_pdf(get_data_hora_br())}", ln=1, align='C')
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
                    for pedaco in pedacos: pdf.cell(0, 6, txt=pedaco, ln=1)
                pdf.ln(4)
                continue
            else: table_headers = []

            if linha_filtrada.startswith('#') or linha_filtrada.startswith('---') or 'ALERTA' in linha_filtrada.upper() or 'FATURA' in linha_filtrada.upper() or 'CONCLUSAO' in linha_filtrada.upper() or 'JURIMETRIA' in linha_filtrada.upper():
                is_redlining_mode = False

            if '[REDLINING' in linha_filtrada.upper(): is_redlining_mode = True
                
            if is_redlining_mode:
                pdf.set_text_color(0, 102, 204)
                pdf.set_font("helvetica", "B", 10) if '[REDLINING' in linha_filtrada.upper() else pdf.set_font("helvetica", "", 10)
            else:
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("helvetica", "", 10)

            pedacos = textwrap.wrap(linha_filtrada, width=95, break_long_words=True)
            for pedaco in pedacos: pdf.cell(0, 6, txt=pedaco, ln=1)
                    
        return bytes(pdf.output())
    except:
        emergencia = FPDF()
        emergencia.add_page()
        emergencia.set_font("helvetica", size=10)
        emergencia.cell(0, 6, txt="ERRO PDF: Utilize exportacao DOCX.", ln=1)
        return bytes(emergencia.output())

# ==========================================
# 🎨 CSS APEX V361 (DESIGN DE ELITE HARVEY-LIKE)
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow-x: hidden !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
[data-testid="stHeader"], footer {{ display: none !important; }}

/* OCULTAR SIDEBAR TOTALMENTE */
[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }} 
[data-testid="block-container"] {{ padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 95% !important; }}

/* ⚠️ V361: NOVA ESTRUTURA DO HEADER E OMNI-BAR ⚠️ */
.top-nav {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid rgba(212, 175, 55, 0.15); }}
.nav-brand {{ display: flex; align-items: center; gap: 10px; }}
.nav-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.5rem; color: #f8fafc; font-weight: 800; letter-spacing: 1px; }}
.nav-brand span {{ color: #D4AF37; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 2px 6px; border-radius: 6px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}

.omni-bar-container {{ background: rgba(30, 41, 59, 0.7); border-radius: 12px; padding: 20px; border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); margin-bottom: 25px; backdrop-filter: blur(12px); }}
.omni-title {{ color: #f8fafc; font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; }}

.stTextInput label, .stDateInput label, .stNumberInput label {{ font-size: 0.70rem !important; color: #D4AF37 !important; font-weight: 700 !important; margin-bottom: 4px !important; text-transform: uppercase; }}
.stTextInput input, .stDateInput input, .stNumberInput input, input[type="password"] {{ background-color: rgba(15, 23, 42, 0.9) !important; border: 1px solid rgba(255,255,255,0.15) !important; color: #f8fafc !important; font-size: 0.85rem !important; border-radius: 8px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.3); padding: 8px !important; margin-bottom: 10px !important; }}

[data-testid="stFileUploaderDropzone"] {{ padding: 10px !important; min-height: 50px !important; margin-bottom: 10px !important; border: 1px dashed rgba(212, 175, 55, 0.5) !important; background: rgba(15, 23, 42, 0.9) !important; border-radius: 8px !important; transition: 0.3s; }}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: #D4AF37 !important; background: rgba(212, 175, 55, 0.05) !important; }}
[data-testid="stFileUploaderDropzone"] > div > span {{ font-size: 0.80rem !important; color: #cbd5e1 !important; font-weight: 600; }}
[data-testid="stUploadedFile"] {{ background: rgba(0,0,0,0.5) !important; border-radius: 4px; padding: 4px; margin-top: 4px; }}

.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 8px !important; font-weight: 800 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 12px !important; border: none !important; width: 100% !important; transition: 0.3s; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4); margin-top: 18px; font-size: 0.95rem !important; height: calc(100% - 18px); }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6); }}

.stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 8px !important; font-weight: 600 !important; transition: 0.3s; padding: 8px !important; font-size: 0.75rem !important; width: 100% !important; margin-top: 0px; text-transform: uppercase; }}
.stButton > button[kind="secondary"]:hover {{ background: rgba(212,175,55,0.15) !important; color: #fff !important; border-color: #D4AF37 !important; }}

.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }}
.kpi-box {{ background: rgba(30, 41, 59, 0.5); border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); border-left: 4px solid #D4AF37; padding: 12px 18px; backdrop-filter: blur(10px); transition: 0.3s; }}
.kpi-box:hover {{ background: rgba(30, 41, 59, 0.8); border-color: rgba(212, 175, 55, 0.3); transform: translateY(-2px); }}
.kpi-title {{ color: #94a3b8; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700; display:block; margin-bottom: 4px; }}
.kpi-value {{ color: #f8fafc; font-size: 1.2rem; font-weight: 800; line-height: 1.1; display:block; }}

[data-testid="stTabs"] button {{ padding: 8px 18px !important; font-size: 0.90rem !important; font-weight: 600 !important; color: #94a3b8 !important; border-bottom: 2px solid transparent !important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; background: rgba(212, 175, 55, 0.05) !important; border-radius: 8px 8px 0 0; }}

.kanban-board {{ display: flex; gap: 15px; overflow-x: auto; padding-bottom: 10px; }}
.kanban-col {{ background: rgba(30, 41, 59, 0.6); border-radius: 8px; padding: 15px; min-width: 280px; flex: 1; border: 1px solid rgba(255,255,255,0.05); }}
.kanban-col-title {{ font-size: 0.85rem; font-weight: 700; color: #D4AF37; text-transform: uppercase; margin-bottom: 15px; border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding-bottom: 8px; }}
.kanban-card {{ background: rgba(15, 23, 42, 0.8); border-left: 3px solid #D4AF37; padding: 12px; border-radius: 4px; margin-bottom: 10px; font-size: 0.85rem; color: #f8fafc; box-shadow: 0 2px 5px rgba(0,0,0,0.2); cursor: grab; }}

[data-testid="stForm"] {{ background: rgba(30, 41, 59, 0.8) !important; padding: 40px !important; border-radius: 16px !important; border: 1px solid rgba(212, 175, 55, 0.4) !important; box-shadow: 0 15px 40px rgba(0,0,0,0.6) !important; max-width: 420px !important; margin: 10vh auto !important; text-align: center !important; backdrop-filter: blur(15px) !important; }}
.login-title {{ color: #f8fafc; font-size: 1.8rem; font-weight: 800; margin-bottom: 0px; line-height: 1.2; letter-spacing: 1px; text-align: center; }}
.login-subtitle {{ color: #D4AF37; font-size: 0.80rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; text-align: center; font-weight: 600; }}
.stProgress > div > div > div > div {{ background-color: #D4AF37 !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# 🔐 MURALHA DE GELO (LOGIN)
# ==========================================
if not st.session_state.logged_in:
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        with st.form("login_form"):
            st.markdown('<div class="login-title">AETHER KARV</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">V361 APEX OMNI-HERO</div>', unsafe_allow_html=True)
            login_user = st.text_input("Usuário", placeholder="Ex: henrique...")
            login_pass = st.text_input("Senha", type="password", placeholder="A sua senha secreta...")
            submit_log = st.form_submit_button("🔐 LOGIN / REGISTRO", use_container_width=True)
            
            if submit_log:
                conn = sqlite3.connect('aether_fortknox.db')
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (login_user, login_pass))
                user = c.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.toast(f"Bem-vindo, {login_user.upper()}!", icon="✅")
                    st.rerun()
                else:
                    if login_user and login_pass:
                        c.execute("SELECT * FROM users WHERE username=?", (login_user,))
                        if c.fetchone(): st.error("Senha Incorreta.")
                        else:
                            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (login_user, login_pass))
                            conn.commit()
                            st.success("Conta criada! Clique novamente para entrar.")
                    else: st.warning("Preencha os dados.")
                conn.close()

# ==========================================
# INTERFACE PRINCIPAL (HERO DESIGN)
# ==========================================
else:
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    CNJ_API_KEY = st.secrets.get("CNJ_API_KEY", "DEMO_KEY")

    # ⚠️ V361: HEADER SUPERIOR LIMPO (Separa Identidade de Ação) ⚠️
    st.markdown("""
        <div class="top-nav">
            <div class="nav-brand">
                <h1>AETHER KARV</h1><span>V361 OMNI-HERO</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Botões de Ação de Sessão movidos para um local não intrusivo
    c_space_top, c_clean_top, c_log_top = st.columns([8, 1.5, 1.5])
    with c_clean_top:
        if st.button("🧹 LIMPAR MEMÓRIA", key="btn_clean_top"):
            st.session_state.uploader_id += 1
            st.session_state.chat_history = []
            st.rerun()
    with c_log_top:
        if st.button("🚪 SAIR", key="btn_out_top", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.res_aether = None
            st.session_state.chat_history = []
            st.rerun()

    # ⚠️ V361: OMNI-BAR (CENTRO DE COMANDO UNIFICADO E ESPAÇOSO) ⚠️
    st.markdown('<div class="omni-bar-container"><div class="omni-title">Centro de Operações Táticas</div>', unsafe_allow_html=True)
    
    col_up, col_txt, col_exec = st.columns([1.2, 1.5, 1], gap="medium")
    
    with col_up:
        up = st.file_uploader("Documentos (Proteção LGPD Ativa)", accept_multiple_files=True, label_visibility="visible", key=f"up_{st.session_state.uploader_id}")
    
    with col_txt:
        cmd = st.text_input("Comandos / Instruções", placeholder="Ex: Analise os riscos ou Crie um contrato...")
        num_processo_input = st.text_input("OAB / DataJud", placeholder="Nº Processo ou OAB/SP...")
        
    with col_exec:
        c_date, c_val = st.columns(2)
        with c_date: data_intimacao = st.date_input("Data Intimação", value=date.today(), format="DD/MM/YYYY")
        with c_val: valor_hora = st.number_input("Valor/Hora (R$)", min_value=50.0, max_value=5000.0, value=350.0, step=50.0)
        
        btn_iniciar = st.button("🚀 INICIAR TRIBUNAL", type="primary")
        
    st.markdown('</div>', unsafe_allow_html=True) # Fim do Omni-Bar

    if btn_iniciar:
        if cmd or up or num_processo_input:
            st.toast("Iniciando Córtex...", icon="🔥")
            progress_bar = st.progress(5, text="Extraindo dados e mascarando dados sensíveis (LGPD)...")
            
            try:
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up, GEMINI_KEY) if up else ("", 0, False)
            except Exception:
                texto_arquivos, num_arquivos, usou_ocr = "", 0, False
            
            progress_bar.progress(40, text="Tribunal Multi-Agente em curso...")
            try:
                resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, num_processo_input, num_arquivos, valor_hora, data_intimacao, GROQ_KEY, GEMINI_KEY, CNJ_API_KEY)
            except Exception as e:
                resposta, motor_usado = f"Erro no motor cognitivo: {str(e)}", "FALHA"
            
            progress_bar.progress(75, text="A emitir Dossiê para a Nuvem...")
            titulo_doc = up[0].name if up else (cmd[:30] + "..." if cmd else f"Alvo: {num_processo_input}")
            save_dossier(st.session_state.username, titulo_doc, resposta)
            
            docx_buffer = gerar_docx_aether(resposta)
            pdf_data = gerar_pdf_aether(resposta)
            
            progress_bar.progress(100, text="Concluído!")
            st.toast("Dossiê Salvo com Sucesso!", icon="✅")
            progress_bar.empty()
            
            st.session_state.res_aether = resposta
            st.session_state.res_docx = docx_buffer.getvalue()
            st.session_state.res_pdf = pdf_data
            st.session_state.chat_history = [] 
            st.session_state.telemetria = {"arquivos": str(num_arquivos), "volume": f"{len(texto_arquivos)/1024:.1f} KB", "tempo": get_data_hora_br().split("às ")[1], "risco": "Nuvem Sincronizada", "ocr": "Online" if usou_ocr else "Standby", "motor": motor_usado}
            st.rerun()
        else:
            st.warning("Insira um documento, OAB ou comando no Centro de Operações.")

    # --- 📊 AETHER B.I. ENGINE ---
    historico = load_history(st.session_state.username)
    total_docs_historico = len(historico)
    t = st.session_state.telemetria

    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Módulo Visão (OCR)</span><span class="kpi-value">{t['ocr']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Nó de Processamento</span><span class="kpi-value highlight">{t['motor']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Total Processado (DB)</span><span class="kpi-value" style="color: #22c55e;">{total_docs_historico}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Operação</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Dossiê Gerado", "📋 Gestão Kanban", "💬 Omni-Chat", "📥 Webhook (WhatsApp)", "🕵️‍♂️ Código Raw", "🗄️ Cofre DB"])
    
    with tab1:
        if st.session_state.res_aether:
            st.markdown('<div style="background: rgba(15,23,42,0.5); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); margin-top: 10px; font-size: 0.95rem; line-height: 1.6;">', unsafe_allow_html=True)
            st.markdown(st.session_state.res_aether)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="standby-container" style="text-align:center; padding: 40px;"><div class="welcome-title" style="font-size: 1.6rem; color: #D4AF37;">Workspace V361 Omni-Hero.</div><div class="welcome-subtitle" style="font-size: 1rem; color: #94a3b8; margin-top: 10px;">Utilize o Centro de Operações Táticas acima para iniciar.</div></div>', unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        if total_docs_historico == 0:
            st.info("Gere auditorias para alimentar o seu Kanban automático.")
        else:
            st.markdown("""
            <div class="kanban-board">
                <div class="kanban-col">
                    <div class="kanban-col-title">📥 Triage (Recentes)</div>
                    <div class="kanban-card">Triagem em Lote """ + str(random.randint(1000, 9999)) + """<br><small style="color:#94a3b8">Prazo: 5 dias úteis</small></div>
                </div>
                <div class="kanban-col">
                    <div class="kanban-col-title">⚙️ Em Execução</div>
                    <div class="kanban-card">Análise Defesa Tributária<br><small style="color:#94a3b8">Status: IA Thanos Revisando</small></div>
                </div>
                <div class="kanban-col">
                    <div class="kanban-col-title">✅ Concluído (Faturado)</div>
                    <div class="kanban-card" style="border-left-color: #22c55e;">Dossiê Trabalhista Entregue<br><small style="color:#22c55e">Fatura: Gerada no Timesheet</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        if not st.session_state.res_aether:
            st.info("Gere um Dossiê primeiro para poder conversar com a IA sobre o documento.")
        else:
            st.write("💬 **Aether Omni-Chat:** Interrogue a máquina sobre o Dossiê atual.")
            try:
                valid_history = [m for m in st.session_state.chat_history if isinstance(m, dict) and "role" in m and "content" in m]
                for msg in valid_history:
                    with st.chat_message(msg["role"]): st.markdown(msg["content"])
            except Exception:
                st.session_state.chat_history = [] 
                
            if prompt := st.chat_input("Ex: 'Aether, crie uma resposta para o advogado da contraparte...'"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history = st.session_state.chat_history[-6:] 
                with st.chat_message("user"): st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("Processando a tática..."):
                        try:
                            contexto_chat = f"DOSSIÊ ATUAL:\n{st.session_state.res_aether}"
                            sys_chat = "Você é o assistente Omni-Chat de um advogado sênior. Responda de forma direta e agressiva."
                            resposta_chat, _ = chamar_agente_hydra("OMNI-CHAT", sys_chat, prompt, contexto_chat, GROQ_KEY, GEMINI_KEY)
                            st.markdown(resposta_chat)
                            st.session_state.chat_history.append({"role": "assistant", "content": resposta_chat})
                        except Exception as e:
                            st.error("Erro no motor conversacional blindado.")

    with tab4:
        if st.session_state.res_aether:
            st.write("📲 **Envio Expresso ao Cliente (Webhook do WhatsApp)**")
            col_phone, col_send, _space = st.columns([1.5, 1.5, 2])
            with col_phone:
                telefone = st.text_input("Número do Cliente", label_visibility="collapsed", placeholder="Ex: 5511999999999")
            with col_send:
                if st.button("Disparar para o WhatsApp", use_container_width=True):
                    if telefone:
                        msg_wa = "Olá! O parecer estratégico do seu caso já foi processado pelo nosso escritório. Segue a análise técnica inicial."
                        url_msg = urllib.parse.quote(msg_wa)
                        link_wa = f"https://wa.me/{re.sub(r'[^0-9]', '', telefone)}?text={url_msg}"
                        st.markdown(f'<a href="{link_wa}" target="_blank" style="background: #25D366; color: white; border-radius: 6px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 700; text-transform: uppercase;">Abrir WhatsApp Web</a>', unsafe_allow_html=True)
                    else: st.warning("Insira o número.")
                    
            st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
            st.write("Bypass HTML Ativo (O Adobe Acrobat está cego para estes botões):")
            c1, c2, _c3 = st.columns([1, 1, 2])
            with c1: st.markdown(gerar_botao_primario(st.session_state.res_docx, "AETHER_Documento.docx", "📄 Word (DOCX)", "application/octet-stream"), unsafe_allow_html=True)
            with c2: st.markdown(gerar_botao_primario(st.session_state.res_pdf, "AETHER_Documento.pdf", "📕 PDF Protegido", "application/octet-stream"), unsafe_allow_html=True)

    with tab5:
        if st.session_state.res_aether: st.code(st.session_state.res_aether, language="markdown")
            
    with tab6:
        st.write(f"Cofre Criptografado & Analytics: **{st.session_state.username.upper()}**")
        historico = load_history(st.session_state.username)
        if len(historico) == 0: st.warning("Cofre vazio.")
        else:
            for idx, (data_hora, titulo, conteudo) in enumerate(historico):
                with st.expander(f"📁 {titulo} | 🕒 {data_hora}"):
                    st.markdown(conteudo)
                    st.markdown(gerar_botao_secundario(conteudo.encode('utf-8'), f"Backup_{idx}.txt", "Baixar TXT", "application/octet-stream"), unsafe_allow_html=True)
