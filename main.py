import re
import sys
import time
from datetime import datetime, timezone
from dataclasses import dataclass
sys.stdout.reconfigure(encoding="utf-8")

import requests
import feedparser
from bs4 import BeautifulSoup


STOCK_CODES = ["VMA", "TMT", "SVC", "HAX", "HTL", "GGG", "HHS"]

STOCK_PATTERN = re.compile(r"\b(" + "|".join(STOCK_CODES) + r")\b")

COMPANY_KEYWORDS: dict[str, list[str]] = {
    "VMA": ["Vinacomin", "Công nghiệp Ô tô Vinacomin"],
    "TMT": ["Ô tô TMT", "TMT Motors"],
    "SVC": ["Savico", "Dịch vụ Tổng hợp Sài Gòn"],
    "HAX": ["Hàng Xanh", "Dịch vụ Ô tô Hàng Xanh", "Haxaco"],
    "HTL": ["Kỹ thuật và Ô tô Trường Long", "Trường Long", "Truong Long"],
    "GGG": ["Ô tô Giải Phóng", "Auto Giải Phóng"],
    "HHS": ["Hoàng Huy", "Đầu tư Dịch vụ Hoàng Huy"],
}

COMPANY_NAME_PATTERNS: dict[str, re.Pattern] = {}
for code, keywords in COMPANY_KEYWORDS.items():
    escaped = [re.escape(kw) for kw in keywords]
    COMPANY_NAME_PATTERNS[code] = re.compile(r"(?i)(" + "|".join(escaped) + r")")

