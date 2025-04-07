import aiohttp
import asyncio
import time
from io import BytesIO

async def download_file(url, msg):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"وضعیت دریافت لینک: {resp.status}")

            file_size = int(resp.headers.get("Content-Length", 0))
            file_name = url.split("/")[-1] or "file"

            downloaded = 0
            start_time = time.time()
            chunk_size = 1024 * 64

            buffer = BytesIO()
            last_edit = time.time()

            async for chunk in resp.content.iter_chunked(chunk_size):
                buffer.write(chunk)
                downloaded += len(chunk)

                now = time.time()
                if now - last_edit > 2:
                    percent = downloaded * 100 / file_size if file_size else 0
                    speed = downloaded / (now - start_time + 1)
                    eta = (file_size - downloaded) / speed if speed > 0 else 0
                    await msg.edit(
                        f"**در حال دانلود...**\n"
                        f"نام فایل: `{file_name}`\n"
                        f"پیشرفت: `{percent:.2f}%`\n"
                        f"دانلود شده: `{human_readable(downloaded)}` از `{human_readable(file_size)}`\n"
                        f"سرعت: `{human_readable(speed)}/s`\n"
                        f"زمان باقی‌مانده: `{human_time(eta)}`"
                    )
                    last_edit = now

            buffer.seek(0)
            return file_name, buffer, file_size

def human_readable(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def human_time(seconds):
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    elif m:
        return f"{m}m {s}s"
    else:
        return f"{s}s"
