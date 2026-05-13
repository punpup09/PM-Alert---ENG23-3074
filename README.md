🚀 PM-Alert — ENG23 3074
> แอปพลิเคชันสำหรับตรวจสอบคุณภาพอากาศ PM2.5 แบบเรียลไทม์ พร้อมระบบ CI/CD, Kubernetes deployment และ Monitoring ด้วย Prometheus/Grafana อัตโนมัติ

---

## 👥 สมาชิกในกลุ่ม

| รหัสนักศึกษา | ชื่อ-นามสกุล | ความรับผิดชอบ |
| :--- | :--- | :--- |
| B6608972 | พชร โจชัวร์ คริกเค | Git, App Development |
| B6628895 | ธัญเทพ คู่ชัยภูมิ | Jenkins, Docker |
| B6611859 | พิชญุตม์ พิมพ์ภาค | Terraform, Ansible |
| B6628239 | กิตติธัช แช่มขุนทด | Kubernetes, Monitoring |

---

## 📌 ภาพรวมโปรเจค

### แอปพลิเคชัน
* **ชื่อ:** PM-Alert
* **ประเภท:** Web App / REST API
* **ภาษา / Framework:** Python / Flask
* **คำอธิบาย:** PM-Alert เป็นแอปพลิเคชันเฝ้าระวังคุณภาพอากาศ PM2.5 แบบเรียลไทม์ โดยดึงข้อมูลจาก DustBoy API (CMU CCDC) มาแสดงผลบนหน้า Dashboard เพื่อติดตามมลพิษในพื้นที่และให้คำแนะนำการปฏิบัติตัวด้านสุขภาพตามเกณฑ์มาตรฐาน TH AQI ของประเทศไทย

### Architecture Diagram
```text
Developer
    │
    ▼  git push
 GitHub ──── webhook ────▶ Jenkins CI/CD
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                 Build        Test      Docker Build
                                            │
                                            ▼
                                       Docker Hub
                                            │
                                    ┌───────┴───────┐
                                    ▼               ▼
                                Terraform        Ansible
                                    │               │
                                    └───────┬───────┘
                                            ▼
                                   Kubernetes Cluster
                                   ┌────────────────┐
                                   │  Pod 1  Pod 2  │
                                   │  [App]  [App]  │
                                   │                │
                                   │  Service (NodePort :30001)  │
                                   └────────────────┘
                                            │
                              ┌─────────────┴──────────────┐
                              ▼                             ▼
                          Prometheus  ──────────────▶  Grafana
                        (scrape /metrics)            (dashboard)
```

---

## 📁 โครงสร้าง Repository

```text
PM-Alert/
├── app/
│   ├── app.py                  # โค้ดหลักของแอปพลิเคชัน Flask
│   ├── test_app.py             # โค้ดสำหรับ Unit Test
│   ├── test_api.py             # โค้ดสำหรับทดสอบดึงข้อมูล API 
│   ├── requirements.txt        # Python dependencies
│   └── templates/              # โฟลเดอร์เก็บไฟล์ HTML
│       └── index.html          # หน้า Dashboard ของแอป
├── Dockerfile                  # คำสั่งสร้าง Docker image ของแอปพลิเคชัน
├── Dockerfile.jenkins          # คำสั่งสร้าง Custom Jenkins Image
├── Jenkinsfile                 # กำหนด CI/CD pipeline ทุก stage
├── terraform/
│   ├── main.tf                 # กำหนด resource ที่จะ provision
│   ├── variables.tf            # ตัวแปร input
│   ├── outputs.tf              # ค่า output หลัง apply
│   └── inventory.tpl           # Template สำหรับสร้างไฟล์ Ansible inventory
├── ansible/
│   ├── inventory               # รายชื่อ host เป้าหมาย (สร้างโดย Terraform)
│   └── playbook.yml            # tasks สำหรับ configure environment บน Kubernetes
├── k8s/
│   ├── deployment.yaml         # กำหนด Pods และ replicas
│   └── service.yaml            # เปิดพอร์ต NodePort (30001) ให้เข้าถึงแอปจากภายนอก
├── monitoring/
│   ├── prometheus.yml          # ตั้งค่า scrape target
│   └── grafana-dashboard.json  # Dashboard ที่ export จาก Grafana
└── README.md
```

