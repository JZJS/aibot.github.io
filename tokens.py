import requests
import asyncio
from config import NODIT_API_KEY

# EVM compatible chains token query
async def query_evm_tokens(chain: str, address: str, update):
    """Query tokens for EVM compatible chains"""
    await update.message.reply_text(f"Querying {chain.capitalize()} tokens, please wait...")
    url = f"https://web3.nodit.io/v1/{chain}/mainnet/token/getTokensOwnedByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "accountAddress": address,
        "withCount": False
    }
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            result = resp.json()
            tokens = result.get("items", [])
            if not tokens:
                await update.message.reply_text(f"No tokens found for {address} on {chain.capitalize()}.")
                return

            # Helper function to calculate real balance for sorting
            def get_real_balance(token):
                decimals = token.get("contract", {}).get("decimals", 18)
                try:
                    return int(token.get("balance", 0)) / (10 ** int(decimals))
                except Exception:
                    return 0

            # Sort tokens by balance in descending order and take top 10
            sorted_tokens = sorted(tokens, key=get_real_balance, reverse=True)[:10]

            # Build response lines
            reply_lines = []
            for t in sorted_tokens:
                contract = t.get("contract", {})
                name = contract.get("name", "N/A")
                symbol = contract.get("symbol", "N/A")
                decimals = contract.get("decimals", 18)
                try:
                    real_balance = int(t.get("balance", 0)) / (10 ** int(decimals))
                    balance_str = f"{real_balance:.6f}"
                except Exception:
                    balance_str = t.get("balance", "0")
                reply_lines.append(f"{name} ({symbol}): {balance_str}")

            reply_text = f"Tokens for {address} on {chain.capitalize()} (sorted by balance):\n" + "\n".join(reply_lines)
            await update.message.reply_text(reply_text)
        else:
            await update.message.reply_text(f"Failed to get tokens, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching tokens: {str(e)}")

# Individual chain functions
async def query_polygon_tokens(address, update):
    await query_evm_tokens("polygon", address, update)

async def query_ethereum_tokens(address, update):
    await query_evm_tokens("ethereum", address, update)

async def query_arbitrum_tokens(address, update):
    await query_evm_tokens("arbitrum", address, update)

async def query_base_tokens(address, update):
    await query_evm_tokens("base", address, update)

async def query_optimism_tokens(address, update):
    await query_evm_tokens("optimism", address, update)

async def query_kaia_tokens(address, update):
    await query_evm_tokens("kaia", address, update)

# Aptos token query (includes native token)
async def query_aptos_tokens(address, update):
    """Query all tokens including native token for Aptos"""
    await update.message.reply_text("Querying Aptos tokens, please wait...")
    url = "https://web3.nodit.io/v1/aptos/mainnet/graphql"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    
    # GraphQL query
    query = """
    query GetAccountBalances($address: String!) {
        current_fungible_asset_balances(
            where: {
                owner_address: {
                    _eq: $address
                }
            }
        ) {
            amount
            metadata {
                name
                symbol
                decimals
            }
        }
    }
    """
    
    variables = {
        "address": address
    }
    
    data = {
        "query": query,
        "variables": variables
    }
    
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            resp_json = resp.json()
            balances = resp_json.get("data", {}).get("current_fungible_asset_balances", [])
            
            if not balances:
                await update.message.reply_text(f"No tokens found for address {address}")
                return
                
            # Build balance information
            balance_info = []
            for balance in balances:
                amount = int(balance.get("amount", "0"))
                metadata = balance.get("metadata", {})
                symbol = metadata.get("symbol", "Unknown")
                decimals = metadata.get("decimals", 8)
                name = metadata.get("name", "Unknown Token")
                
                # Calculate actual balance
                actual_balance = amount / (10 ** decimals)
                if actual_balance > 0:  # Only show non-zero balances
                    balance_info.append(f"{name} ({symbol}): {actual_balance:.{decimals}f}")
            
            if balance_info:
                message = f"Tokens for {address} on Aptos:\n" + "\n".join(balance_info)
                await update.message.reply_text(message)
            else:
                await update.message.reply_text(f"No non-zero balances found for address {address}")
        else:
            await update.message.reply_text(f"Failed to get tokens, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching tokens: {str(e)}")

# Bitcoin and Dogecoin don't have token support, so we don't need to implement token query functions for them
