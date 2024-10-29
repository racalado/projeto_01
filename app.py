import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS
from io import BytesIO
from typing import Dict, List, Tuple

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Análise de Vestimenta",
        page_icon="👔",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def setup_gemini():
    """Setup and configure Google's Gemini AI."""
    try:
        import google.generativeai as genai
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            st.error('🚨 GOOGLE_API_KEY não encontrada nas variáveis de ambiente!')
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except ImportError:
        st.error("""
            🚨 O pacote google-generativeai não está instalado. 
            Por favor, instale usando:
            ```
            pip install google-generativeai==0.3.2
            ```
        """)
        return None

def process_image(image: Image) -> Dict:
    """
    Process the uploaded image and return analysis results.
    
    Args:
        image (Image): PIL Image object to analyze
    
    Returns:
        Dict: Analysis results including style, formality, and suggestions
    """
    model = setup_gemini()
    if not model:
        return None
    
    prompt = """
    Analise esta imagem de roupa e forneça:
    1. Estilo geral
    2. Nível de formalidade
    3. Ocasiões apropriadas
    4. Sugestões de combinação
    5. Dicas de cuidados com a peça
    
    Formato a resposta de forma estruturada e profissional.
    """
    
    try:
        response = model.generate_content([prompt, image])
        return {
            'success': True,
            'analysis': response.text
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def display_results(results: Dict):
    """Display the analysis results in the Streamlit interface."""
    if not results or not results.get('success'):
        st.error('❌ Erro ao analisar a imagem: ' + results.get('error', 'Erro desconhecido'))
        return
    
    analysis = results['analysis']
    
    # Create expandable sections for each part of the analysis
    with st.expander("📊 Análise Completa", expanded=True):
        st.markdown(analysis)
    
    # Add text-to-speech option
    if st.button("🔊 Ouvir Análise"):
        tts = gTTS(text=analysis, lang='pt')
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)  # Changed from write_to_audiofile to write_to_fp
        audio_file.seek(0)  # Reset the pointer to the beginning of the BytesIO object
        st.audio(audio_file)

def main():
    """Main function to run the Streamlit application."""
    # Load environment variables
    load_dotenv()
    
    # Setup page
    setup_page_config()
    
    # Header
    st.title("🎭 Análise de Vestimenta AI")
    st.markdown("""
    Upload uma foto da sua roupa para receber uma análise detalhada sobre estilo, 
    formalidade e sugestões de como usá-la.
    """)
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Escolha uma imagem da sua roupa",
        type=['png', 'jpg', 'jpeg'],
        help="Faça upload de uma imagem clara da peça de roupa que deseja analisar"
    )
    
    if uploaded_file:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem Enviada", use_column_width=True)
        
        # Process the image
        with st.spinner('Analisando sua roupa... ⏳'):
            results = process_image(image)
        
        # Display results
        display_results(results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    💡 **Dica**: Para melhores resultados, use fotos bem iluminadas e com fundo neutro.
    """)

if __name__ == "__main__":
    main()
