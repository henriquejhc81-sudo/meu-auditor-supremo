import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io

# --- CONFIGURAÇÃO DE SEGURANÇA ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # Força a configuração para a versão estável da API
    genai.configure(api_key=API_KEY)
except:
    st.error("Chave API não configurada nos Secrets.")

# Seleção direta do modelo estável
model = genai.GenerativeModel('gemini-1.5-flash')

def preparar_download(texto_final):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA - RELATÓRIO', 0)
    for linha in texto_final.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Supremo v16.4 - Edição Infalível")

with st.sidebar:
    st.header("📂 Entrada")
    arquivo = st.file_uploader("Subir Arquivo/Foto", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.success("🔒 Servidor Conectado")

dados_ia = []
if arquivo:
    if arquivo.type.startswith("image"):
        img = Image.open(arquivo)
        st.image(img, width=300)
        dados_ia = [img]
    else:
        texto = arquivo.read().decode("utf-8", errors="ignore")
        dados_ia = [f"CONTEÚDO: {texto}"]

comando = st.text_area("Instruções:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if comando:
        with st.spinner("Buscando resposta..."):
            try:
                # O segredo para não dar erro: usar apenas o texto ou lista simples
                if dados_ia:
                    conteudo_final = [comando] + dados_ia
                    response = model.generate_content(conteudo_final)
                else:
                    response = model.generate_content(comando)
                
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 BAIXAR EM WORD",
                    data=preparar_download(response.text),
                    file_name="Auditoria.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                # Caso o flash falhe, tenta o pro automaticamente
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    response = alt_model.generate_content(comando)
                    st.markdown(response.text)
                except:
                    st.error("O Google está demorando para responder. Aguarde 30 segundos e tente novamente.")
    else:
        st.warning("Digite uma pergunta.")
