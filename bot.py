from pyrogram import Client, filters
from pyrogram.types import Message
from downloader import download_file
from uploader import upload_file
import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL"))

client = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@client.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply_text("سلام! لینک خود را ارسال کنید تا آن را دریافت کنید.")

@client.on_message(filters.private & filters.text)
async def handle_link(client: Client, message: Message):
    url = message.text
    msg = await message.reply_text("⏬ در حال دانلود فایل...")

    try:
        import aiohttp
        async with aiohttp.ClientSession() as session:
            await download_file(url, session, client, message.chat.id)

        # مسیر فرضی فایل دانلود شده
        file_path = "/tmp/downloaded_file.bin"
        file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            sent_msg = await upload_file(client, file_name, f, LOG_CHANNEL, msg)

    except Exception as e:
        await message.reply_text(f"❌ خطا در پردازش فایل:\n{e}")

client.run()
