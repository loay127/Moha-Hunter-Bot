import telebot
import threading
import time
import os

# معلومات البوت
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)

# وظيفة الصيد (تشتغل في الخلفية)
def hunting_process():
    print("🚀 بدأت عملية الصيد...")
    while True:
        # هنا السكربت يكتب في الملف
        with open("ulp.txt", "a") as f:
            f.write("shahid:user:pass\n") # مثال تجريبي
        print("✅ تم تحديث ملف ulp.txt")
        time.sleep(60) # يصيد كل دقيقة مثلاً

# تشغيل الصيد في Thread منفصل باش ما يحبسش البوت
threading.Thread(target=hunting_process, daemon=True).start()

@bot.message_handler(commands=['url'])
def find_url(message):
    target = message.text.replace('/url ', '')
    if os.path.exists("ulp.txt"):
        with open("ulp.txt", "r") as f:
            lines = f.readlines()
            # يحوس على الكلمة اللي بعثتها
            results = [l for l in lines if target in l]
            if results:
                bot.reply_to(message, "".join(results[:10]))
            else:
                bot.reply_to(message, "❌ مالقيت والو لهاد الموقع")
    else:
        bot.reply_to(message, "⚠️ الملف مزال ما تصنعش، اصبر شوية")

bot.infinity_polling()
