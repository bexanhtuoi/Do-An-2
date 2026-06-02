## Nguồn tin

### 1. RSS Feeds — ưu tiên hàng đầu
Dễ parse, chuẩn hóa, ít bị block.

| Nguồn | RSS URL | Ghi chú |
|-------|---------|---------|
| **Cafef.vn** | `https://cafef.vn/oto-xe-may.rss` | Tin oto |
| | `https://cafef.vn/doanh-nghiep.rss` | Tin doanh nghiệp |
| | `https://cafef.vn/thi-truong-chung-khoan.rss` | Tin chứng khoán |
| **VnExpress** | `https://vnexpress.net/rss/oto-xe-may.rss` | Chuyên mục ô tô |
| | `https://vnexpress.net/rss/kinh-doanh.rss` | Kinh doanh |
| **Vietnamnet** | `https://vietnamnet.vn/rss/oto-xe-may.rss` | Ô tô |
| | `https://vietnamnet.vn/rss/kinh-doanh.rss` | Kinh doanh |
| **NDH.vn** | `https://ndh.vn/rss/oto-xe-may.rss` | Ô tô |
| **Tinnhanhchungkhoan.vn** | `https://tinnhanhchungkhoan.vn/rss/oto-xe-may.rss` | |
| **Baogiaothong.vn** | `https://www.baogiaothong.vn/rss/oto-xe-may.rss` | |
| **Autopro.com.vn** | `https://autopro.com.vn/rss.rss` | Tin xe chuyên sâu |

### 2. Trang tài chính có search
Các trang có chức năng search theo mã CK — dùng cho backfill + crawl hằng ngày.

| Trang | URL gốc | Phương pháp |
|-------|---------|-------------|
| **Cafef.vn** | `https://s.cafef.vn/bao-cao-tai-chinh/VMA/` | Theo mã doanh nghiệp |
| **Vietstock.vn** | `https://vietstock.vn/VMA/...` | Tin theo mã |
| **Fireant.vn** | `https://fireant.vn/...` | Có API không chính thức |
| **Stockbiz.vn** | `https://stockbiz.vn/...` | Trang thông tin doanh nghiệp |
| **24hMoney** | `https://24hmoney.vn/...` | Thông tin tài chính |

### 3. Web Search (chủ động)
Search DuckDuckGo theo keyword để tìm tin tức không nằm trong RSS.

> [!example] Search keywords
> Mỗi công ty có 3 keyword: tên viết tắt, tên đầy đủ, mã CK.
> Xem chi tiết trong [[main.py#COMPANY_KEYWORDS]]

## Chiến lược crawl

- **Hằng ngày**: RSS → parse → kiểm tra mention → ghi Sheet
- **Backfill**: Crawl theo URL pattern + Google News Archive với filter date range

## Xác định mention (1/0)

```regex
\b(VMA|TMT|SVC|HAX|HTL|GGG|HHS)\b
```

Duyệt `title + content` viết HOA, dùng word boundary để tránh False Positive.

> [!warning] Content trim
> Google Sheet giới hạn ~10k ký tự mỗi ô. Nếu content dài hơn thì trim.

## Giới hạn Google Apps Script
- `UrlFetchApp.fetch()`: tối đa 60s mỗi request
- Thời gian chạy tối đa: 30 phút (free) / 6 phút (trigger)
- → Tách nhiều trigger chạy so le nếu cần
- → Dùng `CacheService` để lưu state giữa các lần chạy
