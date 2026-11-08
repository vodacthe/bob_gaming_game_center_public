## Tính năng mới trong v1.5.0

- **Cài đặt Việt Hoá 1 chạm & Huy hiệu cờ Việt Nam**: Tích hợp hệ thống cài đặt/gỡ Việt Hoá tự động kèm sao lưu Write-Ahead Journal an toàn, huy hiệu cờ đỏ sao vàng trên thẻ game (Thư viện & Kho Game), và đồng bộ danh mục Việt Hoá OTA tự động từ máy chủ.
- **Tự động cài Việt Hoá ngay khi tải game từ Kho Game**: Bổ sung tuỳ chọn *"Tự động cài Việt Hoá sau khi tải xong"* (mặc định bật cho các game có bản dịch) trong hộp thoại tải game; ngay khi giải nén/cài đặt game xong sẽ tự động chạy cài Việt Hoá ngầm và thông báo khi hoàn tất.
- **Giải nén gói Việt Hoá PyInstaller / SFX đa nền tảng**: Tự động bóc tách dữ liệu bản dịch bên trong file `.exe` đóng gói PyInstaller/SFX (như các bản dịch của The Red Team cho Cyberpunk 2077, Elden Ring, Red Dead Redemption 2) mà không cần chạy `.exe`, hoạt động trên cả Windows và Steam Deck.

## Sửa lỗi & Cải thiện ổn định

- **Việt Hoá & SHA-256**: Cập nhật danh mục Việt Hoá v5 với mã băm SHA-256 chuẩn bản PC, mật khẩu giải nén và đường dẫn cài đặt chính xác; tự động ghi nhận cảnh báo và cho phép cài đặt khi nhóm dịch cập nhật bản mới làm đổi mã băm (vẫn chặn trang HTML lỗi/quota).
- **Kho Game (FitGirl / AnkerGames / SteamRIP / Online-Fix)**: Phát hiện Windows Defender cách ly `setup.exe`, tự giải nén lại từng phần `.rar`, bỏ qua các gói lồng tiếng ngoại ngữ dư thừa khi tải FitGirl, ngăn báo hoàn tất giả khi thư mục đích trống, và hỗ trợ trình duyệt Flatpak/Firefox trên Steam Deck khi tải AnkerGames.
- **Steam Deck & Game Trainer**: Khắc phục lỗi treo "Shutting down Steam" trong Game Mode khi khởi chạy game qua Proton, sửa lỗi hiển thị ký tự `&` trên nút cài biểu tượng Game Mode, và lưu bộ nhớ đệm ảnh bìa FLiNG Trainer trên ổ đĩa để mở tức thì.
