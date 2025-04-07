import time
from io import BytesIO

async def upload_file(client, file_name, file_data, channel_id, status_msg):
    start_time = time.time()

    # فرض بر اینه که file_data بایت‌ها هست
        if isinstance(file_data, BytesIO):
        file_obj = file_data
    else:
        file_obj = BytesIO(file_data)
    file_obj.name = file_name  # pyrogram برای نام فایل به این نیاز داره

    sent = await client.send_document(
        chat_id=channel_id,
        document=file_obj,
        caption=f"✅ فایل جدید آپلود شد: `{file_name}`",
        force_document=True
    )

    total_time = time.time() - start_time
    await status_msg.edit(f"✅ فایل در {total_time:.1f}s آپلود شد و در حال ارسال به شماست...")
    return sent
"""
اگر file_data مسیر فایل باشه (نه بایت‌ها):

with open(file_data, "rb") as f:
    await client.send_document(chat_id=channel_id, document=f, ...)
"""
