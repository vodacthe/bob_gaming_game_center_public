## Có gì mới trong v1.4.2-rc1 (Release Candidate)

- **Chia sẻ LAN — BobDrop (AirDrop nội bộ & VPN)**: Truyền trực tiếp nhiều tệp và nguyên thư mục ngang hàng (P2P) qua mạng LAN, ZeroTier, Radmin VPN và Tailscale (hỗ trợ cả chéo nền tảng Windows & SteamOS / Steam Deck). Hỗ trợ kéo thả, gửi chọn lọc hoặc **Chia sẻ cho tất cả**, chạy nền dưới khay hệ thống với 3 chế độ nhận tệp.
- **Mã hoá bảo mật chống giả mạo**: Bảo vệ luồng truyền bằng **TLS 1.3** đầu-cuối, chữ ký định danh ECDSA P-256 gắn kênh chống MITM, mã đối chiếu 6 chữ số (SAS), ghim khoá thiết bị tin cậy (**TOFU**), Mã PIN phòng (`PBKDF2-HMAC-SHA256`) và kiểm tra toàn vẹn `SHA-256` từng tệp trước khi hoàn tất.
- **Thu gọn Side Menu theo từng nhóm**: Bấm trực tiếp vào tiêu đề từng nhóm trên thanh bên (`KHO GAME`, `THƯ VIỆN`, `CÔNG CỤ NÂNG CAO`, `THIẾT BỊ`, `HỆ THỐNG`) để đóng/mở gọn gàng, tự động lưu trạng thái cho các lần khởi động sau và hiển thị chấm đèn báo khi có tính năng chạy nền bên trong nhóm đang thu gọn.
