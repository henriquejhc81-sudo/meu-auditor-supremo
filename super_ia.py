import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    # AJUSTE: Forçamos o modelo flash que é o mais rápido para evitar travamentos
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Erro na Chave API.")

def preparar_download(texto):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA', 0)
    doc.add_paragraph(texto)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.5 - Conexão Direta")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Carregar Arquivo", type=["txt", "pdf", "png", "jpg", "jpeg"])

pergunta = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if pergunta:
        with st.spinner("Buscando resposta imediata..."):
            try:
                # Se tiver arquivo, envia junto. Se não, envia só a pergunta.
                if arquivo and arquivo.type.startswith("image"):
                    img = Image.open(arquivo)
                    response = model.generate_content([pergunta, img])
                else:
                    response = model.generate_content(pergunta)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button("📥 BAIXAR EM WORD", preparar_download(response.text), "Auditoria.docx")
                
            except Exception as e:
                # AJUSTE: Se der erro, ele agora mostra o erro REAL para sabermos o que é
                st.error(f"Erro de Conexão: {e}")
                st.info("Dica: Se aparecer 'Quota Exceeded', aguarde 1 minuto. Se for '404', o modelo ainda está carregando na nuvem.")
    else:
        st.warning("Digite uma pergunta.")
