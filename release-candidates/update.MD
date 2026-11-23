## Bản thử nghiệm RC (v1.7.5-rc3)

- **Sửa lỗi mở nhiều cửa sổ / nhiều instance cùng lúc trên SteamOS**:
  - Dùng khóa nhân hệ điều hành POSIX lock (pp.lock) chống race-condition khi bấm liên tiếp nhiều lần vào icon ứng dụng.
  - Khi ứng dụng đang chạy (hoặc chạy ẩn sau khi tự khởi động), bấm icon lại sẽ gửi tín hiệu qua Unix socket (QLocalServer) để bật cửa sổ hiện có lên trước ngay lập tức — giữ nguyên các tác vụ tải game / chat đang chạy.
  - Nếu tiến trình cũ bị treo hoặc không phản hồi (kể cả khi SDL2 chặn SIGTERM), tự leo thang SIGTERM -> SIGKILL rồi thay thế sạch sẽ.
- **Bao gồm các bản sửa từ RC1 & RC2**:
  - **Thư viện Runtime**: cài Microsoft Visual C++ 2015–2022 (x64/x86), DirectX Jun 2010, .NET, OpenAL và bộ cài đi kèm (UEPrereqSetup_x64.exe) vào thẳng Proton Prefix của game.
  - **Tự động khởi động cùng SteamOS**: hỗ trợ cả Game Mode (systemd --user) và Desktop Mode (XDG autostart).
