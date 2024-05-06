from config import ANKR_RPC_KEY


networks = [
    {
        "name": "ethereum",
        "short_name": "eth",
        "explorer": "https://etherscan.io/",
        "eip1559": True,
        "chainId": 1,
        "rpc": f"https://rpc.ankr.com/eth/{ANKR_RPC_KEY}",
        "url": "https://ethereum.org/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "arbitrum_one",
        "short_name": "arb1",
        "explorer": "https://arbiscan.io/",
        "eip1559": True,
        "chainId": 42161,
        "rpc": f"https://rpc.ankr.com/arbitrum/{ANKR_RPC_KEY}",
        "url": "https://arbitrum.io/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "optimism",
        "short_name": "oeth",
        "explorer": "https://optimistic.etherscan.io/",
        "eip1559": True,
        "chainId": 10,
        "rpc": f"https://rpc.ankr.com/optimism/{ANKR_RPC_KEY}",
        "url": "https://optimism.io/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "zksync",
        "short_name": "zksync",
        "explorer": f"https://explorer.zksync.io/",
        "eip1559": False,
        "chainId": 324,
        "rpc": f"https://rpc.ankr.com/zksync_era/{ANKR_RPC_KEY}",
        "url": "https://zksync.io/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "base",
        "short_name": "base",
        "explorer": "https://basescan.org/",
        "eip1559": True,
        "chainId": 8453,
        "rpc": f"https://rpc.ankr.com/base/{ANKR_RPC_KEY}",
        "url": "https://base.org/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "scroll",
        "short_name": "scr",
        "explorer": "https://scrollscan.com/",
        "eip1559": False,
        "chainId": 534352,
        "rpc": f"https://rpc.ankr.com/scroll/{ANKR_RPC_KEY}",
        "url": "https://scroll.io/",
        "currency": {"name": "ETH", "decimals": 18},
    },
    {
        "name": "polygon",
        "short_name": "matic",
        "explorer": "https://polygonscan.com/",
        "eip1559": True,
        "chainId": 137,
        "rpc": f"https://rpc.ankr.com/polygon/{ANKR_RPC_KEY}",
        "url": "https://polygon.technology/",
        "currency": {"name": "MATIC", "decimals": 18},
    },
    {
        "name": "avalanche",
        "short_name": "avax",
        "explorer": "https://snowtrace.io/",
        "eip1559": True,
        "chainId": 43114,
        "rpc": f"https://rpc.ankr.com/avalanche/{ANKR_RPC_KEY}",
        "url": "https://www.avax.network/",
        "currency": {"name": "AVAX", "decimals": 18},
    },
    {
        "name": "bsc",
        "short_name": "bnb",
        "explorer": "https://bscscan.com/",
        "eip1559": True,
        "chainId": 56,
        "rpc": f"https://rpc.ankr.com/bsc/{ANKR_RPC_KEY}",
        "url": "https://www.bnbchain.org/en/",
        "currency": {"name": "BNB", "decimals": 18},
    },
]


def get_networks():
    return networks


def get_network(name):
    for i in networks:
        if i["name"] == name:
            return i
