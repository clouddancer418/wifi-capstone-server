from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///./wifi_monitor.db")

with engine.begin() as conn:
    result = conn.execute(text("DELETE FROM measurements WHERE building = 'string'"))
    print(f"삭제된 잘못된 데이터 수: {result.rowcount}")

    count = conn.execute(text("SELECT COUNT(*) FROM measurements")).fetchone()[0]
    print(f"남은 데이터 수: {count}")