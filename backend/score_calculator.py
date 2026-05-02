from typing import Optional

def normalize_rssi(rssi: int) -> float:
    RSSI_MIN, RSSI_MAX = -100, -30
    normalized = (rssi - RSSI_MIN) / (RSSI_MAX - RSSI_MIN)
    return max(0.0, min(1.0, normalized))

def normalize_latency(latency_ms: float) -> float:
    if latency_ms < 0: return 0.0
    LATENCY_MAX = 500
    return 1.0 - min(latency_ms / LATENCY_MAX, 1.0)

def normalize_packet_loss(packet_loss: float) -> float:
    return 1.0 - min(packet_loss / 100.0, 1.0)

def calculate_score(rssi: int, latency_ms: float, packet_loss: float = 0.0) -> dict:
    W_RSSI, W_LATENCY, W_PACKET_LOSS = 0.4, 0.4, 0.2
    r_n = normalize_rssi(rssi)
    l_n = normalize_latency(latency_ms)
    p_n = normalize_packet_loss(packet_loss)
    
    score = round((r_n * W_RSSI + l_n * W_LATENCY + p_n * W_PACKET_LOSS) * 100, 1)
    status = "좋음" if score >= 80 else "보통" if score >= 50 else "나쁨"

    return {
        "score": score, "status": status,
        "detail": {"rssi": round(r_n*100, 1), "latency": round(l_n*100, 1), "loss": round(p_n*100, 1)}
    }

def calculate_score_from_dict(data: dict) -> dict:
    return calculate_score(data.get("rssi", -100), data.get("latency", 500), data.get("packet_loss", 0.0))