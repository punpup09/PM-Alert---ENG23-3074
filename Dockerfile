FROM python:3.11-slim

# กำหนด Working Directory
WORKDIR /app

# Copy ไฟล์จากเครื่องเราเข้าไปใน Container
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# เปิดพอร์ต 5000 ตามที่ Flask รัน
EXPOSE 5000

# สั่งให้แอปทำงาน
CMD ["python", "app.py"]
