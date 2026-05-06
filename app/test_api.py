import os
import requests
from dotenv import load_dotenv

# โหลด API Key จากไฟล์ .env
load_dotenv()
API_KEY = os.getenv("DUSTBOY_API_KEY")

print(f"🔑 API Key ที่ใช้: {API_KEY}")
print("📡 กำลังดึงข้อมูลจาก DustBoy...")

# เปลี่ยนบรรทัดนี้
url = f"https://open-api.cmuccdc.org/api/dustboy/station?apikey={API_KEY}"
resp = requests.get(url)

print(f"HTTP Status: {resp.status_code}")

try:
    data = resp.json()
    # เช็คว่าข้อมูลที่ได้มาเป็น List (ปกติ) หรือ Dict (Error)
    if isinstance(data, list):
        print(f"✅ สำเร็จ! ได้ข้อมูลมา {len(data)} สถานี")
        print(f"ตัวอย่างสถานีแรก: {data[0].get('dustboy_name')} -> PM2.5: {data[0].get('pm25')}")
    else:
        print("⚠️ API แจ้งเตือนข้อผิดพลาด (อาจจะติด Limit 10 ครั้ง/ชม.):")
        print(data)
except Exception as e:
    print(f"❌ ระบบพัง ข้อมูลไม่ใช่ JSON: {resp.text}")