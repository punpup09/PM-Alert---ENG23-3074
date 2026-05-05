# 🌬️ SafeBreathe Gateway

**SafeBreathe Gateway** เป็นแอปพลิเคชันสำหรับการตรวจสอบคุณภาพอากาศ (PM2.5) และให้คำแนะนำด้านความปลอดภัยแบบเรียลไทม์ โดยดึงข้อมูลจาก **DustBoy API (CMU CCDC)** โปรเจคนี้ถูกออกแบบมาเพื่อรองรับสถาปัตยกรรมแบบ Cloud-Native และสามารถทำงานร่วมกับระบบ CI/CD (Jenkins), Kubernetes และระบบ Monitoring (Prometheus/Grafana) ได้อย่างสมบูรณ์

## 🌟 ฟีเจอร์หลัก (Key Features)
*   **Real-time Monitoring:** ดึงข้อมูลค่าฝุ่น PM2.5 จากสถานีตรวจวัดจริง
*   **Action Logic:** ประมวลผลและให้คำแนะนำด้านสุขภาพโดยอัตโนมัติ (เช่น Safe, Danger)
*   **Mock Mode:** รองรับโหมดจำลองข้อมูลอัตโนมัติหากไม่ได้ใส่ API Key เพื่อให้ระบบยังคงทำงานได้โดยไม่พัง
*   **Prometheus Integration:** มี Endpoint `/metrics` สำหรับให้ Prometheus ดึงข้อมูลไปทำกราฟบน Grafana
*   **Dockerized:** บรรจุแอปพลิเคชันลงใน Docker Container เพื่อความสะดวกในการ Deploy

---

## 📁 โครงสร้างโปรเจค (Project Structure)
```text
│
├── app/                        ← คน 1 (App Developer)
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
│       └── index.html
│
├── Dockerfile                  ← คน 1
│
├── Jenkinsfile                 ← คน 2 (CI/CD Engineer)
│
├── terraform/                  ← คน 3 (เรา) ✅
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── inventory.tpl
│
├── ansible/                    ← คน 3 (เรา) ✅
│   ├── inventory
│   └── playbook.yml
│
├── k8s/                        ← คน 4 (Platform)
│   ├── deployment.yaml
│   └── service.yaml
│
├── monitoring/                 ← คน 4 (Platform)
│   ├── prometheus.yml
│   └── grafana-dashboard.json
│
└── README.md                   ← คน 1 (ทุกคนช่วยเขียน)


## 🚀 วิธีการติดตั้งและรันแอปพลิเคชัน (Setup Instructions)

โปรเจคนี้รองรับการทำงาน 2 รูปแบบ ทั้งแบบ Local Development และแบบ Docker Container

### ตัวเลือกที่ 1: รันบนเครื่องโดยตรง (Local / Python)
เหมาะสำหรับการพัฒนาและทดสอบโค้ดเบื้องต้น

1. **ติดตั้ง Library ที่จำเป็น:**
   ```bash
   pip install -r app/requirements.txt

2. **กำหนดค่า Environment (ทางเลือก)**
    หากคุณมี API Key จาก CMU CCDC ให้ตั้งค่าตัวแปรแวดล้อมดังนี้ (หากไม่มี ระบบจะใช้ Mock Mode อัตโนมัติ)
    $env:DUSTBOY_API_KEY="your_api_key_here"

3. **รันแอปพลิเคชัน:**
    python app/app.py

4. **เข้าใช้งาน::**
    เปิดเว็บเบราว์เซอร์และไปที่: http://localhost:5000


### ตัวเลือกที่ 2: รันด้วย Docker (Production / CI/CD)
เหมาะสำหรับการจำลองสภาพแวดล้อมจริงก่อนนำไป Deploy บน Kubernetes

1. **สร้าง Docker Image (Build):**
    รันคำสั่งนี้ในโฟลเดอร์หลักของโปรเจค (ที่มีไฟล์ Dockerfile):
    docker build -t safebreathe-app .

2. **รัน Docker Container:**
    docker run -p 5000:5000 safebreathe-app
    *(หากต้องการรันพร้อม API Key ให้เพิ่ม `-e DUSTBOY_API_KEY="your_api_key"` เข้าไปในคำสั่ง)*

3. **เข้าใช้งาน:**
    เปิดเว็บเบราว์เซอร์และไปที่: `http://localhost:5000`

## 📡 โครงสร้าง API (Endpoints)
แอปพลิเคชันนี้มีหน้าต่างสำหรับการแสดงผลและการมอนิเตอร์ดังนี้:
* **`GET /`** : หน้า UI หลัก (Dashboard) สำหรับแสดงค่าฝุ่นปัจจุบันและคำแนะนำ
* **`GET /metrics`** : หน้าสำหรับให้ระบบ **Prometheus** เข้ามาดึงข้อมูล (Scrape) ค่าฝุ่นไปแสดงผลบน **Grafana**