import json, os
c = json.load(open("data/report/chart.json","r",encoding="utf-8"))
for x in c:
    fn = x["path"].split("/")[-1]
    print(f"{fn:35s} {x['chart_type']:15s} {x['file_size_kb']:>5.1f}KB  {x['name']}")
print(f"\nTotal: {len(c)} charts, {sum(x['file_size_kb'] for x in c):.0f} KB")

s = json.load(open("data/report/statistic.json","r",encoding="utf-8"))
print(f"\nstatistic.json:")
print(f"  links: {s['overview']['total_links_crawled']:,}")
print(f"  enriched: {s['overview']['total_articles_enriched']:,}")
print(f"  sources: {s['sources']['total_unique_source_channels']}")
print(f"  companies: {s['companies_and_tickers']['total_companies']}")
print(f"  tickers: {len(s['companies_and_tickers']['ticker_mentions'])}")
print(f"  date: {s['overview']['date_range']['from']} -> {s['overview']['date_range']['to']}")
print(f"  pipeline: {s['articles_pipeline']['stage_1_links_crawled']:,} -> {s['articles_pipeline']['stage_2_title_matched']:,} -> {s['articles_pipeline']['stage_3_content_fetched_ok']:,}")
print(f"  domains: {s['industry_coverage']['domains_covered']}")
