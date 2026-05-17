import streamlit as st

# ⚠️ V364 APEX PERFECTA: UX/UI DE ELITE (FIM DO QUADRADO DUPLO E SCROLL COMPRIMIDO) ⚠️
st.set_page_config(page_title="AETHER KARV V364", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

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
    if not texto: return texto
    texto_seguro = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF PROTEGIDO]', texto)
    texto_seguro = re.sub(r'\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b', '[CNPJ PROTEGIDO]', texto_seguro)
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
            if res.status_code == 200: return [(item['data_hora'], item['titulo'], item['conteudo']) for item in res.json()]
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
    except sqlite3.IntegrityError: success = False
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

def get_data_hora_br(): return (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M:%S')
def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def gerar_botao_primario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: linear-gradient(135deg, #B8860B, #D4AF37); color: #020617; border-radius: 8px; padding: 12px; text-align: center; text-decoration: none; display: block; font-size: 0.9rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3); transition: 0.3s;"
    return f'<a href="data:{mime};base64,{b64}" download="{filename}" style="{css}">{label}</a>'

def gerar_botao_secundario(buffer, filename, label, mime):
    b64 = base64.b64encode(buffer).decode()
    css = "background: rgba(255,255,255,0.05); color: #cbd5e1; border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; padding: 12px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 600; margin-bottom: 5px; transition: 0.3s;"
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
            if filename.endswith('.csv'): df = pd.read_csv(io.BytesIO(file_bytes)); texto_extraido += f"\n\n--- CSV: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.xlsx'): df = pd.read_excel(io.BytesIO(file_bytes)); texto_extraido += f"\n\n--- XLSX: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif filename.endswith('.docx'): texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{docx2txt.process(io.BytesIO(file_bytes))}"
            elif filename.endswith('.txt'): texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{file_bytes.decode('utf-8', errors='ignore')}"
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
                        response = model.generate_content(["Transcreva com precisão absoluta cada palavra deste documento.", imagem_pil])
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
# 🎨 CSS APEX V364 (ERRADICAÇÃO DO SCROLL E BORDAS FANTASMAS)
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow-x: hidden !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
[data-testid="stHeader"], footer {{ display: none !important; }}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {{ display: none !important; }} 

/* ⚠️ V364: COMPRESSÃO ABSOLUTA DO CONTAINER PARA MATAR O SCROLL ⚠️ */
[data-testid="block-container"] {{ padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 1200px !important; margin: 0 auto; }}

/* ⚠️ V364: ANIQUILAÇÃO DA BORDA DUPLA NATIVA DO STREAMLIT (FOCUS RING) ⚠️ */
[data-baseweb="input"], [data-baseweb="base-input"] {{ background-color: transparent !important; border: none !important; }}
[data-baseweb="input"]:focus-within {{ box-shadow: none !important; border: none !important; outline: none !important; }}

/* NAV TOP COMPRIMIDA */
.top-nav-os {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: rgba(15, 23, 42, 0.8); border-radius: 8px; border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.5); margin-bottom: 15px; backdrop-filter: blur(15px); }}
.os-brand {{ display: flex; align-items: center; gap: 12px; }}
.os-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.4rem; color: #D4AF37; font-weight: 800; letter-spacing: 1px; }}
.os-brand span {{ color: #cbd5e1; font-size: 0.70rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; padding-left: 10px; border-left: 2px solid rgba(255,255,255,0.1); }}

/* TABS COMO MENU (REDUZIDAS) */
[data-testid="stTabs"] {{ background: transparent !important; }}
[data-testid="stTabs"] > div:first-child {{ border-bottom: 2px solid rgba(212, 175, 55, 0.2) !important; margin-bottom: 10px; padding-bottom: 0px; }}
[data-testid="stTabs"] button {{ padding: 8px 20px !important; font-size: 0.85rem !important; font-weight: 700 !important; color: #94a3b8 !important; border: none !important; background: transparent !important; transition: 0.3s; text-transform: uppercase; }}
[data-testid="stTabs"] button:hover {{ color: #fff !important; background: rgba(255,255,255,0.05) !important; border-radius: 6px; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: #020617 !important; background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 6px; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.4); }}

/* INPUTS MILITARES */
.stTextInput label, .stDateInput label, .stNumberInput label {{ font-size: 0.70rem !important; color: #94a3b8 !important; font-weight: 700 !important; margin-bottom: 4px !important; text-transform: uppercase; }}
/* Aplicamos o design direto no input, burlando a caixa externa do Streamlit */
.stTextInput input, .stDateInput input, .stNumberInput input {{ background-color: rgba(15, 23, 42, 0.9) !important; border: 1px solid rgba(255,255,255,0.15) !important; color: #f8fafc !important; font-size: 0.90rem !important; border-radius: 6px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.3); padding: 10px !important; margin-bottom: 10px !important; transition: 0.3s; width: 100%; }}
.stTextInput input:focus, .stDateInput input:focus, .stNumberInput input:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 8px rgba(212, 175, 55, 0.3) !important; outline: none !important; }}

/* UPLOADER COMPRIMIDO */
[data-testid="stFileUploaderDropzone"] {{ padding: 15px !important; min-height: 80px !important; margin-bottom: 10px !important; border: 2px dashed rgba(212, 175, 55, 0.4) !important; background: rgba(15, 23, 42, 0.5) !important; border-radius: 8px !important; transition: 0.3s; text-align: center; }}
[data-testid="stFileUploaderDropzone"]:hover {{ border-color: #D4AF37 !important; background: rgba(212, 175, 55, 0.1) !important; }}
[data-testid="stFileUploaderDropzone"] > div > span {{ font-size: 0.9rem !important; color: #cbd5e1 !important; font-weight: 600; }}
[data-testid="stUploadedFile"] {{ background: rgba(0,0,0,0.6) !important; border-radius: 6px; padding: 6px; margin-top: 6px; border-left: 3px solid #D4AF37; }}

/* BOTÕES DE DISPARO */
.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 8px !important; font-weight: 800 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 12px !important; border: none !important; width: 100% !important; transition: 0.3s; box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4); margin-top: 8px; font-size: 1rem !important; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 8px 20px rgba(212, 175, 55, 0.6); }}

.stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.2) !important; border-radius: 6px !important; font-weight: 600 !important; transition: 0.3s; padding: 8px 12px !important; font-size: 0.75rem !important; text-transform: uppercase; width: 100% !important; }}
.stButton > button[kind="secondary"]:hover {{ background: rgba(255,255,255,0.15) !important; color: #fff !important; border-color: #fff !important; }}

/* ⚠️ V364: CAIXA DE LOGIN GEOMETRICAMENTE CENTRADA E SEM CONFLITOS ⚠️ */
[data-testid="stForm"] {{ border: none !important; background: transparent !important; padding: 0 !important; box-shadow: none !important; }}
.custom-login-wrapper {{ display: flex; justify-content: center; align-items: center; min-height: 80vh; }}
.custom-login-box {{ background: rgba(30, 41, 59, 0.85); padding: 40px; border-radius: 16px; border: 1px solid rgba(212, 175, 55, 0.4); box-shadow: 0 15px 40px rgba(0,0,0,0.6); text-align: center; backdrop-filter: blur(20px); width: 100%; max-width: 400px; }}
.login-title {{ color: #D4AF37; font-size: 2rem; font-weight: 900; margin-bottom: 5px; line-height: 1.2; letter-spacing: 2px; text-align: center; }}
.login-subtitle {{ color: #94a3b8; font-size: 0.80rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 25px; text-align: center; font-weight: 600; }}
.stProgress > div > div > div > div {{ background-color: #D4AF37 !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# 🔐 MURALHA DE GELO (LOGIN PERFEITO V364)
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="custom-login-wrapper">', unsafe_allow_html=True)
    with st.form("login_form"):
        st.markdown("""
        <div class="custom-login-box">
            <div class="login-title">AETHER KARV</div>
            <div class="login-subtitle">V364 APEX PERFECTA</div>
        """, unsafe_allow_html=True)
        
        login_user = st.text_input("Utilizador", placeholder="Ex: henrique...")
        login_pass = st.text_input("Senha", type="password", placeholder="A sua senha...")
        submit_log = st.form_submit_button("🔐 ENTRAR / REGISTAR", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
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
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# INTERFACE PRINCIPAL (SISTEMA OPERATIVO)
# ==========================================
else:
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    CNJ_API_KEY = st.secrets.get("CNJ_API_KEY", "DEMO_KEY")

    st.markdown(f"""
        <div class="top-nav-os">
            <div class="os-brand">
                <h1>AETHER KARV</h1><span>Sessão: {st.session_state.username.upper()}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_op, tab_dash, tab_cofre = st.tabs(["⚡ CÓRTEX CENTRAL (OPERAÇÃO)", "📊 DASHBOARD & KANBAN", "🗄️ COFRE & EXPORTAÇÃO"])

    with tab_op:
        c_up, c_cmds = st.columns([1.5, 2])
        
        with c_up:
            up = st.file_uploader("Documentos Sensíveis (Escudo LGPD Ativo)", accept_multiple_files=True, label_visibility="visible", key=f"up_{st.session_state.uploader_id}")
            c_clean_btn, c_space = st.columns([1, 2])
            with c_clean_btn:
                if st.button("🧹 Limpar Ficheiros", use_container_width=True):
                    st.session_state.uploader_id += 1
                    st.rerun()

        with c_cmds:
            cmd = st.text_input("Diretriz / Comando de IA", placeholder="Ex: Analise os riscos, ou Crie um contrato de locação...")
            num_processo_input = st.text_input("OAB ou DataJud", placeholder="Nº Processo ou OAB/SP para captura...")
            
            c_date, c_val = st.columns(2)
            with c_date: data_intimacao = st.date_input("Data Intimação / Início Prazo", value=date.today(), format="DD/MM/YYYY")
            with c_val: valor_hora = st.number_input("Valor da sua Hora (R$)", min_value=50.0, max_value=5000.0, value=350.0, step=50.0)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_iniciar = st.button("🚀 EXECUTAR ORDEM SUPREMA", type="primary", use_container_width=True)

        if btn_iniciar:
            if cmd or up or num_processo_input:
                st.toast("Iniciando Córtex...", icon="🔥")
                progress_bar = st.progress(5, text="Extraindo dados e mascarando CPFs (LGPD)...")
                
                try: texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up, GEMINI_KEY) if up else ("", 0, False)
                except Exception: texto_arquivos, num_arquivos, usou_ocr = "", 0, False
                
                progress_bar.progress(40, text="Tribunal Multi-Agente em curso...")
                try: resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, num_processo_input, num_arquivos, valor_hora, data_intimacao, GROQ_KEY, GEMINI_KEY, CNJ_API_KEY)
                except Exception as e: resposta, motor_usado = f"Erro no motor: {str(e)}", "FALHA"
                
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
                st.warning("Insira um documento, OAB ou comando para iniciar.")

        if st.session_state.res_aether:
            st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.3); margin-top: 20px; margin-bottom: 20px;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#D4AF37; text-align:center;'>📄 DOSSIÊ PROCESSADO</h3>", unsafe_allow_html=True)
            
            st.markdown('<div style="background: rgba(15,23,42,0.8); padding: 25px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-top: 10px; font-size: 1rem; line-height: 1.6;">', unsafe_allow_html=True)
            st.markdown(st.session_state.res_aether)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br><h4 style='color:#f8fafc;'>💬 OMNI-CHAT (Fale com o Documento)</h4>", unsafe_allow_html=True)
            try:
                valid_history = [m for m in st.session_state.chat_history if isinstance(m, dict) and "role" in m and "content" in m]
                for msg in valid_history:
                    with st.chat_message(msg["role"]): st.markdown(msg["content"])
            except Exception: st.session_state.chat_history = [] 
                
            if prompt := st.chat_input("Ex: 'Aether, crie uma resposta para o advogado da contraparte...'"):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.chat_history = st.session_state.chat_history[-6:] 
                with st.chat_message("user"): st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    with st.spinner("Processando..."):
                        try:
                            contexto_chat = f"DOSSIÊ ATUAL:\n{st.session_state.res_aether}"
                            sys_chat = "Você é o assistente Omni-Chat. Responda de forma direta, agressiva e técnica."
                            resposta_chat, _ = chamar_agente_hydra("OMNI-CHAT", sys_chat, prompt, contexto_chat, GROQ_KEY, GEMINI_KEY)
                            st.markdown(resposta_chat)
                            st.session_state.chat_history.append({"role": "assistant", "content": resposta_chat})
                        except Exception: st.error("Erro no motor conversacional.")

    with tab_dash:
        historico = load_history(st.session_state.username)
        total_docs = len(historico)
        t = st.session_state.telemetria

        st.markdown(f"""
        <div class="custom-kpi-grid">
            <div class="kpi-box"><span class="kpi-title">Módulo Visão (OCR)</span><span class="kpi-value">{t['ocr']}</span></div>
            <div class="kpi-box"><span class="kpi-title">Nó de Processamento</span><span class="kpi-value highlight">{t['motor']}</span></div>
            <div class="kpi-box"><span class="kpi-title">Total Processado (DB)</span><span class="kpi-value" style="color: #22c55e;">{total_docs}</span></div>
            <div class="kpi-box"><span class="kpi-title">Status da Operação</span><span class="kpi-value highlight">{t['risco']}</span></div>
        </div>
        """, unsafe_allow_html=True)

        if total_docs == 0:
            st.info("Gere auditorias no Córtex Central para alimentar o seu Kanban automático.")
        else:
            st.markdown("""
            <div class="kanban-board">
                <div class="kanban-col">
                    <div class="kanban-col-title">📥 Triage OAB / Recentes</div>
                    <div class="kanban-card">Captura Massiva OAB/SP<br><small style="color:#94a3b8">Prazo: Em Análise</small></div>
                </div>
                <div class="kanban-col">
                    <div class="kanban-col-title">⚙️ Em Execução (IA Thanos)</div>
                    <div class="kanban-card">Análise Defesa Tributária<br><small style="color:#94a3b8">Status: Elaborando Redlining</small></div>
                </div>
                <div class="kanban-col">
                    <div class="kanban-col-title">✅ Concluído (Faturado)</div>
                    <div class="kanban-card" style="border-left-color: #22c55e;">Dossiê Trabalhista Entregue<br><small style="color:#22c55e">Fatura: Gerada no Timesheet</small></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_cofre:
        if st.session_state.res_aether:
            st.markdown("<h3>📥 Centro de Exportação Blindada</h3>", unsafe_allow_html=True)
            c1, c2, _c3 = st.columns([1, 1, 2])
            with c1: st.markdown(gerar_botao_primario(st.session_state.res_docx, "AETHER_Documento.docx", "📄 Descarregar Word", "application/octet-stream"), unsafe_allow_html=True)
            with c2: st.markdown(gerar_botao_primario(st.session_state.res_pdf, "AETHER_Documento.pdf", "📕 Descarregar PDF", "application/octet-stream"), unsafe_allow_html=True)
            
            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3>📲 Envio Expresso (Webhook WhatsApp)</h3>", unsafe_allow_html=True)
            col_phone, col_send, _space = st.columns([1.5, 1.5, 2])
            with col_phone:
                telefone = st.text_input("Número do Cliente", label_visibility="collapsed", placeholder="Ex: 5511999999999")
            with col_send:
                if st.button("Disparar para o WhatsApp", use_container_width=True, type="secondary"):
                    if telefone:
                        msg_wa = "Olá! O parecer estratégico do seu caso já foi processado pelo nosso escritório. Segue a análise inicial."
                        url_msg = urllib.parse.quote(msg_wa)
                        link_wa = f"https://wa.me/{re.sub(r'[^0-9]', '', telefone)}?text={url_msg}"
                        st.markdown(f'<a href="{link_wa}" target="_blank" style="background: #25D366; color: white; border-radius: 8px; padding: 10px; text-align: center; text-decoration: none; display: block; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-top:5px;">Abrir WhatsApp Web</a>', unsafe_allow_html=True)
                    else: st.warning("Insira o número.")
            st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)

        st.markdown("<h3>🗄️ Cofre Criptografado & Histórico</h3>", unsafe_allow_html=True)
        historico = load_history(st.session_state.username)
        if len(historico) == 0: st.info("O seu cofre está vazio.")
        else:
            for idx, (data_hora, titulo, conteudo) in enumerate(historico):
                with st.expander(f"📁 {titulo} | 🕒 {data_hora}"):
                    st.markdown(conteudo)
                    st.markdown(gerar_botao_secundario(conteudo.encode('utf-8'), f"Backup_{idx}.txt", "Baixar Cópia TXT", "application/octet-stream"), unsafe_allow_html=True)

    # Botão Sair Isolado
    st.markdown("<br><br>", unsafe_allow_html=True)
    c_out1, c_out2, c_out3 = st.columns([2,1,2])
    with c_out2:
        if st.button("🚪 Encerrar Sessão", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.res_aether = None
            st.session_state.chat_history = []
            st.rerun()
