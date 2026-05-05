import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import pandas as pd
import io
import time

# --- UI REVOLUTION (ESTÉTICA DE ALTA PERFORMANCE) ---
st.set_page_config(page_title="AETHER OMNI | Intelligence", layout="wide", page_icon="🛡️")

if 'historico' not in st.session_state:
    st.session_state['historico'] = []
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #080a0d; }
    .main { background: radial-gradient(circle at top right, #0d1117, #080a0d); color: #e1e1e1; }

    /* Cards de Relatório - Efeito Glassmorphism */
    .report-card { 
        padding: 40px; border-radius: 20px; 
        background: rgba(22, 25, 32, 0.7); 
        border: 1px solid rgba(0, 198, 255, 0.1); 
        color: #d1d5db; line-height: 1.8;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }
    
    /* Botões Futuristas */
    .stButton>button { 
        width: 100%; 
        background: linear-gradient(135deg, #1e2128 0%, #11141b 100%); 
        color: #00c6ff; border: 1px solid #2d323d;
        border-radius: 12px; font-weight: 700; letter-spacing: 1px;
        height: 3.8em; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover { 
        background: #00c6ff; color: #080a0d;
        box-shadow: 0 0 20px rgba(0, 198, 255, 0.4);
        transform: translateY(-2px);
    }

    /* Sidebar Refinada */
    .history-card { 
        background: rgba(30, 33, 40, 0.5); 
        padding: 15px; border-radius: 10px; 
        border-left: 4px solid #00c6ff; 
        margin-bottom: 12px; font-size: 0.85em; 
    }
    .stTextArea textarea { background-color: #11141b !important; border-radius: 12px !important; border: 1px solid #2d323d !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA COM FALLBACK ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        try:
            model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(model_list[0] if model_list else 'gemini-1.5-flash')
        except:
            model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("📡 Chave mestra não detectada nos Secrets.")
except Exception as e:
    st.error(f"📡 Erro Crítico: {e}")

def preparar_docx(lista_resultados, unico=True):
    doc = Document()
    if unico:
        doc.add_heading('PARECER TÉCNICO AETHER', 0)
        doc.add_paragraph(lista_resultados[-1]['texto'] if isinstance(lista_resultados, list) else lista_resultados)
    else:
        doc.add_heading('CONSOLIDADO DE MISSÕES OMNI', 0)
        for res in lista_resultados:
            doc.add_heading(f"Missão: {res['titulo']}", level=1)
            doc.add_paragraph(res['texto'])
            doc.add_page_break()
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛡️ AETHER OMNI")
    st.caption("Intelligence & Compliance System")
    
    if st.button("📜 HISTÓRICO DE MISSÕES"):
        st.session_state['show_history'] = not st.session_state['show_history']

    if st.session_state['show_history']:
        if st.session_state['historico']:
            for item in st.session_state['historico']:
                st.markdown(f"<div class='history-card'><b>{item['fonte']}</b><br>{item['titulo']}</div>", unsafe_allow_html=True)
            st.download_button("📥 EXPORTAR HISTÓRICO", preparar_docx(st.session_state['historico'], unico=False), "omni_history.docx")
        else:
            st.caption("Sem registros.")

    st.divider()
    st.subheader("🛠️ Parâmetros Sniper")
    st.toggle("OCR Inteligente", value=True)
    st.toggle("Risco Provisório", value=True)
    st.toggle("Análise Forense", value=True)
    
    st.divider()
    with st.expander("⚙️ Sistema"):
        if st.button("RESET MOTOR"):
            st.session_state['historico'] = []
            st.rerun()
    st.caption("v52.1 Master Gold")

# --- CENTRAL DE OPERAÇÕES ---
st.title("🛡️ AETHER OMNI")
st.markdown("<p style='color:#7b818f; font-family:JetBrains Mono;'>HIGH-FREQUENCY AUDIT TERMINAL // GLOBAL COMPLIANCE</p>", unsafe_allow_html=True)

area_trabalho, area_comando = st.columns([1, 1.3], gap="large")

with area_trabalho:
    st.subheader("📂 Ingestão de Ativos")
    arquivos = st.file_uploader("Arraste evidências para análise", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    
    st.divider()
    st.subheader("⚡ Ação Imediata")
    acao_filtro = st.selectbox("Comportamento Neural:", [
        "Auditoria Técnica",
        "Geração de Contrato Corrigido",
        "Geração de Petição Corrigida"
    ])

with area_comando:
    st.subheader("🔍 Centro de Comando")
    tipo_missao = st.selectbox("Estratégia de Varredura:", [
        "Auditoria Geral", 
        "Auditar Processo Judicial", 
        "Auditar Contrato",
        "Análise Grafotécnica de Assinaturas",
        "Geração Documental Técnica"
    ])
    
    pergunta = st.text_area("Instruções Diretas (Sniper Prompt):", placeholder="Ex: Analise o anexo e aplique as correções do filtro lateral...", height=180)
    
    if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
        if pergunta or arquivos:
            with st.spinner("Processando..."):
                try:
                    conteudo_extra = ""
                    imagens = []
                    nome_fonte = "Input Manual"
                    
                    if arquivos:
                        # Tratamento para múltiplos arquivos
                        primeiro_nome = arquivos[0].name if isinstance(arquivos, list) else arquivos.name
                        nome_fonte = f"{primeiro_nome} (+{len(arquivos)-1})" if len(arquivos) > 1 else primeiro_nome
                        
                        for arq in arquivos:
                            if arq.type.startswith("image"):
                                imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                conteudo_extra += f"\n\nDATASET {arq.name}:\n{df.to_string()}"

                    prompt_final = f"""
                    Atue como o sistema AETHER OMNI (Auditor Forense e Especialista em Compliance Sênior).
                    MISSÃO: {tipo_missao}. AÇÃO: {acao_filtro}.
                    DADOS: {pergunta} {conteudo_extra}
                    ESTRUTURA: Diagnóstico -> Parecer Forense -> Veredito Técnico.
                    NOTA FINAL: 'Este relatório é um parecer técnico gerado por IA para auxílio na tomada de decisão, não substituindo a consultoria jurídica ou contábil individualizada.'
                    """
                    
                    response = model.generate_content([prompt_final, *imagens]) if imagens else model.generate_content(prompt_final)
                    
                    st.session_state['historico'].insert(0, {"titulo": tipo_missao, "fonte": nome_fonte, "texto": response.text})
                    
                    st.markdown("### 📝 PARECER OMNI")
                    t1, t2 = st.tabs(["📄 Relatório Executivo", "💾 Safebox"])
                    with t1: st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    with t2: st.download_button("📥 BAIXAR PARECER (.DOCX)", preparar_docx(response.text, unico=True), f"AETHER_{nome_fonte}.docx")
                except Exception as e:
                    st.error(f"🚨 Falha de Sincronização: {e}")
        else:
            st.warning("Aguardando entrada de dados para iniciar varredura.")
