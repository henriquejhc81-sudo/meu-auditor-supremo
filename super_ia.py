import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER OMNI V128", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO (Memória Blindada) ---
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
def aether_karv_engine(comando, contexto_arquivos, lindb_ativada):
    if not contexto_arquivos.strip():
        contexto_arquivos = "[Nenhum dado de arquivo injetado. Operando apenas com o comando.]"
    
    contexto_lindb = "\nDIRETRIZ DE ALTA PRIORIDADE: Aplicar análise de blindagem de gestores públicos (Art. 22 da LINDB)." if lindb_ativada else ""
    groq_api_key = os.environ.get("GROQ_API_KEY") 
    
    if groq_api_key:
        try:
            client = Groq(api_key=groq_api_key)
            prompt_tatico = f"Você é o AETHER OMNI, um sistema multi-agente.\nAtue como 7 especialistas (TCU, Jurídico, Financeiro, Risco, etc).{contexto_lindb}\nComando: {comando}\nDados: {contexto_arquivos}"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_tatico}],
                model="llama3-70b-8192", temperature=0.2,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"⚠️ FALHA NO LINK NEURAL GROQ: {str(e)}"
    else:
        time.sleep(3) 
        return f"**AUDITORIA OMNI CONCLUÍDA:**\nAnálise processada com sucesso. {contexto_lindb}\n(Configure GROQ_API_KEY para acesso neural)."

# --- 🎨 CSS APEX V128: BLOQUEIO DE SCROLL ---
back_apex_b64 = get_base64_image("back_apex.png")
bg_css = f"background: linear-gradient(rgba(2, 6, 23, 0.92), rgba(2, 6, 23, 0.92)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

