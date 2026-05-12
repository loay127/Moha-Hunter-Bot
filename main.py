import telebot
from telethon import TelegramClient, events
from telethon.sessions import StringSession
import threading
import re
import os
import asyncio

# --- الإعدادات (تأكد أن STRING_SESSION موجود في GitHub Secrets) ---
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
STRING_SESSION = os.getenv("STRING_SESSION") # يسحب الكود الطويل من السكرت

# رابط القناة الخاصة (استعملنا الرابط اللي بعتولي)
SOURCE_LINK = "https://t.me/+lgwPgZsNmwYxODRi"
MY_STORAGE = "MyUlpStorage_Loay" # اسم قناتك

bot = telebot.TeleBot(BOT_TOKEN)
# الربط باستعمال الـ StringSession مباشرة
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def start_scraping():
    await client.start()
    print("✅ تم الاتصال بالحساب بنجاح!")

    # الوصول للقناة وسحب الملفات
    async for message in client.iter_messages(SOURCE_LINK, limit=100):
        if message.document and message.file.ext in ['.txt', '.log']:
            print(f"📥 جاري تحويل: {message.file.name}")
            await client.send_message(MY_STORAGE, message) # يبعث لقناتك

    # مراقبة أي ملف جديد يتلاح ضرك
    @client.on(events.NewMessage(chats=SOURCE_LINK))
    async def handler(event):
        if event.message.document:
            await client.send_message(MY_STORAGE, event.message)
            print("🆕 ملف جديد وصل وحولته!")

    await client.run_until_disconnected()

if __name__ == "__main__":
    # تشغيل البوت للبحث (اختياري) والسكربت للسحب في نفس الوقت
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(start_scraping())
