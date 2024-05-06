from dotenv import load_dotenv
import os

load_dotenv()
ANKR_RPC_KEY = os.getenv("ANKR_RPC_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

COINGECKO_URL = "https://api.coingecko.com/api/v3/"
ODOS_URL = "https://api.odos.xyz/sor/"