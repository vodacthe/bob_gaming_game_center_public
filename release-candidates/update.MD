## Có gì mới trong v1.4.2-rc2 (Release Candidate)

- **Sửa lỗi quét thiết bị LAN & ZeroTier thực tế (BobDrop)**: Khắc phục lỗi cú pháp dải mạng CIDR làm rơi gói quảng bá UDP trên IP thực (`192.168.x.x` / ZeroTier), ưu tiên địa chỉ IP cùng subnet khi máy có nhiều card mạng ảo (WSL/Hyper-V/VPN) và tự động đăng ký rule Windows Firewall giới hạn chặt `LocalSubnet` cho mạng để ở chế độ Public.
- **Sửa mũi tên menu thả xuống (`QComboBox`)**: Thay thế toàn bộ style `border-top` gây lỗi hiển thị vạch ngang bằng biểu tượng mũi tên vector SVG sắc nét đồng bộ trên toàn ứng dụng.
- **Chia sẻ LAN — BobDrop & Thu gọn nhóm Side Menu (từ RC1)**: Chia sẻ tệp/thư mục ngang hàng mã hoá TLS 1.3 + SAS 6 số + TOFU qua LAN/ZeroTier/VPN (Windows & SteamOS) và đóng/mở từng nhóm trên thanh bên.
