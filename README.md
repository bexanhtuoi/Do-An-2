# DA2 — Nhóm 2: Bất động sản / Xây dựng / KCN

Crawl tin tức từ **41 nguồn** (96 RSS + 22 API) cho **17 mã cổ phiếu** BĐS / Xây dựng / KCN.

## Kiến trúc

### Python (crawl lịch sử)

```
main.py ──► pipeline.py ──► lib/ (config, models, fetch, extract, store, enrich, stats)

crawl-links:    RSS (96, sequential) + API (22, 8 workers) ──► SOURCE_INDEX (124K+)
crawl-content:  title scan (STOCK_PATTERN) ──► fetch content ──► NEWS_RAW (4,462 articles)
daily:          RSS latest + API page 1 ──► SOURCE_INDEX (append)
```

### GAS (chạy hàng ngày trên cloud)

```
GS/Code.gs ──► daily()
  B1: crawl RSS (96 feeds) + API (22 zones, page 1)
  B2: keyword filter (findMatchingKeyword)
  B3: date filter (isRecentDate — hôm qua / hôm nay)
  B4: dedup by URL + content_hash
  B5: flush → SOURCE_INDEX + NEWS_RAW
  B6: ghi CRAWL_LOG
  B7: cập nhật DAILY_SUMMARY
```

## Sheets (10 tabs trong Google Sheets)

| Sheet | Mô tả |
|-------|-------|
| COMPANY_INFO | Thông tin 17 công ty |
| SOURCE_LIST | Danh sách 41 nguồn tin |
| SOURCE_INDEX | 124,792 link đã crawl |
| NEWS_RAW | 4,462 bài enriched (18 cột) |
| CONFIG_SOURCES | Cấu hình nguồn |
| CONFIG_KEYWORDS | 58 từ khóa + mã CP |
| CRAWL_LOG | Lịch sử chạy daily |
| DAILY_SUMMARY | Tổng kết theo ngày |
| DATA_QUALITY_CHECK | Kiểm tra chất lượng |
| README | Mô tả bộ dữ liệu |

## Mã cổ phiếu theo dõi (17)

VHM, VIC, VRE, NVL, PDR, DXG, KDH, NLG, CEO, DIG, KBC, BCM, SZC, VCG, CTD, HHV, CII

## Thư mục

| Path | Mô tả |
|------|-------|
| `GS/` | Google Apps Script (9 files) |
| `lib/` | Python modules |
| `data/` | xlsx đầu ra + báo cáo |
| `log/` | Crawl logs |

## GAS Deployment

- **Spreadsheet**: `K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN` (Google Sheets)
- **Script**: Bound script, trigger daily lúc 08:00 và 20:00
- **Push**: `cd GS && clasp push`
- **Test local**: `cd GS && node test_local.js` (77 tests)

## Dependencies (Python)

```bash
pip install requests feedparser beautifulsoup4 lxml openpyxl
```

## Commands

```bash
python main.py crawl-links    # Crawl lịch sử (RSS + multi-page API)
python main.py crawl-content  # Enrich → NEWS_RAW
python main.py daily          # Incremental daily
python main.py stats          # Thống kê
```
