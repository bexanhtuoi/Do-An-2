var SOURCE_INDEX_HEADERS = [
  "Link", "Source", "Category", "Title", "Datetime Public", "Status"
];

var NEWS_RAW_HEADERS = [
  "news_id", "title", "summary", "content", "published_date", "source",
  "url", "industry_group", "tickers", "keywords", "event_type",
  "crawl_time", "content_hash", "crawl_status", "error_message",
  "checked_by", "checked_time", "note"
];

var CONFIG_SOURCES_HEADERS = [
  "source_id", "source_name", "base_url", "search_url_pattern",
  "category_url", "category_tags", "type", "has_rss", "has_api",
  "allowed_to_crawl", "crawl_method", "articles_estimate", "note"
];

var CONFIG_KEYWORDS_HEADERS = [
  "keyword_id", "keyword", "industry_group", "related_tickers",
  "event_type_suggestion", "priority", "note"
];

var CRAWL_LOG_HEADERS = [
  "log_id", "log_date", "member", "source", "keyword_group",
  "date_range_from", "date_range_to", "records_found",
  "records_added", "duplicates", "failed", "status", "note"
];

var DAILY_SUMMARY_HEADERS = [
  "date", "total_records", "new_records_today", "sources_updated",
  "date_coverage_from", "date_coverage_to", "missing_days",
  "duplicate_count", "issue_status", "next_action"
];

var DATA_QUALITY_CHECK_HEADERS = [
  "check_id", "check_date", "checked_by", "total_records",
  "missing_title", "missing_url", "missing_published_date",
  "missing_content", "duplicated_url", "duplicated_content_hash",
  "wrong_date_format", "note"
];

var README_HEADERS = ["field", "value"];

var README_ROWS = [
  ["group_id", "G1"],
  ["group_name", "Nhóm 2 - B\u1ea5t \u0111\u1ed9ng s\u1ea3n / X\u00e2y d\u1ef1ng / Khu c\u00f4ng nghi\u1ec7p"],
  ["members", "SV2, SV3"],
  ["leader", "SV2"],
  ["project_start_date", "2025-01-01"],
  ["update_frequency", "Daily (GAS trigger)"],
  ["data_sources",
   "41 ngu\u1ed3n tin: CafeF, CafeBiz, VietnamNet, VnExpress, VnBusiness, VnEconomy, Thanh Ni\u00ean, D\u00e2n tr\u00ed, B\u00e1o X\u00e2y d\u1ef1ng, NLD, VietnamPlus, Tu\u1ed5i Tr\u1ebb, Nh\u00e2n D\u00e2n, Ti\u1ec1n Phong, Soha, ANT\u0110, CAND, C\u00f4ng Th\u01b0\u01a1ng, SK\u0110S, Infonet, Ki\u1ebfn Th\u1ee9c, PLO, VTC News, 24h, Docnhanh, Nguoiduatin, KTVN Times, VietTimes, Di\u1ec5n \u0111\u00e0n KT, C\u00f4ng Lu\u1eadn, Biz Vi\u1ec7t, Reatimes, VTV, ZNEWS, TINMOI, \u0110\u1ea7u t\u01b0 Vi\u1ec7t Nam, ANTT, VietnamBiz, Ng\u00e2n h\u00e0ng Vi\u1ec7t Nam, \u0110\u1eddi s\u1ed1ng Vi\u1ec7t Nam, Doanh nghi\u1ec7p Vi\u1ec7t Nam"],
  ["crawl_method", "RSS (96 feeds) + API (22 zones) - UrlFetchApp.fetchAll batching"],
  ["enrichment_method", "Title scan -> Content fetch (sequential in GAS)"],
  ["data_coverage_source_index", "Li\u00ean t\u1ee5c c\u1eadp nh\u1eadt h\u00e0ng ng\u00e0y"],
  ["data_coverage_news_raw", "B\u00e0i vi\u1ebft c\u00f3 \u0111\u1ec1 c\u1eadp m\u00e3 c\u1ed5 phi\u1ebfu"],
  ["stock_codes_monitored", "VHM, VIC, VRE, NVL, PDR, DXG, KDH, NLG, CEO, DIG, KBC, BCM, SZC, VCG, CTD, HHV, CII"],
  ["sheets_description",
   "COMPANY_INFO | SOURCE_LIST | SOURCE_INDEX | NEWS_RAW | CONFIG_SOURCES | CONFIG_KEYWORDS | CRAWL_LOG | DAILY_SUMMARY | DATA_QUALITY_CHECK | README"],
  ["news_raw_columns",
   "news_id, title, summary, content, published_date, source, url, industry_group, tickers, keywords, event_type, crawl_time, content_hash, crawl_status, error_message, checked_by, checked_time, note"],
  ["spreadsheet_owner", "Nh\u00f3m 2"],
  ["note", "D\u1ef1 \u00e1n crawl tin t\u1ee9c B\u0110S / X\u00e2y d\u1ef1ng / KCN cho 17 m\u00e3 CP. Ch\u1ea1y daily qua GAS trigger."]
];

var SOURCE_INDEX_NAME = "SOURCE_INDEX";
var NEWS_RAW_NAME = "NEWS_RAW";
var CONFIG_SOURCES_NAME = "CONFIG_SOURCES";
var CONFIG_KEYWORDS_NAME = "CONFIG_KEYWORDS";
var CRAWL_LOG_NAME = "CRAWL_LOG";
var DAILY_SUMMARY_NAME = "DAILY_SUMMARY";
var DATA_QUALITY_NAME = "DATA_QUALITY_CHECK";
var README_NAME = "README";
var COMPANY_INFO_NAME = "COMPANY_INFO";
var NGUON_TIN_NAME = "SOURCE_LIST";
