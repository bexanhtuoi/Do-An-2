```mermaid
flowchart TD
    A[Trigger hằng ngày] --> B[Google Apps Script chạy]
    B --> C[Lấy danh sách nguồn RSS/URL]
    C --> D[Fetch từng nguồn]
    D --> E[Parse: title, content, datetime, link]
    E --> F[Lọc tin đã crawl?]
    F -->|Đã có| G[Skip]
    F -->|Mới| H[Kiểm tra mention 7 mã CK]
    H --> I[Đánh cờ 1/0 cho từng mã]
    I --> J[Append row vào Google Sheet]
    G --> K[Next source]
    J --> K
    K -->|Còn nguồn| D
    K -->|Hết| L[Kết thúc]
```

## Chi tiết

### 1. Trigger
- Time-driven: mỗi ngày 1 lần (ví dụ 8h sáng)
- Có thể chạy thủ công để test

> [!tip] Xử lý trùng lặp
> Dùng cột `Link` làm key. Kiểm tra Link đã tồn tại trong Sheet chưa trước khi append.

### 2. Xử lý lỗi
- Nếu 1 nguồn lỗi → ghi log, skip, không ảnh hưởng nguồn khác
- Nếu timeout → retry 1 lần, nếu vẫn lỗi thì bỏ qua

### 3. Backfill lịch sử
- Script riêng (không chạy trigger)
- Crawl từ RSS archive hoặc search Google site:...
- Giới hạn request để tránh rate limit

## Liên kết
- Xem [[Projects/DA2/overview|Tổng quan dự án]]
- Xem [[Projects/DA2/feature|Tính năng]] chi tiết
