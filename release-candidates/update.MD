## Có gì mới trong v1.4.2-rc3 (Release Candidate)

- **Báo rõ trạng thái từ chối / lỗi gửi cho người gửi (BobDrop)**: Khi người nhận bấm Từ chối, hết thời gian chờ xác nhận hoặc phiên gửi gặp lỗi, màn hình người gửi nay cập nhật ngay thanh trạng thái đỏ, gắn nhãn màu `[BỊ TỪ CHỐI]` / `[THẤT BẠI]` trên dòng phiên truyền, đồng thời hiện hộp thoại báo rõ (hoặc bắn thông báo khay hệ thống khi đang thu nhỏ / gửi hàng loạt nhiều máy).
- **Hỗ trợ gửi thư mục game lớn (> 2 GB & hàng chục nghìn tệp)**: Nâng giới hạn bản kê khai truyền lên 100.000 tệp (khung điều khiển 16 MB) và sửa lỗi tràn số 32-bit (`OverflowError`) khi quét dung lượng tệp/thư mục lớn hơn 2 GB. *(Lưu ý: Cả máy gửi và máy nhận cần cùng cập nhật lên v1.4.2-rc3 để truyền thư mục nhiều nghìn tệp).*
- **Sửa lỗi quét mạng LAN / ZeroTier & Mũi tên QComboBox (từ RC2)**: Đồng bộ phát hiện thiết bị qua LAN/ZeroTier thực tế, tự cấu hình rule Windows Firewall `LocalSubnet` và thay mũi tên `QComboBox` bằng vector SVG.
