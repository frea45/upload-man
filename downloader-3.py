
import tempfile
import aiohttp
import asyncio

async def download_file(url, session, client, chat_id):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                await client.send_message(chat_id, "❌ خطا در دانلود فایل.")
                return

            with tempfile.NamedTemporaryFile(delete=False, suffix=".bin") as tmp:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    tmp.write(chunk)
                tmp_path = tmp.name

        await client.send_document(chat_id, tmp_path)

    except Exception as e:
        await client.send_message(chat_id, f"❌ خطا در پردازش فایل:\n{e}")
