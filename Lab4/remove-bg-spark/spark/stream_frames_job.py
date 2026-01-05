import os, json, base64
import numpy as np
import cv2

from pyspark.sql import SparkSession
from background_remover import remove_background

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "kafka:9092")
TOPIC = os.getenv("TOPIC_FRAMES", "camera_frames")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/opt/output")
CHECKPOINT_DIR = os.getenv("CHECKPOINT_DIR", "/opt/checkpoint")

spark = SparkSession.builder.appName("RemoveBG-Stream").getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", BOOTSTRAP)
    .option("subscribe", TOPIC)
    .option("startingOffsets", "earliest")     # quan trọng: tránh miss data
    .option("failOnDataLoss", "false")         # ổn định khi restart
    .load()
)

value_df = df.selectExpr("CAST(value AS STRING) AS v")

def process_batch(batch_df, batch_id: int):
    rows = batch_df.collect()
    if not rows:
        return

    for r in rows:
        obj = json.loads(r["v"])
        cam = obj.get("camera_id", "cam01")
        idx = int(obj.get("frame_idx", 0))
        jpg_b64 = obj.get("jpg_b64")
        if not jpg_b64:
            continue

        img_bytes = base64.b64decode(jpg_b64)
        img_arr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if frame is None:
            continue

        out = remove_background(frame)

        out_dir = os.path.join(OUTPUT_DIR, cam)
        os.makedirs(out_dir, exist_ok=True)
        cv2.imwrite(os.path.join(out_dir, f"frame_{idx:06d}.png"), out)

query = (
    value_df.writeStream.foreachBatch(process_batch)
    .option("checkpointLocation", CHECKPOINT_DIR)
    .start()
)

query.awaitTermination()
