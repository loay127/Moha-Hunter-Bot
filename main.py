import telebot
from telethon import TelegramClient, events
import threading
import re
import os

# --- الإعدادات (ثابتة) ---
BOT_TOKEN = '8645297843:AAE7x0GWqbXlJRNv7I2Qt14nenCEL9IiIs8'
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'

# اسم قناتك المستودع
MY_STORAGE = 'MyUlpStorage_Loay' 

COMBO_FILE = "ulp.txt"
bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('Moha_Session', API_ID, API_HASH)

async def start_harvesting():
    await client.start()
    print("🔍 جاري البحث عن قناة COMPLEX CL*UD...")
    
    source_entity = None
    # يبحث في كامل القنوات اللي راك داخل فيها
    async for dialog in client.iter_dialogs():
        if "COMPLEX CL" in dialog.name: # يبحث بالاسم لداخل القائمة
            source_entity = dialog.entity
            print(f"✅ لقيت القناة! الـ ID تاعها هو: {source_entity.id}")
            break
    
    if not source_entity:
        print("❌ مالقيتش القناة، تأكد بلي الحساب راهو داخل فيها!")
        return

    try:
        storage_entity = await client.get_entity(MY_STORAGE)
        
        # سحب الملفات القديمة (limit=200 باش ما يتبلوكااش)
        async for message in client.iter_messages(source_entity, limit=200):
            if message.document and (message.file.ext in ['.txt', '.log']):
                print(f"📥 سحب ملف: {message.file.name}")
                await client.send_message(storage_entity, message) # تحويل لقناتك
                
                # استخراج البيانات
                path = await message.download_media()
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    matches = re.findall(r'([a-zA-Z0-9._-]+:[a-zA-Z0-9!@#$%^._-]+)', f.read())
                    if matches:
                        with open(COMBO_FILE, "a", encoding='utf-8') as out:
                            for m in matches: out.write(f"{m}\n")
                os.remove(path)
        
        print("✅ كملت السحب القديم، راني نعس في الجديد ضرك!")

        @client.on(events.NewMessage(chats=source_entity))
        async def handler(event):
            if event.message.document and (event.message.file.ext in ['.txt', '.log']):
                await client.send_message(storage_entity, event.message)
                print("🆕 ملف جديد وصل وحولته!")

        await client.run_until_disconnected()

    except Exception as e:
        print(f"❌ كاين مشكل: {e}")

# أمر البحث
@bot.message_handler(commands=['url'])
def search(message):
    query = message.text.replace('/url', '').strip().lower()
    if os.path.exists(COMBO_FILE):
        with open(COMBO_FILE, "r", encoding="utf-8", errors="ignore") as f:
            res = [l.strip() for l in f if query in l.lower()]
            if res: bot.reply_to(message, f"🎯 هاك واش صيدت لـ {query}:\n\n" + "\n".join(res[:15]))
            else: bot.reply_to(message, "❌ مكانش هاد الموقع.")
    else:
        bot.reply_to(message, "⏳ الماكينة تجمع...")

if __name__ == "__main__":
    threading.Thread(target=lambda: bot.infinity_polling(), daemon=True).start()
    client.loop.run_until_complete(start_harvesting())
