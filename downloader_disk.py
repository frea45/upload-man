import aiohttp
import os
import time
from urllib.parse import unquote, urlparse

async def download_file(url, status_msg):
    parsed = urlparse(url)
    file_name = os.path.basename(unquote(parsed.path)) or "file"
    temp_path = f"/tmp/{file_name}"
    file_size = 0

    await status_msg.edit("⏳ در حال دانلود فایل...")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"خطا در دریافت فایل: وضعیت {resp.status}")

            with open(temp_path, "wb") as f:
                async for chunk in resp.content.iter_chunked(1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        file_size += len(chunk)

    return file_name, temp_path, file_size
