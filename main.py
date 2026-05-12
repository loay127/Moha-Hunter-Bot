import os
import re
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# المعلومات الخاصة بك
api_id = 8029330265 
api_hash = 'ad07473755a47402aef9c3d580886cdf'
session_str = os.getenv('TELEGRAM_SESSION')

# اسم القناة أو الرابط تاعها
target_channel = 'COMPLEX_CLOUD_LOGS' # تأكد من كتابة اليوزر صحيح بدون @

client = TelegramClient(StringSession(session_str), api_id, api_hash)

async def main():
    try:
        await client.start()
        print("✅ تم الدخول للحساب!")

        # فتح الملف للكتابة
        with open("ulp.txt", "w", encoding="utf-8") as f:
            print(f"🔄 جاري سحب الروابط من {target_channel}...")
            
            # سحب آخر 100 رسالة من القناة (تقدر تزيد العدد)
            async for message in client.iter_messages(target_channel, limit=100):
                if message.text:
                    # استخراج الروابط أو النصوص اللي فيها ULP (مثال: http)
                    urls = re.findall(r'(https?://\S+)', message.text)
                    for url in urls:
                        f.write(url + "\n")
        
        print("✅ تم استخراج الروابط وحفظها في ulp.txt")

    except Exception as e:
        print(f"❌ خطأ: {e}")

with client:
    client.loop.run_until_complete(main())
