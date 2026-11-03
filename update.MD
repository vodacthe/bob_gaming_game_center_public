## Có gì mới trong v1.3.1

- **Sửa lỗi Steam Chat Overlay trên game Exclusive Fullscreen**: Bấm `Ctrl+Enter` để mở khung chat không còn làm game chạy toàn màn hình độc quyền (Exclusive Fullscreen) bị thu nhỏ xuống thanh tác vụ, đồng thời vẫn hỗ trợ gõ tiếng Việt có dấu trực tiếp qua Unikey / EVKey.
- **Giữ hiển thị tin nhắn vừa nhận khi gửi phản hồi trên Overlay**: Khắc phục lỗi các tin nhắn mới nhận bị ẩn ngay lập tức sau khi gửi tin trả lời; nay các tin đang hiện lúc mở khung chat (cùng tin mới đến khi đang gõ) sẽ tiếp tục hiển thị và tự ẩn cùng nhịp với tin vừa gửi, hoặc giữ nguyên thời gian hiển thị còn lại khi bấm `Esc` hủy gõ.
- **Khắc phục lỗi chuyển tab menu (`zlib Error -3`) & thoát hẳn từ System Tray**: Ghim trực tiếp archive module `PYZ` ngay khi khởi động để ứng dụng không bị lệch byte offset khi file `.exe` được cập nhật/ghi đè lúc đang chạy, đồng thời đảm bảo thao tác **Thoát ứng dụng** dưới khay hệ thống đóng sạch toàn bộ tiến trình nền.
