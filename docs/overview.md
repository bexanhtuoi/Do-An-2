> [!info] DA2 — Crawl tin tức BĐS & CK cho 17 mã chứng khoán
> Cập nhật: 06/06/2026

## Mục tiêu
Crawl 124K+ bài báo từ **41 nguồn** (96 RSS + 22 API) tin tức Việt Nam, phát hiện đề cập đến 17 mã chứng khoán BĐS/XD/KCN, xuất ra Google Sheet phục vụ phân tích.

## Kiến trúc

### Python (crawl lịch sử)
```
RSS (96 feeds, 41 sources) ──┐
API (22 zones: CafeF 9 +     ├──→ SOURCE_INDEX (124K links)
      CafeBiz 5 + VNNet 8) ──┘       │
                                      ├──→ Enrich (title scan + fetch content)
                                            → NEWS_RAW (4,462 articles)
```

### GAS (chạy daily trên cloud)
```
daily() → RSS (96) + API (22, page 1)
        → keyword filter
        → date filter (today/yesterday)
        → dedup → SOURCE_INDEX + NEWS_RAW
        → CRAWL_LOG + DAILY_SUMMARY
        → Trigger: 08:00 + 20:00 daily
```

## Nguồn tin

| Loại | Số lượng | Chi tiết |
|------|----------|----------|
| RSS + API | 3 | CafeF, CafeBiz, VietnamNet |
| RSS only | 38 | VnExpress, VnBusiness, VnEconomy, Thanh Niên, Dân trí, Báo Xây dựng, NLD, VietnamPlus, Tuổi Trẻ, Nhân Dân, Tiền Phong, Soha, ANTĐ, CAND, Công Thương, SKĐS, Infonet, Kiến Thức, PLO, VTC News, 24h, Docnhanh, Nguoiduatin, KTVN Times, VietTimes, Diễn đàn KT, Công Luận, Biz Việt, Reatimes, VTV, ZNEWS, TINMOI, Đầu tư Việt Nam, ANTT, VietnamBiz, Ngân hàng Việt Nam, Đời sống Việt Nam, Doanh nghiệp Việt Nam |
| **Tổng** | **41** | **96 RSS feeds, 22 API zones** |

## Data Flow

- **Phase 1 (crawl-links)**: RSS + API → SOURCE_INDEX (124,792 links)
- **Phase 2 (crawl-content)**: Title scan → fetch content bài match ticker → NEWS_RAW (4,462 articles)
- **GAS daily**: RSS latest + API page 1 → SOURCE_INDEX + NEWS_RAW (trigger 08:00 + 20:00)

## Sheets (10 tabs)

COMPANY_INFO | SOURCE_LIST | SOURCE_INDEX | NEWS_RAW | CONFIG_SOURCES | CONFIG_KEYWORDS | CRAWL_LOG | DAILY_SUMMARY | DATA_QUALITY_CHECK | README

## Stock Codes
VHM, VIC, VRE, NVL, PDR, DXG, KDH, NLG, CEO, DIG, KBC, BCM, SZC, VCG, CTD, HHV, CII

## Liên kết
- [[Projects/DA2/plan-crawl|Chi tiết nguồn crawl]]
- [[Projects/DA2/feature|Tính năng]]
- [[Projects/DA2/results|Kết quả]]
- [[Projects/DA2/workflow|Workflow]]
- [[Projects/DA2/task|Task list]]
