## Tính năng mới trong v1.6.8

- **Ngăn máy tự ngủ khi đang tải và cài đặt game**: Giữ Steam Deck (cả Game Mode lẫn Desktop Mode) và máy tính không chuyển sang chế độ ngủ (Sleep / Suspend) hoặc tắt màn hình sớm trong suốt quá trình tải game lớn từ Kho Game, giải nén, chạy bộ cài repack, cài game/Runtime Android, thêm lối tắt Steam và cài Việt Hoá. Máy chỉ cho phép ngủ trở lại sau khi tất cả tác vụ tải và cài đặt đã hoàn tất.
- **Tuỳ chọn trong Cài đặt hệ thống**: Bổ sung mục **"Giữ máy không ngủ khi đang tải và cài đặt game"** (mặc định bật) trong phần Cài đặt hệ thống để người dùng chủ động bật/tắt ngay lập tức mà không cần khởi động lại ứng dụng.

## Cải thiện kỹ thuật

- **Tương thích đa nền tảng**: Hỗ trợ đồng thời SteamOS/Linux (`systemd-inhibit`, `org.freedesktop.login1`, `org.freedesktop.ScreenSaver`, `PowerManagement.Inhibit` và X11/XWayland `XScreenSaverSuspend`), Windows (`SetThreadExecutionState` trên luồng định danh cố định) và macOS (`caffeinate`), tự động giải phóng khóa nguồn ngay cả khi tiến trình kết thúc đột ngột.
