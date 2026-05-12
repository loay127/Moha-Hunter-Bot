import telebot
from telethon import TelegramClient, events
import threading
import os

# إعداداتك
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
TARGET_CHANNEL = 'ComplexCloudLogs'
COMBO_FILE = "ulp.txt"

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', api_id, api_hash)

# أول ما يلقى حساب يبعثولك فوراً في تليجرام (مش لازم تستنى الملف)
@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter(event):
    msg = event.raw_text
    if ":" in msg:
        with open(COMBO_FILE, "a") as f:
            f.write(msg + "\n")
        # يبعثلك "صيد طري" فوراً
        bot.send_message(CHAT_ID_TA3EK, f"🎯 صيد جديد:\n{msg}")

@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r") as f:
            res = [line for line in f if query in line.lower()]
            bot.reply_to(message, "\n".join(res[:10]) if res else "❌ مالقيت والو")
    else:
        bot.reply_to(message, "⏳ الماكينة راهي تجمع، اصبر شوية")

def start():
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    start()
