import sqlite3

conn = sqlite3.connect("wifi_monitor.db")
cursor = conn.cursor()

# semester_type 컬럼 추가
try:
    cursor.execute(
        "ALTER TABLE measurements ADD COLUMN semester_type TEXT DEFAULT '학기중'"
    )
    print("semester_type 컬럼 추가 완료")
except Exception as e:
    print(f"이미 있거나 오류: {e}")

# 중간고사 기간 데이터는 '시험기간'으로 태깅
cursor.execute("""
    UPDATE measurements
    SET semester_type = '시험기간'
    WHERE date(created_at) IN (
        '2026-04-14', '2026-04-15', '2026-04-16',
        '2026-04-17', '2026-04-18'
    )
""")

conn.commit()

# 확인 출력
cursor.execute("""
    SELECT semester_type, COUNT(*) as count
    FROM measurements
    GROUP BY semester_type
""")

print("\n학기 구분 현황:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}건")

conn.close()