---

## ⚙️ สิ่งที่ต้องติดตั้งก่อน (Prerequisites)

ตรวจสอบให้แน่ใจว่าติดตั้งทุก tool ครบก่อนรันโปรเจค

| Tool | Version | หน้าที่ |
| :--- | :--- | :--- |
| **Git** | ≥ 2.x | จัดการ source code |
| **Docker** | ≥ 24.x | สร้างและรัน container |
| **Jenkins** | ≥ 2.4xx | ระบบ CI/CD automation |
| **Terraform** | ≥ 1.x | Provision infrastructure |
| **Ansible** | ≥ 2.15 | Configure environment |
| **kubectl** | ≥ 1.28 | สั่งงาน Kubernetes cluster |
| **Minikube / K3s** | latest | Kubernetes แบบ local |
| **Python** | 3.9 - 3.11 | รันแอปพลิเคชันแบบ Local |
| **Prometheus** | ≥ 2.x | เก็บ metrics |
| **Grafana** | ≥ 10.x | แสดง dashboard |

---

## 🏃 วิธีรันโปรเจค (Quick Start)

### 1. Clone Repository
```bash
git clone https://github.com/[username]/PM-Aleart---ENG23-3074.git
cd PM-Aleart---ENG23-3074
```

### 2. รันแอปบนเครื่องโดยตรง (ไม่ผ่าน pipeline)
```bash
cd app
pip install -r requirements.txt
# (ทางเลือก) กำหนด API Key: export DUSTBOY_API_KEY="your_api_key_here"
# สำหรับ Mac/Linux/Git Bash:
export DUSTBOY_API_KEY="your_api_key_here"

# สำหรับ Windows (PowerShell):
$env:DUSTBOY_API_KEY="your_api_key_here"

python app.py
# แอปรันที่ http://localhost:5000
```

### 3. Build และรันด้วย Docker
```bash
docker build -t tanyathep/pm-alert-app:latest .
docker run -p 5000:5000 -e DUSTBOY_API_KEY="your_api_key_here" tanyathep/pm-alert-app:latest
```

---

## 🔄 CI/CD Pipeline (Jenkins)

### ลำดับการทำงานของ Pipeline
```text
Checkout ──▶ Static Analysis ──▶ Unit Test ──▶ Docker Build ──▶ Push to Hub ──▶ Deploy
```

| Stage | คำอธิบาย |
| :--- | :--- |
| **Checkout** | ดึงโค้ดล่าสุดจาก GitHub |
| **Static Analysis** | ตรวจสอบ syntax โค้ด Python |
| **Unit Test** | สร้าง venv, ติดตั้ง dependencies และรัน `unittest` |
| **Docker Build** | สร้าง Docker image ของแอปพลิเคชัน |
| **Push to Docker Hub**| อัปโหลด image ขึ้น Docker Hub โดยใช้ credentials `dockerhub-auth` |
| **Deploy** | ตรวจสอบ syntax ของ Ansible และรัน Terraform apply ซึ่งจะทำหน้าที่เรียก Ansible ไป Deploy บน Kubernetes อีกที |

### วิธีตั้งค่า Jenkins
1. ติดตั้ง Jenkins และเปิดที่ `http://localhost:8080`
2. ติดตั้ง plugin: Git, Pipeline, Docker Pipeline
3. เพิ่ม credentials สำหรับ Docker Hub (ชื่อ `dockerhub-auth`)
4. สร้าง Pipeline job ใหม่ และชี้ไปที่ repository นี้
5. ตั้งค่า Webhook ใน GitHub ไปที่ `http://[jenkins-host]:8080/github-webhook/` ติ๊กเหตุการณ์ Push events (หากรัน Jenkins บนเครื่อง Local ต้องใช้เครื่องมืออย่าง Ngrok เพื่อแปลงเป็น Public URL ก่อน)

