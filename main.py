import telebot
from telethon import TelegramClient, events
import threading
import asyncio
import os

# 1. إعدادات البوت (التوكن تاعك)
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إعدادات الصياد (الـ Hash والـ API ID تاعك)
api_id = 'YOUR_API_ID' 
api_hash = 'YOUR_API_HASH'
client = TelegramClient('Moha_Session', api_id, api_hash)

# اسم الملف اللي راح يتصنع ويتحدث آلياً
COMBO_FILE = "ulp.txt"

# 3. وظيفة الصيد: تسمع للقنوات وتخزن في الملف
@client.on(events.NewMessage)
async def my_event_handler(event):
    message_text = event.raw_text
    # هنا الكود يفلتر الرسائل ويجبد الحسابات (User:Pass)
    if ":" in message_text: 
        with open(COMBO_FILE, "a", encoding="utf-8") as f:
            f.write(message_text + "\n")
        print("✅ تم صيد حساب جديد وحفظه!")

# 4. أوامر البوت للاستخراج
@bot.message_handler(commands=['url'])
def get_combo(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r") as f:
            lines = f.readlines()
            results = [l for l in lines if query in l.lower()]
            if results:
                bot.reply_to(message, "✅ لقيتلك هادو من الصيد الحالي:\n\n" + "\n".join(results[:10]))
            else:
                bot.reply_to(message, "❌ مزال ما صيدناش حسابات لهاد الموقع.")
    else:
        bot.reply_to(message, "⏳ الماكينة بدأت ضرك، مزال ما تعمرش الملف.")

# وظيفة لتشغيل البوت والصياد معاً
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في خيط منفصل
    threading.Thread(target=run_bot, daemon=True).start()
    # تشغيل الصياد (Telethon)
    client.start()
    client.run_until_disconnected()
