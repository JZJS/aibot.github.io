from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command: send welcome video and suggested commands"""

    # Send welcome video (local path)
    try:
        await update.message.reply_video(
            video="https://c756a2e3.noditaibot-video.pages.dev/NoditAIBot.mp4",
            caption="🎬 Welcome to Nodit AIBot! Here's a quick preview of what I can do."
        )
    except Exception as e:
        await update.message.reply_text("Welcome to Nodit AIBot! (Video unavailable)")

    # Send message with copyable commands
    command_text = (
        "⚡ Try these commands right now by copying and pasting them:\n\n"
        "`/balance polygon YOUR_WALLET_ADDRESS`\n"
        "`/tokens base YOUR_WALLET_ADDRESS`\n"
        "`/alert add ethereum YOUR_WALLET_ADDRESS`\n"
        "`/alert list`\n"
        "`/help`\n\n"
        "🧠 `/mcp` - AI Assistant (coming soon)"
    )
    await update.message.reply_text(command_text, parse_mode='Markdown')

    await update.message.reply_text("👇 Tap a button to begin:", reply_markup=reply_markup)
