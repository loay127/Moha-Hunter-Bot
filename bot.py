
import telebot
import os
import subprocess
import multiprocessing
import time

TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(TOKEN)
FILE_PATH = 'MEGA_STORM_ULP.txt'

# دالة تشغيل سكربت الصيد (main.py)
def run_scraper():
    print("بدأ تشغيل سكربت الصيد...")
    subprocess.run(["python", "main.py"])

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلا لؤي! راني خدام ضرك، ابعثلي الكلمة اللي تحوس عليها.")

@bot.message_handler(func=lambda message: True)
def search_combo(message):
    keyword = message.text.lower()
    results = []
    if not os.path.exists(FILE_PATH):
        bot.reply_to(message, "الملف مازال ما وجدش، السكربت راهو يجمع في الداتا.")
        return
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if keyword in line.lower():
                results.append(line.strip())
    if results:
        bot.reply_to(message, f"✅ لقيتلك {len(results)} نتيجة:\n\n" + "\n".join(results[:15]))
    else:
        bot.reply_to(message, "❌ مالقيت والو.")

if __name__ == "__main__":
    # تشغيل السكربت في عملية منفصلة
    p = multiprocessing.Process(target=run_scraper)
    p.start()
    
    # تشغيل البوت في العملية الرئيسية
    print("البوت شغال ضرك...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

