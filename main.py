import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# --- الإعدادات ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'

SOURCE_CHANNEL = 'ComplexCloudLogs' 
MY_PRIVATE_CHANNEL = 'MyUlpStorage_Loay' # تأكد من أن هذا هو اليوزر الصحيح لقناتك

COMBO_FILE = "ulp.txt"
bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

async def process_and_forward(message):
    # إذا كانت الرسالة فيها ملف txt أو log
    if message.document and (message.file.ext in ['.txt', '.log']):
        print(f"📥 جاري سحب ملف: {message.file.name}")
        # يحول الملف لقناتك مباشرة
        await client.send_message(MY_PRIVATE_CHANNEL, message)
        
        # استخراج الحسابات للملف المحلي للبحث
        path = await message.download_media()
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^&*._-]+)', f.read())
            if matches:
                with open(COMBO_FILE, "a", encoding='utf-8') as out:
                    for m in matches:
                        out.write(f"{m}\n")
        os.remove(path)

# يستقبل الرسائل الجديدة
@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    await process_and_forward(event.message)

async def start_harvesting():
    await client.start()
    print(f"🚀 بدأت عملية الكشط من {SOURCE_CHANNEL}...")
    
    # يروح يجيب "كل" الملفات القديمة (تقدر تزيد الـ limit لـ 1000 مثلاً)
    async for message in client.iter_messages(SOURCE_CHANNEL, limit=500):
        await process_and_forward(message)
        
    print("✅ كملت سحب الملفات القديمة. ضرك راني عاس القناة على أي ملف جديد!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(start_harvesting())
