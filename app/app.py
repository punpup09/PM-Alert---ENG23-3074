import os
import time
import threading
import requests
from flask import Flask, render_template, request, Response
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from dotenv import load_dotenv
import psutil

load_dotenv()

app = Flask(__name__)

# ==========================================
# 📊 Metrics สำหรับ Prometheus
# ==========================================
APP_RAM_METRIC = Gauge('sut_app_ram_bytes', 'App RAM Usage in Bytes')
APP_CPU_METRIC = Gauge('sut_app_cpu_percent', 'App CPU Usage Percentage')
PM25_METRIC = Gauge('sut_dust_pm25', 'Current PM2.5 value', ['station_id'])

# ==========================================
# 📦 ตัวแปรเก็บข้อมูล (Cache)
# ==========================================
cached_data = {
    "stations": [],
    "last_updated": "N/A"
}

API_KEY = os.getenv("DUSTBOY_API_KEY")

# ==========================================
# ⚙️ ฟังก์ชันทำงานเบื้องหลัง (Background Tasks)
# ==========================================

# 1. ฟังก์ชันดึงข้อมูลระบบ (RAM/CPU)
def update_sys_metrics():
    # เข้าถึง Process ของแอปพลิเคชันนี้
    process = psutil.Process(os.getpid())
    process.cpu_percent() # เรียกครั้งแรกเพื่อเซ็ตฐานคำนวณ
    
    while True:
        try:
            # ดึงค่า RAM (Resident Set Size) และ CPU
            APP_RAM_METRIC.set(process.memory_info().rss)
            APP_CPU_METRIC.set(process.cpu_percent())
        except Exception as e:
            print(f"Metrics Error: {e}")
        
        time.sleep(15) # อัปเดตข้อมูลระบบทุกๆ 15 วินาที

# 2. ฟังก์ชันดึงข้อมูลฝุ่น (DustBoy API)
def fetch_data():
    while True:
        if API_KEY:
            print("\n" + "="*60)
            print(f"📡 [Time: {time.strftime('%H:%M:%S')}] กำลังดึงข้อมูลจาก DustBoy API...")
            url = f"https://open-api.cmuccdc.org/api/dustboy/station?apikey={API_KEY}"
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    data_list = resp.json()
                    if isinstance(data_list, list):
                        cached_data["stations"] = data_list
                        cached_data["last_updated"] = time.strftime('%Y-%m-%d %H:%M:%S')
                        
                        print(f"✅ ดึงข้อมูลสำเร็จ! พบ {len(data_list)} สถานีที่กำลังออนไลน์:")
                        
                        for station in data_list:
                            st_id = station.get('id')
                            st_name = station.get('dustboy_name')
                            pm_val = float(station.get('pm25', 0))
                            
                            # ปริ้นท์สถานะออกทางหน้าจอ Terminal
                            print(f"  📍 ID: {st_id: <5} | PM2.5: {pm_val: <5.1f} | {st_name}")
                            
                            # อัปเดต Metrics ให้ Prometheus
                            PM25_METRIC.labels(station_id=st_id).set(pm_val)
                            
                        print("\n💡 (หมายเหตุ: ไอดีใดที่คุณตั้งไว้ในเว็บแต่ไม่ปรากฏในนี้ แปลว่าสถานีนั้นออฟไลน์ครับ)")
                    else:
                        print("⚠️ รูปแบบข้อมูลที่ตอบกลับมาไม่ถูกต้อง")
                else:
                    # 💡 แก้ไขการย่อหน้าตรงนี้ให้ถูกต้องแล้วครับ!
                    print(f"❌ API Error: โค้ดตอบกลับ HTTP {resp.status_code}")
            except Exception as e:
                print(f"❌ Error ระบบขัดข้อง: {e}")
            print("="*60 + "\n")
            
        # พัก 10 นาที (600 วินาที) เพื่อรักษาโควตา 10 ครั้ง/ชั่วโมง
        time.sleep(600)

# สั่งรัน Thread ทั้ง 2 ตัวให้ทำงานพร้อมกันเบื้องหลัง
threading.Thread(target=update_sys_metrics, daemon=True).start()
threading.Thread(target=fetch_data, daemon=True).start()


# ==========================================
# 🌐 เส้นทางของเว็บไซต์ (Routes)
# ==========================================

@app.route('/')
def index():
    stations = cached_data["stations"]
    selected_id = request.args.get('station_id')
    
    selected_station = None
    if stations:
        if selected_id:
            selected_station = next((s for s in stations if s.get('id') == selected_id), stations[0])
        else:
            selected_station = stations[0]
            
    # ตรรกะ 5 ระดับตามมาตรฐาน TH AQI
    pm25 = 0.0
    status_color = "gray"
    status_text = "ไม่มีข้อมูล"
    status_caption = "รอการเชื่อมต่อข้อมูล"
    
    if selected_station:
        pm25 = float(selected_station.get('pm25', 0))
        if pm25 <= 15.0:
            status_color = "blue"
            status_text = "คุณภาพอากาศดีมาก 🔵"
            status_caption = "เหมาะสำหรับกิจกรรมกลางแจ้งและการท่องเที่ยว"
        elif pm25 <= 25.0:
            status_color = "green"
            status_text = "คุณภาพอากาศดี 🟢"
            status_caption = "สามารถทำกิจกรรมกลางแจ้งได้ตามปกติ"
        elif pm25 <= 37.5:
            status_color = "yellow"
            status_text = "คุณภาพอากาศปานกลาง 🟡"
            status_caption = "ผู้ที่ต้องดูแลสุขภาพเป็นพิเศษควรลดระยะเวลาทำกิจกรรมกลางแจ้ง"
        elif pm25 <= 75.0:
            status_color = "orange"
            status_text = "เริ่มมีผลกระทบต่อสุขภาพ 🟠"
            status_caption = "ควรเฝ้าระวังสุขภาพ ถ้ามีอาการเบื้องต้นควรลดระยะเวลากิจกรรมกลางแจ้ง"
        else:
            status_color = "red"
            status_text = "มีผลกระทบต่อสุขภาพ 🔴"
            status_caption = "ทุกคนควรหลีกเลี่ยงกิจกรรมกลางแจ้ง หลีกเลี่ยงพื้นที่ที่มีมลพิษทางอากาศสูง"

    return render_template('index.html', 
                           stations=stations, 
                           selected_station=selected_station,
                           pm25=pm25, 
                           status_color=status_color,
                           status_text=status_text,
                           status_caption=status_caption,
                           last_updated=cached_data["last_updated"])

@app.route('/metrics')
def metrics():
    # ส่งข้อมูลออกไปโดยระบุว่าเป็นข้อมูล metrics สำหรับ Prometheus โดยเฉพาะ
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)