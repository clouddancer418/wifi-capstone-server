import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("wifi_monitor.db")
cursor = conn.cursor()

spots = {
    "공학관": [("1층 입구", "1"), ("2층 복도", "2"), ("3층 강의실 앞", "3")],
    "도서관": [("1층 열람실 앞", "1"), ("2층 자료실", "2"), ("3층 창가", "3")],
    "본관": [("1층 로비", "1"), ("2층 복도", "2")],
    "학생회관": [("1층 입구", "1"), ("카페 앞", "1"), ("휴게공간", "2")]
}

buildings = list(spots.keys())
base_time = datetime.now() - timedelta(days=3)

for i in range(200):
    hour = random.randint(8, 21)
    building = random.choice(buildings)
    location_name, floor = random.choice(spots[building])

    rssi = random.randint(-90, -45)
    latency = random.randint(10, 400)
    download_speed = round(random.uniform(5, 80), 1)
    link_speed = random.randint(72, 300)

    base_score = 70 + (rssi + 60) * 0.5 - latency * 0.05
    if 12 <= hour <= 14:
        base_score -= 20

    score = max(10, min(100, base_score + random.gauss(0, 5)))
    status = "좋음" if score >= 80 else "보통" if score >= 50 else "나쁨"

    created_at = base_time + timedelta(
        hours=i * 0.5,
        minutes=random.randint(0, 30)
    )

    cursor.execute("""
        INSERT INTO measurements
        (ssid, bssid, rssi, latency, building, download_speed, link_speed,
         score, status, created_at, is_mock, location_name, floor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "mju_wifi",
        f"00:11:22:33:44:{i%256:02x}",
        rssi,
        latency,
        building,
        download_speed,
        link_speed,
        round(score, 1),
        status,
        created_at.strftime("%Y-%m-%d %H:%M:%S"),
        True,
        location_name,
        floor
    ))

conn.commit()
conn.close()

print("mock 데이터 200건 삽입 완료")