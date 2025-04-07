
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from downloader import download_file
from uploader import upload_file
from database import save_file_info
import asyncio

# برای health check سرور ساده Flask
from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8000)

Thread(target=run).start()

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))

client = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@client.on_message(filters.private & filters.text)
async def handle_message(client: Client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply("لطفاً یک لینک معتبر ارسال کنید.")
        return

    msg = await message.reply("در حال پردازش لینک...")

    try:
        file_name, file_path, file_size = await download_file(url, msg, client, LOG_CHANNEL)

        with open(file_path, "rb") as f:
            sent_msg = await with open(file_path, 'rb') as f:
    await upload_file(client, file_name, f, LOG_CHANNEL, msg)

        os.remove(file_path)

        file_info = {
            "file_name": file_name,
            "file_size": file_size,
            "user_id": message.from_user.id,
            "file_id": sent_msg.document.file_id
        }

        save_file_info(file_info)

        await msg.edit("✅ فایل آپلود شد و در کانال ثبت شد.")

    except Exception as e:
        await msg.edit(f"❌ خطا در پردازش فایل:\n{e}")

print("Instance created. Preparing to start...")

client.run()


from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()
