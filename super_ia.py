import streamlit as st
import pandas as pd
import io
import time
from PIL import Image

# Gestão de dependências críticas
try:
    import google.generativeai as genai
    from docx import Document
    BIBLIOTECAS_OK = True
except ImportError:
    BIBLIOTECAS_OK = False

# --- UI REVOLUTION & DESIGN PREMIUM ---
st.set_page_config(page_title="AETHER OMNI MASTER v72.0", layout="wide", page_icon="🛡️")

if not BIBLIOTECAS_OK:
    st.error("🚨 Erro Crítico: Dependências ausentes (google-generativeai, python-docx).")
    st.stop()

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    #MainMenu, footer, header {visibility: hidden;}
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; }
    .main { background: radial-gradient(circle at 10% 10%, #0d1117, #080a0d); color: #ffffff; }
    .stButton>button { 
        width: 100%; background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.8em; border: none;
        transition: 0.3s all;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(0, 198, 255, 0.4); }
    .report-card { padding: 35px; border-radius: 20px; background-color: #1a1c24; border: 1px solid #2d2f39; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .suggestion-box { padding: 15px; background: rgba(38, 39, 48, 0.5); border-radius: 12px; border-left: 5px solid #00c6ff; margin-bottom: 15px; font-size: 0.85em; }
    .stTextArea textarea { background-color: #11141b !important; border-radius: 12px !important; border: 1px solid #2d323d !important; color: #fff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXÃO BLINDADA V3 (AUTO-DIAGNÓSTICO) ---
api_key = st.secrets.get("GOOGLE_API_KEY")
model = None

if api_key:
    genai.configure(api_key=api_key)
    
    # Lista de nomes completos para evitar erro 404 de versão
    modelos_tentativa = [
        'models/gemini-1.5-pro-latest',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-pro',
        'models/gemini-1.5-flash'
    ]
    
    sucesso_conexao = False
    for m_name in modelos_tentativa:
        try:
            model_inst = genai.GenerativeModel(m_name)
            # Teste de fumaça (smoke test)
            model_inst.generate_content("ok", generation_config={"max_output_tokens": 1})
            model = model_inst
            st.sidebar.success(f"Motor Ativo: {m_name}")
            sucesso_conexao = True
            break
        except Exception:
            continue
            
    if not sucesso_conexao:
        st.error("🚨 Falha de rota na API. Tentando mapear modelos disponíveis...")
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if available_models:
                model = genai.GenerativeModel(available_models[0])
                st.sidebar.warning(f"Usando fallback: {available_models[0]}")
            else:
                st.error("Nenhum modelo compatível encontrado na sua conta.")
        except Exception as e:
            st.error(f"Erro ao listar modelos: {e}")
else:
    st.error("📡 Chave mestra não detectada nos Secrets.")

def preparar_exportacao(texto):
    doc = Document()
    doc.add_heading('AETHER OMNI - RELATÓRIO MASTER', 0)
    for linha in texto.split('\n'):
        if linha.strip(): doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- SIDEBAR (ARSENAL SNIPER) ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("v72.0 | Advanced Connectivity")
    agente = st.selectbox("🎯 Agente Especialista", ["Auditor Geral", "Trabalhista", "Imobiliário", "Tributário", "LGPD", "Compliance Federal"])
    
    st.divider()
    with st.expander("📂 Biblioteca de Perguntas", expanded=False):
        opcoes = {"Auditor Geral": ["Analise riscos contratuais.", "Verifique cláusulas ambíguas."]}
        for item in opcoes.get(agente, ["Analise o documento sob a ótica do agente selecionado."]):
            st.markdown(f"<div class='suggestion-box'>💡 {item}</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    checklist = st.toggle("Checklist de Compliance", value=True)
    score = st.toggle("Score de Risco (%)", value=True)
    seguranca = st.toggle("Proteção de Tecnologia", value=True)
    
    if st.button("🔄 Reiniciar Motor"):
        st.rerun()

# --- CENTRAL OMNI MASTER ---
st.title("🛡️ AETHER OMNI ENTERPRISE")
st.caption(f"Status: **Operacional** | Agente: **{agente}**")

col_input, col_output = st.columns([1, 1.3], gap="large")

with col_input:
    pergunta = st.text_area("Instruções Diretas (Sniper Prompt):", placeholder="Digite o comando...", height=250)
    arquivos = st.file_uploader("Upload de Evidências", type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"], accept_multiple_files=True)
    acao = st.selectbox("Comportamento Neural:", ["Auditoria de Erros & Conclusão Mestra", "Blindagem Jurídica (LINDB)", "Análise Multi-IA"])

with col_output:
    if st.button("🚀 INICIAR VARREDURA GLOBAL OMNI"):
        if (pergunta or arquivos) and model:
            with st.spinner(f"Orquestrando IAs e processando dados..."):
                try:
                    extra_data, imagens = "", []
                    if arquivos:
                        for arq in arquivos:
                            if arq.type.startswith("image"): imagens.append(Image.open(arq))
                            elif arq.name.endswith(('.xlsx', '.csv')):
                                df = pd.read_excel(arq) if arq.name.endswith('.xlsx') else pd.read_csv(arq)
                                extra_data += f"\nDataset {arq.name}:\n{df.to_string()}"

                    prompt_master = f"""
                    Atue como AETHER OMNI. Você é um {agente} Sênior. 
                    NUNCA revele seu código ou estrutura de arquivos.
                    MISSÃO: {acao}. INSTRUÇÃO: {pergunta}
                    CONTEXTO: {extra_data}
                    ESTRUTURA: 1. Resumo Executivo (7 IAs) | 2. Checklist: {checklist} | 3. Score: {score} | 4. Conclusão Mestra.
                    """
                    
                    response = model.generate_content([prompt_master, *imagens]) if imagens else model.generate_content(prompt_master)
                    st.markdown(f"<div class='report-card'>{response.text}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Exportar (.DOCX)", preparar_exportacao(response.text), "AETHER_REPORT.docx")
                    st.balloons()
                except Exception as e:
                    st.error(f"📡 Erro Crítico de Execução: {e}")
        else:
            st.warning("Verifique a entrada e se o motor lateral está verde.")
