## Tính năng mới trong v1.7.0

- **Ghép màn hình (Triple Screen không cần Eyefinity / NVIDIA Surround)**: Bổ sung mục **Ghép màn hình** trong nhóm **Công cụ nâng cao**, cho phép chạy trò chơi tràn 2 hoặc 3+ màn hình không viền trực tiếp qua Win32 mà không cần gộp màn hình ở tầng driver.
- **Tích hợp sẵn Euro Truck Simulator 2 & American Truck Simulator + mọi game tùy chỉnh**: Tự động dò đường dẫn `.exe` cho **ETS 2** và **ATS**, hỗ trợ chọn tệp `.exe` bất kỳ để chạy ngay, bật theo dõi tự động ngầm (`[ON]`) hoặc bấm **Ghép ngay** kèm sơ đồ chọn màn hình trực quan.
- **Tương thích hoàn toàn với Lossless Scaling (LSFG3 / FSR) trên nhiều màn hình**: Tự động can thiệp bộ nhớ tiến trình `LosslessScaling.exe` (W^X in-memory IAT hook, không ghi đè tệp lên ổ đĩa) giúp khung hình bù `LSFG3` và upscale `FSR` trải đều toàn bộ cụm màn hình ghép thay vì nhảy co về 1 màn hình.

## Cải thiện kỹ thuật & Sửa lỗi

- **Sửa lỗi phím tắt `Ctrl+Enter` của Steam Chat Overlay trong game DirectInput8 / Triple Screen**: Bổ sung low-level hook dự phòng và đồng bộ phím bổ trợ vật lý (`Ctrl`/`Shift`/`Alt`), khắc phục tình trạng engine Prism3D (ETS 2, ATS...) chặn `WM_HOTKEY` khiến không mở/đóng được khung nhập chat trong game.
- **Khởi chạy `.exe` chuẩn quyền người dùng & phát hiện khóa màn hình**: Tự động chạy `.exe` qua token desktop Explorer tránh lỗi xung đột quyền với Steam, đồng thời tự động phát hiện và cảnh báo khi game khóa cứng chế độ Fullscreen/Borderless 1 màn hình.
