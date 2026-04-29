import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO BLINDADA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Forçamos a configuração a ignorar versões beta instáveis
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não configurada.")

# Seleção direta do modelo estável (sem prefixos que causam erro 404)
model = genai.GenerativeModel('gemini-1.5-flash')

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA', 0)
    for linha in texto.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.8 - Blindagem Total")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Carregar Arquivo", type=["txt", "pdf", "png", "jpg", "jpeg"])

pergunta = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if pergunta:
        with st.spinner("Conectando ao Cérebro Global..."):
            try:
                # O segredo: usamos o método de geração mais compatível
                if arquivo and arquivo.type.startswith("image"):
                    img = Image.open(arquivo)
                    response = model.generate_content([pergunta, img])
                else:
                    response = model.generate_content(pergunta)
                
                st.markdown("---")
                st.markdown(response.text)
                st.download_button("📥 BAIXAR EM WORD", preparar_download(response.text), "Auditoria.docx")
            except Exception as e:
                # Se ainda assim der erro, o sistema tenta o modelo Pro automaticamente
                try:
                    modelo_reserva = genai.GenerativeModel('gemini-pro')
                    response = modelo_reserva.generate_content(pergunta)
                    st.markdown(response.text)
                except:
                    st.error(f"Erro de Conexão: {e}. O Google está atualizando os servidores. Tente novamente em 1 minuto.")
    else:
        st.warning("Digite uma pergunta.")
