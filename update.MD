## Có gì mới trong v1.3.3

- **Sửa lỗi màn hình đen / xanh khi Remote Gaming tới Steam Deck (Sunshine)**: Tự động loại bỏ khung hình lỗi lúc khởi tạo và tự chuyển luồng tương thích sang `H.264 1080p@60fps` khi bộ mã hóa HEVC của máy chủ gặp lỗi, không làm ảnh hưởng cấu hình lưu sẵn của các máy chủ khác.
- **Sửa trạng thái máy chủ ngoại tuyến & sắp xếp danh sách máy chủ**: Tự xóa trạng thái game đang chạy cũ khi máy chủ đang Offline, hỗ trợ bật máy từ xa qua **Wake-on-LAN**, và ưu tiên xếp các máy chủ **Đã ghép** lên đầu danh sách.
- **Nâng cấp bảng Lệnh máy chủ & ẩn thông số hiệu năng mặc định**: Mở nút **Lệnh máy chủ** ngay tại màn hình Remote Gaming với các thao tác nhanh (**Đánh thức máy WoL**, **Làm mới trạng thái**, **Dừng game đang chạy**) cùng danh sách lệnh hệ thống Apollo theo thời gian thực; mặc định ẩn bảng thông số kỹ thuật khi vào stream (bật/tắt nhanh bằng `Ctrl+Alt+Shift+S`).
