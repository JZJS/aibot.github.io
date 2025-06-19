import requests
import json
import re
from telegram import Update
from telegram.ext import ContextTypes
from config import OLLAMA_API
from support import (
    BALANCE_SUPPORTED_CHAINS,
    TOKEN_SUPPORTED_CHAINS,
    ADDRESS_FORMAT_DESCRIPTIONS
)

async def handle_mcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mcp command for AI conversation"""
    question = update.message.text.replace("/mcp", "").strip()
    if not question:
        await update.message.reply_text(
            "Hello! I'm NoditAI Assistant. You can ask me about blockchain, wallets, or Nodit features.\n"
            "For example:\n"
            "- What is a wallet?\n"
            "- Which chains does Nodit support?\n"
            "- How do I check token balances?"
        )
        return

    # Get conversation history (if any)
    context_str = ""
    if context.user_data.get("mcp_history"):
        context_str = "\n".join(context.user_data["mcp_history"][-5:])  # Keep only last 5 conversations

    # Call AI assistant
    ai_reply = ai_ask(question, context_str)
    
    # Update conversation history
    if "mcp_history" not in context.user_data:
        context.user_data["mcp_history"] = []
    context.user_data["mcp_history"].append(f"User: {question}\nAI: {ai_reply}")
    
    await update.message.reply_text(ai_reply)

def ai_ask(question, context=""):
    """Core AI conversation functionality"""
    # Build address format guide
    address_format_guide = "\n".join([f"- {chain}: {desc}" for chain, desc in ADDRESS_FORMAT_DESCRIPTIONS.items()])
    
    prompt = (
        "You are NoditAIbot, an expert assistant for the Nodit blockchain API platform. Your job is to help users understand and use this Telegram bot. "
        "You should:\n"
        f"1. Briefly introduce what Nodit is: a multi-chain blockchain data platform. It supports major chains such as {', '.join(BALANCE_SUPPORTED_CHAINS)}.\n"
        "2. Explain what this bot can do:\n"
        "   - Check native token balances on supported blockchains using /balance <chain> <address>\n"
        "   - Check non-native tokens (ERC20, etc.) using /tokens <chain> <address>\n"
        "   - Monitor large transactions and perform transfers (where supported)\n"
        "   You can also answer basic questions about blockchain, wallets, and Nodit features.\n"
        "3. Tell users the main usage:\n"
        "   - For native token balance: /balance <chain> <address> (e.g., /balance polygon 0x1234...)\n"
        "   - For non-native tokens: /tokens <chain> <address> (e.g., /tokens ethereum 0x1234...)\n"
        f"   Token queries are supported on: {', '.join(TOKEN_SUPPORTED_CHAINS)}\n"
        "4. Explain address formats for different chains:\n"
        f"{address_format_guide}\n"
        "5. If the user is unsure or asks for help, show a friendly, short guide: 'You can check native token balances with /balance, or view your non-native tokens with /tokens. Try: /balance ethereum 0xabc... or /tokens polygon 0xabc...'\n"
        "6. If the user asks a basic blockchain or Nodit question (like what is a wallet, what is Nodit, which chains are supported), give a concise, plain English answer.\n"
        "7. Always keep your answers concise (under 60 words), friendly, and clear. Never output code, JSON, or any system/internal explanations. Never use <think> tags or mention system processes.\n"
        f"Current conversation:\n{context}\nUser: {question}\nAI:"
    )

    payload = {
        "model": "deepseek-r1:1.5b",
        "prompt": prompt
    }
    response = requests.post(OLLAMA_API, json=payload, stream=True)
    ai_reply = ""
    for line in response.iter_lines():
        if line:
            obj = json.loads(line.decode('utf-8'))
            if "response" in obj:
                ai_reply += obj["response"]
    ai_reply = re.sub(r"<think>.*?</think>", "", ai_reply, flags=re.DOTALL)
    return ai_reply.strip()
