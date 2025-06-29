import json
import aiohttp
from telegram import Update
from telegram.ext import ContextTypes
from config import DIFY_API_KEY, DIFY_APP_ID

API_URL = "https://api.dify.ai/v1/chat-messages"

async def handle_mcp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mcp command for AI conversation via Dify (fully async with aiohttp)"""
    question = update.message.text.replace("/mcp", "").strip()
    if not question:
        await update.message.reply_text(
            "Hello! I'm NoditAIBot. You can ask me anything about how to use this bot's commands and about Nodit's features or API.\n"
            "For example:\n"
            "- /mcp How do I use the /balance command?\n"
            "- /mcp How can I set up /alert?\n"
            "- /mcp How to use Nodit webhook?"
        )
        return

    payload = {
        "inputs": {},
        "query": question,
        "response_mode": "blocking",
        "user": str(update.effective_user.id),
        "app_id": DIFY_APP_ID
    }
    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(API_URL, json=payload, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    answer = data.get("answer")
                    if answer:
                        await update.message.reply_text(answer)
                    else:
                        await update.message.reply_text("No answer found in response.")
                else:
                    text = await response.text()
                    await update.message.reply_text(f"Request failed: {response.status}\n{text}")
    except Exception as e:
        await update.message.reply_text(f"Error communicating with AI: {str(e)}")
