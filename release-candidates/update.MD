## Tính năng mới & Sửa lỗi trong v1.7.5

- **Thêm mục Thư viện Runtime — cài Microsoft Visual C++ / DirectX / .NET / OpenAL vào Proton Prefix (Steam Deck) & Windows**:
  - Khắc phục triệt để lỗi thiếu *Microsoft Visual C++ Runtime* khi mở game Unreal Engine 4/5 Non-Steam trên Steam Deck (ví dụ Phantom Blade Zero).
  - Tự động kiểm tra trạng thái Đã cài / Chưa cài trong từng Proton Prefix (compatdata/<appid>/pfx), hỗ trợ 1 chạm **Cài gói khuyến nghị (VC++ 2015–2022 x64/x86 + DirectX Jun 2010)**.
  - Tự quét các bộ cài đi kèm trong thư mục game (UEPrereqSetup_x64.exe, _CommonRedist, DXSETUP.exe) và cho phép chạy bất kỳ tệp .exe/.msi nào trực tiếp trong Prefix của game.
  - Truy cập nhanh từ Sidebar (**Thư viện Runtime**) hoặc bấm ... trên thẻ game → **Cài thư viện Runtime (VC++ / DirectX)...**.
  - Tự động cài sẵn **Microsoft Visual C++ 2015–2022 (x64)** vào Proton Prefix khi thêm game Non-Steam mới trên SteamOS.
- **Sửa lỗi tự động khởi động cùng SteamOS trên Steam Deck (hỗ trợ cả Game Mode & Desktop Mode)**:
  - Triển khai đầy đủ tự khởi động cho SteamOS/Linux bằng systemd --user (~/.config/systemd/user/bob-game-center.service) cho Game Mode lẫn Desktop Mode và XDG Autostart (~/.config/autostart/bob_game_center.desktop) cho KDE Plasma.
  - Bộ khởi chạy ob_game_center.sh --autostart tự chờ display socket (gamescope / wayland / XWayland) sẵn sàng khi máy vừa khởi động và không ghi đè lên cửa sổ người dùng đang mở.
- **Sửa lỗi mở nhiều cửa sổ (nhiều instance) cùng lúc trên SteamOS**:
  - Khóa nhân hệ điều hành POSIX lock (pp.lock) chống mở trùng khi bấm liên tiếp nhiều lần vào biểu tượng ứng dụng.
  - Khi ứng dụng đang chạy (hoặc chạy ẩn sau khi tự khởi động), bấm icon lại sẽ gửi tín hiệu qua Unix socket (QLocalServer) để bật cửa sổ hiện có lên trước ngay lập tức mà không làm gián đoạn tác vụ tải game / chat.
  - Nếu tiến trình cũ bị treo hoặc không phản hồi (kể cả khi SDL2 chặn SIGTERM), tự động leo thang SIGTERM -> SIGKILL để thay thế sạch sẽ.
