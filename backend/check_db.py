from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./wifi_monitor_current_backup.db")

with engine.connect() as conn:
    print("\n=== 전체 데이터 수 ===")
    print(conn.execute(text("SELECT COUNT(*) FROM measurements")).fetchone())

    print("\n=== building 목록 ===")
    result = conn.execute(text("""
        SELECT building, COUNT(*)
        FROM measurements
        GROUP BY building
    """))
    for row in result:
        print(row)

    print("\n=== is_mock 분포 ===")
    result = conn.execute(text("""
        SELECT is_mock, COUNT(*)
        FROM measurements
        GROUP BY is_mock
    """))
    for row in result:
        print(row)

    print("\n=== 최신 데이터 10개 ===")
    result = conn.execute(text("""
        SELECT id, building, floor, score, created_at, is_mock
        FROM measurements
        ORDER BY created_at DESC
        LIMIT 10
    """))
    for row in result:
        print(row)