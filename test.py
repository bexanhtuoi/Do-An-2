import sys
import time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"C:\Users\PC\Downloads\DA2")

import importlib.util
spec = importlib.util.spec_from_file_location("crawler", r"C:\Users\PC\Downloads\DA2\main.py")
crawler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crawler)

crawler.stored_links.clear()

print("=" * 70)
print("RSS CRAWL TEST")
print("=" * 70)

rss_total = 0
rss_mentioned = 0
for src in crawler.RSS_SOURCES:
    articles = crawler.crawl_rss_source(src)
    mentioned = [a for a in articles if any(a.mentions.values())]
    rss_total += len(articles)
    rss_mentioned += len(mentioned)
    for a in mentioned:
        codes = [k for k, v in a.mentions.items() if v]
        print(f"  [{','.join(codes)}] {a.title[:70]}")

print(f"\nRSS: {rss_mentioned} mentioned / {rss_total} total")

print("\n" + "=" * 70)
print("SEARCH CRAWL TEST")
print("=" * 70)

search_total = 0
search_mentioned = 0
for code in crawler.STOCK_CODES:
    print(f"\n--- {code} ---")

    results = crawler.web_search(crawler.COMPANY_KEYWORDS[code], max_results=5)
    for r in results:
        url = r["href"]
        if crawler.is_duplicate(url):
            continue
        article = crawler.web_fetch_article(url, f"Search:{code}")
        if article is None:
            continue
        crawler.enrich_article_with_mentions(article)
        crawler.mark_as_stored(url)
        search_total += 1
        codes = [k for k, v in article.mentions.items() if v]
        if codes:
            search_mentioned += 1
            print(f"  ✓ [{','.join(codes)}] {article.title[:60]}")
        else:
            print(f"  ✗ [none] {article.title[:60]}")
    time.sleep(1)

    stock_results = crawler.web_search(crawler.SEARCH_TERMS[code], max_results=5)
    for r in stock_results:
        url = r["href"]
        if crawler.is_duplicate(url):
            continue
        article = crawler.web_fetch_article(url, f"Search:{code}")
        if article is None:
            continue
        crawler.enrich_article_with_mentions(article)
        crawler.mark_as_stored(url)
        search_total += 1
        codes = [k for k, v in article.mentions.items() if v]
        if codes:
            search_mentioned += 1
            print(f"  ✓ [{','.join(codes)}] {article.title[:60]}")
        else:
            print(f"  ✗ [none] {article.title[:60]}")
    time.sleep(1)

print(f"\nSEARCH: {search_mentioned} mentioned / {search_total} fetched")
print(f"TOTAL:  {rss_mentioned + search_mentioned} mentioned / {rss_total + search_total} total")
