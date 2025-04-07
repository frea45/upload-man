import tempfile
from io import BytesIO
from pyrogram import Client
from pyrogram.types import Message

async def upload_file(client: Client, file_name: str, file_data, chat_id: int, progress_msg: Message):
    try:
        # اگر BytesIO بود تبدیلش کن به فایل موقت
        if isinstance(file_data, BytesIO):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file_name}") as tmp:
                tmp.write(file_data.getvalue())
                tmp_path = tmp.name
            file_data = tmp_path  # مسیر فایل موقت رو بده به send_document

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