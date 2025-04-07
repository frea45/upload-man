from pyrogram import Client

API_ID = 123456
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

LOG_CHANNEL = -1001234567890

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "link_to_file_bot"

bot = Client(
    "link2file_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
