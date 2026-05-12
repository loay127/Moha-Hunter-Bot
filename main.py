import telebot
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

# إعداداتك
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
api_id = 34023364
api_hash = 'ad07473755a47402aef9c3d580886cdf'
session_str = os.getenv('TELEGRAM_SESSION')
my_storage = 'MyUlpStorage_Loay'

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient(StringSession(session_str), api_id, api_hash)
client.start()

@bot.message_handler(commands=['url'])
def search_handler(message):
    query = message.text.replace('/url ', '').strip()
    if not query:
        bot.reply_to(message, "🔍 اكتب الرابط، مثال: /url target.com")
        return

    bot.reply_to(message, "🔎 جاري فحص المخزن...")
    
    results = []
    # البحث في القناة العامة
    for msg in client.iter_messages(my_storage, search=query):
        results.append(msg.text)
    
    if results:
        with open("res.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(results))
        with open("res.txt", "rb") as d:
            bot.send_document(message.chat.id, d, caption=f"✅ وجدنا {len(results)} نتيجة.")
    else:
        bot.reply_to(message, "❌ ملقينا والو.")

bot.polling()
