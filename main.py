import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# إعداداتك (تأكد منهم مليح يا لؤي)
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'
TARGET_CHANNEL = 'ComplexCloudLogs' 
COMBO_FILE = "ulp.txt"

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

def extract_from_text(text):
    return re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', text)

async def process_message(message):
    count = 0
    # صيد من الملفات
    if message.document and (message.file.ext in ['.txt', '.log']):
        path = await message.download_media()
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            matches = extract_from_text(f.read())
            if matches:
                with open(COMBO_FILE, "a", encoding='utf-8') as out:
                    for m in matches:
                        out.write(f"{m}\n")
                count = len(matches)
        os.remove(path)
    # صيد من النص
    elif message.text:
        matches = extract_from_text(message.text)
        if matches:
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for m in matches:
                    out.write(f"{m}\n")
            count = len(matches)
    return count

@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def handler(event):
    await process_message(event.message)

@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res:
                bot.reply_to(message, f"🎯 صيد طري لـ {query}:\n\n" + "\n".join(res[:15]))
            else:
                bot.reply_to(message, "❌ ما لقيتش هاد الموقع في الصيد.")
    else:
        bot.reply_to(message, "⏳ الماكينة مزال ما عمرت الملف.")

async def start_hunting():
    await client.start()
    print("🚀 الماكينة بدأت تجمع القديم والجديد...")
    # يروح يجيب آخر 100 رسالة باش ما تبقاش تستنى
    async for message in client.iter_messages(TARGET_CHANNEL, limit=100):
        await process_message(message)
    print("✅ كملت جمع الحسابات القديمة. ضرك راني نستنى في الجديد!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(start_hunting())
