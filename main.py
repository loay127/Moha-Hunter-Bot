import telebot
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ImportChatInviteRequest
import threading
import re
import os
import asyncio

# --- الإعدادات (تأكد من وضعهم في GitHub Secrets) ---
API_ID = int(os.getenv("API_ID", "34023364"))
API_HASH = os.getenv("API_HASH", "ad07473755a47402aef9c3d580886cdf")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8")
STRING_SESSION = os.getenv("STRING_SESSION")

# روابط القنوات
SOURCE_INVITE_LINK = "lgwPgZsNmwYxODRi" # الكود اللي بعد الزائد في الرابط
MY_STORAGE_ID = "MyUlpStorage_Loay" 

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)

async def start_hunting():
    await client.start()
    print("✅ الحساب متصل.. جاري فحص القنوات")

    try:
        # محاولة دخول قناة COMPLEX أوتوماتيكياً
        await client(ImportChatInviteRequest(SOURCE_INVITE_LINK))
        print("🔓 تم الدخول للقناة بنجاح!")
    except:
        print("ℹ️ الحساب أصلاً موجود في القناة أو الرابط تغير.")

    # سحب الملفات القديمة (أوتوماتيك 100%)
    async for message in client.iter_messages('https://t.me/+'+SOURCE_INVITE_LINK, limit=100):
        if message.document and message.file.ext in ['.txt', '.log']:
            print(f"📥 صيد ملف: {message.file.name}")
            await client.send_message(MY_STORAGE_ID, message)

    # مراقبة أي ملف جديد
    @client.on(events.NewMessage(chats='https://t.me/+'+SOURCE_INVITE_LINK))
    async def handler(event):
        if event.message.document:
            await client.send_message(MY_STORAGE_ID, event.message)
            print("🆕 ملف جديد تم تحويله!")

    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(start_hunting())
