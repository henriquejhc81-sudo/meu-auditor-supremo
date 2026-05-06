import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aether Omni | Intelligence", page_icon="🛡️", layout="wide")

# --- DESIGN CYBER-SENTINEL ---
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stButton>button { 
        background: linear-gradient(135deg, #00c853 0%, #b2ff59 100%); 
        color: #000; font-weight: bold; border-radius: 8px; width: 100%; height: 3.5em;
    }
    .status-box { padding: 15px; border-radius: 10px; background: #161b22; border-left: 5px solid #00c853; margin-bottom: 20px; }
    .dossie-box { background-color: #1a1c24; padding: 20px; border-radius: 10px; border: 1px solid #00c853; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR ANTI-LOCK 429 E AUTO-HEALING ---
def aether_brain(prompt, modo, contexto):
    try:
        # Priorizando Groq para evitar o erro 429 do Google Gemini
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except:
        return "Erro: Configure sua GROQ_API_KEY nos Secrets!"
        
    for attempt in range(5):
        try:
            prompt_sistema = f"""
            Você é o Aether Omni Sentinel. Missão: {modo}.
            OBRIGATÓRIO: Gere um 'DOSSIÊ DE BLINDAGEM' com Justificativa Técnica e base na LINDB.
            
            NOTA LEGAL OBRIGATÓRIA AO FINAL:
            '⚠️ NOTA: Este relatório é um suporte tecnológico à decisão e análise técnica. Não substitui o parecer jurídico de um advogado ou autoridade competente.'
            """
            completion = client.chat.completions.create(
                messages=[{"role": "system", "content": prompt_sistema}, {"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                st.warning(f"🛡️ Sincronização em curso... Aguarde {attempt+5}s")
                time.sleep(attempt + 5)
            else:
                return f"Erro no sistema: {e}"
    return "O sistema atingiu o limite. Tente novamente em instantes."

# --- BARRA LATERAL ---
with st.sidebar:
    st.title("🛡️ Aether Omni")
    st.caption("Intelligence & Compliance System")
    
    st.divider()
    st.subheader("⚙️ Parâmetros Sniper")
    st.toggle("OCR Inteligente", value=True)
    st.toggle("Risco Provisório", value=True)
    st.toggle("Análise Forense", value=True)
    
    st.divider()
    modo = st.selectbox("🎯 Ação Imediata", [
        "Auditoria Técnica + LINDB",
        "Dossiê de Blindagem",
        "Correção de Código Sentinel",
        "Análise de Risco Compliance"
    ])

# --- ÁREA PRINCIPAL ---
st.title("🛡️ Sistema Aether Omni")
st.markdown("<div class='status-box'><b>CONEXÃO:</b> ESTÁVEL | <b>MODO:</b> BLINDAGEM ATIVA</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 Entrada de Dados")
    user_input = st.text_area("Descreva o caso ou cole o código para auditoria:", height=300)
    upload = st.file_uploader("Upload de Documentos/Código", accept_multiple_files=True)

with col2:
    st.subheader("🚀 Dossiê Gerado")
    if st.button("INICIAR VARREDURA GLOBAL OMNI"):
        if user_input:
            with st.spinner("Aether processando e gerando blindagem..."):
                time.sleep(random.uniform(1.0, 2.0))
                try:
                    with DDGS() as ddgs:
                        busca = [r['body'] for r in ddgs.text(f"jurisprudência e técnica: {user_input}", max_results=2)]
                        contexto = "\n".join(busca)
                except:
                    contexto = "Base interna offline."
                
                resultado = aether_brain(user_input, modo, contexto)
                st.session_state['res_aether'] = resultado
                st.markdown(f"<div class='dossie-box'>{resultado}</div>", unsafe_allow_html=True)
        else:
            st.error("Insira os dados para análise.")

    if 'res_aether' in st.session_state:
        st.divider()
        formato = st.selectbox("Formato do Relatório:", [".txt", ".pdf (como texto)", ".py", ".html"])
        st.download_button(label=f"📥 BAIXAR DOSSIÊ ({formato})", data=st.session_state['res_aether'], file_name=f"dossie_aether{formato}")

# --- CHAT SUPORTE ---
st.divider()
st.subheader("💬 Consultar Analista Omni")
chat_in = st.text_input("Dúvida sobre este dossiê?")
if chat_in and 'res_aether' in st.session_state:
    with st.chat_message("assistant"):
        st.markdown(aether_brain(f"Contexto: {st.session_state['res_aether']}. Dúvida: {chat_in}", "Chat Suporte", ""))
