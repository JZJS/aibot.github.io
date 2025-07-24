from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from support import (
    BALANCE_SUPPORTED_CHAINS,
    TOKEN_SUPPORTED_CHAINS,
    ALERT_SUPPORTED_CHAINS,
    DAILY_SUPPORTED_CHAINS,
    NFT_SUPPORTED_CHAINS,
    GAS_SUPPORTED_CHAINS
)

HELP_DETAILS = {
    "balance": {
        "title": "Balance Command",
        "desc": "Query native token balance for a given address.",
        "usage": "/balance <chain> <address>\nExample: /balance ethereum 0x1234...",
        "chains": BALANCE_SUPPORTED_CHAINS
    },
    "tokens": {
        "title": "Tokens Command",
        "desc": "Query top 10 contract token balances for a given address.",
        "usage": "/tokens <chain> <address>\nExample: /tokens polygon 0x1234...",
        "chains": TOKEN_SUPPORTED_CHAINS
    },
    "alert": {
        "title": "Alert Command",
        "desc": "Create and manage transaction alerts for addresses.",
        "usage": (
            "/alert add [<chain>] [<address>] - Add an alert\n"
            "/alert list - List all alerts\n"
            "/alert del [<chain>] [<address>] - Delete alert by chain and address\n"
            "/alert del [<subscription_id>] - Delete alert by subscription ID\n"
            "/alert del all - Delete all alerts"
        ),
        "chains": ALERT_SUPPORTED_CHAINS
    },
    "daily": {
        "title": "Daily Command",
        "desc": "Query ten days ago to today's active accounts and transactions stats for a contract.",
        "usage": "/daily <chain> [contract_address]\nExample: /daily ethereum 0x1234...",
        "chains": DAILY_SUPPORTED_CHAINS
    },
    "nft": {
        "title": "NFT Command",
        "desc": "Query top 5 NFTs for a given address on a supported chain.",
        "usage": "/nft <chain> <address>\nExample: /nft ethereum 0x1234...",
        "chains": NFT_SUPPORTED_CHAINS
    },
    "gas": {
        "title": "Gas Command",
        "desc": "Query gas price for a given chain, or use 'min' to find the chain with the lowest gas price.",
        "usage": "/gas <chain>\n/gas min\nExample: /gas optimism or /gas min",
        "chains": GAS_SUPPORTED_CHAINS
    },

    "mcp": {
        "title": "MCP Command (AI Chat) ",
        "desc": "Start an AI conversation for blockchain and wallet questions.",
        "usage": (
            "/mcp - Start a conversation\n"
            "/mcp <your question> - Ask a question"
        ),
        "chains": None
    }
}

def get_command_help(command: str) -> str:
    detail = HELP_DETAILS[command]
    msg = f"*{detail['title']}*\n\n{detail['desc']}\n\n*Usage:*\n{detail['usage']}"
    if detail['chains']:
        msg += f"\n\n*Supported chains:*\n{', '.join(detail['chains'])}"
    return msg

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command. Show main menu with callback buttons or detailed usage for a command."""
    if not context.args:
        keyboard = [
            [InlineKeyboardButton("🪙 balance", callback_data="help_balance")],
            [InlineKeyboardButton("📊 tokens", callback_data="help_tokens")],
            [InlineKeyboardButton("🖼️ nft", callback_data="help_nft")],
            [InlineKeyboardButton("🔔 alert", callback_data="help_alert")],
            [InlineKeyboardButton("📅 daily", callback_data="help_daily")],
            [InlineKeyboardButton("⛽ gas", callback_data="help_gas")],
            [InlineKeyboardButton("🤖 mcp", callback_data="help_mcp")],
        ]
        await update.message.reply_text(
            "This bot supports multiple blockchain functions.\n"
            "To learn how to use each feature, please click a button below:",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return
    
    cmd = context.args[0].lower()
    if cmd not in HELP_DETAILS:
        await update.message.reply_text(
            f"Unknown command: {cmd}. Supported: balance, tokens, nft, alert, daily, gas, mcp."
        )
        return
    msg = get_command_help(cmd)
    await update.message.reply_text(msg, parse_mode='Markdown')

async def help_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    command = query.data.replace("help_", "")
    if command not in HELP_DETAILS:
        await query.edit_message_text("Unknown command.")
        return
    msg = get_command_help(command)
    await query.edit_message_text(msg, parse_mode='Markdown')
