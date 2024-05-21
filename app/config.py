from dotenv import load_dotenv
import os

### ENVIROMENTS
load_dotenv()
ANKR_RPC_KEY = os.getenv("ANKR_RPC_KEY")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
ONE_INCH_KEY=os.getenv("ONE_INCH_KEY")

### SWAGGER
SWAGGER_API_URL = "/api/docs"
SWAGGER_FILE = "/static/swagger.json"

class APIS:
    COINGECKO = "https://api.coingecko.com/api/v3/"
    ODOS = "https://api.odos.xyz/sor/"
    ONE_INCH = "https://api.1inch.dev/swap/v6.0/"
    NITRO = "https://api-beta.pathfinder.routerprotocol.com/api/v2/"