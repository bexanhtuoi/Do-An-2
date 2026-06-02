# DA2 — Crawl Tin tức Ô tô Niêm yết

Crawl dữ liệu tin tức hằng ngày về **7 công ty ô tô niêm yết** trên sàn chứng khoán Việt Nam.  
Code Python prototype (convertible sang Google Apps Script), lưu vào Google Sheets.

## Công ty mục tiêu

VMA · TMT · SVC · HAX · HTL · GGG · HHS

## Cấu trúc project

```
da2/
├── main.py              # Crawl Python chính
├── data/                # Output xlsx
├── pyproject.toml       # uv project
├── Projects/DA2/        # Obsidian vault docs
│   ├── overview.md      # Tổng quan
│   ├── feature.md       # Tính năng
│   ├── task.md          # Task list
│   ├── workflow.md      # Luồng hoạt động
│   ├── results.md       # Kết quả dự kiến
│   └── plan-crawl.md    # Kế hoạch craw
└── README.md
```

## Chạy

```bash
uv run python main.py
```
