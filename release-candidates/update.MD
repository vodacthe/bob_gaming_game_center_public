## Nội dung thay đổi trong `v1.6.7-rc1`

- **Sửa lỗi tải trực tiếp từ Buzzheavier (`app/core/online_fix/steamrip_client.py`):**
  - Chặn hành vi `/download` trả `HTTP 204` kèm `HX-Redirect` trỏ ngược về chính trang chia sẻ (`bzzhr.to` / `buzzheavier.com`) qua `_is_buzzheavier_stream_url()`, không để `aria2c` tải nhầm trang HTML.
  - Bổ sung bước phân giải 2 bước qua HTTP gắn `SSLContext` ép **TLS 1.3** (`_buzzheavier_tls_session()` + `_resolve_buzzheavier_via_tls13()`): truy cập trang chia sẻ với `Referer` SteamRIP để lấy nút tải có chữ ký thời gian `hx-get="/<id>/download?t=..."`, tên tệp `<title>` và dung lượng `.size`, sau đó lấy liên kết stream `ts.bzzhr.to/d/...` mà không cần mở trình duyệt.
  - Giữ nguyên nhánh dự phòng Chromium CDP (`_resolve_buzzheavier_via_cdp()`) và thông báo lỗi tiếng Việt rõ ràng khi máy không có trình duyệt.
- **Thêm hỗ trợ tải trực tiếp từ 1fichier (`app/core/online_fix/steamrip_client.py`, `app/core/online_fix/manager.py`):**
  - Nhận diện liên kết `1fichier.com/?<id>` trên trang game SteamRIP, cung cấp tuỳ chọn `Tải Trực Tiếp (1fichier)` (qua `aria2c`) và `1fichier (Trình duyệt)`.
  - Thêm `_resolve_1fichier()` hỗ trợ cả biểu mẫu 1fichier 2026 (không có trường ẩn `adz`, nút tải `a.ok` `"Start your download"`) lẫn biểu mẫu cũ, kèm thông báo tiếng Việt cho các trường hợp chờ giữa hai lượt tải miễn phí, tệp bị xoá hoặc có mật khẩu.
  - Bổ sung cơ chế truyền tuỳ chọn `options` theo từng mục trong `aria2_urls.txt` (whitelist `split=1`, `max-connection-per-server=1` và chỉ nhận giá trị số) để tương thích với giới hạn 1 kết nối của 1fichier miễn phí.
- **Kiểm thử (`tests/test_online_fix.py`):**
  - Bổ sung bộ unit test đầy đủ cho luồng Buzzheavier (TLS 1.3 token, self-redirect, CDP fallback, chuẩn hoá nhãn trình duyệt đa nền tảng) và 1fichier (bóc link, form 2026 không có `adz`, whitelist option `aria2c`, và các nhánh lỗi).
