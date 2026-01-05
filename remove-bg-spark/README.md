# Lab 04 – Streaming Remove Background with Spark

## Mô tả bài toán
Bài thực hành này xây dựng một hệ thống mô phỏng xử lý và xoá phông nền ảnh **theo luồng (streaming)** sử dụng **Apache Spark**.  
Dữ liệu hình ảnh được giả lập từ camera, truyền theo thời gian thực qua Kafka và được xử lý trong ngữ cảnh Spark Structured Streaming.

Kiến trúc tổng thể được xây dựng nhất quán theo mô hình đã sử dụng trong Lab 4.

---

## Đáp ứng yêu cầu đề bài

### Yêu cầu 1  
**Xây dựng module giả lập camera server**

- Camera đọc video đầu vào
- Tách video thành từng frame
- Đóng gói frame thành message
- Gửi dữ liệu **theo luồng (streaming)** đến server xử lý thông qua Kafka

✔️ **Đã đáp ứng**

---

### Yêu cầu 2  
**Xây dựng module xử lý trong Spark**

- Nhận stream frame từ Kafka
- Xử lý xoá nền cho từng frame
- Quá trình xử lý được thực hiện trong **Spark Structured Streaming**
- Lưu kết quả thành các file ảnh

✔️ **Đã đáp ứng**

---

## Công nghệ sử dụng
- Apache Spark (Structured Streaming)
- Apache Kafka
- Docker & Docker Compose
- Python
- OpenCV / MediaPipe

---

## Cách chạy chương trình

## 1. Chuẩn bị dữ liệu đầu vào
### Đặt video mẫu tại: videos/sample.mp4 hoặc thay đổi biến môi trường `VIDEO_SRC` trong `docker-compose.yml` (service `camera`) để sử dụng video khác.
---

## 2. Khởi chạy hệ thống
```bash
docker compose up -d --build
```
### Lệnh trên sẽ tự động:
- Khởi động Kafka và Zookeeper
- Chạy camera server để giả lập streaming video
- Submit Spark Structured Streaming job để xử lý và xoá nền từng frame
## 3. Theo dõi quá trình streaming và xử lý
```bash
docker compose logs -f camera spark-job
```
## 4. Kết quả
### Các frame sau khi được xử lý (xoá nền) sẽ được lưu tại: output/cam01/
### Thư mục này được tạo tự động theo CAMERA_ID.
## Dừng hệ thống
```bash
docker compose down
```
