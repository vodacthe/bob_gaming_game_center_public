## Có gì mới trong v1.3.0

- **Bổ sung kho game AnkerGames (Direct CDN tốc độ cao)**: Tích hợp kho game thứ 4 bên cạnh Online-Fix, FitGirl Repacks và SteamRIP; tự động gộp gói **Tải Full Game + Online Fix** cho các tựa game Co-op/Online và giải nén đè fix tự động vào đúng thư mục gốc của game.
- **Sắp xếp Kho Game theo ngày phát hành thực tế & kệ báo cập nhật**: Loại bỏ tình trạng bài ghim cũ luôn nằm đầu trang; thêm kệ **"Đã cài đặt · Có bản cập nhật"** cùng nhãn **CÓ CẬP NHẬT** cho các game đã cài trên máy khi cửa hàng có bản mới hơn.
- **Nhận diện & gắn nhãn Hypervisor (`HV`)**: Tự động phát hiện các bản game dùng cơ chế Hypervisor Bypass (như *Phantom Blade Zero*), gắn nhãn đỏ **`HV`** góc dưới phải ảnh bìa trên thẻ Kho Game và hiển thị thông báo hướng dẫn trong hộp thoại Chi tiết.
- **Nâng cấp tìm kiếm liên kho chuẩn xác**: Loại trừ hoàn toàn các phần mềm/công cụ ngoài game (*GameRanger*, `/programs/`, `/guides/`), lọc bỏ kết quả rác chỉ khớp nội dung bài viết, tự động tìm từ viết tắt có dấu chấm (`REPO` -> `R.E.P.O.`) và ưu tiên xếp hạng khớp chính xác lên đầu.
- **Tự phục hồi ảnh bìa Thư viện & gỡ cài đặt không khởi động lại Steam**: Tự động xóa ảnh bìa lỗi chống hotlink kích thước nhỏ và lấy ảnh dự phòng từ Kho Game; gỡ cài đặt game trên Thư viện không còn tự đóng và khởi động lại Steam.
