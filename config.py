import os
OLLAMA_API = "https://ai.web3luck.com/api/generate"
#OLLAMA_API = "http://localhost:11434/api/generate"  # Your local Ollama LLM API address

# Environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
NODIT_API_KEY = os.environ.get("NODIT_API_KEY")
DIFY_API_KEY = os.environ.get("DIFY_API_KEY")
DIFY_APP_ID = os.environ.get("DIFY_APP_ID")
