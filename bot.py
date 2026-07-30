import asyncio

# Create event loop for newer Python versions
asyncio.set_event_loop(asyncio.new_event_loop())

import os
from pyrogram import Client, filters
import yt_dlp

API_ID = 28905002
API_HASH = "610ac01833c507d7e15b2f90a30d8595"
BOT_TOKEN = "8801346914:AAHm0kttNSwXmSPtWFsFIJX1q0g8sqBCSlo"

app = Client(
    "LeechBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Welcome!\n\nSend:\n/leech <url>"
    )

@app.on_message(filters.command("leech"))
async def leech(client, message):
    if len(message.command) < 2:
        await message.reply_text("Usage:\n/leech <url>")
        return

    url = message.command[1]

    os.makedirs("downloads", exist_ok=True)

    opts = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "quiet": True,
    }

    status = await message.reply_text("⬇️ Downloading...")

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)

        await status.edit("📤 Uploading...")
        await message.reply_document(file)

        os.remove(file)
        await status.delete()

    except Exception as e:
        await status.edit(f"❌ Error:\n{e}")

print("Bot Started...")
app.run()
