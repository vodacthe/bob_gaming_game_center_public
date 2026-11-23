## Sửa lỗi & Cải thiện trong v1.7.4

- **Sửa lỗi lấy nhầm ảnh bìa của bản game khác khi thêm Non-Steam (ví dụ EA SPORTS FC 27 lấy ảnh FC 24)**: Bắt buộc đối chiếu khớp tên game nghiêm ngặt trên cả SteamGridDB và Steam Store, không bao giờ tự lấy kết quả đầu tiên khác năm/phiên bản.
- **Hỗ trợ tải đầy đủ 5 loại ảnh bìa có SHA1 hash từ Steam CDN mới**: Bổ sung giải pháp lấy trực tiếp Poster, Grid, Hero, Logo và Icon từ hệ thống CDN mới của Steam (IStoreBrowseService & library_assets_full) cho các tựa game phát hành mới chưa có trên SteamGridDB, đồng thời tự dọn ảnh cũ bị lệch khi đồng bộ lại.
- **Thông báo rõ khi AnkerGames chặn tải trực tiếp ngoài trình duyệt**: Ghi nhận lý do từ máy chủ AnkerGames khi trả về HTTP 403 và hướng dẫn mở tải qua nút **AnkerGames (Trình duyệt)**.
