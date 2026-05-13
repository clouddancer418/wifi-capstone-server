import sqlite3

conn = sqlite3.connect("wifi_monitor.db")
cur = conn.cursor()

render_rows = [

    (
        10001,
        "MJU-WIFI",
        "00:11:22:33:44:55",
        -55,
        30.5,
        "공학관",
        4,
        83.3,
        "좋음",
        "2026-05-05T13:08:59",
        100,
        866,
        0,
        "공학관 4층"
    ),

    (
        10002,
        "MJU-WIFI",
        "00:11:22:33:44:55",
        -55,
        30.5,
        "공학관",
        4,
        83.3,
        "좋음",
        "2026-05-05T13:00:28",
        100,
        866,
        0,
        "공학관 4층"
    )

]

for row in render_rows:

    try:
        cur.execute("""
        INSERT INTO measurements (
            id,
            ssid,
            bssid,
            rssi,
            latency,
            building,
            floor,
            score,
            status,
            created_at,
            download_speed,
            link_speed,
            is_mock,
            location_name
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, row)

        print("추가 성공:", row[0])

    except Exception as e:
        print("추가 실패:", e)

conn.commit()

cur.execute("SELECT COUNT(*) FROM measurements")
print("최종 데이터 개수:", cur.fetchone()[0])

conn.close()