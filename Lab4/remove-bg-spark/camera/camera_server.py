import os
import time
import json
import cv2
import base64
from kafka import KafkaProducer

# =========================
# ENV
# =========================
CAMERA_ID = os.getenv("CAMERA_ID", "cam01")
VIDEO_SRC = os.getenv("VIDEO_SRC", "/videos/sample.mp4")
FPS = float(os.getenv("FPS", "5"))
TOPIC = os.getenv("TOPIC", "camera_frames")
BOOTSTRAP = os.getenv("BOOTSTRAP", "kafka:9092")

print(f"[camera] CAMERA_ID={CAMERA_ID} VIDEO_SRC={VIDEO_SRC} FPS={FPS} TOPIC={TOPIC} BOOTSTRAP={BOOTSTRAP}")

# =========================
# WAIT FOR KAFKA
# =========================
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            api_version=(0, 10)
        )
        break
    except Exception:
        print("[camera] Kafka not ready, retrying in 3s...")
        time.sleep(3)

print("[camera] Connected to Kafka")

# =========================
# OPEN VIDEO
# =========================
cap = cv2.VideoCapture(VIDEO_SRC)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open VIDEO_SRC={VIDEO_SRC}")

frame_interval = 1.0 / FPS
frame_idx = 0

# =========================
# MAIN LOOP (CRITICAL)
# =========================
while True:
    ret, frame = cap.read()

    # 🔴 QUAN TRỌNG: video hết thì quay lại đầu
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    _, buffer = cv2.imencode(".jpg", frame)
    jpg_bytes = base64.b64encode(buffer).decode("utf-8")

    msg = {
        "camera_id": CAMERA_ID,
        "frame_idx": frame_idx,
        "ts": time.time(),
        "jpg_b64": jpg_bytes
    }

    producer.send(TOPIC, msg)
    producer.flush()

    frame_idx += 1
    time.sleep(frame_interval)
