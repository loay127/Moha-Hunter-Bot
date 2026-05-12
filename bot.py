import telebot
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

# الإعدادات
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
api_id = 8029330265
api_hash = 'ad07473755a47402aef9c3d580886cdf'
session_str = os.getenv('TELEGRAM_SESSION')
my_storage_channel = 'https://t.me/+FVbinze0Xk4wYjlk'

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient(StringSession(session_str), api_id, api_hash)
client.start()

@bot.message_handler(commands=['url'])
def search_handler(message):
    query = message.text.replace('/url ', '').strip()
    if not query:
        bot.reply_to(message, "⚠️ أرسل الرابط بعد الأمر، مثال: /url google.com")
        return

    bot.reply_to(message, f"🔍 جاري البحث عن {query} في المخزن...")
    
    results = []
    # البحث داخل رسائل قناتك الخاصة مباشرة
    for msg in client.iter_messages(my_storage_channel, search=query):
        if msg.text:
            results.append(msg.text)
    
    if results:
        # حفظ أول 20 نتيجة في ملف وإرساله
        with open("search_results.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(results))
        
        with open("search_results.txt", "rb") as doc:
            bot.send_document(message.chat.id, doc, caption=f"✅ وجدنا {len(results)} نتيجة لـ {query}")
    else:
        bot.reply_to(message, "❌ لم نجد أي نتائج لهذا الرابط.")

bot.polling()
