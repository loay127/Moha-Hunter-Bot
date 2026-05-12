import telebot
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import threading
import re
import os
import asyncio

# --- الإعدادات (تأكد من الأسماء في GitHub Secrets) ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'

# هادا هو الكود الطويل اللي عطيتهولي، حطه في GitHub Secrets باسم STRING_SESSION
STRING_SESSION = os.getenv("STRING_SESSION") 

SOURCE_NAME = "COMPLEX" 
MY_STORAGE_NAME = "ULP" 

COMBO_FILE = "ulp.txt"
bot = telebot.TeleBot(BOT_TOKEN)

# هنا الماكينة تخدم بالكود الطويل بلا ملفات
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def main_logic():
    await client.start()
    print("✅ تم الاتصال بنجاح باستعمال الـ String Session!")
    
    source_entity = None
    storage_entity = None

    async for dialog in client.iter_dialogs():
        if SOURCE_NAME.upper() in dialog.name.upper():
            source_entity = dialog.entity
        if MY_STORAGE_NAME.upper() in dialog.name.upper():
            storage_entity = dialog.entity

    if not source_entity or not storage_entity:
        print("❌ مالقيتش القنوات! تأكد بلي راك داخل فيهم.")
        return

    print(f"🚀 بدأت السحب من {source_entity.title}...")

    # سحب الملفات القديمة
    async for message in client.iter_messages(source_entity, limit=100):
        if message.document and message.file.ext in ['.txt', '.log']:
            await client.send_message(storage_entity, message)
            path = await message.download_media()
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^._-]+)', f.read())
                if matches:
                    with open(COMBO_FILE, "a", encoding='utf-8') as out:
                        for m in matches: out.write(f"{m}\n")
            os.remove(path)

    @client.on(events.NewMessage(chats=source_entity))
    async def handler(event):
        if event.message.document:
            await client.send_message(storage_entity, event.message)
            print("🆕 ملف جديد وصل!")

    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(main_logic())
