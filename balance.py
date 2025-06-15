import asyncio
import requests
from config import NODIT_API_KEY

async def query_polygon_balance(address, update):
    await update.message.reply_text("Querying Polygon balance, please wait...")
    url = "https://web3.nodit.io/v1/polygon/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            resp_json = resp.json()
            wei_balance = int(resp_json.get("balance", "0"))
            pol_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"POL Balance for {address} on Polygon: {pol_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_arbitrum_balance(address, update):
    await update.message.reply_text("Querying Arbitrum balance, please wait...")
    url = "https://web3.nodit.io/v1/arbitrum/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            wei_balance = int(resp.json().get("balance", "0"))
            eth_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"ETH Balance for {address} on Arbitrum: {eth_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_base_balance(address, update):
    await update.message.reply_text("Querying Base balance, please wait...")
    url = "https://web3.nodit.io/v1/base/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            wei_balance = int(resp.json().get("balance", "0"))
            eth_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"ETH Balance for {address} on Base: {eth_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_bitcoin_balance(address, update):
    await update.message.reply_text("Querying Bitcoin balance, please wait...")
    url = "https://web3.nodit.io/v1/bitcoin/mainnet/account/getBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            satoshi_balance = int(resp.json().get("balance", "0"))
            btc_balance = satoshi_balance / 1e8
            await update.message.reply_text(
                f"BTC Balance for {address}: {btc_balance:.8f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_dogecoin_balance(address, update):
    await update.message.reply_text("Querying Dogecoin balance, please wait...")
    url = "https://web3.nodit.io/v1/dogecoin/mainnet/account/getBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            satoshi_balance = int(resp.json().get("balance", "0"))
            doge_balance = satoshi_balance / 1e8
            await update.message.reply_text(
                f"DOGE Balance for {address}: {doge_balance:.8f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_ethereum_balance(address, update):
    await update.message.reply_text("Querying Ethereum balance, please wait...")
    url = "https://web3.nodit.io/v1/ethereum/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            wei_balance = int(resp.json().get("balance", "0"))
            eth_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"ETH Balance for {address}: {eth_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_kaia_balance(address, update):
    await update.message.reply_text("Querying Kaia balance, please wait...")
    url = "https://web3.nodit.io/v1/kaia/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            wei_balance = int(resp.json().get("balance", "0"))
            kaia_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"KAIA Balance for {address}: {kaia_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")


async def query_optimism_balance(address, update):
    await update.message.reply_text("Querying Optimism balance, please wait...")
    url = "https://web3.nodit.io/v1/optimism/mainnet/native/getNativeBalanceByAccount"
    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {"accountAddress": address}
    loop = asyncio.get_running_loop()
    try:
        resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=headers, json=data))
        if resp.status_code == 200:
            wei_balance = int(resp.json().get("balance", "0"))
            eth_balance = wei_balance / 1e18
            await update.message.reply_text(
                f"ETH Balance for {address} on Optimism: {eth_balance:.6f}"
            )
        else:
            await update.message.reply_text(f"Failed to get balance, status: {resp.status_code}\nRaw response: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"Error fetching balance: {str(e)}")