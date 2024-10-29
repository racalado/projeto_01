import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import requests
from gtts import gTTS
from io import BytesIO
from typing import Dict, List, Tuple

# Configurações da página
st.set_page_config(
    page_title="Análise de Vestimenta",
    page_icon="👔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carrega variáveis de ambiente
load_dotenv()

# Tenta importar o google.generativeai com tratamento de erro
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    st.error("""
        🚨 O pacote google-generativeai não está instalado. 
        Por favor, instale usando:
        ```
        pip install google-generativeai==0.3.2
        ```
    """)

# Resto do seu código aqui (mantenha o mesmo da versão anterior)
# ...

if __name__ == "__main__":
    main()
