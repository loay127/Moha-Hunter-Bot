import telebot
import os

TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
bot = telebot.TeleBot(TOKEN)
FILE_PATH = 'MEGA_STORM_ULP.txt'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلا لؤي! ابعثلي أي كلمة مفتاحية (Keyword) أو رابط حاب تخرج الكومبو تاعو من الداتا.")

@bot.message_handler(func=lambda message: True)
def search_combo(message):
    keyword = message.text.lower()
    results = []
    
    if not os.path.exists(FILE_PATH):
        bot.reply_to(message, "الملف MEGA_STORM_ULP.txt مازال ما تكرياش، لازم السكربت يخدم المرة الأولى.")
        return

    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if keyword in line.lower():
                results.append(line.strip())

    if results:
        count = len(results)
        response = f"✅ لقيتلك {count} نتيجة لـ '{keyword}':\n\n"
        # نبعثو أول 20 نتيجة باش ما تتبلوكااش الرسالة
        response += "\n".join(results[:20])
        if count > 20:
            response += f"\n\n... وكاين {count-20} نتائج أخرى."
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, f"❌ مالقيت والو متعلق بـ '{keyword}' في الداتا.")

bot.polling()