/* RESET GERAL & BLOQUEIO DE SCROLL VERTICAL */
html, body {{ overflow: hidden !important; height: 100vh !important; }}
.stApp {{ {bg_css} color: #94a3b8; font-family: 'Inter', sans-serif; height: 100vh !important; overflow: hidden !important; }}

/* ESPAÇAMENTO MÁXIMO (Zero margens fantasmas) */
.block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; max-width: 98% !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* TOPBAR CORPORATIVA */
.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.6); border-bottom: 1px solid #1e293b; padding: 6px 20px; margin-bottom: 10px; border-radius: 4px; }}
.omni-brand h1 {{ margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: #10b981; letter-spacing: 1px; }}
.omni-brand span {{ color: #475569; font-size: 0.7rem; letter-spacing: 2px; }}
.omni-status {{ font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #34d399; }}

/* ESTILIZAÇÃO DOS CONTAINERS */
[data-testid="column"] {{ background: rgba(15, 23, 42, 0.4) !important; border: 1px solid #1e293b !important; border-radius: 4px !important; padding: 12px !important; height: 85vh; display: flex; flex-direction: column; }}

/* TÍTULOS DE SESSÃO */
.section-title {{ color: #f8fafc; font-size: 0.8rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; border-bottom: 1px solid #1e293b; padding-bottom: 4px; }}

/* UPLOADER & TEXT AREA COMPACTOS */
[data-testid="stFileUploadDropzone"] {{ background-color: rgba(2, 6, 23, 0.5) !important; border: 1px dashed #334155 !important; border-radius: 4px !important; padding: 5px !important; min-height: 40px !important; }}
.stTextArea label, .stCheckbox label span {{ font-size: 0.7rem !important; color: #cbd5e1 !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px !important; }}
.stTextArea textarea {{ background-color: rgba(2, 6, 23, 0.8) !important; border: 1px solid #334155 !important; color: #f8fafc !important; font-size: 0.8rem !important; border-radius: 4px !important; height: 100px !important; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: none !important; }}

/* BOTÃO DE PROCESSAR COLADO NO FUNDO */
.stButton > button[kind="primary"] {{ background: #10b981 !important; border-radius: 2px !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; padding: 8px !important; border: none !important; width: 100% !important; margin-top: auto !important; transition: 0.2s; }}
.stButton > button[kind="primary"]:hover {{ background: #059669 !important; }}

/* KPIs HTML (Substituindo o nativo que causou o bug) */
.custom-kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 10px; }}
.kpi-box {{ background: rgba(2, 6, 23, 0.6); border: 1px solid #1e293b; border-left: 2px solid #10b981; padding: 8px; border-radius: 4px; display: flex; flex-direction: column; }}
.kpi-title {{ color: #64748b; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }}
.kpi-value {{ color: #10b981; font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: bold; }}

/* AGENT GRID */
.agent-grid {{ display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }}
.agent-badge {{ background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace; padding: 3px 6px; border-radius: 2px; }}
.agent-standby {{ background: rgba(51, 65, 85, 0.2); border: 1px solid #334155; color: #64748b; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace; padding: 3px 6px; border-radius: 2px; }}

/* DOSSIÊ CONSOLE COM SCROLL INTERNO */
.console-output {{ background: #020617 !important; border: 1px solid #1e293b !important; border-radius: 4px !important; padding: 15px !important; flex-grow: 1; overflow-y: auto; font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #e2e8f0; margin-bottom: 10px; }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
[data-testid="stCodeBlock"] code {{ font-family: 'JetBrains Mono', monospace !important; color: #a7f3d0 !important; font-size: 0.8rem !important; }}

/* BOTÕES SECUNDÁRIOS */
.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: #1e293b !important; color: #cbd5e1 !important; border: 1px solid #334155 !important; border-radius: 2px !important; font-size: 0.7rem !important; padding: 4px !important; width: 100% !important; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- TOPBAR ---
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER OMNI</h1><span>ENTERPRISE ORCHESTRATOR</span></div>
    <div class="omni-status">● SYSTEM: ONLINE | KERNEL: V128.APEX</div>
</div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO PRINCIPAL ---
col_setup, col_main = st.columns([1, 2.5], gap="medium")

# ==========================================
# PAINEL 1: SETUP E INGESTÃO (ESQUERDA)
# ==========================================
with col_setup:
    st.markdown('<div class="section-title">NEXUS DATA INGESTION</div>', unsafe_allow_html=True)
    up = st.file_uploader("DROP ZONE", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<div class="section-title" style="margin-top:10px;">ORQUESTRAÇÃO & GRC</div>', unsafe_allow_html=True)
    ativar_lindb = st.checkbox("Ativar Matriz LINDB (Art. 22)", value=True)
    
    cmd = st.text_area("DIRETRIZ DE EXECUÇÃO:", key="cmd_input", placeholder="Insira o escopo da auditoria ou M&A...")

    if st.button("▶ PROCESSAR ORQUESTRAÇÃO", type="primary"):
        if cmd:
            with st.spinner("Sincronizando 7 Agentes AETHER..."):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                time.sleep(1) 
                resposta = aether_karv_engine(cmd, texto_arquivos, ativar_lindb)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = {
                    "arquivos": str(num_arquivos),
                    "volume": f"{len(texto_arquivos)/1024:.1f} KB",
                    "tempo": time.strftime("%H:%M:%S"),
                    "risco": "Mapeado"
                }
            st.rerun() 
        else:
            st.warning("Forneça uma diretriz.")

# ==========================================
# PAINEL 2: MAIN STAGE (DIREITA)
# ==========================================
with col_main:
    # --- LINHA 1: KPIs CUSTOMIZADOS (Sem erro e sem margens gigantes) ---
    t = st.session_state.telemetria
    st.markdown(f"""
    <div class="custom-kpi-grid">
        <div class="kpi-box"><span class="kpi-title">ATIVOS PROCESSADOS</span><span class="kpi-value">{t['arquivos']}</span></div>
        <div class="kpi-box"><span class="kpi-title">VOLUME DE DADOS</span><span class="kpi-value">{t['volume']}</span></div>
        <div class="kpi-box"><span class="kpi-title">TIMESTAMP (UTC)</span><span class="kpi-value">{t['tempo']}</span></div>
        <div class="kpi-box"><span class="kpi-title">STATUS DE RISCO</span><span class="kpi-value">{t['risco']}</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- LINHA 2: MULTI-AGENT VISUALIZATION ---
    st.markdown('<div class="section-title" style="margin-top:5px;">STATUS MULTI-AGENTE (NEURAL ORCHESTRATION)</div>', unsafe_allow_html=True)
    
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">● TCU: OK</div>
            <div class="agent-badge">● FRAUDE: OK</div>
            <div class="agent-badge">● JURÍDICO: OK</div>
            <div class="agent-badge">● RISCO: OK</div>
            <div class="agent-badge">● LINDB: ATIVA</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-standby">○ TCU: WAIT</div>
            <div class="agent-standby">○ FRAUDE: WAIT</div>
            <div class="agent-standby">○ JURÍDICO: WAIT</div>
            <div class="agent-standby">○ RISCO: WAIT</div>
            <div class="agent-standby">○ LINDB: WAIT</div>
        </div>
        """, unsafe_allow_html=True)

    # --- LINHA 3: CONSOLE OUTPUT ---
    if st.session_state.res_aether:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        
        b1, b2, b3 = st.columns([1,1,2])
        with b1: st.download_button("⬇ EXPORTAR TXT", data=st.session_state.res_aether, file_name="relatorio.txt", use_container_width=True)
        with b2: st.download_button("⬇ EXPORTAR MD", data=st.session_state.res_aether, file_name="matriz.md", use_container_width=True)
        with b3: 
            if st.button("⟳ CLEAR TERMINAL", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.session_state.telemetria = {"arquivos": "0", "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}
                st.rerun()
    else:
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; flex-grow:1; border: 1px dashed #1e293b; border-radius: 4px; background: rgba(2,6,23,0.3);">
            <div style="text-align: center; color: #475569; font-family: 'JetBrains Mono', monospace;">
                <h3 style="margin:0; font-size: 1.2rem; color: #334155;">AETHER KERNEL AWAITING INPUT</h3>
                <p style="font-size: 0.75rem; margin-top:5px;">Aguardando submissão de diretrizes no painel lateral.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
