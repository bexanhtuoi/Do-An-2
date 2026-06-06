> [!success] Kết quả — cập nhật 06/06/2026

## Sources

| Metric | Giá trị |
|--------|---------|
| Tổng nguồn | 41 |
| RSS+API | 3 (CafeF, CafeBiz, VietnamNet) |
| RSS only | 38 |
| RSS feeds | 96 |
| API zones | 22 |
| Stock codes | 17 |

## Dữ liệu Python

| Sheet | Số dòng |
|-------|---------|
| SOURCE_INDEX | 124,792 |
| NEWS_RAW | 4,462 |
| CONFIG_KEYWORDS | 58 |
| COMPANY_INFO | 17 |
| SOURCE_LIST | 41 |

## GAS Daily Test (06/06/2026)

| Lần | SOURCE_INDEX | NEWS_RAW |
|-----|-------------|----------|
| 1 | +1,315 | +33 |
| 2 | +4 | +0 |
| 3 | +721 | +15 |

## Phân bố ticker (NEWS_RAW)

| Mã | Số bài |
|----|--------|
| NVL | 2,215 |
| VIC | 1,941 |
| VHM | 1,771 |
| DXG | 273 |
| DIG | 50 |
| ... | ... |
| CII | 1 |

## Kiến trúc
- Python: lib/ + pipeline.py + main.py CLI
- GAS: 9 files, clasp push, 2 triggers daily
- Output: Google Sheets (10 tabs) + xlsx backup

## Bug đã fix
- `VIETNAMESE_CHARS` regex thiếu `re.IGNORECASE` / `i` flag
- `remainingTime()` đệ quy vô hạn (replaceAll lỗi)
- `getActiveSpreadsheet()` → `openById()` để ghi đúng file
