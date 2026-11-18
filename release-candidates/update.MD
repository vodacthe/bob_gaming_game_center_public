## Sửa lỗi & Cải thiện trong v1.7.2

- **Sửa lỗi Steam Chat Overlay kẹt "Cần khởi động lại Steam để kết nối"**: Tự động phát hiện khi cổng mặc định `8080` nằm trong dải TCP bị Windows / Hyper-V giữ sẵn (`WSAEACCES` / `10013`) hoặc bị ứng dụng khác chiếm, tự chuyển CEF DevTools của Steam sang cổng dự phòng (`27062`, `27063`, `38080`, `48080`) qua cờ `-cef-enable-debugging -devtools-port` khi bấm **Khởi động lại Steam**.
- **Tự dò cổng CEF dự phòng & đánh thức kết nối tức thì**: Bộ dò kết nối (`steam_debug.probe`) tự động kiểm tra cổng dự phòng đang lắng nghe và log `logs/webhelper.txt` của Steam, đồng thời đánh thức vòng lặp kết nối ngay sau khi Steam khởi động lại hoặc bấm kiểm tra lại.
- **Khởi động lại Steam an toàn khi ứng dụng chạy quyền Administrator**: Đợi và dọn dẹp tiến trình con `steamwebhelper.exe` còn kẹt trước khi mở lại Steam, đồng thời ưu tiên khởi chạy `steam.exe` ở quyền người dùng thường qua Desktop Shell để không gây cảnh báo nâng quyền của Steam.
