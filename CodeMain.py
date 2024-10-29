pip install streamlit google-generativeai Pillow requests gtts

import streamlit as st
from PIL import Image
import google.generativeai as genai
from io import BytesIO
import requests
from gtts import gTTS
import os
from typing import Dict, List, Tuple

class StreamlitDressCodeAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        self.event_dress_codes = {
            "Funeral": {
                "appropriate": ["terno preto", "vestido preto", "roupa social escura", "sapato social"],
                "inappropriate": ["tênis", "roupas coloridas", "roupas casuais", "jeans", "camiseta"],
                "description": "vestuário formal e discreto, predominantemente em cores escuras",
                "praise_points": ["respeito", "discrição", "formalidade"]
            },
            "Casamento": {
                "appropriate": ["terno", "vestido social", "roupa formal", "sapato social"],
                "inappropriate": ["jeans", "tênis", "camiseta", "roupa muito casual"],
                "description": "vestuário formal adequado à cerimônia",
                "praise_points": ["elegância", "adequação ao evento", "formalidade"]
            },
            # Adicione os outros eventos aqui como no código original
        }

    def analyze_image(self, image, event: str) -> str:
        try:
            prompt = """
            Em português brasileiro, forneça uma descrição detalhada da imagem no formato de autodescrição para pessoas com deficiência visual,
            com foco especial no que a pessoa está vestindo e calçando. A descrição deve ser respeitosa e profissional.
            """
            
            response = self.model.generate_content([prompt, image])
            base_description = response.text
            
            is_appropriate, inappropriate_items, appropriate_items = self._evaluate_dress_code(event, base_description)
            feedback = self._generate_feedback(event, is_appropriate, appropriate_items, inappropriate_items)
            
            return base_description + feedback
            
        except Exception as e:
            return f"Ocorreu um erro durante a análise: {str(e)}"

    # Mantenha os métodos auxiliares (_evaluate_dress_code, _generate_feedback, etc.) 
    # do código original aqui

def main():
    st.set_page_config(page_title="Análise de Vestimenta", page_icon="👔")
    
    st.title("Análise de Vestimenta com IA")
    st.write("Upload uma foto e escolha o evento para análise da vestimenta")

    # Configuração da API key
    api_key = st.sidebar.text_input("Digite sua API key do Google Gemini", type="password")
    
    if not api_key:
        st.warning("Por favor, insira sua API key para continuar.")
        return

    analyzer = StreamlitDressCodeAnalyzer(api_key)
    
    # Upload de imagem
    image_source = st.radio("Escolha a fonte da imagem:", ["Upload", "URL"])
    
    if image_source == "Upload":
        uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
    else:
        url = st.text_input("Digite a URL da imagem:")
        if url:
            try:
                response = requests.get(url)
                image = Image.open(BytesIO(response.content))
            except:
                st.error("Erro ao carregar a imagem da URL. Verifique se o link está correto.")
                return
    
    # Seleção do evento
    eventos = list(analyzer.event_dress_codes.keys())
    evento = st.selectbox("Selecione o evento:", eventos)
    
    # Botão de análise
    if st.button("Analisar Vestimenta"):
        if 'image' in locals():
            with st.spinner("Analisando a imagem..."):
                # Mostrar a imagem
                st.image(image, caption="Imagem enviada", use_column_width=True)
                
                # Fazer a análise
                resultado = analyzer.analyze_image(image, evento)
                
                # Mostrar resultados
                st.subheader("Resultado da Análise")
                st.write(resultado)
                
                # Gerar áudio (opcional)
                if st.checkbox("Gerar narração em áudio"):
                    try:
                        tts = gTTS(text=resultado, lang='pt-br')
                        tts.save("output.mp3")
                        
                        with open("output.mp3", "rb") as audio_file:
                            audio_bytes = audio_file.read()
                            st.audio(audio_bytes, format="audio/mp3")
                            
                        os.remove("output.mp3")
                    except Exception as e:
                        st.error(f"Erro ao gerar áudio: {str(e)}")
        else:
            st.warning("Por favor, faça upload de uma imagem primeiro.")

if __name__ == "__main__":
    main()
