import asyncio
import requests
from config import NODIT_API_KEY
from support import GAS_SUPPORTED_CHAINS

async def query_gas_price(chain: str, update):
    """Query gas price for a given chain."""
    await update.message.reply_text(f"Querying gas price on {chain.capitalize()}, please wait...")
    url = f"https://web3.nodit.io/v1/{chain}/mainnet/blockchain/getGasPrice"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }

    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json={}))
        if resp.status_code == 200:
            data = resp.json()
            high = int(data.get("high", 0)) / 1e9
            avg = int(data.get("average", 0)) / 1e9
            low = int(data.get("low", 0)) / 1e9
            base = int(data.get("baseFee", 0)) / 1e9
            block = data.get("latestBlock", "N/A")
            msg = (
                f"⛽ Gas Price on {chain.capitalize()} (Block {block}):\n"
                f"- High: {high:.6f} Gwei\n"
                f"- Average: {avg:.6f} Gwei\n"
                f"- Low: {low:.6f} Gwei\n"
                f"- Base Fee: {base:.6f} Gwei"
            )
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text(f"Failed to get gas data, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching gas data: {str(e)}")

async def query_min_gas(update):
    """Query all supported chains and return the one with the lowest average gas price."""
    await update.message.reply_text("Querying all supported chains for the lowest gas price, please wait...")
    url_template = "https://web3.nodit.io/v1/{chain}/mainnet/blockchain/getGasPrice"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    loop = asyncio.get_running_loop()
    results = []
    for chain in GAS_SUPPORTED_CHAINS:
        try:
            resp = await loop.run_in_executor(None, lambda: requests.post(url_template.format(chain=chain), headers=headers, json={}))
            if resp.status_code == 200:
                data = resp.json()
                avg = int(data.get("average", 0)) / 1e9
                results.append((chain, avg))
        except Exception:
            continue
    if not results:
        await update.message.reply_text("Failed to fetch gas prices for all chains.")
        return
    # Find the chain with the minimum average gas price
    min_chain, min_price = min(results, key=lambda x: x[1])
    msg = f"The chain with the lowest average gas price is {min_chain.capitalize()}: {min_price:.6f} Gwei"
    await update.message.reply_text(msg)

# Command handler for /gas
async def handle_gas(update, context):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text(
            f"Usage: /gas <chain>|min\nSupported chains: {', '.join(GAS_SUPPORTED_CHAINS)} or 'min' for the cheapest."
        )
        return
    chain = args[0].lower()
    if chain == "min":
        await query_min_gas(update)
        return
    if chain not in GAS_SUPPORTED_CHAINS:
        await update.message.reply_text(
            f"Gas query not supported for chain: {chain}\nSupported chains: {', '.join(GAS_SUPPORTED_CHAINS)}"
        )
        return
    await query_gas_price(chain, update)
