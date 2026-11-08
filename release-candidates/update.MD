### Tính năng mới — Việt Hoá tự động 1-Click (Bản thử nghiệm RC)
- **Huy hiệu Cờ Việt Nam (VN Badge):** Tự động nhận diện các tựa game có bản Việt Hoá trên cả **Online-Fix Store** và **Thư viện Game** (chế độ Lưới & Danh sách), hiển thị tag cờ đỏ sao vàng sắc nét đồng bộ với tag `HV`.
- **Cài đặt & Gỡ Việt Hoá 1-Click trong Thư viện:** Bổ sung nút **Cài đặt Việt Hoá** ngay trên thẻ game có hỗ trợ:
  - Tự động tải gói Việt Hoá (hỗ trợ GitHub Releases, Google Drive vượt xác nhận quét virus, Pixeldrain và mirror dự phòng), kiểm tra toàn vẹn `SHA-256`, tự nhận diện định dạng nén (`.zip`, `.rar`, `.7z`, `.pak`, ...) và chép thẳng vào đúng thư mục con của game mà không cần thao tác thủ công.
  - Tự động sao lưu (backup) các tệp gốc trước khi ghi đè và hỗ trợ **Gỡ Việt Hoá** khôi phục nguyên trạng game bất kỳ lúc nào.
  - Tự động dò tìm thư mục cài đặt game qua Steam (`libraryfolders.vdf` / `appmanifest_<appid>.acf`) kể cả khi game chưa chạy lần đầu.
- **Danh mục Việt Hoá tích hợp sẵn (`v2`):** Bao gồm 16 tựa game đã xác thực mã băm `SHA-256` (RimWorld, Project Zomboid, State of Decay 2, Kingdom Come: Deliverance II, Black Myth: Wukong, Elden Ring, Red Dead Redemption 2, Grand Theft Auto V, The Witcher 3, Cyberpunk 2077, Valheim, Civilization VI, Cities: Skylines II, Dawn of Man, Subnautica: Below Zero, Resident Evil 4 Remake).
