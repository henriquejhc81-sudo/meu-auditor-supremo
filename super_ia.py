import streamlit as st
import pandas as pd
import os, time, base64
import docx2txt

# --- 🛡️ PROTOCOLO DE PRESERVAÇÃO & LIBS TÁTICAS ---
try:
    from groq import Groq
except ImportError:
    pass

st.set_page_config(page_title="AETHER OMNI V127", page_icon="⚖️", layout="wide", initial_sidebar_state="collapsed")

def get_base64_image(file):
    if os.path.exists(file):
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- 🧠 ESTADO DA SESSÃO ---
if "cmd_input" not in st.session_state: st.session_state.cmd_input = ""
if "res_aether" not in st.session_state: st.session_state.res_aether = None
if "telemetria" not in st.session_state: 
    st.session_state.telemetria = {"arquivos": 0, "volume": "0 KB", "tempo": "--:--:--", "risco": "Aguardando"}

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

# --- 🎨 CSS APEX V127: ENTERPRISE DASHBOARD ---
back_apex_b64 = get_base64_image("back_apex.png")
# Fundo ultra-escuro (92% de opacidade) para o background não poluir, apenas dar textura.
bg_css = f"background: linear-gradient(rgba(2, 6, 23, 0.92), rgba(2, 6, 23, 0.92)), url('data:image/png;base64,{back_apex_b64}'); background-size: cover; background-position: center; background-attachment: fixed;" if back_apex_b64 else "background-color: #020617;"

css_code = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;500;600;700&display=swap');

