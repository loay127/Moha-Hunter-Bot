import telebot
import os

# توكن البوت تاعك
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(BOT_TOKEN)

# اسم الملف اللي فيه الكومبو (تأكد بلي راهو موجود في GitHub)
COMBO_FILE = "ulp.txt" 

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "يا لؤي، راني واجد للصيد! ابعتلي: /url + اسم الموقع")

@bot.message_handler(commands=['url'])
def hunt_combo(message):
    # نجبدو الكلمة اللي كتبتها مورا /url
    target = message.text.replace('/url ', '').strip()
    
    if not target or target == "/url":
        bot.reply_to(message, "لازم تكتب اسم الموقع، مثلا: /url shahid")
        return

    bot.reply_to(message, f"🔎 راني نحوس على حسابات {target} في الملفات...")
    
    found_accounts = []
    
    # البحث داخل الملف
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if target.lower() in line.lower():
                    found_accounts.append(line.strip())
                
                # باش ما يبعثش بزاف ويتبلوكا، نحددوه بـ 20 حساب مثلا
                if len(found_accounts) >= 20:
                    break
    
    if found_accounts:
        result = "\n".join(found_accounts)
        bot.reply_to(message, f"✅ لقيتلك هادو:\n\n{result}")
    else:
        bot.reply_to(message, f"❌ مالقيت والو خاص بـ {target} في ملف ULP.")

if __name__ == "__main__":
    bot.infinity_polling()
        # مثال بسيط للتجربة، عاود حط كود الصيد تاعك هنا
        print("🎮 سكريبت الصيد بدأ...")
        # إذا عندك loop.run_until_complete حطها هنا
        while True: # هادي باش السكربت ما يحبسش في GitHub
            import time
            time.sleep(10)
            print("🕒 النظام مازال حي...")
    except Exception as e:
        print(f"❌ خطأ قاتل في سكريبت الصيد: {e}")
