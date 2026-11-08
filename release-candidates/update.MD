## Sửa lỗi giải nén FitGirl trên Windows & tối ưu giải nén bổ sung (v1.4.3-rc9)

- **Phát hiện tức thì khi Windows Security cách ly `setup.exe` của FitGirl**: Kiểm tra danh mục tệp trong gói `.rar` và phát hiện ngay nếu phần mềm diệt virus cách ly `setup.exe` sau khi giải nén (kèm hướng dẫn khôi phục / thêm thư mục vào Exclusions rõ ràng, không chạy phí thời gian giải nén tiếp các gói ngôn ngữ).
- **Thử lại siêu tốc (không tải lại & không giải nén lại từ đầu)**: Khi bấm **Thử lại** trên tác vụ lỗi giải nén, ứng dụng bỏ qua bước quét lại máy chủ CDN và chỉ trích xuất đúng tệp `setup.exe` còn thiếu (~1 giây thay vì giải nén lại hàng chục GB tệp `.bin`).
- **Chuyển thư mục tạm bộ cài FitGirl vào `<Game>\temp-fitgirl`**: Tránh đầy ổ `C:` khi bung nén game lớn và nằm gọn trong cùng một thư mục loại trừ của ổ chứa game.
- **Tự động loại bỏ các gói lồng tiếng ngoại ngữ dư thừa (`fg-selective-*`) trên Direct CDN**: Chỉ giữ gói tiếng Anh và nội dung bonus, tiết kiệm 40–65 GB dung lượng tải cho các game đa ngôn ngữ như *Cyberpunk 2077*.
