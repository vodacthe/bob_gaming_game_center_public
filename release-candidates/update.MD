## Bản thử nghiệm RC (v1.7.5-rc1)

- **Thêm mục Thư viện Runtime (Cài VC++ / DirectX / .NET / OpenAL vào Proton Prefix cho Steam Deck & Windows)**:
  - Sửa lỗi thiếu *Microsoft Visual C++ Runtime* khi mở các game Unreal Engine 4/5 Non-Steam trên Steam Deck (ví dụ Phantom Blade Zero).
  - Tự động phát hiện trạng thái đã cài / chưa cài trong từng Proton Prefix (compatdata/<appid>/pfx), hỗ trợ 1 chạm **Cài gói khuyến nghị (VC++ 2015–2022 x64/x86 + DirectX Jun 2010)**.
  - Tự quét các bộ cài đi kèm trong thư mục game (UEPrereqSetup_x64.exe, _CommonRedist, DXSETUP.exe) và hỗ trợ chạy bất kỳ file .exe/.msi nào trực tiếp vào Prefix của game.
  - Mở nhanh từ Sidebar (**Thư viện Runtime**) hoặc bấm ... trên từng thẻ game → **Cài thư viện Runtime (VC++ / DirectX)...**.
- **Tự động cài sẵn Visual C++ 2015–2022 (x64) trên SteamOS** khi thêm game Non-Steam mới vào Steam.
