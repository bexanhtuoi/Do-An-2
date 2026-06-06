```mermaid
flowchart TD
    CMD[python main.py ...] --> CMDTYPE{Command}
    CMDTYPE -->|crawl-links| CL[Phase 1: Index All Sources]
    CMDTYPE -->|daily| DAILY_PY[Daily Python]
    CMDTYPE -->|crawl-content| ENRICH[Phase 2: Enrich from Index]
    CMDTYPE -->|stats| STATS[Stats]

    CL --> RSS[RSS: 96 feeds / 41 sources]
    RSS --> ACC1[(Accumulator in-memory)]
    ACC1 --> FLUSH1[Flush 500 entries → xlsx]

    CL --> API[API: 22 zones]
    API --> CAFEF[CafeF: timelinelist.chn]
    API --> CAFEBIZ[CafeBiz: timelinelist.chn]
    API --> VNNet[VietnamNet: JSON POST]
    CAFEF --> ACC2[(Accumulator)]
    CAFEBIZ --> ACC2
    VNNet --> ACC2
    ACC2 --> FLUSH2[Flush → xlsx]

    ENRICH --> LOAD[Load SOURCE_INDEX]
    LOAD --> FILTER[Filter: STOCK_PATTERN match title]
    FILTER --> FETCH[Fetch full article content 8 workers]
    FETCH --> BUILD[Rebuild NEWS_RAW 18 cols]

    subgraph GAS ["GAS Daily (cloud)"]
        GDAILY[Trigger 08:00 + 20:00] --> G1[Crawl RSS 96 feeds]
        G1 --> G2[Crawl API page 1]
        G2 --> G3[Keyword filter 58 keywords]
        G3 --> G4[Date filter today/yesterday]
        G4 --> G5[Dedup URL + hash]
        G5 --> G6[Flush → SOURCE_INDEX + NEWS_RAW]
        G6 --> G7[Ghi CRAWL_LOG + DAILY_SUMMARY]
    end
```

## GAS daily() 7 bước
1. **Crawl RSS** (96 feeds, fetchUrl + XmlService.parse)
2. **Crawl API** (22 zones, page 1)
3. **Keyword filter** (findMatchingKeyword — substring match case-insensitive)
4. **Date filter** (isRecentDate — hôm qua/hôm nay)
5. **Dedup** (URL + content_hash)
6. **Flush** → SOURCE_INDEX + NEWS_RAW
7. **Ghi log** → CRAWL_LOG + DAILY_SUMMARY

## Batch Accumulator
- `_idx_links: Set`: in-memory dedup
- `_idx_accumulator: Array`: pending SOURCE_INDEX rows
- `_raw_accumulator: Array`: pending NEWS_RAW rows
- Flush khi hết daily() hoặc ≥500 entries
