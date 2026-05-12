import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# إعداداتك
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'
TARGET_CHANNEL = 'ComplexCloudLogs' 
COMBO_FILE = "ulp.txt"

# صنع الملف فارغ إذا مكانش موجود باش ما يصرى حتى Error
if not os.path.exists(COMBO_FILE):
    with open(COMBO_FILE, "w") as f:
        f.write("--- بداية الصيد ---\n")

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter(event):
    if event.message.document and (event.message.file.ext in ['.txt', '.log']):
        path = await event.message.download_media()
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', data)
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for m in matches:
                    out.write(f"{m}\n")
        os.remove(path)
        print(f"✅ صيد جديد من ملف!")

@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res:
                bot.reply_to(message, "✅ الصيد اللي لقيتو:\n\n" + "\n".join(res[:15]))
            else:
                bot.reply_to(message, "❌ مزال ما صيدناش هاد الموقع.")
    else:
        bot.reply_to(message, "⏳ الملف راهو يتصنع، اصبر دقيقة.")

def run():
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    run()
