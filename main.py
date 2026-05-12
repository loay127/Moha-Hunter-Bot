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

bot = telebot.TeleBot(BOT_TOKEN)

# التغيير هنا: ندخل باستعمال توكن البوت باش السكربت ما يحبسش يطلب كود
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter(event):
    if event.message.document and (event.message.file.ext in ['.txt', '.log']):
        path = await event.message.download_media()
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()
            matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', data)
            if matches:
                with open(COMBO_FILE, "a", encoding='utf-8') as out:
                    for m in matches:
                        out.write(f"{m}\n")
        os.remove(path)

@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res:
                bot.reply_to(message, "🎯 هاك واش صيدت:\n\n" + "\n".join(res[:15]))
            else:
                bot.reply_to(message, "❌ مزال ما صيدناش هاد الموقع.")
    else:
        bot.reply_to(message, "⏳ الماكينة تجمع، اصبر شوية.")

def run():
    print("🚀 الماكينة انطلقت!")
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.run_until_disconnected()

if __name__ == "__main__":
    run()
