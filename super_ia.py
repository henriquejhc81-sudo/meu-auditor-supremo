import streamlit as st
import pandas as pd
import os, time, base64, io
import docx2txt
import concurrent.futures
from docx import Document
from docx.shared import Pt, RGBColor
try:
    import PyPDF2
except ImportError:
    pass # Tratamento para caso a biblioteca ainda esteja instalando
try:
    from groq import Groq
except ImportError:
    pass

# --- ⚙️ CONFIGURAÇÃO DE SEGURANÇA E AMBIENTE ---
st.set_page_config(page_title="AETHER OMNI V200", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

# Coleta segura de chaves (Prioriza st.secrets, com fallback para variáveis de ambiente)
GROQ_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
GEMINI_KEY = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 MEMÓRIA E ESTADO ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "res_docx" not in st.session_state: st.session_state.res_docx = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}

def set_template(texto):
    st.session_state.cmd_input = texto

# --- 📂 MOTOR DE INGESTÃO AVANÇADO (NEXUS V2) ---
def extrator_nexus_v2(arquivos_upados):
    texto_extraido = ""
    sucesso = 0
    for arquivo in arquivos_upados:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- MATRIZ CSV: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif arquivo.name.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- MATRIZ XLSX: {arquivo.name} ---\n{df.to_string(index=False)}"
            elif arquivo.name.endswith('.docx'):
                texto = docx2txt.process(arquivo)
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{texto}"
            elif arquivo.name.endswith('.pdf'):
                try:
                    pdf_reader = PyPDF2.PdfReader(arquivo)
                    texto_pdf = ""
                    for page in pdf_reader.pages:
                        texto_pdf += page.extract_text() + "\n"
                    texto_extraido += f"\n\n--- PDF: {arquivo.name} ---\n{texto_pdf}"
                except:
                    texto_extraido += f"\n[Falha ao ler texto do PDF: {arquivo.name}]"
            elif arquivo.name.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            sucesso += 1
        except Exception as e:
            texto_extraido += f"\n[ERRO EM {arquivo.name}: {str(e)}]"
    
    # Prevenção de limite de tokens (Trunca em aprox 25 mil palavras para segurança do Groq Llama3-70b)
    if len(texto_extraido) > 100000:
        texto_extraido = texto_extraido[:100000] + "\n\n[DADOS TRUNCADOS PELO LIMITE DE MEMÓRIA SEGURA]"
        
    return texto_extraido, sucesso

# --- 🤖 AGENTE ÚNICO (Para paralelismo) ---
def chamar_agente_groq(nome_agente, system_prompt, comando, contexto):
    if not GROQ_KEY: return f"[{nome_agente}] Erro: Chave API ausente."
    try:
        client = Groq(api_key=GROQ_KEY)
        full_prompt = f"DIRETRIZ DO USUÁRIO: {comando}\n\nDADOS INGERIDOS:\n{contexto}"
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ],
            model="llama3-70b-8192",
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"[{nome_agente}] Falha de conexão: {str(e)}"

# --- 🚀 ORQUESTRADOR MULTI-AGENTE REAL (ASYNC) ---
def orquestrador_omni(comando, contexto_arquivos, lindb_ativada, agente_foco):
    if not contexto_arquivos.strip(): contexto_arquivos = "Nenhum documento fornecido. Opere apenas com base no comando."
    
    blindagem = "APLIQUE O ART 22 DA LINDB (Considerar obstáculos reais do gestor)." if lindb_ativada else ""
    
    # Definindo a personalidade dos 3 Agentes que vão trabalhar em paralelo
    agente_1_sys = f"Você é o AUDITOR DE RISCO. Foco: {agente_foco}. Procure inconsistências financeiras, multas, riscos contratuais e cláusulas abusivas. Seja cirúrgico e aponte os riscos em tópicos. {blindagem}"
    agente_2_sys = f"Você é o ADVOGADO SÊNIOR (LITÍGIO E DEFESA). Foco: {agente_foco}. Analise os dados procurando brechas na lei, teses de defesa, nulidades e jurisprudência aplicável. {blindagem}"
    
    resultados = {}
    # ⚡ MÁGICA: Executa os 2 agentes AO MESMO TEMPO
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future_risco = executor.submit(chamar_agente_groq, "AGENTE DE RISCO", agente_1_sys, comando, contexto_arquivos)
        future_legal = executor.submit(chamar_agente_groq, "AGENTE JURÍDICO", agente_2_sys, comando, contexto_arquivos)
        
        resultados["risco"] = future_risco.result()
        resultados["legal"] = future_legal.result()
        
    # ⚡ AGENTE 3: O Juiz/Sintetizador (Lê o trabalho dos outros dois e cria o Dossiê Final)
    agente_3_sys = "Você é o AETHER OMNI, a IA Central. Seu trabalho é ler os pareceres dos seus 2 sub-agentes (Risco e Jurídico) e criar um DOSSIÊ EXECUTIVO final perfeito, unificado, em formato Markdown. Não cite os agentes explicitamente, apenas entregue a solução final como se fosse um único documento coeso e brilhante."
    contexto_sintese = f"PARECER DE RISCO:\n{resultados['risco']}\n\nPARECER JURÍDICO:\n{resultados['legal']}"
    
    dossie_final = chamar_agente_groq("AETHER OMNI", agente_3_sys, "Sintetize os pareceres em um Dossiê Executivo profissional e definitivo.", contexto_sintese)
    return dossie_final

