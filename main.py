import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# 1. إعداداتك (حط معلوماتك هنا)
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'
TARGET_CHANNEL = 'ComplexCloudLogs' # اليوزر نيم بلا @
COMBO_FILE = "ulp.txt"

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

# 2. وظيفة الصيد (تجبد من النص ومن الملفات)
@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter_handler(event):
    count = 0
    # إذا كانت الرسالة فيها ملف .txt أو .log
    if event.message.document and (event.message.file.ext in ['.txt', '.log']):
        path = await event.message.download_media()
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for line in f:
                    matches = re.findall(r'([a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9._-]+):([a-zA-Z0-9!@#$%^&*._-]+)', line)
                    for m in matches:
                        out.write(f"{m[0]}:{m[1]}\n")
                        count += 1
        os.remove(path)
        print(f"✅ صيد طري من ملف: {count} حساب")

    # إذا كانت الرسالة نصية
    elif event.message.text:
        matches = re.findall(r'([a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9._-]+):([a-zA-Z0-9!@#$%^&*._-]+)', event.message.text)
        if matches:
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for m in matches:
                    out.write(f"{m[0]}:{m[1]}\n")
                    count += 1
            print(f"✅ صيد طري من نص: {count} حساب")

# 3. أمر البوت للاستخراج (كيما الهاتف)
@bot.message_handler(commands=['url'])
def search_in_ulp(message):
    query = message.text.replace('/url', '').strip().lower()
    if not query:
        bot.reply_to(message, "اكتب واش راك تحوس (مثلا: /url shahid)")
        return

    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            # نحوسوا على الكلمة في الملف اللي تعمر بالصيد
            results = [line.strip() for line in f if query in line.lower()]
            if results:
                bot.reply_to(message, f"🎯 لقيتلك هادو لـ {query}:\n\n" + "\n".join(results[:15]))
            else:
                bot.reply_to(message, f"❌ مالقيتش '{query}' في الصيد الجديد.")
    else:
        bot.reply_to(message, "⏳ الماكينة راهي تجمع، اصبر شوية.")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    print("🚀 الماكينة بدأت تزغرد... الصيد والاستخراج شغالين!")
    threading.Thread(target=run_bot, daemon=True).start()
    client.start()
    client.run_until_disconnected()
