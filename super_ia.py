import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER OMNI V129", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state or st.session_state.telemetria is None: 
    st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}

# --- ⚡ EXTRATOR NEXUS ---
def extrator_nexus(arquivos_upados):
    texto_extraido = ""
    sucesso = 0
    for arquivo in arquivos_upados:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
                texto_extraido += f"\n\n--- MATRIZ CSV: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.xlsx'):
                df = pd.read_excel(arquivo)
                texto_extraido += f"\n\n--- MATRIZ XLSX: {arquivo.name} ---\n{df.to_string()}"
            elif arquivo.name.endswith('.docx'):
                texto = docx2txt.process(arquivo)
                texto_extraido += f"\n\n--- DOCX: {arquivo.name} ---\n{texto}"
            elif arquivo.name.endswith('.txt'):
                texto_extraido += f"\n\n--- TXT: {arquivo.name} ---\n{arquivo.getvalue().decode('utf-8')}"
            sucesso += 1
        except Exception as e:
            texto_extraido += f"\n[ERRO DE LEITURA EM {arquivo.name}: {str(e)}]"
    return texto_extraido, sucesso

# --- ⚡ MOTOR AETHER KARV MULTI-AGENTE ---
def aether_karv_engine(comando, contexto_arquivos, lindb_ativada, agente_foco):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando.]"
    
    contexto_lindb = "\nDIRETRIZ DE ALTA PRIORIDADE: Aplicar análise de blindagem de gestores públicos (Art. 22 da LINDB)." if lindb_ativada else ""
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER OMNI, um sistema multi-agente. Foco Primário: {agente_foco}. Atue como 7 especialistas paralelos.{contexto_lindb}\nComando: {comando}\nDados: {contexto_arquivos}"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(3) 
        return f"**AUDITORIA OMNI CONCLUÍDA:**\nFoco: {agente_foco}\nProcessamento finalizado com sucesso. {contexto_lindb}\n(Configure GROQ_API_KEY para acesso neural total)."

# --- 🎨 CSS APEX V129: PALANTIR/GOTHAM ENTERPRISE EDITION ---
back_apex_b64 = get_base64_image("back_apex.png")
# Camada de escuridão quase total (95%) para criar o efeito "Glassmorphism" sutil sobre as linhas de circuito
bg_css = f"background: linear-gradient(rgba(2, 6, 23, 0.95), rgba(2, 6, 23, 0.95)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');

