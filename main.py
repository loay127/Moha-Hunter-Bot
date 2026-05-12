import telebot
from telethon import TelegramClient, events
import threading
import asyncio
import os

# 1. إعدادات البوت
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إعدادات الصياد (Telethon)
api_id = 'YOUR_API_ID' 
api_hash = 'YOUR_API_HASH'
client = TelegramClient('Moha_Session', api_id, api_hash)

# اسم القناة المستهدفة (تأكد من كتابة اليوزر نيم تاعها بدون @ أو الـ ID)
TARGET_CHANNEL = 'ComplexCloudLogs' 

COMBO_FILE = "ulp.txt"

# 3. وظيفة الصيد من القناة المحددة
@client.on(events.NewMessage(chats=TARGET_CHANNEL))
async def hunter_handler(event):
    msg = event.raw_text
    # نفلترو الرسائل اللي فيها ايميل وباسورد (User:Pass)
    if ":" in msg:
        with open(COMBO_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        print(f"🎯 صيد جديد من القناة: {msg[:30]}...")

# 4. أمر البوت للاستخراج
@bot.message_handler(commands=['url'])
def get_combo(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            # يحوس على الكلمة (مثلا shahid) لداخل السطور اللي صيدناهم
            results = [l.strip() for l in lines if query in l.lower()]
            
            if results:
                bot.reply_to(message, "✅ هاهي الحسابات اللي لقيتها:\n\n" + "\n".join(results[:15]))
            else:
                bot.reply_to(message, f"❌ مالقيتش '{query}' في الصيد تاع القناة ضرك.")
    else:
        bot.reply_to(message, "⏳ الماكينة مزال ما بدأت الصيد، اصبر شوية.")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    client.start()
    client.run_until_disconnected()
