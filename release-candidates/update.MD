## Bản thử nghiệm RC (v1.7.5-rc2)

- **Sửa lỗi tự động khởi động cùng SteamOS trên Steam Deck (hỗ trợ cả Game Mode & Desktop Mode)**:
  - Triển khai đầy đủ set_auto_start cho SteamOS/Linux thay vì chỉ gọi Windows Task Scheduler: tự tạo và kích hoạt systemd --user service (~/.config/systemd/user/bob-game-center.service) cho Game Mode lẫn Desktop Mode và tệp XDG Autostart (~/.config/autostart/bob_game_center.desktop) cho KDE Plasma.
  - Bộ khởi chạy ob_game_center.sh --autostart tự chờ display socket (gamescope / wayland / XWayland) sẵn sàng khi Steam Deck vừa boot, tránh lỗi không kết nối được màn hình.
  - Bảo vệ chạy 1 phiên bản khi tự khởi động (--autostart) để không đè lên cửa sổ người dùng đang mở và cấu hình SuccessExitStatus=0 143 SIGTERM để không bị vòng lặp khởi động lại.
- **Bao gồm tính năng Thư viện Runtime từ RC1**: cài Microsoft Visual C++ 2015–2022 (x64/x86), DirectX Jun 2010, .NET, OpenAL và bộ cài đi kèm (UEPrereqSetup_x64.exe) thẳng vào Proton Prefix của game.
