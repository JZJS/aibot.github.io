import requests
import asyncio
from datetime import datetime, timedelta
from config import NODIT_API_KEY
from support import DAILY_SUPPORTED_CHAINS

async def query_daily_stats(update, context):
    """Query daily active accounts and transactions stats for ethereum + contract"""
    args = context.args
    if not args or args[0].lower() not in DAILY_SUPPORTED_CHAINS:
        await update.message.reply_text(
            "Usage: /daily ethereum <contract_address>"
        )
        return

    chain = args[0].lower()
    contract_address = args[1] if len(args) > 1 else None

    if not contract_address:
        await update.message.reply_text("Please provide a contract address for active accounts stats.")
        return

    today = datetime.utcnow().strftime("%Y-%m-%d")
    ten_days_ago = (datetime.utcnow() - timedelta(days=10)).strftime("%Y-%m-%d")

    headers = {
        "X-API-KEY": NODIT_API_KEY,
        "accept": "application/json",
        "content-type": "application/json"
    }

    base_url = f"https://web3.nodit.io/v1/{chain}/mainnet/stats"
    accounts_url = f"{base_url}/getDailyActiveAccountsStatsByContract"
    transactions_url = f"{base_url}/getDailyTransactionsStats"

    accounts_data = {
        "contractAddress": contract_address,
        "startDate": ten_days_ago,
        "endDate": today
    }

    transactions_data = {
        "startDate": ten_days_ago,
        "endDate": today
    }

    loop = asyncio.get_running_loop()

    try:
        accounts_resp = await loop.run_in_executor(None, lambda: requests.post(accounts_url, headers=headers, json=accounts_data))
        transactions_resp = await loop.run_in_executor(None, lambda: requests.post(transactions_url, headers=headers, json=transactions_data))

        reply = f"📅 Daily Stats ({ten_days_ago} → {today}) on {chain}:\n"

        if accounts_resp.status_code == 200:
            items = accounts_resp.json().get("items", [])
            if items:
                for item in items:
                    reply += f"• Active Accounts {item['date']}: {item['count']}\n"
            else:
                reply += "• No Active Accounts data found.\n"
        else:
            reply += f"• Active Accounts request failed (Status {accounts_resp.status_code})\n"

        # Add a single blank line between sections
        reply += "\n"

        if transactions_resp.status_code == 200:
            items = transactions_resp.json().get("items", [])
            if items:
                for item in items:
                    reply += f"• Transactions {item['date']}: {item['count']}\n"
            else:
                reply += "• No Transactions data found.\n"
        else:
            reply += f"• Transactions request failed (Status {transactions_resp.status_code})\n"

        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")
