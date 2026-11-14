## Sửa lỗi trong v1.6.5

- **Cài game FitGirl không còn làm mất bản tải về**: Khi bộ cài FitGirl gặp lỗi giải nén (`Failed to start CLS-srep_x64.exe`, `Unarc.dll returned an error code: -11`), trước đây toàn bộ các tệp `.bin` vừa tải bị xoá theo. Nay bản repack được tạm chuyển ra ngoài thư mục game trong lúc cài, cài lỗi thì được trả về nguyên vẹn để thử lại mà không phải tải lại.
- **Thư mục tạm của bộ cài FitGirl**: Bộ cài được chạy với thư mục tạm ngắn, không dấu cách và nằm ngoài thư mục game, tránh lỗi không khởi chạy được công cụ giải nén của repack.
- **Mục "Có cập nhật" không còn gợi ý cho game bản quyền**: Game mua trên Steam, Epic, GOG, Xbox, EA, Ubisoft, Battle.net được tự động loại khỏi danh sách cập nhật của cửa hàng miễn phí, chỉ còn các game cài từ Online-Fix, FitGirl, SteamRIP, AnkerGames hoặc bản repack.

## Cải thiện

- **Không ghi rác vào thư mục Temp của Windows**: Tệp tạm của ứng dụng (tải bản cập nhật, driver ViGEmBus, đồng bộ save, LAN Drop, nhật ký máy ảo Android...) giờ chỉ nằm trong thư mục tải game (`.bobtemp`) hoặc thư mục `Bob Gaming\GameCenter`, và được dọn sau khi dùng xong.
