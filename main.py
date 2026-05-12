import telebot
import os
import threading
import sys

# إعدادات البوت
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
try:
    bot = telebot.TeleBot(BOT_TOKEN)
    print("✅ تم تجهيز البوت بنجاح")
except Exception as e:
    print(f"❌ مشكل في توكن البوت: {e}")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "يا لؤي راني خدام!")

def run_bot():
    try:
        print("🚀 بدأت عملية تشغيل البوت (Polling)...")
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ البوت توقف بسبب خطأ: {e}")

if __name__ == "__main__":
    print("📡 بداية تشغيل النظام...")
    
    # تشغيل البوت في خيط منفصل
    t = threading.Thread(target=run_bot, daemon=True)
    t.start()
    
    print("⏳ البوت راهو يدور في الخلفية، ضرك نشغلو السكربت الأساسي...")
    
    # هنا حط كود الصيد تاعك (Telethon)
    # ملاحظة: إذا كان كود الصيد فيه غلطة، راح تبان هنا في GitHub
    try:
        # مثال بسيط للتجربة، عاود حط كود الصيد تاعك هنا
        print("🎮 سكريبت الصيد بدأ...")
        # إذا عندك loop.run_until_complete حطها هنا
        while True: # هادي باش السكربت ما يحبسش في GitHub
            import time
            time.sleep(10)
            print("🕒 النظام مازال حي...")
    except Exception as e:
        print(f"❌ خطأ قاتل في سكريبت الصيد: {e}")
