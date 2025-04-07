import aiohttp
import asyncio
import time
from io import BytesIO

async def download_file(url, msg):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception("وضعیت دریافت لینک: {}".format(resp.status))

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
                    status_text = "⬇️ در حال دانلود...\n"
                    status_text += "درصد: {:.2f}%\n".format(percent)
                    status_text += "سرعت: {:.2f} KB/s\n".format(speed / 1024)
                    status_text += "زمان باقی‌مانده: {:.1f} ثانیه".format(eta)
                    await msg.edit(status_text)
                    last_edit = now

            buffer.seek(0)
            return file_name, buffer, file_size