---

## 🏗️ Infrastructure as Code

### Terraform — Provision Infrastructure
```bash
cd terraform
terraform init      # ดาวน์โหลด provider plugins
terraform plan      # ตรวจสอบว่าจะสร้างอะไรบ้าง
terraform apply     # สร้าง resource จริง
```
> **สิ่งที่ Terraform สร้าง:** เตรียม Minikube cluster, สร้าง Kubernetes namespace `dustwatch`, และนำ template มาสร้างเป็นไฟล์ `ansible/inventory` ให้กับ Ansible

### Ansible — Configure Environment
```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```
> **สิ่งที่ Ansible ทำ:** ช่วยติดตั้ง dependencies เพิ่มเติม, สร้าง namespace, apply ไฟล์ deployment และ service ลงใน Kubernetes, เซ็ตอัป docker image ของแอปพลิเคชัน, และตรวจสอบ rollout status
> ⚠️ **หมายเหตุ:** ใน pipeline จริง Jenkins จะเรียก Terraform ซึ่งจะเรียกใช้ Ansible อัตโนมัติในขั้นตอน Deploy ไม่ต้องรันด้วยมือ

---

## ☸️ Kubernetes Deployment

### Apply Manifests ด้วยตัวเอง
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### ตรวจสอบสถานะ
```bash
kubectl get pods -n dustwatch
kubectl get svc -n dustwatch
```

### ผลลัพธ์ที่ควรจะได้
```text
NAME                        READY   STATUS    RESTARTS   AGE
pm-alert-xxxxxxxxx-xxxxx    1/1     Running   0          2m
pm-alert-xxxxxxxxx-yyyyy    1/1     Running   0          2m

NAME               TYPE       CLUSTER-IP     PORT(S)          AGE
pm-alert-service   NodePort   10.96.xx.xxx   80:30001/TCP   2m
```

### เข้าถึงแอปพลิเคชัน
```text
วิธีที่ 1 (ผ่าน NodePort): http://localhost:30001
วิธีที่ 2 (เจาะพอร์ตตรง หากวิธีแรกไม่ทำงาน):
kubectl port-forward -n dustwatch svc/pm-alert-service 5000:80
แล้วเข้าผ่าน http://localhost:5000
```

---

## 📊 Monitoring

### Prometheus — เก็บ Metrics
* **ไฟล์ config:** `monitoring/prometheus.yml`
* **Scrape:** ทุก 15 วินาที
* **Target endpoint:** `http://[app-host]:5000/metrics`

**รัน Prometheus:**
```bash
prometheus --config.file=monitoring/prometheus.yml
# เปิด UI ที่ http://localhost:9090
```

### Grafana — แสดง Dashboard
* **ไฟล์ dashboard:** `monitoring/grafana-dashboard.json`
* **Data source:** Prometheus (`http://localhost:9090`)

**วิธี import dashboard:**
1. เปิด Grafana ที่ `http://localhost:3001`
2. ไปที่ Dashboards → Import
3. อัปโหลดไฟล์ `grafana-dashboard.json`

**Panels ใน Dashboard**
| Panel | Metric (PromQL) | แสดงข้อมูลอะไร |
| :--- | :--- | :--- |
| PM2.5 Value | `sut_dust_pm25` | ค่าฝุ่นปัจจุบันแบ่งตาม ID สถานี |
| App RAM Usage | `sut_app_ram_bytes` | แรมที่แอปพลิเคชันกำลังใช้งาน |
| App CPU Usage | `sut_app_cpu_percent` | CPU ที่แอปพลิเคชันกำลังใช้งาน |

