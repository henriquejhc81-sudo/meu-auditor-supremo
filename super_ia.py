import streamlit as st

# ⚠️ V340 APEX: SEQUÊNCIA DE IGNIÇÃO BLINDADA ⚠️
st.set_page_config(page_title="AETHER KARV V340 APEX", page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")

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
# 🗄️ MÓDULO ENTERPRISE DE BANCO DE DADOS
# ==========================================
def init_db():
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, data_hora TEXT, titulo TEXT, conteudo TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS api_keys (username TEXT PRIMARY KEY, groq_key TEXT, gemini_key TEXT, cnj_key TEXT)')
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    conn.close()

def save_dossier(username, titulo, conteudo):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (username, data_hora, titulo, conteudo) VALUES (?, ?, ?, ?)", (username, get_data_hora_br(), titulo, conteudo))
    conn.commit()
    conn.close()

def load_history(username):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("SELECT data_hora, titulo, conteudo FROM history WHERE username = ? ORDER BY id DESC", (username,))
    data = c.fetchall()
    conn.close()
    return data

def get_api_keys(username):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("SELECT groq_key, gemini_key, cnj_key FROM api_keys WHERE username = ?", (username,))
    keys = c.fetchone()
    conn.close()
    return keys

def save_api_keys(username, groq, gemini, cnj):
    conn = sqlite3.connect('aether_fortknox.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO api_keys (username, groq_key, gemini_key, cnj_key) VALUES (?, ?, ?, ?)", (username, groq, gemini, cnj))
    conn.commit()
    conn.close()

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

def get_data_hora_br():
    fuso_br = datetime.utcnow() - timedelta(hours=3)
    return fuso_br.strftime('%d/%m/%Y às %H:%M:%S')

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

# ⚠️ V340 APEX: THE CHRONOS ENGINE (Cálculo Determinístico de Prazos do CPC) ⚠️
def calcular_prazo_cpc(dias_uteis):
    # Baseado no Art. 219 do CPC (Conta apenas dias úteis)
    data_atual = datetime.utcnow() - timedelta(hours=3)
    dias_adicionados = 0
    
    while dias_adicionados < dias_uteis:
        data_atual += timedelta(days=1)
        # 5 = Sábado, 6 = Domingo
        if data_atual.weekday() < 5:
            dias_adicionados += 1
            
    return data_atual.strftime('%d/%m/%Y (%A)')

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
        Alvo da Busca: {numero_processo}
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

def processar_com_rag(texto, comando, gemini_api_key):
    if not MODULO_RAG or not gemini_api_key: return texto[:90000]
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=400)
        chunks = text_splitter.split_text(texto)
        embeddings = GoogleGenerativeAIEmbeddings(google_api_key=gemini_api_key, model="models/embedding-001")
        vector_store = FAISS.from_texts(chunks, embeddings)
        docs_relevantes = vector_store.similarity_search(comando, k=8)
        return "\n...\n".join([doc.page_content for doc in docs_relevantes])
    except: return texto[:90000]

# --- 🤖 HYDRA ENGINE ---
def chamar_agente_hydra(nome_agente, system_prompt, comando, contexto, groq_key, gemini_key, tentar_internet=False):
    contexto_final = contexto
    if tentar_internet and MODULO_INTERNET:
        contexto_final += buscar_na_internet(comando)
        
    full_prompt = f"DIRETRIZ DE INVESTIGAÇÃO: {comando}\n\nEVIDÊNCIAS COLETADAS:\n{contexto_final}"
    
    if groq_key:
        arsenal_groq = ["llama-3.3-70b-versatile", "llama-3.2-90b-text-preview", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        client = Groq(api_key=groq_key)
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

    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            prompt_gemini = f"{system_prompt}\n\n{full_prompt}"
            response = model.generate_content(prompt_gemini)
            return response.text, "GEMINI (1.5 Pro)"
        except Exception as e:
            return f"[{nome_agente}] Hydra Engine Falhou: {str(e)}", "OFFLINE"

    return f"[{nome_agente}] Erro Crítico: Sistema sem Chaves API Oficiais.", "OFFLINE"

def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, num_processo_cnj, agente_foco, ativar_redlining, valor_hora, ativar_prazos, groq_k, gemini_k, cnj_k):
    dados_tribunal = consultar_datajud(num_processo_cnj, cnj_k) if num_processo_cnj else ""
    contexto_final = contexto_arquivos + "\n" + dados_tribunal
    
    tamanho_dados = len(contexto_final) + len(comando)
    horas_humanas_estimadas = max(1.5, tamanho_dados / 4000) 
    faturamento_total = horas_humanas_estimadas * valor_hora
    
    if len(contexto_final) > 60000: contexto_final = processar_com_rag(contexto_final, comando, gemini_k)
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
        f_risco = executor.submit(chamar_agente_hydra, "AGENTE RISK", agente_1_sys, comando, contexto_final, groq_k, gemini_k, True)
        f_legal = executor.submit(chamar_agente_hydra, "AGENTE LEGAL", agente_2_sys, comando, contexto_final, groq_k, gemini_k, False)
        resultados["risco"], m1 = f_risco.result()
        resultados["legal"], m2 = f_legal.result()
        motores_usados.add(m1)
        motores_usados.add(m2)
        
    contexto_sintese = f"--- PARTE 1 ---\n{resultados['risco']}\n\n--- PARTE 2 ---\n{resultados['legal']}"
    dossie_final, m3 = chamar_agente_hydra("AETHER OMNI", agente_3_sys, "Crie o Dossiê Final. Use Tabela Markdown com barras verticais (|).", contexto_sintese, groq_k, gemini_k)
    motores_usados.add(m3)
    
    # ⚠️ V340 APEX: INJEÇÃO DO ALERTA DE PRAZOS (CHRONOS ENGINE) ⚠️
    if ativar_prazos:
        data_inicio_str = (datetime.utcnow() - timedelta(hours=3)).strftime('%d/%m/%Y')
        prazo_fatal_str = calcular_prazo_cpc(15)
        bloco_prazos = f"""
        
---
### ALERTA DE PRAZO (Motor Chronos - CPC)
* **Data de Início da Contagem (Hoje):** {data_inicio_str}
* **Regra Aplicada:** 15 dias úteis (Art. 219 CPC)
* **DATA FATAL (Fim do Prazo):** **{prazo_fatal_str}**
*(Nota do Sistema: O Motor Chronos excluiu sábados e domingos do cálculo matemático. Feriados estaduais e municipais devem ser confirmados pelo usuário).*
"""
        dossie_final += bloco_prazos

    # Fatura Automática
    bloco_fatura = f"""
---
### Fatura Pro-Forma (Timesheet Audit)
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
# 🎨 CSS APEX V340
# ==========================================
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #0F172A;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body {{ overflow-x: hidden !important; width: 100vw !important; margin: 0; padding: 0; }}
.stApp {{ {bg_css} color: #cbd5e1; font-family: 'Inter', sans-serif; }}
[data-testid="stHeader"], footer {{ display: none !important; }}

[data-testid="stSidebar"] {{ background: rgba(15, 23, 42, 0.95) !important; border-right: 1px solid rgba(212, 175, 55, 0.2) !important; padding-top: 10px; }}
[data-testid="stSidebarContent"] {{ padding: 0 10px; }}
[data-testid="stSidebar"] img {{ max-width: 140px; margin: 0 auto 5px auto; display: block; filter: grayscale(100%) brightness(150%); }}

.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(212, 175, 55, 0.15); padding: 5px 15px; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4); }}
.omni-brand {{ display: flex; align-items: center; gap: 10px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.0rem; color: #f8fafc; font-weight: 700; letter-spacing: 0.5px; }}
.omni-brand span {{ color: #D4AF37; font-size: 0.55rem; font-weight: 700; letter-spacing: 1px; border: 1px solid rgba(212, 175, 55, 0.4); padding: 2px 6px; border-radius: 6px; background: rgba(212, 175, 55, 0.05); text-transform: uppercase; }}

div[data-testid="stExpander"] {{ background: rgba(15, 23, 42, 0.3) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 6px !important; margin-bottom: 0px !important; padding: 0 !important; }}
div[data-testid="stExpander"] p {{ font-size: 0.70rem !important; font-weight: 600 !important; color: #D4AF37 !important; text-transform: uppercase; margin: 0 !important; }}

div[data-baseweb="select"] > div {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.75rem !important; border-radius: 6px !important; min-height: 28px !important; }}
.stTextArea label, .stCheckbox label span, .stTextInput label, .stNumberInput label {{ font-size: 0.65rem !important; color: #cbd5e1 !important; font-weight: 600 !important; margin-bottom: 0px !important; }}
.stTextArea textarea, .stTextInput input, .stNumberInput input, input[type="password"] {{ background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(255,255,255,0.05) !important; color: #f8fafc !important; font-size: 0.75rem !important; border-radius: 6px !important; box-shadow: inset 0 2px 5px rgba(0,0,0,0.2); padding: 5px !important; }}
.stTextArea textarea:focus, .stTextInput input:focus, .stNumberInput input:focus, input[type="password"]:focus {{ border-color: #D4AF37 !important; box-shadow: 0 0 8px rgba(212, 175, 55, 0.1) !important; }}
.stTextArea textarea {{ height: 60px !important; min-height: 60px !important; }}

.stButton > button[kind="primary"] {{ background: linear-gradient(135deg, #B8860B, #D4AF37) !important; border-radius: 6px !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; padding: 6px !important; border: none !important; width: 100% !important; transition: 0.3s; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.2); margin-top: 5px; font-size: 0.75rem !important; }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-2px); box-shadow: 0 6px 15px rgba(212, 175, 55, 0.4); }}

[data-testid="stDownloadButton"] button {{
    background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 6px !important; font-size: 0.70rem !important; font-weight: 600 !important; padding: 4px !important; width: 100% !important; transition: 0.3s !important;
}}
[data-testid="stDownloadButton"] button:hover {{ background: rgba(212,175,55,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}

.stButton > button[kind="secondary"] {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.15) !important; border-radius: 6px !important; font-weight: 600 !important; transition: 0.3s; padding: 4px !important; font-size: 0.70rem !important; }}
.stButton > button[kind="secondary"]:hover {{ background: rgba(212,175,55,0.1) !important; color: #fff !important; border-color: #D4AF37 !important; }}

.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 10px; }}
.kpi-box {{ background: rgba(30, 41, 59, 0.4); border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); border-left: 3px solid #D4AF37; padding: 8px 12px; backdrop-filter: blur(10px); }}
.kpi-title {{ color: #94a3b8; font-size: 0.55rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; display:block; margin-bottom: 2px; }}
.kpi-value {{ color: #f8fafc; font-size: 1.0rem; font-weight: 600; line-height: 1.2; display:block; }}
.kpi-value.highlight {{ color: #D4AF37; font-weight: 700; }}

[data-testid="stTabs"] button {{ padding: 6px 15px !important; font-size: 0.8rem !important; font-weight: 600 !important; color: #94a3b8 !important; border-bottom: 2px solid transparent !important; }}
[data-testid="stTabs"] button[aria-selected="true"] {{ color: #D4AF37 !important; border-bottom: 2px solid #D4AF37 !important; background: rgba(212, 175, 55, 0.05) !important; border-radius: 6px 6px 0 0; }}

.login-box {{ background: rgba(30, 41, 59, 0.6); padding: 30px; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.3); box-shadow: 0 10px 30px rgba(0,0,0,0.5); max-width: 380px; margin: 60px auto; text-align: center; backdrop-filter: blur(10px); }}
.login-box img {{ max-width: 160px; margin-bottom: 10px; filter: grayscale(100%) brightness(150%); }}
.login-title {{ color: #f8fafc; font-size: 1.6rem; font-weight: 700; margin-bottom: 0px; line-height: 1.2; }}
.login-subtitle {{ color: #D4AF37; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px; }}

.stProgress > div > div > div > div {{ background-color: #D4AF37 !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# ==========================================
# 🔐 MURALHA DE GELO (TELA DE LOGIN)
# ==========================================
if not st.session_state.logged_in:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=False)
    st.markdown('<div class="login-title">AETHER KARV</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-subtitle">ENTERPRISE EDITION V340</div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color: #94a3b8; font-size: 0.75rem; margin-bottom: 15px;'>Acesso Restrito ao Cofre de Dados</p>", unsafe_allow_html=True)
    
    login_user = st.text_input("Usuário", placeholder="Ex: henrique...")
    login_pass = st.text_input("Senha", type="password", placeholder="Sua senha secreta...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 LOGIN", type="primary", use_container_width=True):
            conn = sqlite3.connect('aether_fortknox.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (login_user, login_pass))
            user = c.fetchone()
            conn.close()
            
            if user:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.toast(f"Bem-vindo, {login_user.upper()}!", icon="✅")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Credenciais Inválidas.")
    with col2:
        if st.button("📝 CRIAR CONTA", type="secondary", use_container_width=True):
            if login_user and login_pass:
                if create_new_user(login_user, login_pass):
                    st.success("Conta criada! Pode fazer login.")
                else:
                    st.error("Usuário já existe.")
            else:
                st.warning("Preencha usuário e senha.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# INTERFACE PRINCIPAL (SÓ APARECE SE LOGADO)
# ==========================================
else:
    GROQ_KEY = st.secrets.get("GROQ_API_KEY", "")
    GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", "")
    CNJ_API_KEY = st.secrets.get("CNJ_API_KEY", "DEMO_KEY")

    with st.sidebar:
        if os.path.exists("logo.png"):
            st.image("logo.png")
        else:
            st.markdown(f'<div class="omni-brand" style="margin-bottom: 10px;"><h1>AETHER KARV</h1><span>V340 CHRONOS | {st.session_state.username.upper()}</span></div>', unsafe_allow_html=True)

        with st.expander("📁 Base de Conhecimento", expanded=True):
            up = st.file_uploader("Documentos base...", accept_multiple_files=True, label_visibility="collapsed")
            num_processo_input = st.text_input("Nº do Processo / CNPJ (DataJud)", placeholder="Insira para extração...")
            cmd = st.text_area("", key="cmd_input", placeholder="Instruções ou cole o contrato aqui...", label_visibility="collapsed", height=60)

        with st.expander("⚙️ Motor de Configurações", expanded=False):
            agente_foco = st.selectbox("Especialidade", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"])
            
            # ⚠️ V340 APEX: ATIVAÇÃO DO MOTOR DE PRAZOS ⚠️
            ativar_prazos = st.checkbox("Ativar Calculadora de Prazos (15 Dias Úteis CPC)", value=True, help="Se ativado, calcula a data fatal matemática ignorando sábados e domingos.")
            
            ativar_redlining = st.checkbox("Ativar Redlining (Reescrita Ativa)", value=False)
            valor_hora = st.number_input("Sua Hora Técnica (R$)", min_value=50.0, max_value=5000.0, value=350.0, step=50.0)

        if st.button("🚀 INICIAR AUDITORIA", type="primary"):
            if not GROQ_KEY and not GEMINI_KEY:
                st.error("⚠️ ERRO CRÍTICO: O Administrador não configurou as chaves no Servidor (st.secrets).")
            elif cmd or up or num_processo_input:
                st.toast("Iniciando Motor Hydra...", icon="🔥")
                progress_bar = st.progress(5, text="Iniciando Córtex de Ingestão...")
                time.sleep(0.5)
                
                progress_bar.progress(20, text="Extraindo dados...")
                texto_arquivos, num_arquivos, usou_ocr = extrator_nexus_v3(up) if up else ("", 0, False)
                
                progress_bar.progress(40, text="Consultando bases e estruturando RAG...")
                resposta, motor_usado = orquestrador_omni(cmd, texto_arquivos, True, num_processo_input, agente_foco, ativar_redlining, valor_hora, ativar_prazos, GROQ_KEY, GEMINI_KEY, CNJ_API_KEY)
                
                progress_bar.progress(75, text="Gravando no Banco de Dados (Fort Knox)...")
                
                if up: titulo_doc = up[0].name
                elif cmd: titulo_doc = cmd[:30] + "..."
                elif num_processo_input: titulo_doc = f"Proc: {num_processo_input}"
                else: titulo_doc = "Auditoria Genérica"
                
                save_dossier(st.session_state.username, titulo_doc, resposta)
                
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
                
        if st.button("🚪 LOGOUT", type="secondary"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.res_aether = None
            st.rerun()

    # --- ÁREA PRINCIPAL (WORKSPACE) ---
    st.markdown(f"""
    <div class="omni-topbar">
        <div style="font-weight: 600; color: #f8fafc; font-size: 0.8rem;">DASHBOARD ANALÍTICO</div>
        <div style="font-size: 0.70rem; color: #94a3b8;">Sessão Ativa: <span style="color: #22c55e;">{st.session_state.username.upper()}</span></div>
    </div>
    """, unsafe_allow_html=True)

    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Documentos Lidos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Nó de Processamento</span><span class="kpi-value highlight">{t['motor']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Módulo de Visão</span><span class="kpi-value">{t['ocr']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Operação</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dossiê", "📥 Exportação", "🕵️‍♂️ Raw", "🗄️ Cofre Nuvem"])
    
    with tab1:
        if st.session_state.res_aether:
            st.markdown('<div style="background: rgba(15,23,42,0.5); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); margin-top: 5px;">', unsafe_allow_html=True)
            st.markdown(st.session_state.res_aether)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="standby-container">', unsafe_allow_html=True)
            st.markdown('<div class="welcome-title">Workspace Online.</div>', unsafe_allow_html=True)
            st.markdown('<div class="welcome-subtitle">Injete documentos no painel lateral.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        if st.session_state.res_aether:
            st.write("Baixe o relatório:")
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.download_button("📄 WORD", data=st.session_state.res_docx, file_name="AETHER_Parecer.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
            with c2: st.download_button("📕 PDF", data=st.session_state.res_pdf, file_name="AETHER_Parecer.pdf", mime="application/octet-stream", use_container_width=True)
            with c3: st.download_button("📝 TXT", data=st.session_state.res_aether.encode('utf-8'), file_name="AETHER_Parecer.txt", mime="text/plain", use_container_width=True)
            with c4: st.download_button("📊 MD", data=st.session_state.res_aether.encode('utf-8'), file_name="AETHER_Parecer.md", mime="text/markdown", use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⟳ Limpar Tela", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.res_docx = None
                st.session_state.res_pdf = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando", "ocr": "Inativo", "motor": "Standby"}
                st.rerun()
        else:
            st.info("Gere uma análise primeiro.")
            
    with tab3:
        if st.session_state.res_aether:
            st.code(st.session_state.res_aether, language="markdown")
        else:
            st.info("Nenhum código raw na memória.")
            
    with tab4:
        st.write(f"Cofre Criptografado: **{st.session_state.username.upper()}**")
        historico = load_history(st.session_state.username)
        
        if len(historico) == 0:
            st.warning("O seu cofre de dados está vazio.")
        else:
            for idx, (data_hora, titulo, conteudo) in enumerate(historico):
                with st.expander(f"📁 {titulo} | 🕒 {data_hora}"):
                    st.markdown(conteudo)
                    st.download_button("Baixar Backup (MD)", data=conteudo.encode('utf-8'), file_name=f"Backup_Aether_{idx}.md", mime="text/markdown", key=f"bkp_{idx}")
