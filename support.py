"""
Centralized support chains configuration for Nodit Bot.
All supported chains are defined here with standardized naming convention:
<INTERFACE_NAME>_SUPPORTED_CHAINS
"""
from config import NODIT_API_KEY

# Balance query supported chains
BALANCE_SUPPORTED_CHAINS = [
    "arbitrum",
    "base",
    "bitcoin",
    "doge",
    "ethereum",
    "kaia",
    "optimism",
    "polygon"
]

# Token query supported chains
TOKEN_SUPPORTED_CHAINS = [
    "aptos",
    "arbitrum",
    "base",
    "ethereum",
    "kaia",
    "optimism",
    "polygon"
]

# Alert system supported chains (Coming Soon)
ALERT_SUPPORTED_CHAINS = [
    "ethereum",
    "polygon",
    "arbitrum",
    "base",
    "optimism",
    "kaia"
]

# Map each chain to its mainnet Nodit endpoint, NODIT_API_KEY appended as query param
ALERT_WEBHOOK_ENDPOINTS = {
    "ethereum": f"https://ethereum-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}",
    "polygon":  f"https://polygon-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}",
    "arbitrum": f"https://arbitrum-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}",
    "base":     f"https://base-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}",
    "optimism": f"https://optimism-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}",
    "kaia":     f"https://kaia-mainnet.nodit.io/?X-API-KEY={NODIT_API_KEY}"
}

# Transaction history supported chains (Coming Soon)
TXS_SUPPORTED_CHAINS = [
    "ethereum",
    "polygon",
    "arbitrum",
    "base",
    "optimism",
    "kaia",
    "bitcoin",
    "doge"
]

# Address format descriptions for each chain
ADDRESS_FORMAT_DESCRIPTIONS = {
    "ethereum": "42-character hexadecimal address starting with 0x (e.g., 0x7e3c30e93f1...)",
    "polygon": "42-character hexadecimal address starting with 0x (e.g., 0x8f30fd7cb834...)",
    "arbitrum": "42-character hexadecimal address starting with 0x (e.g., 0x23b8b1e2d...)",
    "base": "42-character hexadecimal address starting with 0x (e.g., 0x0000111122223333...)",
    "optimism": "42-character hexadecimal address starting with 0x (e.g., 0xC0ffee254...)",
    "kaia": "42-character hexadecimal address starting with 0x (e.g., 0x6e4eC32ba...)",
    "bitcoin": "25-34 character address starting with 1 or 3, or 39-59 character address starting with bc1 (e.g., 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa or bc1qw4...)",
    "doge": "25-34 character address starting with D, A, or 9 (e.g., D8B8Cn2axuzWc63...)"
}

# Address format validation rules
ADDRESS_FORMATS = {
    # EVM compatible chains
    "ethereum": r"^0x[a-fA-F0-9]{40}$",
    "polygon": r"^0x[a-fA-F0-9]{40}$",
    "arbitrum": r"^0x[a-fA-F0-9]{40}$",
    "base": r"^0x[a-fA-F0-9]{40}$",
    "optimism": r"^0x[a-fA-F0-9]{40}$",
    "kaia": r"^0x[a-fA-F0-9]{40}$",
    
    # Bitcoin
    "bitcoin": r"^(1|3)[a-zA-Z0-9]{25,34}$|^bc1[a-z0-9]{39,59}$",
    
    # Dogecoin
    "doge": r"^[DA9][a-zA-Z0-9]{25,34}$"
}
