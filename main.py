from telethon import TelegramClient, functions, types
import re
import os

# --- إعدادات الحساب ---
API_ID = 34023364
API_HASH = 'ad07473755a47402aef9c3d580886cdf'

# --- القناة الواحدة للتجربة ---
# حط هنا يوزر القناة اللي راك حاب تتيستي بيها (بدون @)
TARGET_CHANNEL = 'COMPLEX CL*UD|L*GS' 

TARGET_FILE = "TEST_EXTRACT.txt"
client = TelegramClient('Moha_Session', API_ID, API_HASH)

async def main():
    print(f"--- جاري بدء التيست على قناة: {TARGET_CHANNEL} ---")
    
    try:
        # محاولة الوصول للقناة
        entity = await client.get_entity(TARGET_CHANNEL)
        print(f"[+] تم الاتصال بالقناة بنجاح: {entity.title}")
        
        count = 0
        # فحص آخر 50 رسالة فقط للتيست السريع
        async for message in client.iter_messages(entity, limit=50):
            
            # سحب الحسابات من الملفات
            if message.document and (message.file.ext in ['.txt', '.log']):
                print(f"   [*] جاري تحميل ملف: {message.file.name}")
                path = await message.download_media()
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    with open(TARGET_FILE, "a", encoding='utf-8') as out:
                        for line in f:
                            matches = re.findall(r'([a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9._-]+):([a-zA-Z0-9!@#$%^&*._-]+)', line)
                            for m in matches:
                                out.write(f"{m[0]}:{m[1]}\n")
                                count += 1
                os.remove(path)
                
            # سحب الحسابات من النصوص
            elif message.text:
                matches = re.findall(r'([a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|[a-zA-Z0-9._-]+):([a-zA-Z0-9!@#$%^&*._-]+)', message.text)
                if matches:
                    with open(TARGET_FILE, "a", encoding='utf-8') as out:
                        for m in matches:
                            out.write(f"{m[0]}:{m[1]}\n")
                            count += 1
        
        print(f"\n[DONE] التيست خلص. لقيت {count} حساب.")
        print(f"تلقاهم في ملف: {TARGET_FILE}")

    except Exception as e:
        print(f"[!] كاين مشكلة في الوصول لهاد القناة: {e}")

with client:
    client.loop.run_until_complete(main())
