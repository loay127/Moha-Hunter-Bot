import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# --- الإعدادات ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'

# القنوات اللي تحب تسحب منها (المنبع)
SOURCE_CHANNELS = ['ComplexCloudLogs'] 
# قناتك الجديدة اللي ضفتها (المستودع)
MY_PRIVATE_CHANNEL = 'MyUlpStorage_Loay' 

COMBO_FILE = "ulp.txt"
bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

# وظيفة السحب والتحويل لقناتك
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forwarder(event):
    try:
        # 1. يحول الرسالة فوراً لقناتك MyUlpStorage_Loay
        await client.send_message(MY_PRIVATE_CHANNEL, event.message)
        
        # 2. استخراج الحسابات للبحث السريع
        text = ""
        if event.message.text:
            text = event.message.text
        elif event.message.document and event.message.file.ext in ['.txt', '.log']:
            path = await event.message.download_media()
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            os.remove(path)
        
        matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', text)
        if matches:
            with open(COMBO_FILE, "a", encoding='utf-8') as out:
                for m in matches:
                    out.write(f"{m}\n")
            print(f"✅ تم تحويل وصيد {len(matches)} حساب إلى قناتك!")
    except Exception as e:
        print(f"❌ مشكلة في التحويل: {e}")

# أمر البوت للبحث
@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res:
                bot.reply_to(message, f"🎯 لقيتلك هادو في قناتك:\n\n" + "\n".join(res[:15]))
            else:
                bot.reply_to(message, f"❌ مالقيتش '{query}' في الصيد الجديد.")
    else:
        bot.reply_to(message, "⏳ الماكينة راهي تعمر في قناتك، اصبر شوية.")

def run():
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.start()
    client.run_until_disconnected()

if __name__ == "__main__":
    print(f"🚀 الماكينة بدأت تحول الحسابات لقناة: {MY_PRIVATE_CHANNEL}")
    run()
