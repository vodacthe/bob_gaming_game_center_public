## Tính năng mới trong v1.7.1

- **Chuyển đổi ngôn ngữ ứng dụng (English / Tiếng Việt) kèm biểu tượng lá cờ**: Bổ sung mục **Ngôn ngữ hiển thị** ở đầu phần **Cài đặt hệ thống** (và hộp thoại Cài đặt nhanh) với cờ Vương quốc Anh (`English`) và cờ Việt Nam (`Tiếng Việt`).
- **Đổi ngôn ngữ trực tiếp (Live Switch) không cần khởi động lại**: Toàn bộ giao diện chính, thanh điều hướng, Kho Game, Kho Game Android, các bộ lọc thể loại, thẻ game, hộp thoại thông báo và khung **Steam Chat Overlay** (bao gồm danh sách gợi ý lệnh `/...`) tự động chuyển ngôn ngữ ngay lập tức mà không làm gián đoạn quá trình tải game hay stream đang chạy.
- **Tự động chọn ngôn ngữ mặc định thông minh**: Máy cài đặt mới lần đầu mặc định sử dụng **English** (và khi Khôi phục cài đặt gốc), trong khi các máy đã cài đặt và sử dụng ứng dụng từ trước tự động giữ nguyên **Tiếng Việt**.

## Cải thiện kỹ thuật & Sửa lỗi

- **Bảo toàn tên trò chơi gốc & chuẩn phím tắt Qt**: Giữ nguyên tên riêng của trò chơi trong Thư viện và Kho Game khi chuyển đổi ngôn ngữ, đồng thời chuẩn hóa ký tự `&` trên nút bấm/tab để không sinh gạch chân phím tắt ngoài ý muốn.
- **Đồng bộ ngôn ngữ truy vấn Kho Game Android**: Tự động đồng bộ tham số ngôn ngữ khi tìm kiếm danh mục trên Google Play theo ngôn ngữ hiển thị đang chọn.
