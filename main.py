import os
import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# معلوماتك
api_id = 8029330265
api_hash = 'ad07473755a47402aef9c3d580886cdf'
session_str = os.getenv('TELEGRAM_SESSION')

# القناة المصدر وقناتك الجديدة (المخزن)
source_channel = 'COMPLEX_CLOUD_LOGS' 
my_storage_channel = 'https://t.me/+FVbinze0Xk4wYjlk' # قناتك اللي أنشأتها الآن

async def update_storage():
    client = TelegramClient(StringSession(session_str), api_id, api_hash)
    try:
        await client.start()
        print("✅ متصل بالحساب.. جاري تحديث المخزن")
        
        # سحب آخر 100 رسالة وإرسالها لقناتك
        async for message in client.iter_messages(source_channel, limit=100):
            if message.text:
                # نرسل النص مباشرة لقناتك ليكون قابلاً للبحث لاحقاً
                await client.send_message(my_storage_channel, message.text)
        
        print("✅ تم نقل البيانات بنجاح لقناتك.")
    except Exception as e:
        print(f"❌ خطأ: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(update_storage())
