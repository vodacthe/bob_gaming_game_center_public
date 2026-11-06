## Có gì mới trong v1.4.0

- **Hỗ trợ đầy đủ Arch Linux / SteamOS cho Steam Deck**: Hoạt động mượt mà trên cả **Desktop Mode** và **Steam Game Mode**, cài đặt gọn trong user-space (`/home/deck/Applications/BobGameCenter`) kèm lệnh cài online 1 dòng (`install.sh`).
- **Tải, giải nén & Thêm Non-Steam Game 1-Click kèm Proton**: Đóng gói sẵn `aria2c` Linux tĩnh, tự động ghi `shortcuts.vdf`, đồng bộ ảnh bìa thư viện và tự động gán `Proton Experimental` trong `config.vdf`.
- **Tích hợp Online-Fix Runner cho Steam Deck**: Tự động cấu hình `WINEDLLOVERRIDES`, tạo `steam_appid.txt` (`480`), sửa `OnlineFix.ini` chống lỗi Overlay và sinh script chạy multiplayer ổn định.
- **Tự động cập nhật đa nền tảng & Cải thiện Khay hệ thống**: Hỗ trợ tự cập nhật tại chỗ ngay trong Game Mode/Desktop Mode trên Linux và hỗ trợ click chuột trái mở lại cửa sổ từ System Tray trên KDE Plasma.