---

## 🌿 Branching Strategy

```text
main        ──── โค้ดที่พร้อม production, protected branch
dev         ──── รวมโค้ดก่อน merge ขึ้น main
feature/*   ──── พัฒนา feature แต่ละอัน
```

| Branch | Protected | คำอธิบาย |
| :--- | :--- | :--- |
| `main` | ✅ | trigger pipeline อัตโนมัติเมื่อ merge |
| `dev` | ✅ | ทดสอบก่อน merge ขึ้น main |
| `feature/*` | ❌ | พัฒนาแยกกันแล้วค่อย merge เข้า dev |

---

## 🧪 API Endpoints

| Method | Endpoint | คำอธิบาย |
| :--- | :--- | :--- |
| `GET` | `/` | Health check และหน้า UI หลัก (Dashboard) แสดงค่าฝุ่น |
| `GET` | `/metrics` | Prometheus metrics endpoint ส่งข้อมูลออกไปให้ Prometheus นำไปแสดงกราฟ |

---

## 🐛 ปัญหาที่พบบ่อย (Troubleshooting)

**1. แอปพลิเคชันรันได้ปกติ แต่หน้าเว็บไม่แสดงค่าฝุ่น (หรือ /metrics ไม่มีค่า PM2.5 โผล่มา)**
```bash
# สาเหตุ: คอนเทนเนอร์ใน Kubernetes หรือ Docker ไม่มี DUSTBOY_API_KEY ทำให้ข้ามการดึงข้อมูล
# วิธีแก้สำหรับ Kubernetes (ฉีด Key เข้าไปตอนรัน):
kubectl set env deployment/pm-alert DUSTBOY_API_KEY="ใส่คีย์ของคุณตรงนี้" -n dustwatch

# วิธีแก้สำหรับ Docker:
docker run -p 5000:5000 -e DUSTBOY_API_KEY="ใส่คีย์ของคุณตรงนี้" tanyathep/pm-alert-app:latest
```

**2. เข้าเว็บผ่าน K8s NodePort (http://localhost:30001) ไม่ได้บน Windows**
```bash
# สาเหตุ: ข้อจำกัดการทำ Network Mapping ของ Docker Desktop บน Windows
# วิธีแก้: ใช้ท่าไม้ตาย Port-forward เจาะทะลุเข้า Service โดยตรง
kubectl port-forward -n dustwatch svc/pm-alert-service 5000:80
# จากนั้นเข้าเว็บผ่าน http://localhost:5000 ได้เลย
```

**3. เข้า Grafana ไม่ผ่าน หรือรหัสผ่าน admin ไม่ถูกต้อง**
```bash
# สาเหตุ: เข้าผิดพอร์ต (ไปเข้า localhost:3000 ซึ่งอาจชนกับ Service อื่นในเครื่อง)
# วิธีแก้: โปรเจคนี้ตั้งค่าพอร์ต Grafana หลบไว้ที่ 3001 เพื่อป้องกันปัญหา
# URL ที่ถูกต้อง: http://localhost:3001
# Username / Password เริ่มต้น: admin / admin
```

**4. กราฟ PM2.5 ใน Grafana เบิ้ลเป็น 2 แท่งคู่กัน หรือไม่แสดงชื่อสถานีภาษาไทย**
```plaintext
# สาเหตุ: Prometheus ดึงข้อมูลเก่า (ที่ไม่มีชื่อ) และข้อมูลใหม่มาโชว์พร้อมกัน
# วิธีแก้: 
1. แก้ Query (PromQL) ให้กรองเฉพาะข้อมูลที่มีชื่อสถานี: 
   sut_dust_pm25{station_name!=""}
2. ในหน้าตั้งค่า Grafana ช่อง Display Name ให้พิมพ์โค้ดนี้เพื่อดึงชื่อมาโชว์: 
   ${__field.labels.station_name}
```
