from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # ข้อมูลสมมติสำหรับ Mock Mode 
    data = {
        "pm25": 25.5,
        "action": "Safe",
        "time": "2026-05-05 21:00:00"
    }
    return render_template('index.html', 
                           pm25=data["pm25"], 
                           action=data["action"], 
                           last_updated=data["time"])

if __name__ == '__main__':
    # รันบนพอร์ต 5000 เพื่อให้ตรงกับ Dockerfile 
    app.run(host='0.0.0.0', port=5000, debug=True)