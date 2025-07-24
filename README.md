---

# NoditAIBot

[![YouTube 1st Wave](https://img.shields.io/badge/YouTube-1st_Wave-red)](https://youtu.be/V4XEvYiv0p8)
[![YouTube 2nd Wave](https://img.shields.io/badge/YouTube-2nd_Wave-red)](https://youtu.be/zqO7iRJ_oEs)
[![YouTube 3rd Wave](https://img.shields.io/badge/YouTube-3rd_Wave-red)](https://youtu.be/EjowAu2FakM)
[![YouTube MCP Demo](https://img.shields.io/badge/YouTube-MCP_Demo-green)](https://youtu.be/Fj4NvrJSnEU)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue)](https://t.me/test_ttest_bbot_bot)
[![Contact on X](https://img.shields.io/badge/X-Contact-informational)](https://x.com/BTCtensai)


---

## Introduction

**NoditAIBot** is a next-generation Telegram AI bot for the Web3 world.
It combines AI-powered chat, real-time blockchain data queries, and an advanced alert subscription system—making on-chain life easier than ever.

* Get live wallet/token/NFT/gas data from multiple chains
* Query blockchain insights through an intelligent AI layer (via Dify)
* Use buttons or natural language in Telegram chat
* Watch short video guides to get started instantly

Whether you’re a trader, developer, or just getting started with crypto, NoditAIBot is your all-in-one assistant for on-chain monitoring and interaction.

---

## 🔄 Latest Wave Update

**Final Wave: Full MCP + Multi-Chain Intelligence**  
🎥 [Watch the update demo here](https://youtu.be/Fj4NvrJSnEU)

🧠 We’ve upgraded the AI layer with Dify AI + Function Calling support. The new `/mcp` command enables the bot to understand your natural questions and fetch answers directly from the blockchain.

### Now, our Nodit agent can:
- ✅ Retrieve knowledge from the **Nodit website**
- ✅ Access the full **NoditAIBot codebase** (via embedded docs)
- ✅ **Query blockchain data via MCP**, automatically calling the right API
- ✅ Recommend bot commands automatically if your question matches one

---

## All Commands & Usage

All commands and formats are also shown in `/help` in the bot.
Key features:

### `/start`

Sends a **quick-start video guide** and shows easy copy-paste commands for beginners.
<img width="476" height="210" alt="image" src="https://github.com/user-attachments/assets/b0e7f281-6d60-4007-837f-e0849a96493e" />

### `/help`

Displays all features and how to use them, now with quick buttons for each command.
<img width="495" height="361" alt="image" src="https://github.com/user-attachments/assets/9a6eb176-07fb-4ee3-9981-f30baab57848" />



### `/balance`

Query native token balance for any address.

```
/balance <chain> <address>
Example: /balance ethereum 0x1234...
```

### `/tokens`

Query your top contract token balances (sorted by balance).

```
/tokens <chain> <address>
Example: /tokens polygon 0x1234...
```

### `/alert`

Create/manage/delete on-chain transaction alerts.

```
/alert add <chain> <address>       - Add a new alert
/alert list                        - List all active alerts
/alert del <chain> <address>       - Delete by chain+address
/alert del <subscription_id>       - Delete by subscriptionId
/alert del all                     - Delete all your alerts
```

### `/mcp` (**AI chat**, MCP-driven)

Start a conversation with the bot, and it will:
- Check if your question matches known bot functions (like `/balance`)
- Help you form the correct command, or
- Use MCP tools to retrieve data from-chain via `list → get → call`

```
/mcp
/mcp <your question>
```


### `/daily`

Query daily active accounts and transactions stats for the past ten days.

```
/daily <chain> [contract_address]
Example: /daily ethereum 0x1234...
```
Use this to get on-chain daily usage stats for a specific contract (like USDT) and total transactions.



### `/nft`

Query the top 5 NFTs owned by an address.

```
/nft <chain> <address>
Example: /nft ethereum 0xabc...
```

### `/gas`

Get gas prices for any supported chain, or use `min` to find the cheapest chain:

```
/gas <chain>
Example: /gas optimism

/gas min
→ Shows the chain with lowest average gas right now
```



---

## Quick Links

* **Telegram Bot:** [@test\_ttest\_bbot\_bot](https://t.me/test_ttest_bbot_bot) *(subject to change in official release)*
* **Contact on X:** [BTCtensai](https://x.com/BTCtensai)

---

## Get Involved

Try NoditAIBot, share feedback, and follow our journey on social media.
Pull requests, issues, and feature suggestions are always welcome!

---
