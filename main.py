import os
import re
import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# المعلومات الخاصة بك
api_id = 8029330265 
api_hash = 'ad07473755a47402aef9c3d580886cdf'
session_str = os.getenv('TELEGRAM_SESSION')

# اسم القناة المستهدفة
target_channel = 'COMPLEX_CLOUD_LOGS' 

async def run_scraper():
    if not session_str:
        print("❌ خطأ: TELEGRAM_SESSION غير موجود في إعدادات Secrets!")
        return

    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    
    try:
        await client.start()
        print("✅ تم الاتصال بالحساب!")

        # إنشاء الملف في المسار الرئيسي للعمل
        with open("ulp.txt", "w", encoding="utf-8") as f:
            print(f"🔄 جاري سحب البيانات من {target_channel}...")
            
            # سحب آخر 200 رسالة (تقدر تزيد العدد)
            async for message in client.iter_messages(target_channel, limit=200):
                if message.text:
                    # سحب أي نص يشبه الروابط أو صيغ ULP المعينة
                    # هذا النمط يسحب الروابط، يمكنك تعديله حسب صيغة الـ Logs في القناة
                    found_items = re.findall(r'(https?://\S+|[a-zA-Z0-9.-]+:[0-9]+:[a-zA-Z0-9]+:[a-zA-Z0-9]+)', message.text)
                    for item in found_items:
                        f.write(item + "\n")
        
        print("✅ تم إنشاء ملف ulp.txt بنجاح!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء السحب: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(run_scraper())
