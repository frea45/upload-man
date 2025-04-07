from pyrogram import Client

API_ID = 3335796 
API_HASH = "138b992a0e672e8346d8439c3f42ea78"
BOT_TOKEN = "7136875110:AAFzyr2i2FbRrmst1sklkJPN7Yz2rXJvSew"

LOG_CHANNEL = -1001792962793

MONGO_URL = "mongodb+srv://abirhasan2005:abirhasan@cluster0.i6qzp.mongodb.net/cluster0?retryWrites=true&w=majority"
DB_NAME = "link_to_file_bot"

bot = Client(
    "link2file_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)
