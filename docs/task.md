> [!example] Task list — cập nhật 06/06/2026

## Phase 1: Prototype Python ✅
- [x] 41 nguồn tin: 3 RSS+API + 38 RSS only
- [x] Modular: lib/ + pipeline.py + main.py CLI
- [x] SOURCE_INDEX: 6 cột, 124,792 links
- [x] Accumulator: batch 500, O(1) dedup
- [x] Crawl đến 404
- [x] Enrichment: title scan → fetch content → NEWS_RAW (4,462 articles)
- [x] False positive filter
- [x] Daily runner
- [x] 10 statistical charts + summary report

## Phase 2: Chạy lấy dữ liệu ✅
- [x] `python main.py crawl-links` → 124,792 links
- [x] `python main.py crawl-content` → 4,462 articles enriched
- [x] Stats verified
- [x] Dead code cleanup (test/, dead functions, 23→11 files)

## Phase 3: Google Apps Script ✅
- [x] Port daily() sang GAS (9 files, 77 tests)
- [x] Time-driven trigger (08:00 + 20:00)
- [x] Fix remainingTime() wrapper
- [x] Fix getActiveSpreadsheet() → openById()

## Known Issues
- CafeF API trên GAS trả về null (cần debug URL endpoint)
- RSS feeds một số nguồn có XML lỗi → XmlService.parse() fail
- Thứ 7 + CN không có trigger (chỉ weekday)
