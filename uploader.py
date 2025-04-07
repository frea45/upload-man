from pyrogram.types import InputFile
import time

async def upload_file(client, file_name, file_data, channel_id, status_msg):
    start_time = time.time()
    input_file = InputFile(file_data, file_name=file_name)

    sent = await client.send_document(
        chat_id=channel_id,
        document=input_file,
        caption=f"✅ فایل جدید آپلود شد: `{file_name}`",
        force_document=True
    )

    total_time = time.time() - start_time
    await status_msg.edit(f"✅ فایل در {total_time:.1f}s آپلود شد و در حال ارسال به شماست...")
    return sent
