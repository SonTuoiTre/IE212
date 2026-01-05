FROM apache/spark:3.5.3-python3

WORKDIR /opt/app
USER root

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Python deps tối thiểu
RUN pip install --no-cache-dir numpy opencv-python-headless kafka-python

# ------------------------------------------------------------
# Kafka connector jars for Spark Structured Streaming
# Spark 3.5.3 / Scala 2.12
# ------------------------------------------------------------
ENV SPARK_JARS_DIR=/opt/spark/jars

RUN curl -fL -o ${SPARK_JARS_DIR}/spark-sql-kafka-0-10_2.12-3.5.3.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar \
 && curl -fL -o ${SPARK_JARS_DIR}/spark-token-provider-kafka-0-10_2.12-3.5.3.jar \
      https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.3/spark-token-provider-kafka-0-10_2.12-3.5.3.jar \
 && curl -fL -o ${SPARK_JARS_DIR}/kafka-clients-3.6.1.jar \
      https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.6.1/kafka-clients-3.6.1.jar \
 && curl -fL -o ${SPARK_JARS_DIR}/commons-pool2-2.12.0.jar \
      https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.12.0/commons-pool2-2.12.0.jar

# Copy code
COPY stream_frames_job.py background_remover.py ./

CMD ["/opt/spark/bin/spark-submit", "/opt/app/stream_frames_job.py"]
