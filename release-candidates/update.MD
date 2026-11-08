### Tự động đồng bộ Crawler Việt Hoá & Cờ đỏ sao vàng (1.4.3-rc5)
- **Tương thích hoàn toàn với Crawler tự động trên GitHub Actions**: Hỗ trợ đầy đủ cả cấu trúc danh mục lồng nhau (`download.primary.url`) và phẳng (`download_url`) khi xác thực bản cập nhật OTA `vietnamese_catalog.json` từ CDN.
- **Tự động cập nhật danh mục mới mỗi 6 giờ**: Máy chủ GitHub Actions tự động quét GitHub Releases & Steam Guides, kiểm định mã băm SHA-256 + cấu trúc gói nén và đẩy thẳng lên CDN để ứng dụng tự nhận game Việt Hoá mới.
- **Giữ nguyên huy hiệu Cờ đỏ sao vàng sắc nét** trên toàn bộ Thư viện, Chi tiết trò chơi và Kho Game.
