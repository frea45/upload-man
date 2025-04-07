from pyrogram import filters
from pyrogram.types import Message
from config import bot, LOG_CHANNEL
from database import save_file_info
from downloader import download_file
from uploader import upload_file
import re

def is_direct_link(url: str) -> bool:
    return re.match(r'^https?://', url)

@bot.on_message(filters.private & filters.text)
async def handle_link(client, message: Message):
    url = message.text.strip()

    if not is_direct_link(url):
        return await message.reply("لطفاً یک لینک مستقیم معتبر ارسال کن.")

    msg = await message.reply("دانلود آغاز شد...")

    try:
        file_name, file_data, file_size = await download_file(url, msg)
        sent_msg = await upload_file(client, file_name, file_data, LOG_CHANNEL, msg)
        save_file_info(message.from_user.id, url, file_name, file_size)
        await sent_msg.copy(chat_id=message.chat.id)
        await msg.edit("✅ فایل با موفقیت برای شما ارسال شد.")
    except Exception as e:
        await msg.edit(f"❌ خطا در پردازش فایل:\n{e}")

if __name__ == "__main__":
    bot.run()