/* RESET GERAL */
.stApp {{ {bg_css} color: #94a3b8; font-family: 'Inter', sans-serif; }}
.block-container {{ padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 98% !important; }}
[data-testid="stHeader"] {{ display: none !important; }}

/* TOPBAR CORPORATIVA */
.omni-topbar {{ display: flex; justify-content: space-between; align-items: center; background: rgba(15, 23, 42, 0.6); border-bottom: 1px solid #1e293b; padding: 10px 20px; margin-bottom: 15px; border-radius: 4px; }}
.omni-brand h1 {{ margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; color: #10b981; letter-spacing: 1px; }}
.omni-brand span {{ color: #475569; font-size: 0.75rem; letter-spacing: 2px; }}
.omni-status {{ font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #34d399; }}

/* ESTILIZAÇÃO DOS CONTAINERS (Flat Design, Sem bordas arredondadas exageradas) */
[data-testid="column"] {{ background: rgba(15, 23, 42, 0.4) !important; border: 1px solid #1e293b !important; border-radius: 4px !important; padding: 15px !important; }}

/* TÍTULOS DE SESSÃO */
.section-title {{ color: #f8fafc; font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 15px; border-bottom: 1px solid #1e293b; padding-bottom: 5px; }}

/* UPLOADER & TEXT AREA (Militar/Corporativo) */
[data-testid="stFileUploadDropzone"] {{ background-color: rgba(2, 6, 23, 0.5) !important; border: 1px dashed #334155 !important; border-radius: 4px !important; padding: 10px !important; min-height: 50px !important; }}
.stTextArea label, .stCheckbox label span {{ font-size: 0.75rem !important; color: #cbd5e1 !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px !important; }}
.stTextArea textarea {{ background-color: rgba(2, 6, 23, 0.8) !important; border: 1px solid #334155 !important; color: #f8fafc !important; font-size: 0.85rem !important; border-radius: 4px !important; height: 120px !important; }}
.stTextArea textarea:focus {{ border-color: #10b981 !important; box-shadow: none !important; }}

/* BOTÃO DE PROCESSAR */
.stButton > button[kind="primary"] {{ background: #10b981 !important; border-radius: 2px !important; font-family: 'JetBrains Mono', monospace !important; font-weight: 700 !important; color: #020617 !important; text-transform: uppercase !important; padding: 8px !important; border: none !important; width: 100% !important; margin-top: 10px !important; transition: 0.2s; }}
.stButton > button[kind="primary"]:hover {{ background: #059669 !important; }}
.stButton > button[kind="secondary"], .stDownloadButton > button {{ background: #1e293b !important; color: #cbd5e1 !important; border: 1px solid #334155 !important; border-radius: 2px !important; font-size: 0.75rem !important; padding: 4px !important; width: 100% !important; }}

/* KPIs / METRICS (Estilo Terminal Bloomberg) */
[data-testid="stMetricValue"] {{ font-family: 'JetBrains Mono', monospace !important; color: #10b981 !important; font-size: 1.5rem !important; }}
[data-testid="stMetricLabel"] {{ color: #64748b !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 1px; }}

/* DOSSIÊ CONSOLE */
.console-output {{ background: #020617 !important; border: 1px solid #1e293b !important; border-radius: 4px !important; padding: 15px !important; height: 50vh; overflow-y: auto; font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #e2e8f0; }}
[data-testid="stCodeBlock"] {{ background: transparent !important; border: none !important; padding: 0 !important; }}
[data-testid="stCodeBlock"] code {{ font-family: 'JetBrains Mono', monospace !important; color: #a7f3d0 !important; font-size: 0.8rem !important; }}

/* AGENT GRID */
.agent-grid {{ display: flex; gap: 10px; margin-bottom: 15px; flex-wrap: wrap; }}
.agent-badge {{ background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #34d399; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; padding: 4px 8px; border-radius: 2px; }}
.agent-standby {{ background: rgba(51, 65, 85, 0.2); border: 1px solid #334155; color: #64748b; font-size: 0.7rem; font-family: 'JetBrains Mono', monospace; padding: 4px 8px; border-radius: 2px; }}
</style>
"""
st.markdown(css_code, unsafe_allow_html=True)

# --- TOPBAR ---
st.markdown(f"""
<div class="omni-topbar">
    <div class="omni-brand"><h1>AETHER OMNI</h1><span>ENTERPRISE ORCHESTRATOR</span></div>
    <div class="omni-status">● SYSTEM: ONLINE | KERNEL: V127.APEX</div>
</div>
""", unsafe_allow_html=True)

# --- GRID TÁTICO PRINCIPAL ---
# Coluna 1 (25%): Setup | Coluna 2 (75%): Operação
col_setup, col_main = st.columns([1, 3], gap="medium")

# ==========================================
# PAINEL 1: SETUP E INGESTÃO (ESQUERDA)
# ==========================================
with col_setup:
    st.markdown('<div class="section-title">NEXUS DATA INGESTION</div>', unsafe_allow_html=True)
    up = st.file_uploader("DROP ZONE", accept_multiple_files=True, label_visibility="collapsed")
    
    st.markdown('<br><div class="section-title">ORQUESTRAÇÃO & GRC</div>', unsafe_allow_html=True)
    ativar_lindb = st.checkbox("Ativar Matriz LINDB (Art. 22)", value=True, help="Aplica proteção jurídica de gestão pública.")
    
    cmd = st.text_area("DIRETRIZ DE EXECUÇÃO:", key="cmd_input", placeholder="Insira o escopo da auditoria ou M&A...")

    if st.button("▶ PROCESSAR ORQUESTRAÇÃO", type="primary"):
        if cmd:
            with st.spinner("Sincronizando 7 Agentes AETHER..."):
                texto_arquivos, num_arquivos = extrator_nexus(up) if up else ("", 0)
                # Simulação visual de tempo de execução
                time.sleep(1) 
                resposta = aether_karv_engine(cmd, texto_arquivos, ativar_lindb)
                
                st.session_state.res_aether = resposta
                st.session_state.telemetria = {
                    "arquivos": num_arquivos,
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
    # --- LINHA 1: KPIs (Dashboard Style) ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(label="ATIVOS PROCESSADOS", value=st.session_state.telemetria["arquivos"])
    kpi2.metric(label="VOLUME DE DADOS", value=st.session_state.telemetria["volume"])
    kpi3.metric(label="TIMESTAMP (UTC)", value=st.session_state.telemetria["tempo"])
    kpi4.metric(label="STATUS DE RISCO", value=st.session_state.telemetria["risco"])
    
    st.markdown("<hr style='border: 1px solid #1e293b; margin: 10px 0;'>", unsafe_allow_html=True)
    
    # --- LINHA 2: MULTI-AGENT VISUALIZATION ---
    st.markdown('<div class="section-title">STATUS MULTI-AGENTE (NEURAL ORCHESTRATION)</div>', unsafe_allow_html=True)
    
    # Mostra badges verdes se processou, cinzas se está em standby
    if st.session_state.res_aether:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-badge">● AGENTE TCU: CONCLUÍDO</div>
            <div class="agent-badge">● AGENTE FRAUDE: CONCLUÍDO</div>
            <div class="agent-badge">● AGENTE JURÍDICO: CONCLUÍDO</div>
            <div class="agent-badge">● AGENTE RISCO (GRC): CONCLUÍDO</div>
            <div class="agent-badge">● MATRIZ LINDB: ATIVA</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="agent-grid">
            <div class="agent-standby">○ AGENTE TCU: STANDBY</div>
            <div class="agent-standby">○ AGENTE FRAUDE: STANDBY</div>
            <div class="agent-standby">○ AGENTE JURÍDICO: STANDBY</div>
            <div class="agent-standby">○ AGENTE RISCO (GRC): STANDBY</div>
            <div class="agent-standby">○ MATRIZ LINDB: STANDBY</div>
        </div>
        """, unsafe_allow_html=True)

    # --- LINHA 3: CONSOLE OUTPUT ---
    if st.session_state.res_aether:
        st.markdown('<div class="console-output">', unsafe_allow_html=True)
        st.code(st.session_state.res_aether, language="markdown")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botões na base
        st.markdown("<br>", unsafe_allow_html=True)
        b1, b2, b3 = st.columns([1,1,2])
        with b1: st.download_button("⬇ EXPORTAR TXT", data=st.session_state.res_aether, file_name="relatorio.txt", use_container_width=True)
        with b2: st.download_button("⬇ EXPORTAR MD", data=st.session_state.res_aether, file_name="matriz.md", use_container_width=True)
        with b3: 
            if st.button("⟳ CLEAR TERMINAL", type="secondary", use_container_width=True):
                st.session_state.res_aether = None
                st.rerun()
    else:
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; height: 40vh; border: 1px dashed #1e293b; border-radius: 4px; background: rgba(2,6,23,0.3);">
            <div style="text-align: center; color: #475569; font-family: 'JetBrains Mono', monospace;">
                <h3 style="margin:0; font-size: 1.5rem; color: #334155;">AETHER KERNEL AWAITING INPUT</h3>
                <p style="font-size: 0.85rem; margin-top:5px;">Aguardando submissão de diretrizes no painel lateral.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
