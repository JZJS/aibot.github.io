import json
import os
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional
from config import NODIT_API_KEY
from support import ALERT_SUPPORTED_CHAINS, ALERT_WEBHOOK_ENDPOINTS

# File to store alert configurations
ALERT_CONFIG_FILE = "alert_config.json"

class AlertManager:
    def __init__(self):
        self.alerts: Dict[str, List[Dict]] = {}  # {chain: [{user_id, address, webhook_id}]}
        self.load_alerts()
        
    def load_alerts(self):
        """Load alert configurations from file"""
        if os.path.exists(ALERT_CONFIG_FILE):
            try:
                with open(ALERT_CONFIG_FILE, 'r') as f:
                    self.alerts = json.load(f)
            except Exception as e:
                print(f"Error loading alerts: {e}")
                self.alerts = {}
    
    def save_alerts(self):
        """Save alert configurations to file"""
        try:
            with open(ALERT_CONFIG_FILE, 'w') as f:
                json.dump(self.alerts, f, indent=4)
        except Exception as e:
            print(f"Error saving alerts: {e}")

    async def create_webhook(self, chain: str, address: str, description: str, chat_id: str) -> Optional[str]:
        """Create a webhook for transaction monitoring"""
        if chain not in ALERT_SUPPORTED_CHAINS:
            return None
            
        # Construct webhook URL for the specific chain
        url = f"https://web3.nodit.io/v1/{chain}/mainnet/webhooks"
        headers = {
            "X-API-KEY": NODIT_API_KEY,
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        # Create webhook for successful transactions with correct structure
        webhook_data = {
            "eventType": "SUCCESSFUL_TRANSACTION",
            "description": f"{description} - Transaction Alert",
            "notification": {
                "webhookUrl": f"https://nodit-webhook.yuxialun123.workers.dev/?chat_id={chat_id}"
            },
            "condition": {
                "addresses": [
                    address
                ]
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=webhook_data) as resp:
                    if resp.status in [200, 201]:
                        result = await resp.json()
                        return result.get('subscriptionId') 
                    print(f"Failed to create transaction webhook: {await resp.text()}")
                    return None
        except Exception as e:
            print(f"Error creating webhook: {e}")
            return None

    async def delete_webhook(self, chain: str, webhook_id: str) -> bool:
        """Delete a webhook"""
        if chain not in ALERT_SUPPORTED_CHAINS:
            return False
            
        # Construct webhook URL for the specific chain
        url = f"https://web3.nodit.io/v1/{chain}/mainnet/webhooks/{webhook_id}"
        headers = {
            "X-API-KEY": NODIT_API_KEY,
            "accept": "application/json",
            "content-type": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    return resp.status == 200
        except Exception as e:
            print(f"Error deleting webhook: {e}")
            return False

    async def add_alert(self, user_id: int, chain: str, address: str, update) -> bool:
        """Add a new alert for a user"""
        chain = chain.lower()
        if chain not in ALERT_SUPPORTED_CHAINS:
            await update.message.reply_text(f"Unsupported chain: {chain}")
            return False
            
        if chain not in self.alerts:
            self.alerts[chain] = []
            
        # Check if alert already exists
        for alert in self.alerts[chain]:
            if alert['user_id'] == user_id and alert['address'] == address:
                await update.message.reply_text(f"Alert already exists for {address} on {chain.capitalize()}")
                return False
                
        # Create webhook for monitoring
        description = f"Alert for {address} on {chain}"
        chat_id = str(update.effective_chat.id)
        webhook_id = await self.create_webhook(chain, address, description, chat_id)
        
        if not webhook_id:
            await update.message.reply_text(f"Failed to create alert for {address} on {chain.capitalize()}")
            return False
            
        self.alerts[chain].append({
            'user_id': user_id,
            'address': address,
            'webhook_id': webhook_id,
            'created_at': datetime.now().isoformat()
        })
        
        self.save_alerts()
        await update.message.reply_text(
            f"Alert added successfully!\n"
            f"Chain: {chain.capitalize()}\n"
            f"Address: {address}\n"
            f"Subscription ID: {webhook_id}\n"
            f"You will be notified of any transactions for this address."
        )
        return True

    async def remove_alert(self, user_id: int, chain: str, address: str, update) -> bool:
        """Remove an existing alert"""
        chain = chain.lower()
        if chain not in self.alerts:
            await update.message.reply_text(f"No alerts found for {chain.capitalize()}")
            return False
            
        # Find and remove the alert
        alert_to_remove = None
        for alert in self.alerts[chain]:
            if alert['user_id'] == user_id and alert['address'] == address:
                alert_to_remove = alert
                break
                
        if not alert_to_remove:
            await update.message.reply_text(f"No alert found for {address} on {chain.capitalize()}")
            return False
            
        # Delete the webhook
        if await self.delete_webhook(chain, alert_to_remove['webhook_id']):
            self.alerts[chain] = [
                alert for alert in self.alerts[chain]
                if not (alert['user_id'] == user_id and alert['address'] == address)
            ]
            self.save_alerts()
            await update.message.reply_text(f"Alert removed successfully for {address} on {chain.capitalize()}")
            return True
        else:
            await update.message.reply_text(f"Failed to remove alert for {address} on {chain.capitalize()}")
            return False

    async def list_webhooks(self, chain: str) -> List[Dict]:
        """List all webhooks for a specific chain"""
        if chain not in ALERT_SUPPORTED_CHAINS:
            return []
            
        url = f"https://web3.nodit.io/v1/{chain}/mainnet/webhooks"
        headers = {
            "X-API-KEY": NODIT_API_KEY,
            "accept": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("items", [])
                    return []
        except Exception as e:
            print(f"Error listing webhooks: {e}")
            return []

    async def delete_webhook_by_id(self, chain: str, subscription_id: str) -> bool:
        """Delete a webhook by subscription ID"""
        if chain not in ALERT_SUPPORTED_CHAINS:
            return False
            
        url = f"https://web3.nodit.io/v1/{chain}/mainnet/webhooks/{subscription_id}"
        headers = {
            "X-API-KEY": NODIT_API_KEY,
            "accept": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(url, headers=headers) as resp:
                    return resp.status in [200, 204]
        except Exception as e:
            print(f"Error deleting webhook by ID: {e}")
            return False

    async def delete_all_webhooks(self, chain: str) -> int:
        """Delete all webhooks for a specific chain"""
        if chain not in ALERT_SUPPORTED_CHAINS:
            return 0
            
        webhooks = await self.list_webhooks(chain)
        deleted_count = 0
        
        for webhook in webhooks:
            subscription_id = webhook.get("subscriptionId")
            if subscription_id:
                if await self.delete_webhook_by_id(chain, subscription_id):
                    deleted_count += 1
                    
        return deleted_count

    async def list_user_alerts(self, user_id: int, update) -> None:
        """List all alerts for a specific user"""
        if not self.alerts:
            await update.message.reply_text("No alerts found.")
            return
            
        alert_list = []
        for chain, alerts in self.alerts.items():
            for alert in alerts:
                if alert['user_id'] == user_id:
                    alert_list.append({
                        'chain': chain,
                        'address': alert['address'],
                        'subscription_id': alert['webhook_id'],
                        'created_at': alert['created_at']
                    })
        
        if not alert_list:
            await update.message.reply_text("No alerts found for your account.")
            return
            
        # Build response message
        message = "Your active alerts:\n\n"
        for i, alert in enumerate(alert_list, 1):
            message += f"[{i}] Chain: {alert['chain'].capitalize()}\n"
            message += f"Address: {alert['address']}\n"
            message += f"Subscription ID: {alert['subscription_id']}\n"
            message += f"Created: {alert['created_at'][:19]}\n\n"
        
        await update.message.reply_text(message)

    async def delete_alert_by_subscription_id(self, user_id: int, subscription_id: str, update) -> bool:
        """Delete an alert by subscription ID"""
        # Find the alert in our local storage
        alert_to_remove = None
        chain_to_remove = None
        
        for chain, alerts in self.alerts.items():
            for alert in alerts:
                if alert['user_id'] == user_id and alert['webhook_id'] == subscription_id:
                    alert_to_remove = alert
                    chain_to_remove = chain
                    break
            if alert_to_remove:
                break
                
        if not alert_to_remove:
            await update.message.reply_text(f"No alert found with subscription ID: {subscription_id}")
            return False
            
        # Delete from Nodit
        if await self.delete_webhook_by_id(chain_to_remove, subscription_id):
            # Remove from local storage
            self.alerts[chain_to_remove] = [
                alert for alert in self.alerts[chain_to_remove]
                if not (alert['user_id'] == user_id and alert['webhook_id'] == subscription_id)
            ]
            self.save_alerts()
            await update.message.reply_text(f"Alert deleted successfully for subscription ID: {subscription_id}")
            return True
        else:
            await update.message.reply_text(f"Failed to delete alert with subscription ID: {subscription_id}")
            return False

    async def delete_all_user_alerts(self, user_id: int, update) -> bool:
        """Delete all alerts for a specific user"""
        if not self.alerts:
            await update.message.reply_text("No alerts found.")
            return False
            
        deleted_count = 0
        failed_count = 0
        
        for chain, alerts in list(self.alerts.items()):
            for alert in list(alerts):
                if alert['user_id'] == user_id:
                    if await self.delete_webhook_by_id(chain, alert['webhook_id']):
                        self.alerts[chain].remove(alert)
                        deleted_count += 1
                    else:
                        failed_count += 1
        
        self.save_alerts()
        
        if deleted_count > 0:
            message = f"Deleted {deleted_count} alert(s) successfully."
            if failed_count > 0:
                message += f" Failed to delete {failed_count} alert(s)."
            await update.message.reply_text(message)
            return True
        else:
            await update.message.reply_text("No alerts were deleted.")
            return False

# Global alert manager instance
alert_manager = AlertManager()

user_queues = {}
user_tasks = {}

async def handle_alert_command(update, context):
    """Handle /alert command with per-user queue and action-specific waiting message"""
    user_id = update.effective_user.id
    action = context.args[0].lower() if context.args else ""
    # 根据 action 回复不同的等待提示
    if action == "add":
        wait_msg = "Adding alert, please wait..."
    elif action == "del":
        if len(context.args) >= 2 and context.args[1].lower() == "all":
            wait_msg = "Deleting all alerts, please wait..."
        elif len(context.args) == 2:
            wait_msg = "Deleting alert by subscription ID, please wait..."
        elif len(context.args) >= 3:
            wait_msg = "Removing alert, please wait..."
        else:
            wait_msg = "Deleting alert, please wait..."
    elif action == "list":
        wait_msg = "Listing your alerts, please wait..."
    else:
        wait_msg = "Processing your request, please wait..."
    await update.message.reply_text(wait_msg)
    # 入队
    if user_id not in user_queues:
        user_queues[user_id] = asyncio.Queue()
    await user_queues[user_id].put((update, context))
    if user_id not in user_tasks or user_tasks[user_id].done():
        user_tasks[user_id] = asyncio.create_task(process_user_queue(user_id))

async def process_user_queue(user_id):
    while not user_queues[user_id].empty():
        update, context = await user_queues[user_id].get()
        try:
            await handle_alert_command_inner(update, context)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

async def handle_alert_command_inner(update, context):
    """原有 handle_alert_command 逻辑，去掉等待提示部分"""
    if not context.args:
        await update.message.reply_text(
            "Invalid command format. Please use:\n"
            "/alert add <chain> <address> - Add an alert\n"
            "/alert del <chain> <address> - Remove an alert by chain and address\n"
            "/alert del <subscription_id> - Remove an alert by subscription ID\n"
            "/alert del all - Remove all your alerts\n"
            "/alert list - List all your alerts\n"
            f"Supported chains: {', '.join(ALERT_SUPPORTED_CHAINS)}"
        )
        return

    action = context.args[0].lower()
    user_id = update.effective_user.id

    if action == "list":
        await alert_manager.list_user_alerts(user_id, update)
        return

    if action == "del":
        if len(context.args) < 2:
            await update.message.reply_text(
                "Please specify what to delete:\n"
                "/alert del <chain> <address> - Remove an alert by chain and address\n"
                "/alert del <subscription_id> - Remove an alert by subscription ID\n"
                "/alert del all - Remove all your alerts"
            )
            return
        if context.args[1].lower() == "all":
            await alert_manager.delete_all_user_alerts(user_id, update)
            return
        if len(context.args) == 2:
            # Delete by subscription ID
            subscription_id = context.args[1]
            await alert_manager.delete_alert_by_subscription_id(user_id, subscription_id, update)
            return
        if len(context.args) >= 3:
            # Delete by chain and address
            chain = context.args[1].lower()
            address = context.args[2]
            if chain not in ALERT_SUPPORTED_CHAINS:
                await update.message.reply_text(
                    f"Unsupported chain. Supported chains: {', '.join(ALERT_SUPPORTED_CHAINS)}"
                )
                return
            await alert_manager.remove_alert(user_id, chain, address, update)
            return

    if action == "add":
        if len(context.args) < 3:
            await update.message.reply_text(
                "Please use the correct format: /alert add <chain> <address>\n"
                f"Supported chains: {', '.join(ALERT_SUPPORTED_CHAINS)}"
            )
            return
        chain = context.args[1].lower()
        address = context.args[2]
        if chain not in ALERT_SUPPORTED_CHAINS:
            await update.message.reply_text(
                f"Unsupported chain. Supported chains: {', '.join(ALERT_SUPPORTED_CHAINS)}"
            )
            return
        await alert_manager.add_alert(user_id, chain, address, update)
        return

    # If we get here, the action is not recognized
    await update.message.reply_text(
        "Invalid action. Please use:\n"
        "/alert add <chain> <address> - Add an alert\n"
        "/alert del <chain> <address> - Remove an alert by chain and address\n"
        "/alert del <subscription_id> - Remove an alert by subscription ID\n"
        "/alert del all - Remove all your alerts\n"
        "/alert list - List all your alerts"
    )
