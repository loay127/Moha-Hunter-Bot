import telebot
import threading
import time
import os

# 1. إعداد البوت
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)

# اسم الملف اللي راح يتصيد فيه الكومبو
COMBO_FILE = "ulp.txt"

# 2. وظيفة الصيد (تشتغل في الخلفية)
def start_hunting():
    print("🚀 الماكينة بدأت الصيد في الخلفية...")
    while True:
        try:
            # هنا تحط كود السكربت اللي يصيد (Telethon أو غيره)
            # كمثال: راح نكتب سطر تجريبي باش تتأكد بلي الملف شغال
            with open(COMBO_FILE, "a", encoding="utf-8") as f:
                f.write("shahid.net:loay_pro:password123\n")
            
            print(f"✅ تم تحديث {COMBO_FILE}")
            time.sleep(60) # يصيد كل دقيقة
        except Exception as e:
            print(f"❌ خطأ في الصيد: {e}")
            time.sleep(10)

# تشغيل وظيفة الصيد في "خيط" (Thread) منفصل
threading.Thread(target=start_hunting, daemon=True).start()

# 3. أوامر البوت في تليجرام
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "يا لؤي، البوت والصياد راهم خدامين 100%! 🎯\nاستعمل /url + اسم الموقع باش نجبدلك الحسابات.")

@bot.message_handler(commands=['url'])
def search_combo(message):
    # نجبدو الكلمة اللي كتبتها مورا /url
    query = message.text.replace('/url', '').strip().lower()
    
    if not query:
        bot.reply_to(message, "لازم تكتب واش راك تحوس، مثلاً: /url shahid")
        return

    bot.reply_to(message, f"🔎 جاري البحث عن '{query}' في ملفات ULP...")

    results = []
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if query in line.lower():
                    results.append(line.strip())
                if len(results) >= 15: # نبعثو أول 15 حساب لقاه
                    break
    
    if results:
        bot.reply_to(message, "✅ لقيتلك هاد الحسابات:\n\n" + "\n".join(results))
    else:
        bot.reply_to(message, f"❌ مالقيت حتى حساب خاص بـ '{query}' حالياً.")

# 4. تشغيل البوت
print("🤖 البوت راهو يدور ضرك...")
bot.infinity_polling()
