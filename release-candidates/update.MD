## Thay đổi trong v1.6.6

- **Tắt toàn bộ thông báo khi ứng dụng đang active trên màn hình**: Tập trung hoá mọi luồng phát thông báo hệ thống (tray balloon và toast cảnh báo pin tay cầm) qua cổng kiểm soát thống nhất (`app/ui/notifications.py`). Thông báo bị chặn hoàn toàn khi cửa sổ ứng dụng đang hiển thị active trên màn hình (xử lý chính xác cả môi trường Steam Deck Game Mode), chỉ hiển thị khi ứng dụng thu nhỏ (minimized) hoặc ẩn xuống khay hệ thống (tray).
- **Thêm mục Debug kiểm tra thông báo trong Cài đặt**: Bổ sung mục **Debug** → nút **Test notification** kèm nhãn trạng thái thời gian thực và tuỳ chọn ép hiện (**Buộc hiện khi test**).
