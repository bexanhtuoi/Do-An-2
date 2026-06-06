> [!success] Tính năng (06/06/2026)

## Source Index Architecture
- SOURCE_INDEX: 6 cột (Link, Source, Category, Title, Datetime Public, Status)
- NEWS_RAW: 18 cột (news_id → note)
- Tách biệt indexing và enrichment

## Crawl đến 404
- 404 / network error → dừng
- 3 page liên tiếp empty → dừng
- Không hardcoded max_pages

## Batch Save
- Accumulate 500 entries in-memory → flush 1 lần
- O(1) dedup via Set/Hash
- GAS: accumulator + flush ở cuối daily()

## 41 Nguồn tin
- 3 nguồn RSS+API: CafeF, CafeBiz, VietnamNet
- 38 nguồn RSS only
- 96 RSS feeds, 22 API zones

## GAS Daily Trigger
- `daily()`: 7 bước (crawl → filter → dedup → flush)
- Keyword filter: 58 keywords từ CONFIG_KEYWORDS
- Date filter: chỉ lấy bài hôm qua/hôm nay
- 2 triggers: 08:00 + 20:00

## CLI Commands
| Command | Chức năng |
|---------|-----------|
| `python main.py crawl-links` | Phase 1: Index tất cả nguồn (124K links) |
| `python main.py crawl-content` | Phase 2: Enrich → NEWS_RAW (4,462 articles) |
| `python main.py daily` | Daily: RSS + API page 1 |
| `python main.py stats` | Thống kê coverage |
| `cd GS && node test_local.js` | Test GAS (77 tests) |
| `cd GS && clasp push` | Deploy lên cloud |

## GAS Files (9 files)
| File | Chức năng |
|------|-----------|
| Code.gs | daily(), crawlRssSource, crawlApiPage1, helpers |
| Config.gs | Constants, stock codes, 41 sources, 96 RSS, 22 API, 58 keywords |
| Models.gs | 10 sheet headers + README_ROWS |
| Fetch.gs | fetchUrl, fetchMultiple, normalizeDate, md5Hash |
| Extract.gs | parseRssArticles, indexRssSource, API extractors |
| Enrich.gs | detectMentionsInText, findMatchingKeyword |
| Store.gs | initWorkbook, ensureAllSheets, accumulators, flush |
| Log.gs | LOG_BUFFER, logInfo/Warn/Error/Fetch/Rss, flushLog |
| appsscript.json | V8 runtime, Asia/Ho_Chi_Minh TZ |
