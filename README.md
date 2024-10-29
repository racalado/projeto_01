# Análise de Vestimenta com IA

Uma aplicação Streamlit que analisa vestimentas usando IA para diferentes eventos sociais.

## 🚀 Demo

Você pode acessar a aplicação em: [seu-app.streamlit.app](https://seu-app.streamlit.app)

## 💻 Requisitos

- Python 3.8+
- Conta no Google Cloud Platform com acesso à API do Gemini
- Streamlit Account (para deploy)

## 🛠️ Instalação Local

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
- Crie um arquivo `.env` na raiz do projeto
- Adicione sua API key do Google:
```
GOOGLE_API_KEY=sua_api_key_aqui
```

5. Execute a aplicação
```bash
streamlit run app.py
```

## 🌐 Deploy no Streamlit Cloud

1. Faça um fork deste repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Faça login com sua conta GitHub
4. Clique em "New app"
5. Selecione o repositório
6. Configure as variáveis de ambiente secretas (GOOGLE_API_KEY)
7. Deploy!

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