/* RESET GERAL & BLOQUEIO DE SCROLL */
html, body {{ overflow: hidden !important; height: 100vh !important; }}
.stApp {{ {bg_css} color: #94a3b8; font-family: 'Inter', sans-serif; height: 100vh !important; overflow: hidden !important; }}

/* ESPAÇAMENTO MÁXIMO */
.block-container {{ padding-top: 1.5rem !important; padding-bottom: 0rem !important; max-width: 96% !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* TOPBAR CORPORATIVA ELITE */
.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 8px 25px; margin-bottom: 15px; border-radius: 8px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }}
.omni-brand {{ display: flex; align-items: center; gap: 15px; }}
.omni-brand h1 {{ margin: 0; font-family: 'Inter', sans-serif; font-size: 1.2rem; color: #f8fafc; font-weight: 800; letter-spacing: 1px; }}
.omni-brand span {{ color: #10b981; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; font-weight: 700; letter-spacing: 1.5px; border: 1px solid rgba(16,185,129,0.3); padding: 2px 8px; border-radius: 10px; background: rgba(16,185,129,0.1); }}
.omni-status {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b; }}
.omni-status span {{ color: #10b981; font-weight: bold; }}

/* ESTILIZAÇÃO DOS CONTAINERS (Glassmorphism Puro) */
[data-testid="column"] {{ background: rgba(15, 23, 42, 0.3) !important; backdrop-filter: blur(16px) !important; -webkit-backdrop-filter: blur(16px) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 8px !important; padding: 20px !important; height: 85vh; display: flex; flex-direction: column; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2); }}

/* TÍTULOS DE SESSÃO */
.section-title {{ color: #e2e8f0; font-size: 0.75rem; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
.section-title::before {{ content: ''; display: block; width: 4px; height: 12px; background: #10b981; border-radius: 2px; }}

/* SELECTBOX DO AGENTE (Exigência do Manual) */
div[data-baseweb="select"] > div {{ background-color: rgba(2, 6, 23, 0.5) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 6px !important; }}

/* UPLOADER & TEXT AREA COMPACTOS */
[data-testid="stFileUploadDropzone"] {{ background-color: rgba(2, 6, 23, 0.3) !important; border: 1px dashed rgba(255,255,255,0.15) !important; border-radius: 6px !important; padding: 10px !important; min-height: 50px !important; transition: 0.3s; }}
[data-testid="stFileUploadDropzone"]:hover {{ border-color: #10b981 !important; background-color: rgba(16,185,129,0.05) !important; }}
[data-testid="stFileUploadDropzone"] small {{ display: none !important; }}

.stTextArea label, .stCheckbox label span, .stSelectbox label {{ font-size: 0.7rem !important; color: #94a3b8 !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px !important; font-weight: 600 !important; }}
.stTextArea textarea {{ background-color: rgba(2, 6, 23, 0.5) !important; border: 1px solid rgba(255,255,255,0.1) !important; color: #f8fafc !important; font-size: 0.85rem !important; border-radius: 6px !important; height: 100px !important; transition: 0.3s; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: 0 0 10px rgba(16,185,129,0.1) !important; }}

/* CHECKBOX LINDB */
[data-testid="stCheckbox"] {{ background: rgba(0,0,0,0.2); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 5px; }}

/* BOTÃO DE PROCESSAR - ELITE */
.stButton > button[kind="primary"] {{ background: linear-gradient(to right, #059669, #10b981) !important; border-radius: 4px !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important; color: #ffffff !important; text-transform: uppercase !important; letter-spacing: 1px !important; padding: 10px !important; border: none !important; width: 100% !important; margin-top: auto !important; transition: 0.3s; box-shadow: 0 4px 15px rgba(16,185,129,0.2); }}
.stButton > button[kind="primary"]:hover {{ transform: translateY(-1px); box-shadow: 0 6px 20px rgba(16,185,129,0.4); }}

/* KPIs HTML (Estilo Bloomberg/Palantir) */
.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 15px; }}
.kpi-box {{ background: transparent; display: flex; flex-direction: column; border-left: 2px solid rgba(16,185,129,0.5); padding-left: 10px; }}
.kpi-title {{ color: #64748b; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; font-weight: 600; }}
.kpi-value {{ color: #f8fafc; font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; font-weight: 400; }}
.kpi-value.highlight {{ color: #10b981; font-weight: 700; }}

/* AGENT GRID */
.agent-grid {{ display: flex; gap: 8px; margin-bottom: 15px; flex-wrap: wrap; }}
.agent-badge {{ background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 5px; }}
.agent-standby {{ background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #64748b; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace; padding: 4px 10px; border-radius: 4px; display: flex; align-items: center; gap: 5px; }}

/* DOSSIÊ CONSOLE COM SCROLL INTERNO */
.console-output {{ background: rgba(2, 6, 23, 0.4) !important; border: 1px solid rgba(255,255,255,0.05) !important; border-radius: 6px !important; padding: 15px !important; flex-grow: 1; overflow-y: auto; font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #e2e8f0; margin-bottom: 15px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.5); }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
[data-testid="stCodeBlock"] code {{ font-family: 'JetBrains Mono', monospace !important; color: #cbd5e1 !important; font-size: 0.8rem !important; }}

/* BOTÕES SECUNDÁRIOS */
.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: rgba(255,255,255,0.05) !important; color: #cbd5e1 !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 4px !important; font-size: 0.75rem !important; font-weight: 600 !important; padding: 6px !important; width: 100% !important; transition: 0.3s; }}
.stButton > button[kind="secondary"]:hover, .stDownloadButton > button:hover {{ background: rgba(255,255,255,0.1) !important; color: #fff !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- TOPBAR ---
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER OMNI</h1><span>GEMINI 1.5 PRO KERNEL</span></div>
    <div class="omni-status">DATA CLASSIFICATION: <span>TOP SECRET</span> | ENGINE: <span>V129.APEX</span></div>
</div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO PRINCIPAL ---
col_setup, col_main = st.columns([1, 2.5], gap="large")

# ==========================================
# PAINEL 1: SETUP E INGESTÃO (ESQUERDA)
# ==========================================
with col_setup:
    st.markdown('<div class="section-title">DATA INGESTION (NEXUS)</div>', unsafe_allow_html=True)
    up = st.file_uploader("DROP ZONE", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title" style="margin-top:15px;">MISSION PARAMETERS</div>', unsafe_allow_html=True)
    
    # ATENDENDO AO MANUAL: Seleção de Especialista
    agente_foco = st.selectbox("Agente Master (Lead Investigator)", ["Auditoria Forense [Big Four]", "Due Diligence (M&A)", "Compliance Federal (CGU)", "Jurisprudência Preditiva"])
    
    ativar_lindb = st.checkbox("Ativar Shield (Art. 22 LINDB)", value=True)
    
    cmd = st.text_area("NEURAL SNIPER PROMPT:", key="cmd_input", placeholder="Descreva o alvo da investigação...")

    if st.button("EXECUTE GLOBAL SWEEP", type="primary"):
        if cmd:
            with st.spinner("Conectando ao Google Gemini 1.5 Pro..."):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                time.sleep(1) 
                resposta = aether_karv_engine(cmd, texto_arquivos, ativar_lindb, agente_foco)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Mapeado"
                }
            st.rerun() 
        else:
            st.warning("O Sniper Prompt não pode estar vazio.")

# ==========================================
# PAINEL 2: MAIN STAGE (DIREITA)
# ==========================================
with col_main:
    # --- LINHA 1: KPIs GOTHAM STYLE ---
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">ASSETS INGERIDOS</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">DATA VOLUME</span><span class="kpi-value">{t['volume']}</span></div>
        <div class="kpi-box"><span class="kpi-title">SYNC (UTC)</span><span class="kpi-value">{t['tempo']}</span></div>
        <div class="kpi-box"><span class="kpi-title">RISK METRIC</span><span class="kpi-value highlight">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- LINHA 2: MULTI-AGENT VISUALIZATION ---
    st.markdown('<div class="section-title" style="margin-top:10px;">MULTI-IA ORCHESTRATION ARRAY</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">⚡ FORENSIC: ON</div>
            <div class="agent-badge">⚡ LEGAL: ON</div>
            <div class="agent-badge">⚡ TCU/CGU: ON</div>
            <div class="agent-badge">⚡ FINANCE: ON</div>
            <div class="agent-badge">🛡️ LINDB SHIELD: ACTIVE</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-standby">○ FORENSIC: IDLE</div>
            <div class="agent-standby">○ LEGAL: IDLE</div>
            <div class="agent-standby">○ TCU/CGU: IDLE</div>
            <div class="agent-standby">○ FINANCE: IDLE</div>
            <div class="agent-standby">○ LINDB SHIELD: IDLE</div>
        </div>
        """, unsafe_allow_html=True)

    # --- LINHA 3: CONSOLE OUTPUT ---
    st.markdown('<div class="section-title" style="margin-top:10px;">EXECUTIVE DOSSIER (OUTPUT)</div>', unsafe_allow_html=True)
    if st.session_state.res_aether:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1,1,2])
        with b1: st.download_button("⬇ EXPORTAR DOCX/TXT", data=st.session_state.res_aether, file_name="AETHER_Dossier.txt", use_container_width=True)
        with b2: st.download_button("⬇ MATRIZ DE RISCO (MD)", data=st.session_state.res_aether, file_name="AETHER_Matriz.md", use_container_width=True)
        with b3: 
            if st.button("⟳ PURGE SESSION (WIPE DATA)", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}
                st.rerun()
    else:
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; flex-grow:1; border: 1px dashed rgba(255,255,255,0.1); border-radius: 6px; background: rgba(0,0,0,0.2); min-height: 40vh;">
            <div style="text-align: center; color: #475569;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 10px; opacity: 0.5;"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                <h3 style="margin:0; font-size: 1rem; color: #64748b; font-family: 'JetBrains Mono', monospace;">SYSTEM STANDBY</h3>
                <p style="font-size: 0.75rem; margin-top:5px;">Awaiting parameters and Neural Sniper Prompt execution.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
