from pyrogram import filters
from pyrogram.types import Message
from config import bot, LOG_CHANNEL
from database import save_file_info
from downloader import download_file
from uploader import upload_file
import re

# اضافه کردن Web Server
from flask import Flask
import threading

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

def run_web():
    web_app.run(host="0.0.0.0", port=8000)

threading.Thread(target=run_web).start()

# ادامه‌ی کد اصلی
def is_direct_link(url: str) -> bool:
    return re.match(r'^https?://', url)

@bot.on_message(filters.private & filters.text)
async def handle_link(client, message: Message):
    url = message.text.strip()

    if not is_direct_link(url):
        return await message.reply("لطفاً یک لینک مستقیم معتبر ارسال کن.")

    msg = await message.reply("دانلود آغاز شد...")

    try:
        file_name, file_path, file_size = await download_file(url, msg)
        with open(file_path, 'rb') as f:
        sent_msg = await upload_file(client, file_name, f, LOG_CHANNEL, msg)
        save_file_info(message.from_user.id, url, file_name, file_size)
        await sent_msg.copy(chat_id=message.chat.id)
        await msg.edit("✅ فایل با موفقیت برای شما ارسال شد.")
    except Exception as e:
        await msg.edit(f"❌ خطا در پردازش فایل:\n{e}")

if __name__ == "__main__":
    bot.run()

    os.remove(file_path)