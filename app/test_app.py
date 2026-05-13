import unittest
from app.app import app # ดึงแอป Flask ของเรามาทดสอบ

class BasicTests(unittest.TestCase):
    def setUp(self):
        # เปิดโหมด Testing และสร้างหุ่นยนต์จำลองการเข้าเว็บ (Test Client)
        app.testing = True
        self.client = app.test_client()

    def test_main_page_is_working(self):
        # 1. หุ่นยนต์จำลองการเข้าหน้าเว็บหลัก
        response = self.client.get('/')
        # 2. เช็คว่าเซิร์ฟเวอร์ตอบกลับมาเป็น 200 (OK) หรือไม่
        self.assertEqual(response.status_code, 200, "หน้าเว็บหลัก (/) ใช้งานไม่ได้!")

    def test_metrics_page_is_working(self):
        # 1. หุ่นยนต์จำลองการเข้าหน้าของ Prometheus
        response = self.client.get('/metrics')
        # 2. เช็คว่าเซิร์ฟเวอร์ตอบกลับมาเป็น 200 (OK) หรือไม่
        self.assertEqual(response.status_code, 200, "หน้า /metrics ใช้งานไม่ได้!")

if __name__ == "__main__":
    unittest.main()