> [!info] Mục tiêu
> Crawl dữ liệu tin tức hằng ngày về **7 công ty ô tô đã niêm yết** trên sàn chứng khoán Việt Nam (HOSE/UPCoM) bằng **Google Apps Script**, lưu trữ vào **Google Sheets**.

## Các công ty mục tiêu

| # | Công ty | Mã CK | Sàn | Năm TL | Năm NY | Lĩnh vực chính |
|---|---------|-------|-----|--------|--------|----------------|
| 1 | CTCP Công nghiệp Ô tô - Vinacomin | `VMA` | UPCoM | 1960 | 2015 | Công nghiệp ô tô, cơ khí |
| 2 | CTCP Ô tô TMT | `TMT` | HOSE | 1976 | 2010 | Nhập khẩu, phân phối ô tô |
| 3 | CTCP Dịch vụ Tổng hợp Sài Gòn (Savico) | `SVC` | HOSE | 1982 | 2009 | Phân phối ô tô (số 1 VN) |
| 4 | CTCP Dịch vụ Ô tô Hàng Xanh (HAX) | `HAX` | HOSE | 1992 | 2008 | Phân phối Mercedes-Benz, MG |
| 5 | CTCP Kỹ thuật và Ô tô Trường Long | `HTL` | HOSE | 1998 | 2011 | Kỹ thuật ô tô, phân phối xe tải |
| 6 | CTCP Ô tô Giải Phóng | `GGG` | HOSE | 2001 | - | Sản xuất ô tô tải |
| 7 | CTCP Đầu tư Dịch vụ Hoàng Huy | `HHS` | HOSE | 2008 | - | Nhập khẩu ô tô, BĐS |

## Cấu trúc dữ liệu

| Cột | Mô tả |
|-----|-------|
| Datetime | Ngày giờ crawl |
| Link | URL bài viết |
| Source | Nguồn (vnexpress, cafef, ...) |
| Title | Tiêu đề bài viết |
| Content | Nội dung bài viết |
| `VMA` | 1 nếu mention, 0 nếu không |
| `TMT` | 1 nếu mention, 0 nếu không |
| `SVC` | 1 nếu mention, 0 nếu không |
| `HAX` | 1 nếu mention, 0 nếu không |
| `HTL` | 1 nếu mention, 0 nếu không |
| `GGG` | 1 nếu mention, 0 nếu không |
| `HHS` | 1 nếu mention, 0 nếu không |
| Datetime Public | Ngày giờ đăng bài |

> [!warning] Yêu cầu
> - Crawl hằng ngày tự động qua Google Apps Script
> - Dữ liệu tối thiểu **3 năm gần đây**
> - Không giới hạn số năm, càng nhiều càng tốt
> - Mỗi tin tức có thể gắn với 1 hoặc nhiều công ty (cột 1/0)

## Liên kết

- Xem chi tiết [[Projects/DA2/feature|Tính năng]]
- Xem [[Projects/DA2/workflow|Workflow]] hoạt động
- [[Projects/DA2/plan-crawl|Kế hoạch Crawl]] chi tiết
