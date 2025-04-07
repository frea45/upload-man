import tempfile
import aiohttp
import os

async def download_file(url, msg, client, chat_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await msg.edit("❌ خطا در دانلود فایل.")
                    return None, None, None

                content_disposition = response.headers.get("Content-Disposition", "")
                file_name = "downloaded_file"

                if "filename=" in content_disposition:
                    file_name = content_disposition.split("filename=")[-1].strip().strip('"')

                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[-1]) as tmp:
                    while True:
                        chunk = await response.content.read(1024 * 1024)  # 1MB
                        if not chunk:
                            break
                        tmp.write(chunk)
                    tmp_path = tmp.name

        file_size = os.path.getsize(tmp_path)
        return file_name, tmp_path, file_size

    except Exception as e:
        await msg.edit(f"❌ خطا در پردازش فایل:\n{e}")
        return None, None, None