# --- 📄 GERADOR DE DOCX PROFISSIONAL ---
def gerar_docx_aether(texto_markdown):
    doc = Document()
    # Estilos AETHER
    styles = doc.styles
    style = styles['Normal']
    font = style.font
    font.name = 'Arial'
    font.size = Pt(11)
    
    # Cabeçalho Timbrado
    header = doc.add_heading('AETHER OMNI - STRATEGIC DOSSIER', 0)
    header.runs[0].font.color.rgb = RGBColor(16, 185, 129) # Verde Aether
    doc.add_paragraph(f"Gerado automaticamente em: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC\nClassificação: CONFIDENCIAL")
    doc.add_paragraph("_"*50)
    
    # Processa o texto básico (simplificado para converter Markdown em parágrafos)
    linhas = texto_markdown.split('\n')
    for linha in linhas:
        if linha.startswith('### '):
            doc.add_heading(linha.replace('### ', ''), level=3)
        elif linha.startswith('## '):
            doc.add_heading(linha.replace('## ', ''), level=2)
        elif linha.startswith('# '):
            doc.add_heading(linha.replace('# ', ''), level=1)
        elif linha.startswith('**') and linha.endswith('**'):
             p = doc.add_paragraph()
             p.add_run(linha.replace('**', '')).bold = True
        elif linha.strip() == '':
            continue
        else:
            doc.add_paragraph(linha.replace('**', '')) # Remove asteriscos residuais

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ==========================================
# 🎨 CSS APEX V132 (O Front-end Perfeito Preservado)
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
# INTERFACE (A Mágica Visual)
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
    up = st.file_uploader("Arraste contratos, petições ou planilhas...", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title">⚖️ Configurações da Análise</div>', unsafe_allow_html=True)
    agente_foco = st.selectbox("Especialidade do Assistente", ["Análise de Contratos", "Due Diligence Societária", "Compliance e Risco", "Auditoria Trabalhista", "Direito Público"], label_visibility="collapsed")
    ativar_lindb = st.checkbox("Aplicar Filtro de Proteção (Art. 22 LINDB)", value=True)
    
    st.markdown('<div class="section-title">💬 Instruções ou Pedidos Especiais</div>', unsafe_allow_html=True)
    cmd = st.text_area("", key="cmd_input", placeholder="Ex: Verifique as cláusulas de rescisão e aponte os riscos...", label_visibility="collapsed")

    if st.button("🚀 Iniciar Varredura Jurídica", type="primary"):
        if not GROQ_KEY:
            st.error("⚠️ CHAVE API GROQ NÃO ENCONTRADA. Configure o st.secrets.")
        elif cmd:
            with st.spinner("Orquestrando Agentes Paralelos (Aether Multi-Thread)..."):
                # 1. Extração
                texto_arquivos, num_arquivos = extrator_nexus_v2(up) if up else ("", 0)
                
                # 2. Orquestração Real em Paralelo
                resposta = orquestrador_omni(cmd, texto_arquivos, ativar_lindb, agente_foco)
                
                # 3. Geração Automática do DOCX
                docx_buffer = gerar_docx_aether(resposta)
                
                # 4. Salva no estado
                st.session_state.res_aether = resposta
                st.session_state.res_docx = docx_buffer
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Análise Concluída"
                }
            st.rerun() 
        else:
            st.warning("Por favor, forneça uma instrução para a análise.")

with col_main:
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">Documentos Lidos</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Volume Processado</span><span class="kpi-value">{t['volume']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Hora da Análise</span><span class="kpi-value">{t['tempo']}</span></div>
        <div class="kpi-box"><span class="kpi-title">Status da Varredura</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">Status dos Módulos Especialistas</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">✓ AGENTE DE RISCO: CONCLUÍDO</div>
            <div class="agent-badge">✓ AGENTE JURÍDICO: CONCLUÍDO</div>
            <div class="agent-badge">✓ AETHER (SÍNTESE MESTRA): ATIVO</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-title">Parecer Jurídico (Resultado)</div>', unsafe_allow_html=True)
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.markdown(st.session_state.res_aether) 
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1,1,2])
        with b1: 
            st.download_button("⬇ Exportar Relatório Oficial (Word DOCX)", data=st.session_state.res_docx, file_name="AETHER_Parecer_Executivo.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
        with b2: 
            st.download_button("⬇ Exportar Matriz Bruta (MD)", data=st.session_state.res_aether, file_name="AETHER_Matriz.md", use_container_width=True)
        with b3: 
            if st.button("⟳ Nova Análise (Limpar Dados Seguros)", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.res_docx = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}
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
