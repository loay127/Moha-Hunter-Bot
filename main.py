import telebot
import os
import threading
import time
from telethon import TelegramClient, events

# --- 1. إعدادات البوت (الواجهة) ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)
FILE_PATH = 'MEGA_STORM_ULP.txt'

@bot.message_handler(commands=['start'])
def start(m): 
    bot.reply_to(m, "يا لؤي، راني شغال ونصيد! ابعثلي برك واش تحوس.")

@bot.message_handler(func=lambda m: True)
def search(m):
    if not os.path.exists(FILE_PATH):
        return bot.reply_to(m, "مزال ما كملتش الصيد، اصبر شوية الملف مازال ما تكرياش.")
    
    query = m.text.lower()
    results = []
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if query in line.lower():
                results.append(line.strip())
    
    if results:
        bot.reply_to(m, f"✅ لقيت {len(results)} نتيجة:\n\n" + "\n".join(results[:15]))
    else:
        bot.reply_to(m, "❌ مالقيت والو في الملف.")

def run_bot():
    print("بدأ تشغيل البوت...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

# --- 2. إعدادات سكريبت الصيد (الماكينة) ---
# ملاحظة: حط هنا الـ API_ID و API_HASH تاعك باش يخدم Telethon
api_id = 'YOUR_API_ID' 
api_hash = 'YOUR_API_HASH'
client = TelegramClient('session_name', api_id, api_hash)

async def scraper_main():
    print("بدأ تشغيل سكريبت الصيد (Telethon)...")
    await client.start()
    # هنا حط الكود تاع الصيد تاعك (الـ handlers والـ events)
    # مثال:
    # @client.on(events.NewMessage)
    # async def handler(event): ...
    
    await client.run_until_disconnected()

# --- 3. التشغيل النهائي ---
if __name__ == "__main__":
    # تشغيل البوت في خيط (Thread) منفصل باش ما يبلوركيش السكربت
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # تشغيل سكريبت الصيد في الخيط الرئيسي
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(scraper_main())
    except Exception as e:
        print(f"صرا مشكل في السكربت: {e}")
        # إذا حبس السكربت، نخلو البوت شغال
        while True:
            time.sleep(1)
