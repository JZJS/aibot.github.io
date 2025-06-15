import requests
import json
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from balance import (
    query_polygon_balance,
    query_arbitrum_balance,
    query_base_balance,
    query_bitcoin_balance,
    query_dogecoin_balance,
    query_ethereum_balance,
    query_kaia_balance,
    query_optimism_balance
)
from tokens import (
    query_polygon_tokens,
    query_ethereum_tokens,
    query_arbitrum_tokens,
    query_base_tokens,
    query_optimism_tokens,
    query_kaia_tokens,
    query_aptos_tokens
)
from config import TELEGRAM_TOKEN
from mcp import handle_mcp
from help import handle_help
from support import (
    BALANCE_SUPPORTED_CHAINS,
    TOKEN_SUPPORTED_CHAINS,
    ADDRESS_FORMATS,
    ADDRESS_FORMAT_DESCRIPTIONS
)

import logging
logging.basicConfig(level=logging.ERROR)

# Chain name to function mapping for balance queries
CHAIN_BALANCE_FN = {
    "arbitrum": query_arbitrum_balance,
    "base": query_base_balance,
    "bitcoin": query_bitcoin_balance,
    "doge": query_dogecoin_balance,
    "ethereum": query_ethereum_balance,
    "kaia": query_kaia_balance,
    "optimism": query_optimism_balance,
    "polygon": query_polygon_balance
}

# Chain name to function mapping for token queries
CHAIN_TOKENS_FN = {
    "aptos": query_aptos_tokens,
    "arbitrum": query_arbitrum_tokens,
    "base": query_base_tokens,
    "ethereum": query_ethereum_tokens,
    "kaia": query_kaia_tokens,
    "optimism": query_optimism_tokens,
    "polygon": query_polygon_tokens
}

def validate_address(chain: str, address: str) -> tuple[bool, str]:
    """Validate address format"""
    if chain not in ADDRESS_FORMATS:
        return False, f"Unsupported chain: {chain}"
    
    pattern = ADDRESS_FORMATS[chain]
    if not re.match(pattern, address):
        return False, f"Invalid {chain} address format. Expected format: {ADDRESS_FORMAT_DESCRIPTIONS[chain]}"
    
    return True, ""

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /balance command"""
    await update.message.reply_text("进入到 handle_balance 了，正在解析命令...")

    text = update.message.text.strip()
    balance_match = re.match(r"^/balance\s+(\w+)\s+(\S+)$", text)
    if not balance_match:
        await update.message.reply_text(
            "Please use the correct format: /balance <chain> <address>\n"
            "Example: /balance ethereum 0x1234..."
        )
        return

    chain = balance_match.group(1).lower()
    address = balance_match.group(2)
    
    # Validate chain support
    if chain not in CHAIN_BALANCE_FN:
        supported_chains = ", ".join(BALANCE_SUPPORTED_CHAINS)
        await update.message.reply_text(
            f"Unsupported chain: {chain}\n"
            f"Supported chains are: {supported_chains}"
        )
        return
        
    # Validate address format
    is_valid, message = validate_address(chain, address)
    if not is_valid:
        await update.message.reply_text(message)
        return
        
    # Execute balance query
    await CHAIN_BALANCE_FN[chain](address, update)

async def handle_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tokens command"""
    await update.message.reply_text("进入到 handle_tokens 了，正在解析命令...")
    text = update.message.text.strip()
    tokens_match = re.match(r"^/tokens\s+(\w+)\s+(\S+)$", text)
    if not tokens_match:
        await update.message.reply_text(
            "Please use the correct format: /tokens <chain> <address>\n"
            "Example: /tokens ethereum 0x1234..."
        )
        return

    chain = tokens_match.group(1).lower()
    address = tokens_match.group(2)
    
    # Validate chain support
    if chain not in CHAIN_TOKENS_FN:
        supported_chains = ", ".join(TOKEN_SUPPORTED_CHAINS)
        await update.message.reply_text(
            f"Token queries not supported for chain: {chain}\n"
            f"Supported chains for token queries are: {supported_chains}"
        )
        return
        
    # Validate address format
    is_valid, message = validate_address(chain, address)
    if not is_valid:
        await update.message.reply_text(message)
        return
        
    # Execute token query
    await CHAIN_TOKENS_FN[chain](address, update)

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands"""
    await update.message.reply_text(
        "Sorry, I don't recognize this command.\n"
        "You can:\n"
        "- Use /balance to check native token balances\n"
        "- Use /tokens to check token balances\n"
        "- Use /mcp to chat with me and learn more features"
    )

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler("balance", handle_balance))
    app.add_handler(CommandHandler("tokens", handle_tokens))
    app.add_handler(CommandHandler("mcp", handle_mcp))
    app.add_handler(CommandHandler("help", handle_help))
    
    # Handle unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, handle_unknown))
    
    # Start the bot
    app.run_polling()
