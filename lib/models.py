from dataclasses import dataclass
from datetime import datetime

SOURCE_INDEX_HEADERS = [
    "Link",
    "Source",
    "Category",
    "Title",
    "Datetime Public",
    "Status",
]

NEWS_RAW_HEADERS = [
    "news_id",
    "title",
    "summary",
    "content",
    "published_date",
    "source",
    "url",
    "industry_group",
    "tickers",
    "keywords",
    "event_type",
    "crawl_time",
    "content_hash",
    "crawl_status",
    "error_message",
    "checked_by",
    "checked_time",
    "note",
]

CONFIG_SOURCES_HEADERS = [
    "source_id",
    "source_name",
    "base_url",
    "search_url_pattern",
    "category_url",
    "category_tags",
    "type",
    "has_rss",
    "has_api",
    "allowed_to_crawl",
    "crawl_method",
    "articles_estimate",
    "note",
]

CONFIG_KEYWORDS_HEADERS = [
    "keyword_id",
    "keyword",
    "industry_group",
    "related_tickers",
    "event_type_suggestion",
    "priority",
    "note",
]

CRAWL_LOG_HEADERS = [
    "log_id",
    "log_date",
    "member",
    "source",
    "keyword_group",
    "date_range_from",
    "date_range_to",
    "records_found",
    "records_added",
    "duplicates",
    "failed",
    "status",
    "note",
]

DAILY_SUMMARY_HEADERS = [
    "date",
    "total_records",
    "new_records_today",
    "sources_updated",
    "date_coverage_from",
    "date_coverage_to",
    "missing_days",
    "duplicate_count",
    "issue_status",
    "next_action",
]

DATA_QUALITY_CHECK_HEADERS = [
    "check_id",
    "check_date",
    "checked_by",
    "total_records",
    "missing_title",
    "missing_url",
    "missing_published_date",
    "missing_content",
    "duplicated_url",
    "duplicated_content_hash",
    "wrong_date_format",
    "note",
]

README_HEADERS = [
    "field",
    "value",
]

README_ROWS = [
    ["group_id", "G1"],
    ["group_name", "Nhóm 2 - Bất động sản / Xây dựng / Khu công nghiệp"],
    ["members", "SV2, SV3"],
    ["leader", "SV2"],
    ["project_start_date", "2025-01-01"],
    ["update_frequency", "Daily (via python main.py daily)"],
    ["data_sources",
     "41 nguồn tin: CafeF, CafeBiz, VietnamNet, VnExpress, VnBusiness, VnEconomy, Thanh Niên, Dân trí, Báo Xây dựng, NLD, VietnamPlus, Tuổi Trẻ, Nhân Dân, Tiền Phong, Soha, ANTĐ, CAND, Công Thương, SKĐS, Infonet, Kiến Thức, PLO, VTC News, 24h, Docnhanh, Nguoiduatin, KTVN Times, VietTimes, Diễn đàn KT, Công Luận, Biz Việt, Reatimes, VTV, ZNEWS, TINMOI, Đầu tư Việt Nam, ANTT, VietnamBiz, Ngân hàng Việt Nam, Đời sống Việt Nam, Doanh nghiệp Việt Nam"],
    ["crawl_method", "RSS (96 feeds) + API (22 zones) - 8 workers parallel"],
    ["enrichment_method", "Title scan (124,792) -> Content fetch (4,462 candidates) -> ThreadPoolExecutor 8 workers"],
    ["data_coverage_source_index", "124,792 links từ 2011-03-25 đến 2026-06-05"],
    ["data_coverage_news_raw", "4,462 candidates, 4,398 enriched với content + ticker detection"],
    ["stock_codes_monitored", "VHM, VIC, VRE, NVL, PDR, DXG, KDH, NLG, CEO, DIG, KBC, BCM, SZC, VCG, CTD, HHV, CII (17 codes)"],
    ["ticker_mention_top5", "NVL (2,215), VIC (1,941), VHM (1,771), DXG (273), VRE (272)"],
    ["top_sources", "CafeBiz (20K), CafeBiz TC (16K), CafeF DN (10K), CafeF Vĩ mô (10K), CafeF TC (10K)"],
    ["sheets_description",
     "COMPANY_INFO: 17 companies | SOURCE_LIST: 41 sources | SOURCE_INDEX: 124,792 links (6 cols) | NEWS_RAW: 4,398 enriched (18 cols) | CONFIG_SOURCES: 41 sources (13 cols) | CONFIG_KEYWORDS: 58 keywords (7 cols) | CRAWL_LOG: Crawl history | DAILY_SUMMARY: Progress | DATA_QUALITY_CHECK: Quality | README: This sheet"],
    ["news_raw_columns",
     "news_id, title, summary, content, published_date, source, url, industry_group, tickers, keywords, event_type, crawl_time, content_hash, crawl_status, error_message, checked_by, checked_time, note"],
    ["quality_metrics",
     "missing_title=0, missing_url=0, missing_pub_date=0, dup_url=0, dup_hash=0, wrong_date=0, missing_content=13 (failed fetches)"],
    ["spreadsheet_owner", "Nhóm 2"],
    ["note",
     "Dự án crawl tin tức nhóm Bất động sản / Xây dựng / Khu công nghiệp cho 17 mã CP. CLI: python main.py {crawl-links, crawl-content, daily, stats}"],
]