RSS_SOURCES: list[dict] = [
    {"name": "Cafef Oto", "url": "https://cafef.vn/oto-xe-may.rss"},
    {"name": "Cafef CK", "url": "https://cafef.vn/thi-truong-chung-khoan.rss"},
    {"name": "Cafef DN", "url": "https://cafef.vn/doanh-nghiep.rss"},
    {"name": "VnExpress Oto", "url": "https://vnexpress.net/rss/oto-xe-may.rss"},
    {"name": "VnExpress KD", "url": "https://vnexpress.net/rss/kinh-doanh.rss"},
    {"name": "Vietnamnet Oto", "url": "https://vietnamnet.vn/rss/oto-xe-may.rss"},
    {"name": "Vietnamnet KD", "url": "https://vietnamnet.vn/rss/kinh-doanh.rss"},
    {"name": "CafeBiz", "url": "https://cafebiz.vn/kinh-doanh.rss"},
    {"name": "NDH", "url": "https://ndh.vn/feed.rss"},
    {"name": "Baodautu CK", "url": "https://baodautu.vn/chung-khoan.rss"},
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 30
MAX_RETRIES = 2
SEARCH_MAX_RESULTS = 15

SEARCH_TERMS: dict[str, list[str]] = {
    "VMA": ["VMA cổ phiếu", "VMA chứng khoán", "VMA Vinacomin"],
    "TMT": ["TMT cổ phiếu", "TMT chứng khoán", "TMT ô tô"],
    "SVC": ["SVC cổ phiếu", "SVC chứng khoán", "SVC Savico"],
    "HAX": ["HAX cổ phiếu", "HAX chứng khoán", "HAX Haxaco"],
    "HTL": ["HTL cổ phiếu", "HTL chứng khoán", "HTL Trường Long"],
    "GGG": ["GGG cổ phiếu", "GGG chứng khoán", "GGG Giải Phóng"],
    "HHS": ["HHS cổ phiếu", "HHS chứng khoán", "HHS Hoàng Huy"],
}

BLOCKED_DOMAINS = [
    "wikipedia.org", "hhs.gov", "grokipedia", "wikidata.org",
    "wikimedia.org", "windy.com", "pinterest", "nordinvasion.com",
]

VIETNAMESE_CHARS = re.compile(r"[ăâđêôơưàảãáạăằẳẵắặâầẩẫấậđèẻẽéẹêềểễếệìỉĩíịòỏõóọôồổỗốộơờởỡớợùủũúụưừửữứựỳỷỹýỵ]")


@dataclass
class Article:
    link: str
    source: str
    title: str
    content: str
    datetime_public: str

    def __post_init__(self):
        self.mentions: dict[str, int] = {code: 0 for code in STOCK_CODES}


def fetch_url(url: str) -> str | None:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException:
            if attempt == MAX_RETRIES - 1:
                return None
            time.sleep(2 ** attempt)


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def strip_html_tags(html_text: str) -> str:
    soup = BeautifulSoup(html_text, "lxml")
    return soup.get_text(separator=" ", strip=True)


def normalize_date(date_str: str) -> str:
    try:
        parsed = feedparser._parse_date(date_str)
        if parsed:
            dt = datetime(*parsed[:6], tzinfo=timezone.utc)
            return dt.isoformat()
    except Exception:
        pass
    return date_str


def web_search(keywords: list[str], max_results: int = SEARCH_MAX_RESULTS) -> list[dict]:
    from ddgs import DDGS
    all_results: list[dict] = []
    seen_urls: set[str] = set()

    for keyword in keywords:
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(keyword, max_results=max_results):
                    url = r.get("href", "").strip()
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        all_results.append({
                            "title": r.get("title", ""),
                            "href": url,
                            "body": r.get("body", ""),
                        })
        except Exception:
            pass
        time.sleep(1)

    return all_results


def web_fetch_article(url: str, source_name: str) -> Article | None:
    html = fetch_url(url)
    if html is None:
        return None
    soup = parse_html(html)
    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    for tag in ("article", "main", "div[itemprop=articleBody]"):
        container = soup.select_one(tag)
        if container:
            break
    else:
        container = soup.find("body")

    content = container.get_text(separator=" ", strip=True) if container else ""
    if len(content) > 10000:
        content = content[:10000]

    return Article(link=url, source=source_name, title=title, content=content, datetime_public="")


def fetch_rss(source: dict) -> str | None:
    return fetch_url(source["url"])


def parse_rss_articles(xml_text: str, source_name: str) -> list[Article]:
    feed = feedparser.parse(xml_text)
    articles: list[Article] = []

    for entry in feed.entries:
        link = entry.get("link", "").strip()
        if not link:
            continue

        title = strip_html_tags(entry.get("title", ""))
        content_html = (
            entry.get("content", [{}])[0].get("value", "")
            or entry.get("summary", "")
            or entry.get("description", "")
        )
        content = strip_html_tags(content_html)
        date_pub = normalize_date(entry.get("published", ""))

        articles.append(
            Article(
                link=link,
                source=source_name,
                title=title,
                content=content,
                datetime_public=date_pub,
            )
        )

    return articles


def fetch_articles_from_rss(source: dict) -> list[Article]:
    xml_text = fetch_rss(source)
    if xml_text is None:
        return []
    return parse_rss_articles(xml_text, source["name"])


def is_blocked_domain(url: str) -> bool:
    return any(d in url.lower() for d in BLOCKED_DOMAINS)


def has_vietnamese(text: str) -> bool:
    return bool(VIETNAMESE_CHARS.search(text))


def detect_mentions(article: Article) -> dict[str, int]:
    text = f"{article.title} {article.content}".upper()
    stock_hits = set(STOCK_PATTERN.findall(text))
    result: dict[str, int] = {}
    for code in STOCK_CODES:
        if code in stock_hits:
            result[code] = 1
        elif COMPANY_NAME_PATTERNS[code].search(text):
            result[code] = 1
        else:
            result[code] = 0
    return result


def filter_false_positives(article: Article) -> None:
    if is_blocked_domain(article.link):
        for code in article.mentions:
            article.mentions[code] = 0
        return
    text = f"{article.title} {article.content}".upper()
    has_vi = has_vietnamese(text)
    for code in STOCK_CODES:
        if article.mentions[code] == 1:
            name_matched = bool(COMPANY_NAME_PATTERNS[code].search(text))
            if not name_matched and not has_vi:
                article.mentions[code] = 0


def enrich_article_with_mentions(article: Article) -> Article:
    article.mentions = detect_mentions(article)
    filter_false_positives(article)
    return article


SHEET_HEADERS = [
    "Datetime",
    "Link",
    "Source",
    "Title",
    "Content",
    *STOCK_CODES,
    "Datetime Public",
]

stored_links: set[str] = set()


def is_duplicate(link: str) -> bool:
    return link in stored_links


def mark_as_stored(link: str) -> None:
    stored_links.add(link)


def article_to_row(article: Article) -> list[str]:
    return [
        datetime.now(timezone.utc).isoformat(),
        article.link,
        article.source,
        article.title,
        article.content,
        *[str(article.mentions[code]) for code in STOCK_CODES],
        article.datetime_public,
    ]


def append_to_sheet(article: Article) -> bool:
    if is_duplicate(article.link):
        return False

    row = article_to_row(article)
    mark_as_stored(article.link)
    print(f"  Appended: {article.title[:60]}... | {row[5:12]}")
    return True


def crawl_rss_source(source: dict) -> list[Article]:
    print(f"[RSS] Fetching: {source['name']} ({source['url']})")
    articles = fetch_articles_from_rss(source)
    print(f"  -> {len(articles)} articles found")

    result: list[Article] = []
    for article in articles:
        if is_duplicate(article.link):
            continue
        enrich_article_with_mentions(article)
        result.append(article)

    return result


def crawl_all_rss() -> list[Article]:
    all_articles: list[Article] = []
    for source in RSS_SOURCES:
        try:
            articles = crawl_rss_source(source)
            all_articles.extend(articles)
        except Exception as e:
            print(f"  [ERROR] {source['name']}: {e}")
    return all_articles


def crawl_by_search() -> list[Article]:
    all_articles: list[Article] = []

    for code in STOCK_CODES:
        print(f"[SEARCH] {code}: company name search")
        results = web_search(COMPANY_KEYWORDS[code])
        for r in results:
            url = r["href"]
            if is_duplicate(url):
                continue
            article = web_fetch_article(url, f"Search:{code}")
            if article is None:
                continue
            enrich_article_with_mentions(article)
            all_articles.append(article)
            mark_as_stored(url)
            print(f"  + {article.title[:60]}... | {article.mentions}")

        print(f"[SEARCH] {code}: stock code search")
        stock_results = web_search(SEARCH_TERMS[code])
        for r in stock_results:
            url = r["href"]
            if is_duplicate(url):
                continue
            article = web_fetch_article(url, f"Search:{code}")
            if article is None:
                continue
            enrich_article_with_mentions(article)
            all_articles.append(article)
            mark_as_stored(url)
            print(f"  + {article.title[:60]}... | {article.mentions}")

    total_unique = len(set(a.link for a in all_articles))
    mentioned = [a for a in all_articles if any(a.mentions.values())]
    print(f"\n[SEARCH DONE] {total_unique} unique fetched, {len(mentioned)} with mentions")
    return all_articles


def save_articles(articles: list[Article]) -> int:
    count = 0
    for article in articles:
        if append_to_sheet(article):
            count += 1
    return count


def run_crawl() -> dict:
    start = datetime.now(timezone.utc)
    print(f"\n=== CRAWL START: {start.isoformat()} ===\n")

    rss_articles = crawl_all_rss()
    saved_rss = save_articles(rss_articles)

    search_articles = crawl_by_search()
    saved_search = save_articles(search_articles)

    articles = rss_articles + search_articles
    saved = saved_rss + saved_search

    end = datetime.now(timezone.utc)
    print(f"\n=== CRAWL DONE: {end.isoformat()} ===")
    print(f"Total fetched: {len(articles)}, New saved: {saved}")
    print(f"Duration: {(end - start).total_seconds():.1f}s")

    return {
        "total": len(articles),
        "new": saved,
        "duration_s": (end - start).total_seconds(),
    }


COMPANY_INFO = [
    {"code": "VMA", "full_name": "CTCP Công nghiệp Ô tô - Vinacomin",
     "english_name": "Vietnam Coal and Mineral Industries Group - Automotive",
     "former_name": "Vinacomin - Công nghiệp Ô tô", "exchange": "UPCoM",
     "industry": "Sản xuất ô tô & phụ tùng", "website": "https://vmic.vn",
     "established": "2007", "employees": "~500",
     "business": "Sản xuất, lắp ráp ô tô; sản xuất phụ tùng; bảo dưỡng, sửa chữa ô tô; kinh doanh thương mại xe ô tô",
     "keywords": "Vinacomin, VMA, VMIC, xe tải Vinacomin"},
    {"code": "TMT", "full_name": "CTCP Ô tô TMT",
     "english_name": "TMT Motor Joint Stock Company",
     "former_name": "Công ty TNHH SX & TM Ô tô TMT", "exchange": "HOSE",
     "industry": "Phân phối ô tô", "website": "https://ototmt.com",
     "established": "2005", "employees": "~300",
     "business": "Phân phối xe tải TATA, HOWO; lắp ráp xe tải; kinh doanh phụ tùng ô tô tải",
     "keywords": "TMT Motors, TMT, xe tải TATA, HOWO TMT"},
    {"code": "SVC", "full_name": "CTCP Dịch vụ Tổng hợp Sài Gòn (Savico)",
     "english_name": "Saigon General Service Corporation (SAVICO)",
     "former_name": "Công ty Dịch vụ Tổng hợp Sài Gòn", "exchange": "HOSE",
     "industry": "Dịch vụ ô tô & Bất động sản", "website": "https://savico.com.vn",
     "established": "1992", "employees": "~1,500",
     "business": "Kinh doanh xe ô tô Mercedes-Benz, Hyundai; trung tâm đăng kiểm; bất động sản; dịch vụ tài chính",
     "keywords": "Savico, SVC, Mercedes-Benz Savico, đại lý ô tô Sài Gòn"},
    {"code": "HAX", "full_name": "CTCP Dịch vụ Ô tô Hàng Xanh (Haxaco)",
     "english_name": "Hang Xanh Motors Service Joint Stock Company (Haxaco)",
     "former_name": "Xí nghiệp Sửa chữa Ô tô Hàng Xanh", "exchange": "HOSE",
     "industry": "Đại lý ô tô cao cấp", "website": "https://haxaco.com.vn",
     "established": "1972", "employees": "~400",
     "business": "Đại lý ủy quyền Mercedes-Benz, VinFast; dịch vụ sửa chữa bảo dưỡng ô tô hạng sang",
     "keywords": "Haxaco, Hàng Xanh, HAX, Mercedes-Benz Haxaco"},
    {"code": "HTL", "full_name": "CTCP Kỹ thuật và Ô tô Trường Long (Truong Long)",
     "english_name": "Truong Long Engineering & Auto Joint Stock Company",
     "former_name": "Công ty TNHH Kỹ thuật Ô tô Trường Long", "exchange": "HOSE",
     "industry": "Sửa chữa & bảo dưỡng ô tô", "website": "https://truonglong.com",
     "established": "2003", "employees": "~200",
     "business": "Sửa chữa, bảo trì, bảo dưỡng ô tô; kinh doanh phụ tùng; dịch vụ kỹ thuật ô tô chuyên nghiệp",
     "keywords": "Trường Long, HTL, kỹ thuật ô tô, bảo dưỡng xe"},
    {"code": "GGG", "full_name": "CTCP Ô tô Giải Phóng",
     "english_name": "Auto Giai Phong Joint Stock Company",
     "former_name": "Xí nghiệp Cơ khí Ô tô Giải Phóng", "exchange": "HOSE",
     "industry": "Phân phối & dịch vụ ô tô tải", "website": "https://otogiaiphong.com.vn",
     "established": "2004", "employees": "~150",
     "business": "Phân phối xe tải JAC, xe chuyên dùng; dịch vụ sửa chữa; bảo dưỡng xe tải",
     "keywords": "Ô tô Giải Phóng, Auto Giải Phóng, GGG, xe tải JAC"},
    {"code": "HHS", "full_name": "CTCP Đầu tư Dịch vụ Hoàng Huy",
     "english_name": "Hoang Huy Investment Services Joint Stock Company",
     "former_name": "CTCP Vận tải Hoàng Huy", "exchange": "HOSE",
     "industry": "Đầu tư & Dịch vụ", "website": "https://hoanghuyinvest.vn",
     "established": "2006", "employees": "~250",
     "business": "Đầu tư tài chính; dịch vụ logistics; kinh doanh bất động sản; vận tải",
     "keywords": "Hoàng Huy, HHS, Hoàng Huy Invest, dịch vụ đầu tư"},
]


def export_xlsx(output_path: str = "") -> None:
    import openpyxl as xl
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

    if not output_path:
        output_path = r"C:\Users\PC\Downloads\DA2\data\crawl_output.xlsx"

    hdr_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    hdr_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    body_font = Font(name="Calibri", size=11)
    thin = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    wrap = Alignment(wrap_text=True)

    wb = xl.Workbook()
    ws1 = wb.active
    ws1.title = "Company Info"
    fields = ["Mã CK", "Tên đầy đủ", "Tên tiếng Anh", "Tên cũ", "Sàn", "Ngành", "Website", "Thành lập", "Nhân sự", "Kinh doanh chính", "Từ khóa"]
    for col, f in enumerate(fields, 1):
        c = ws1.cell(row=1, column=col, value=f)
        c.fill = hdr_fill; c.font = hdr_font; c.border = thin; c.alignment = Alignment(horizontal="center", vertical="center")
    for ri, ci in enumerate(COMPANY_INFO, 2):
        vals = [ci["code"], ci["full_name"], ci["english_name"], ci["former_name"], ci["exchange"], ci["industry"], ci["website"], ci["established"], ci["employees"], ci["business"], ci["keywords"]]
        for ci2, v in enumerate(vals, 1):
            c = ws1.cell(row=ri, column=ci2, value=v)
            c.font = body_font; c.border = thin; c.alignment = wrap
    widths1 = [8, 40, 40, 35, 8, 25, 30, 10, 10, 60, 40]
    for i, w in enumerate(widths1, 1):
        ws1.column_dimensions[xl.utils.get_column_letter(i)].width = w
    ws1.auto_filter.ref = f"A1:K{len(COMPANY_INFO) + 1}"
    ws1.freeze_panes = "A2"

    print("Running crawl for xlsx export...")
    stored_links.clear()
    all_a: list[Article] = []
    for src in RSS_SOURCES:
        try:
            all_a.extend(crawl_rss_source(src))
        except Exception as e:
            print(f"  RSS error {src['name']}: {e}")
    for code in STOCK_CODES:
        try:
            for res in web_search(COMPANY_KEYWORDS[code], max_results=5):
                if not is_duplicate(res["href"]):
                    a = web_fetch_article(res["href"], f"Search:{code}")
                    if a: enrich_article_with_mentions(a); mark_as_stored(res["href"]); all_a.append(a)
            for res in web_search(SEARCH_TERMS[code], max_results=5):
                if not is_duplicate(res["href"]):
                    a = web_fetch_article(res["href"], f"Search:{code}")
                    if a: enrich_article_with_mentions(a); mark_as_stored(res["href"]); all_a.append(a)
        except Exception as e:
            print(f"  Search error {code}: {e}")

    mentioned = [a for a in all_a if any(a.mentions.values())]
    ws2 = wb.create_sheet("Crawled Data")
    for col, h in enumerate(SHEET_HEADERS, 1):
        c = ws2.cell(row=1, column=col, value=h)
        c.fill = hdr_fill; c.font = hdr_font; c.border = thin; c.alignment = Alignment(horizontal="center", vertical="center")
    for ri, a in enumerate(mentioned, 2):
        for ci2, v in enumerate(article_to_row(a), 1):
            c = ws2.cell(row=ri, column=ci2, value=v)
            c.font = body_font; c.border = thin; c.alignment = wrap
    ws2.auto_filter.ref = f"A1:M{len(mentioned) + 1}"
    ws2.freeze_panes = "A2"

    wb.save(output_path)
    print(f"Saved: {output_path}")
    print(f"Company info: {len(COMPANY_INFO)} rows, Crawled data: {len(mentioned)} rows with mentions")


def main():
    run_crawl()


if __name__ == "__main__":
    main()
