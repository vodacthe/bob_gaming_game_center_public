## Tính năng mới trong v1.6.9

- **Tự động dò tìm vị trí lưu game (Auto Save Location) trên Windows và Steam Deck / SteamOS**: Thay thế thao tác mở tìm kiếm Google thủ công bằng hệ thống tự động nhận diện thư mục save cho hơn **20.100 trò chơi** ngay trong ứng dụng.
- **Hỗ trợ đầy đủ SteamOS / Proton & thẻ nhớ microSD**: Tự động quét các tiền tố Proton (`compatdata/<appid>/pfx`, `<thư mục game>/compatdata/pfx`), đường dẫn thư viện phụ trong `libraryfolders.vdf` (gồm cả thẻ nhớ microSD trên Steam Deck), `shortcuts.vdf` và đường dẫn Linux gốc (`XDG_DATA_HOME` / `XDG_CONFIG_HOME`).
- **Tự động nhận diện Online-Fix, Steam Emulator & Game Engine**: Hỗ trợ dò save cho `Online-Fix`, `Goldberg / GSE Saves`, `RUNE`, `CODEX`, `FLT`, `EMPRESS`, `SmartSteamEmu`, `Steam userdata` cùng cơ chế phân tích engine (`Unity`, `Unreal Engine`, `Ren'Py`, `RPG Maker`).
- **Đồng bộ Cloud xuyên nền tảng (Windows <-> Steam Deck)**: Tự động chuyển đổi đường dẫn lưu game giữa Windows và SteamOS Proton khi tải bản lưu từ Cloud về máy mới, đồng thời tự tạo sẵn thư mục lưu game ngay cả khi chưa khởi chạy game lần đầu.
- **Chọn nhanh khi có nhiều vị trí lưu hợp lệ**: Tự động ưu tiên thư mục chứa bản lưu mới nhất khi quét nền, hoặc hiển thị hộp thoại chọn thư mục kèm số tệp và thời gian cập nhật khi người dùng bấm **"Tự động tìm vị trí save"**.

## Cải thiện kỹ thuật

- **Cập nhật cơ sở dữ liệu Save tự động (OTA)**: Tích hợp sẵn cơ sở dữ liệu nén ngoại tuyến (`save_locations_db.json.gz`) và tự động đồng bộ bản cập nhật mới trong tiến trình nền mà không làm khựng giao diện.
