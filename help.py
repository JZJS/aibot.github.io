from telegram import Update
from telegram.ext import ContextTypes
from support import (
    BALANCE_SUPPORTED_CHAINS,
    TOKEN_SUPPORTED_CHAINS,
    ALERT_SUPPORTED_CHAINS,
    TXS_SUPPORTED_CHAINS,
    ADDRESS_FORMAT_DESCRIPTIONS
)

# Available commands and their descriptions
COMMANDS = {
    "balance": "Check native token balance on supported blockchains",
    "tokens": "Check top 10 contract tokens (ERC20, etc.) on supported blockchains",
    "mcp": "Start AI conversation for blockchain and wallet assistance",
    "help": "Show this help message",
    "alert": "Register and manage blockchain alerts (Coming Soon)",
    "txs": "Query transaction history (Coming Soon)"
}

# Detailed usage examples for each command
USAGE_EXAMPLES = {
    "balance": "/balance <chain> <address>\nExample: /balance ethereum 0x1234...",
    "tokens": "/tokens <chain> <address>\nExample: /tokens polygon 0x1234...",
    "mcp": "/mcp <your question>\nExample: /mcp what is a wallet?",
    "alert": "/alert <action> <parameters>\n(Coming Soon)",
    "txs": "/txs <chain> <address>\n(Coming Soon)"
}

# Supported chains for each command
SUPPORTED_CHAINS = {
    "balance": BALANCE_SUPPORTED_CHAINS,
    "tokens": TOKEN_SUPPORTED_CHAINS,
    "alert": ALERT_SUPPORTED_CHAINS,
    "txs": TXS_SUPPORTED_CHAINS
}

async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command and show available commands with usage instructions"""
    help_text = "🤖 *Nodit Bot Help Guide*\n\n"
    
    # Add available commands section
    help_text += "*Available Commands:*\n"
    for cmd, desc in COMMANDS.items():
        help_text += f"• /{cmd} - {desc}\n"
    help_text += "\n"
    
    # Add detailed usage section
    help_text += "*Detailed Usage:*\n"
    for cmd, usage in USAGE_EXAMPLES.items():
        help_text += f"_{cmd.title()}_\n{usage}\n\n"
    
    # Add supported chains section
    help_text += "*Supported Chains:*\n"
    for cmd, chains in SUPPORTED_CHAINS.items():
        if cmd in ["balance", "tokens"]:  # Only show for implemented commands
            help_text += f"_{cmd.title()}_: {', '.join(chains)}\n"
    
    # Add address format information
    help_text += "\n*Address Formats:*\n"
    help_text += "• EVM chains (ETH, MATIC, etc.): 0x followed by 40 hex characters\n"
    help_text += "• Bitcoin: 25-34 characters starting with 1 or 3, or bc1...\n"
    help_text += "• Dogecoin: 25-34 characters starting with D, A, or 9\n"
    
    # Add development notice
    help_text += "\n*Coming Soon:*\n"
    help_text += "• /alert - Register and manage blockchain alerts\n"
    help_text += "• /txs - Query transaction history\n"
    
    # Add footer
    help_text += "\n_Use /help anytime to see this guide_"

    await update.message.reply_text(help_text, parse_mode='Markdown')

def get_command_help(command: str) -> str:
    """Get detailed help for a specific command"""
    if command not in COMMANDS:
        return f"Unknown command: {command}"
    
    help_text = f"*{command.title()} Command Help*\n\n"
    help_text += f"_{COMMANDS[command]}_\n\n"
    help_text += f"*Usage:*\n{USAGE_EXAMPLES[command]}\n\n"
    
    if command in SUPPORTED_CHAINS:
        help_text += f"*Supported Chains:*\n{', '.join(SUPPORTED_CHAINS[command])}\n"
    
    return help_text
