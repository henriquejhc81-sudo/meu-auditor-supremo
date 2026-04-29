import streamlit as st
import google.generativeai as genai
from docx import Document
from PIL import Image
import io
import time
import random

# --- CONFIGURAÇÃO SUPREMA PARA NUVEM ---
# O comando abaixo busca a chave escondida nas configurações do site
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Erro: Chave API não configurada nos 'Secrets' do Streamlit.")

def conectar_ao_cerebro():
    try:
        modelos_validos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return genai.GenerativeModel(modelos_validos)
    except:
        return genai.GenerativeModel('gemini-1.5-flash')

model = conectar_ao_cerebro()

def preparar_download(texto_final):
    doc = Document()
    doc.add_heading('AUDITORIA SUPREMA - RELATÓRIO FINAL', 0)
    for linha in texto_final.split('\n'):
        doc.add_paragraph(linha)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# --- INTERFACE ---
st.set_page_config(page_title="Auditor Supremo Online", layout="wide")
st.title("🛡️ Auditor Supremo v16.0 - Cloud Edition")

with st.sidebar:
    st.header("📂 Entrada de Dados")
    arquivo = st.file_uploader("Subir Documento ou Imagem", type=["txt", "pdf", "png", "jpg", "jpeg"])
    st.divider()
    st.success("✅ Sistema Online e Seguro")

# LÓGICA
input_data = []
if arquivo:
    if arquivo.type.startswith("image"):
        img = Image.open(arquivo)
        st.image(img, caption="Imagem Carregada", width=300)
        input_data = [img]
    else:
        texto = arquivo.read().decode("utf-8", errors="ignore")
        input_data = [f"CONTEÚDO: {texto}"]

comando = st.text_area("Instruções para a Auditoria:", height=100)

if st.button("🚀 EXECUTAR AUDITORIA"):
    if comando:
        with st.spinner("Sincronizando com a rede neural global..."):
            try:
                prompt = f"Atue como um Auditor Supremo Profissional. Analise e corrija: {comando}"
                time.sleep(1)
                
                if input_data:
                    response = model.generate_content([prompt, *input_data])
                else:
                    response = model.generate_content(prompt)
                
                resultado = response.text
                st.markdown("---")
                st.markdown(resultado)
                
                st.divider()
                st.download_button(
                    label="📥 BAIXAR RELATÓRIO EM WORD (.DOCX)",
                    data=preparar_download(resultado),
                    file_name="Auditoria_Nuvem.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.warning("Digite uma pergunta.")
