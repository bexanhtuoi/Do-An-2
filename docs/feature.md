> [!abstract] Các tính năng chính
> Hệ thống gồm 4 nhóm tính năng: crawl, phát hiện mention, lưu trữ, và lịch sử.

## 1. Crawl dữ liệu
- **Trigger**: Google Apps Script time-driven trigger (hằng ngày)
- **Nguồn**: RSS feeds + [[Projects/DA2/plan-crawl#Web Search|web search]] các trang tin tức tài chính và ô tô
- **Xử lý**: Lọc bài viết liên quan đến 7 mã cổ phiếu

## 2. Phát hiện mention
- Duyệt `content` và `title`, kiểm tra sự xuất hiện của từng mã CK (`VMA`, `TMT`, `SVC`, `HAX`, `HTL`, `GGG`, `HHS`)
- Một bài viết có thể mention nhiều công ty → nhiều cột được đánh `1`
- Dùng regex `\b(STOCK_CODE)\b` để phân biệt chính xác

> [!tip] Xử lý đa công ty
> Một tin tức có thể đề cập nhiều mã CK, tất cả đều được ghi nhận.

## 3. Lưu trữ
- Google Sheets làm destination
- Mỗi row là một bài viết
- Append liên tục, không ghi đè
- Chống trùng lặp bằng cột Link

## 4. Lịch sử
- **Backfill** 3+ năm: chạy lần đầu với dữ liệu lịch sử
- **Crawl hằng ngày**: chỉ lấy tin mới từ lần chạy gần nhất

## 5. Google Sheet columns

| # | Cột | Mô tả |
|---|-----|-------|
| 1 | `Datetime` | Thời điểm crawl |
| 2 | `Link` | Đường dẫn bài viết |
| 3 | `Source` | Tên nguồn |
| 4 | `Title` | Tiêu đề |
| 5 | `Content` | Nội dung (trim 10k ký tự) |
| 6-12 | `VMA`...`HHS` | 1/0 cho từng mã |
| 13 | `Datetime Public` | Thời điểm đăng bài |
