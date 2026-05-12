import telebot
import os
import threading
from telethon import TelegramClient, events

# --- إعدادات البوت (الواجهة) ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)
FILE_PATH = 'MEGA_STORM_ULP.txt'

@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "يا لؤي، راني شغال ونصيد! ابعثلي برك واش تحوس.")

@bot.message_handler(func=lambda m: True)
def search(m):
    if not os.path.exists(FILE_PATH):
        return bot.reply_to(m, "مزال ما كملتش الصيد، اصبر شوية.")
    query = m.text.lower()
    with open(FILE_PATH, 'r') as f:
        res = [l.strip() for l in f if query in l.lower()]
    bot.reply_to(m, f"✅ لقيت {len(res)} نتيجة:\n\n" + "\n".join(res[:15]) if res else "❌ مالقيت والو.")

def run_bot(): bot.infinity_polling()

# --- إعدادات سكريبت الصيد (الماكينة) ---
# حط هنا كود الـ Telethon تاعك اللي كان في main.py مقبيل
# ... (الكود القديم تاعك) ...

if __name__ == "__main__":
    # تشغيل البوت في خيط (Thread) منفصل
    threading.Thread(target=run_bot, daemon=True).start()
    
    # هنا كود تشغيل السكريبت تاعك (Client.run_until_disconnected)
    print("الكل شغال ضرك...")
