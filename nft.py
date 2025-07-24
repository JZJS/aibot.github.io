import asyncio
import requests
from config import NODIT_API_KEY
from support import NFT_SUPPORTED_CHAINS

async def query_nft_tokens(chain: str, address: str, update):
    """Query NFTs for supported chains"""
    await update.message.reply_text(f"Querying NFTs on {chain.capitalize()}, please wait...")
    url = f"https://web3.nodit.io/v1/{chain}/mainnet/nft/getNftsOwnedByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "accountAddress": address,
        "withCount": False,
        "withMetadata": False
    }
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            result = resp.json()
            items = result.get("items", [])
            if not items:
                await update.message.reply_text(f"No NFTs found for {address} on {chain.capitalize()}.")
                return
            reply_lines = [f"NFTs owned by {address} on {chain.capitalize()} (Top 5):"]
            for item in items[:5]:
                contract_name = item.get("contract", {}).get("name", "Unknown")
                token_id = item.get("tokenId", "N/A")
                reply_lines.append(f"- {contract_name} #{token_id}")
            await update.message.reply_text("\n".join(reply_lines))
        else:
            await update.message.reply_text(f"Failed to get NFTs, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching NFTs: {str(e)}")

# Command handler for /nft
async def handle_nft(update, context):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text(
            f"Usage: /nft <chain> <address>\nSupported chains: {', '.join(NFT_SUPPORTED_CHAINS)}"
        )
        return
    chain = args[0].lower()
    address = args[1]
    if chain not in NFT_SUPPORTED_CHAINS:
        await update.message.reply_text(
            f"NFT queries not supported for chain: {chain}\nSupported chains: {', '.join(NFT_SUPPORTED_CHAINS)}"
        )
        return
    await query_nft_tokens(chain, address, update)
