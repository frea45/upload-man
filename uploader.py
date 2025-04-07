from pyrogram import Client
from pyrogram.types import Message
from io import BytesIO

async def upload_file(client: Client, file_name: str, file_data, chat_id: int, progress_msg: Message):
    try:
        # اگر فایل به صورت BytesIO نبود، تبدیلش نمی‌کنیم و مستقیم می‌فرستیم
        sent = await client.send_document(
            chat_id=chat_id,
            document=file_data,
            file_name=file_name,
            caption=f"نام فایل: {file_name}"
        )
        return sent

    except Exception as e:
        await progress_msg.edit(f"❌ خطا در آپلود فایل:\n{e}")
        raise e
