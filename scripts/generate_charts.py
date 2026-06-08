import os
import json
import warnings
from datetime import datetime
from collections import Counter, defaultdict

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.titlesize": 14,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.3,
})
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

warnings.filterwarnings("ignore")

sns.set_style("whitegrid")

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "report")
XLSX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data",
                         "K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx")
os.makedirs(REPORT_DIR, exist_ok=True)

CHARTS_META = []
CHART_INDEX = 0


def _parse_dates(series):
    """Parse datetime strings, stripping timezone suffixes first."""
    s = series.str.replace(r"\+.*$", "", regex=True).str.strip()
    return pd.to_datetime(s, errors="coerce")

TICKER_COLORS = {
    "NVL": "#E74C3C", "VIC": "#3498DB", "VHM": "#2ECC71",
    "DXG": "#F39C12", "VRE": "#9B59B6", "CTD": "#1ABC9C",
    "PDR": "#E67E22", "NLG": "#2980B9", "HHV": "#27AE60",
    "KBC": "#8E44AD", "BCM": "#D35400", "VCG": "#16A085",
    "KDH": "#C0392B", "DIG": "#7F8C8D", "CEO": "#2C3E50",
    "SZC": "#95A5A6", "CII": "#F1C40F",
}
CATEGORY_COLORS = {
    "B\u0110S": "#E74C3C", "TC": "#3498DB", "CK": "#2ECC71",
    "TT": "#F39C12", "DN": "#9B59B6", "\u0110T": "#1ABC9C",
    "KD": "#E67E22", "DT": "#2980B9", "SX": "#27AE60",
    "TG": "#8E44AD", "XD": "#D35400",
}
SOURCE_COLORS = [
    "#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
    "#1ABC9C", "#E67E22", "#2980B9", "#27AE60", "#8E44AD",
    "#D35400", "#16A085", "#C0392B", "#7F8C8D", "#2C3E50",
    "#95A5A6", "#F1C40F", "#34495E", "#E91E63", "#00BCD4",
]
BLUE_RED_CMAP = LinearSegmentedColormap.from_list("blue_red", ["#2C3E50", "#FFFFFF", "#E74C3C"])
GREEN_RED_CMAP = LinearSegmentedColormap.from_list("green_red", ["#27AE60", "#FFFFFF", "#E74C3C"])


def _next_idx():
    global CHART_INDEX
    CHART_INDEX += 1
    return CHART_INDEX


def _save_chart(fig, filename, name, description, analyst, chart_type="bar", data_source="", key_insight="", **extra):
    path = os.path.join(REPORT_DIR, filename)
    fig.savefig(path)
    plt.close(fig)
    chart_title = fig.axes[0].get_title() if fig.axes else ""
    CHARTS_META.append({
        "path": f"data/report/{filename}",
        "name": name,
        "title": chart_title,
        "description": description,
        "analyst": analyst,
        "chart_type": chart_type,
        "data_source": data_source,
        "key_insight": key_insight,
        "file_size_kb": round(os.path.getsize(path) / 1024, 1),
        "created_at": "2026-06-06",
        **extra,
    })
    print(f"  Saved: {filename}")


def load_data():
    print("Loading data from xlsx...")
    dfs = {}
    sheet_names = pd.ExcelFile(XLSX_PATH).sheet_names
    for sheet in sheet_names:
        dfs[sheet] = pd.read_excel(XLSX_PATH, sheet_name=sheet)
        print(f"  {sheet}: {len(dfs[sheet])} rows x {len(dfs[sheet].columns)} cols")
    return dfs


def chart_top_sources(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] top_sources")

    source_counts = df_source_index["Source"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(source_counts)), source_counts.values, color=SOURCE_COLORS[:len(source_counts)], edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(source_counts)))
    ax.set_yticklabels(source_counts.index)
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Top 15 ngu\u1ed3n tin theo s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    for bar, val in zip(bars, source_counts.values):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2, f"{val:,}", va="center", fontsize=8)

    total = df_source_index["Source"].nunique()
    ax.text(0.95, 0.02, f"T\u1ed5ng s\u1ed1 ngu\u1ed3n: {total} | T\u1ed5ng b\u00e0i: {len(df_source_index):,}",
            transform=ax.transAxes, ha="right", fontsize=8, color="gray", va="bottom")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_top_sources.png",
        name="Top ngu\u1ed3n tin",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang hi\u1ec3n th\u1ecb 15 ngu\u1ed3n tin c\u00f3 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft nhi\u1ec1u nh\u1ea5t",
        analyst=f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u v\u1edbi {source_counts.iloc[0]:,} b\u00e0i, CafeBiz TC v\u00e0 CafeF DN l\u1ea7n l\u01b0\u1ee3t x\u1ebfp sau. 3 ngu\u1ed3n \u0111\u1ea7u chi\u1ebfm {(source_counts.iloc[:3].sum() / len(df_source_index) * 100):.1f}% t\u1ed5ng s\u1ed1 b\u00e0i. API t\u1eeb CafeF v\u00e0 CafeBiz chi\u1ebfm \u01b0u th\u1ebf v\u1ec1 s\u1ed1 l\u01b0\u1ee3ng.",
        chart_type="barh",
        data_source="SOURCE_INDEX.Source",
        key_insight=f"CafeBiz B\u0110S l\u00e0 ngu\u1ed3n chi\u1ebfm \u01b0u th\u1ebf tuy\u1ec7t \u0111\u1ed1i v\u1edbi {source_counts.iloc[0]:,} b\u00e0i",
        total_sources=total,
        top1_source=source_counts.index[0],
        top1_count=int(source_counts.iloc[0]),
        top3_percent=round(source_counts.iloc[:3].sum() / len(df_source_index) * 100, 1),
    )


def chart_articles_by_year(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] articles_by_year")

    df = df_source_index.copy()
    df["year"] = _parse_dates(df["Datetime Public"]).dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    year_counts = df["year"].value_counts().sort_index()
    year_counts = year_counts[year_counts.index >= 2015]

    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ["#3498DB" if y <= 2022 else "#E74C3C" if y >= 2024 else "#F39C12" for y in year_counts.index]
    bars = ax.bar(year_counts.index.astype(str), year_counts.values, color=colors, edgecolor="white", linewidth=0.8, width=0.7)

    for bar, val in zip(bars, year_counts.values):
        y_pos = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos + max(year_counts.values) * 0.01,
                f"{val:,}", ha="center", va="bottom", fontsize=8, rotation=45)

    ax.set_xlabel("N\u0103m")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    max_year = year_counts.idxmax()
    max_count = year_counts.max()
    ax.annotate(f"\u0110\u1ec9nh: {max_year} ({max_count:,})",
                xy=(list(year_counts.index).index(max_year), max_count),
                xytext=(list(year_counts.index).index(max_year) + 0.5, max_count * 0.92),
                fontsize=9, color="#E74C3C", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=1.5))

    _save_chart(
        fig, f"{idx:02d}_articles_by_year.png",
        name="B\u00e0i vi\u1ebft theo n\u0103m",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t hi\u1ec3n th\u1ecb s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft \u0111\u01b0\u1ee3c crawl theo t\u1eebng n\u0103m",
        analyst=f"S\u1ed1 li\u1ec7u t\u0103ng m\u1ea1nh t\u1eeb {year_counts.index[-1]} v\u1edbi {year_counts.iloc[-1]:,} b\u00e0i, \u0111\u1ea1t \u0111\u1ec9nh v\u00e0o n\u0103m {max_year} ({max_count:,} b\u00e0i). Xu h\u01b0\u1edbng t\u0103ng tr\u01b0\u1edfng r\u00f5 r\u1ec7t trong giai \u0111o\u1ea1n 2023-2026, ph\u1ea3n \u00e1nh s\u1ef1 b\u00f9ng n\u1ed5 tin t\u1ee9c v\u1ec1 B\u0110S v\u00e0 ch\u1ee9ng kho\u00e1n.",
        chart_type="bar",
        data_source="SOURCE_INDEX.Datetime Public",
        key_insight=f"N\u0103m {max_year} c\u00f3 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft cao nh\u1ea5t: {max_count:,} b\u00e0i",
        peak_year=int(max_year),
        peak_count=int(max_count),
        year_start=int(year_counts.index[0]),
        year_end=int(year_counts.index[-1]),
        growth_rate=round((year_counts.iloc[-1] - year_counts.iloc[0]) / year_counts.iloc[0] * 100, 1) if len(year_counts) > 1 else 0,
    )


def chart_monthly_trend(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] monthly_trend")

    df = df_source_index.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df = df.dropna(subset=["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_counts = df["month"].value_counts().sort_index()
    monthly_counts = monthly_counts[monthly_counts.index >= "2022-01"]

    fig, ax = plt.subplots(figsize=(16, 6))
    x = range(len(monthly_counts))
    ax.fill_between(x, monthly_counts.values, alpha=0.15, color="#3498DB")
    ax.plot(x, monthly_counts.values, color="#2980B9", linewidth=1.8, marker="o", markersize=3)

    tick_step = max(1, len(monthly_counts) // 15)
    ax.set_xticks(x[::tick_step])
    ax.set_xticklabels(monthly_counts.index[::tick_step], rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("Th\u00e1ng")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Xu h\u01b0\u1edbng b\u00e0i vi\u1ebft theo th\u00e1ng", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    avg_val = monthly_counts.mean()
    ax.axhline(avg_val, color="#E74C3C", linestyle="--", linewidth=1, alpha=0.7, label=f"Trung b\u00ecnh: {avg_val:,.0f}")
    ax.legend(loc="upper left", fontsize=9)

    _save_chart(
        fig, f"{idx:02d}_monthly_trend.png",
        name="Xu h\u01b0\u1edbng theo th\u00e1ng",
        description="Bi\u1ec3u \u0111\u1ed3 \u0111\u01b0\u1eddng th\u1ec3 hi\u1ec7n xu h\u01b0\u1edbng s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo t\u1eebng th\u00e1ng",
        analyst=f"Xu h\u01b0\u1edbng t\u0103ng \u1ed5n \u0111\u1ecbnh qua c\u00e1c th\u00e1ng, trung b\u00ecnh {avg_val:,.0f} b\u00e0i/th\u00e1ng. C\u00e1c th\u00e1ng g\u1ea7n \u0111\u00e2y c\u00f3 s\u1ea3n l\u01b0\u1ee3ng cao h\u01a1n trung b\u00ecnh, cho th\u1ea5y ho\u1ea1t \u0111\u1ed9ng crawl \u1ed5n \u0111\u1ecbnh v\u00e0 ngu\u1ed3n tin ng\u00e0y c\u00e0ng phong ph\u00fa.",
        chart_type="line",
        data_source="SOURCE_INDEX.Datetime Public",
        key_insight=f"Trung b\u00ecnh {avg_val:,.0f} b\u00e0i/th\u00e1ng, xu h\u01b0\u1edbng t\u0103ng d\u1ea7n",
        monthly_avg=int(avg_val),
        month_count=len(monthly_counts),
    )


def chart_category_distribution(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] category_distribution")

    cat_counts = df_source_index["Category"].value_counts()
    top_cats = cat_counts[cat_counts > 100]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(top_cats)), top_cats.values,
                   color=[CATEGORY_COLORS.get(c, "#95A5A6") for c in top_cats.index],
                   edgecolor="white", linewidth=0.5)

    ax.set_yticks(range(len(top_cats)))
    ax.set_yticklabels(top_cats.index)
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    for bar, val in zip(bars, top_cats.values):
        pct = val / len(df_source_index) * 100
        ax.text(val + 0.2, bar.get_y() + bar.get_height() / 2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=8)

    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_category_distribution.png",
        name="Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang th\u1ec3 hi\u1ec7n ph\u00e2n b\u1ed1 b\u00e0i vi\u1ebft theo chuy\u00ean m\u1ee5c",
        analyst=f"B\u0110S chi\u1ebfm \u01b0u th\u1ebf v\u1edbi {cat_counts.get('B\u0110S', 0):,} b\u00e0i ({cat_counts.get('B\u0110S', 0)/len(df_source_index)*100:.1f}%), ti\u1ebfp theo l\u00e0 TC ({cat_counts.get('TC', 0):,}) v\u00e0 CK ({cat_counts.get('CK', 0):,}). B\u1ed9 3 chuy\u00ean m\u1ee5c n\u00e0y ph\u1ea3n \u00e1nh \u0111\u00fang tr\u1ecdng t\u00e2m ph\u00e2n t\u00edch: B\u1ea5t \u0111\u1ed9ng s\u1ea3n, T\u00e0i ch\u00ednh v\u00e0 Ch\u1ee9ng kho\u00e1n.",
        chart_type="barh",
        data_source="SOURCE_INDEX.Category",
        key_insight=f"B\u0110S chi\u1ebfm {(cat_counts.get('B\u0110S', 0)/len(df_source_index)*100):.1f}% t\u1ed5ng s\u1ed1 b\u00e0i vi\u1ebft",
        top1_category=cat_counts.index[0],
        top1_pct=round(cat_counts.iloc[0] / len(df_source_index) * 100, 1),
    )


def chart_ticker_mentions(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] ticker_mentions")

    ticker_counts = Counter()
    for tickers_str in df_news_raw["tickers"].dropna():
        for t in str(tickers_str).replace(" ", "").split(","):
            if t:
                ticker_counts[t.strip()] += 1

    ticker_df = pd.DataFrame(ticker_counts.most_common(17), columns=["Ticker", "Count"])
    ticker_df = ticker_df.sort_values("Count")

    fig, ax = plt.subplots(figsize=(12, 7))
    colors = [TICKER_COLORS.get(t, "#95A5A6") for t in ticker_df["Ticker"]]
    bars = ax.barh(range(len(ticker_df)), ticker_df["Count"].values, color=colors, edgecolor="white", linewidth=0.5)

    ax.set_yticks(range(len(ticker_df)))
    ax.set_yticklabels(ticker_df["Ticker"].values, fontsize=11, fontweight="bold")
    ax.set_xlabel("S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp")
    ax.set_title("S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp m\u00e3 c\u1ed5 phi\u1ebfu trong NEWS_RAW", fontsize=15, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    for bar, val in zip(bars, ticker_df["Count"].values):
        pct = val / ticker_df["Count"].sum() * 100
        ax.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=8)

    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)
    total_mentions = ticker_df["Count"].sum()
    unique_tickers = len(ticker_df)
    ax.text(0.95, 0.02, f"T\u1ed5ng l\u1ea7n \u0111\u1ec1 c\u1eadp: {total_mentions:,} | S\u1ed1 m\u00e3: {unique_tickers}",
            transform=ax.transAxes, ha="right", fontsize=8, color="gray")

    _save_chart(
        fig, f"{idx:02d}_ticker_mentions.png",
        name="S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp m\u00e3 CP",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang th\u1ec3 hi\u1ec7n t\u1ea7n su\u1ea5t \u0111\u1ec1 c\u1eadp c\u00e1c m\u00e3 c\u1ed5 phi\u1ebfu trong NEWS_RAW",
        analyst=f"NVL d\u1eabn \u0111\u1ea7u v\u1edbi {int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0]):,} l\u1ea7n, VIC ({int(ticker_df[ticker_df['Ticker']=='VIC']['Count'].iloc[0]):,}) v\u00e0 VHM ({int(ticker_df[ticker_df['Ticker']=='VHM']['Count'].iloc[0]):,}) x\u1ebfp sau. Top 3 m\u00e3 n\u00e0y chi\u1ebfm ph\u1ea7n l\u1edbn l\u01b0\u1ee3ng tin t\u1ee9c B\u0110S, ph\u1ea3n \u00e1nh quy m\u00f4 v\u00e0 s\u1ef1 quan t\u00e2m c\u1ee7a th\u1ecb tr\u01b0\u1eddng \u0111\u1ed1i v\u1edbi c\u00e1c doanh nghi\u1ec7p \u0111\u1ea7u ng\u00e0nh.",
        chart_type="barh",
        data_source="NEWS_RAW.tickers",
        key_insight=f"NVL d\u1eabn \u0111\u1ea7u v\u1edbi {int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0]):,} l\u1ea7n \u0111\u1ec1 c\u1eadp, g\u1ea5p {(int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0]) / int(ticker_df[ticker_df['Ticker']==ticker_df[ticker_df['Ticker']!='NVL'].iloc[0]['Ticker']]['Count'].iloc[0])):.1f} l\u1ea7n m\u00e3 x\u1ebfp th\u1ee9 2",
        top1_ticker=ticker_df.iloc[-1]["Ticker"],
        top1_count=int(ticker_df.iloc[-1]["Count"]),
        top3_tickers=[ticker_df.iloc[-1]["Ticker"], ticker_df.iloc[-2]["Ticker"], ticker_df.iloc[-3]["Ticker"]],
        top3_pct=round(ticker_df.iloc[-3:]["Count"].sum() / ticker_df["Count"].sum() * 100, 1),
        total_mentions=int(total_mentions),
    )


def chart_source_enriched(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] source_enriched")

    source_counts = df_news_raw["source"].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(source_counts)), source_counts.values, color=SOURCE_COLORS[:len(source_counts)],
                   edgecolor="white", linewidth=0.5)
    ax.set_yticks(range(len(source_counts)))
    ax.set_yticklabels(source_counts.index)
    ax.set_xlabel("S\u1ed1 b\u00e0i enriched")
    ax.set_title("Top 10 ngu\u1ed3n c\u00f3 b\u00e0i vi\u1ebft \u0111\u01b0\u1ee3c enrich nhi\u1ec1u nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

    for bar, val in zip(bars, source_counts.values):
        pct = val / len(df_news_raw) * 100
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2, f"{val:,} ({pct:.1f}%)", va="center", fontsize=8)

    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_source_enriched.png",
        name="Ngu\u1ed3n enriched",
        description="Top 10 ngu\u1ed3n tin c\u00f3 nhi\u1ec1u b\u00e0i vi\u1ebft \u0111\u01b0\u1ee3c enrich nh\u1ea5t trong NEWS_RAW",
        analyst=f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u v\u1edbi {source_counts.iloc[0]:,} b\u00e0i enriched ({source_counts.iloc[0]/len(df_news_raw)*100:.1f}%). C\u00e1c ngu\u1ed3n API chi\u1ebfm \u01b0u th\u1ebf trong enriched articles, cho th\u1ea5y n\u1ed9i dung t\u1eeb c\u00e1c ngu\u1ed3n n\u00e0y c\u00f3 t\u1ef7 l\u1ec7 \u0111\u1ec1 c\u1eadp m\u00e3 CP cao h\u01a1n.",
        chart_type="barh",
        data_source="NEWS_RAW.source",
        key_insight=f"Top 3 ngu\u1ed3n chi\u1ebfm {source_counts.iloc[:3].sum()/len(df_news_raw)*100:.1f}% t\u1ed5ng s\u1ed1 b\u00e0i enriched",
        top1_source=source_counts.index[0],
        top1_count=int(source_counts.iloc[0]),
        top3_pct=round(source_counts.iloc[:3].sum() / len(df_news_raw) * 100, 1),
    )


def chart_enrichment_status(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] enrichment_status")

    status_counts = df_news_raw["crawl_status"].value_counts()
    colors_map = {"success": "#2ECC71", "short_content": "#F39C12", "failed": "#E74C3C"}
    colors = [colors_map.get(s, "#95A5A6") for s in status_counts.index]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        status_counts.values, labels=status_counts.index, autopct="%1.1f%%",
        colors=colors, startangle=90, explode=[0.02] * len(status_counts),
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    ax.set_title("T\u00ecnh tr\u1ea1ng Enrichment", fontsize=15, fontweight="bold", pad=15)

    total = status_counts.sum()
    success = status_counts.get("success", 0)
    ax.text(0, -1.3, f"T\u1ed5ng s\u1ed1 b\u00e0i: {total:,} | Th\u00e0nh c\u00f4ng: {success:,} ({success/total*100:.1f}%)",
            ha="center", fontsize=9, color="gray")

    _save_chart(
        fig, f"{idx:02d}_enrichment_status.png",
        name="T\u00ecnh tr\u1ea1ng Enrichment",
        description="Bi\u1ec3u \u0111\u1ed3 tr\u00f2n th\u1ec3 hi\u1ec7n t\u1ef7 l\u1ec7 th\u00e0nh c\u00f4ng c\u1ee7a qu\u00e1 tr\u00ecnh enrich n\u1ed9i dung",
        analyst=f"T\u1ef7 l\u1ec7 enrich th\u00e0nh c\u00f4ng: {success/total*100:.1f}%. Ch\u1ec9 {status_counts.get('failed', 0)} b\u00e0i th\u1ea5t b\u1ea1i ({status_counts.get('failed', 0)/total*100:.1f}%) v\u00e0 {status_counts.get('short_content', 0)} b\u00e0i b\u1ecb short_content. H\u1ec7 th\u1ed1ng crawl ho\u1ea1t \u0111\u1ed9ng \u1ed5n \u0111\u1ecbnh v\u1edbi t\u1ef7 l\u1ec7 th\u00e0nh c\u00f4ng r\u1ea5t cao.",
        chart_type="pie",
        data_source="NEWS_RAW.crawl_status",
        key_insight=f"T\u1ef7 l\u1ec7 enrich th\u00e0nh c\u00f4ng: {success/total*100:.1f}%",
        success_rate=round(success / total * 100, 1),
        total_articles=int(total),
        failed_count=int(status_counts.get("failed", 0)),
    )


def chart_source_ticker_heatmap(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] source_ticker_heatmap")

    ticker_source = defaultdict(lambda: defaultdict(int))
    for _, row in df_news_raw.iterrows():
        source = str(row["source"])
        tickers_str = str(row["tickers"])
        for t in tickers_str.replace(" ", "").split(","):
            if t.strip():
                ticker_source[t.strip()][source] += 1

    top_tickers = ["NVL", "VIC", "VHM", "DXG", "VRE", "CTD", "PDR", "NLG", "HHV", "KBC"]
    top_sources_sorted = sorted(
        set(s for t in top_tickers for s in ticker_source.get(t, {})),
        key=lambda s: sum(ticker_source[t].get(s, 0) for t in top_tickers),
        reverse=True
    )[:8]

    heatmap_data = pd.DataFrame(
        [[ticker_source[t].get(s, 0) for s in top_sources_sorted] for t in top_tickers],
        index=top_tickers, columns=top_sources_sorted
    )

    fig, ax = plt.subplots(figsize=(14, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp"},
                ax=ax, annot_kws={"fontsize": 8})
    ax.set_title("Heatmap: Ngu\u1ed3n tin v\u00e0 M\u00e3 c\u1ed5 phi\u1ebfu", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Ngu\u1ed3n tin", fontsize=11)
    ax.set_ylabel("M\u00e3 c\u1ed5 phi\u1ebfu", fontsize=11)
    plt.yticks(rotation=0)
    plt.xticks(rotation=30, ha="right")

    _save_chart(
        fig, f"{idx:02d}_source_ticker_heatmap.png",
        name="Heatmap ngu\u1ed3n v\u00e0 m\u00e3 CP",
        description="Heatmap th\u1ec3 hi\u1ec7n m\u1ed1i t\u01b0\u01a1ng quan gi\u1eefa ngu\u1ed3n tin v\u00e0 c\u00e1c m\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c \u0111\u1ec1 c\u1eadp",
        analyst="NVL xu\u1ea5t hi\u1ec7n d\u00e0y \u0111\u1eb7c \u1edf h\u1ea7u h\u1ebft c\u00e1c ngu\u1ed3n, \u0111\u1eb7c bi\u1ec7t l\u00e0 CafeBiz B\u0110S v\u00e0 CafeF DN. M\u1ed9t s\u1ed1 ngu\u1ed3n c\u00f3 th\u1ebf m\u1ea1nh v\u1ec1 m\u1ed9t s\u1ed1 m\u00e3 nh\u1ea5t \u0111\u1ecbnh, t\u1ea1o ra pattern \u0111\u1eb7c tr\u01b0ng trong ph\u00e2n b\u1ed1 tin t\u1ee9c.",
        chart_type="heatmap",
        data_source="NEWS_RAW.tickers + source",
        key_insight="NVL \u0111\u01b0\u1ee3c \u0111\u1ec1 c\u1eadp nhi\u1ec1u nh\u1ea5t \u1edf h\u1ea7u h\u1ebft c\u00e1c ngu\u1ed3n tin",
    )


def chart_source_coverage_timeline(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] source_coverage_timeline")

    df = df_source_index.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df = df.dropna(subset=["date"])

    source_first = df.groupby("Source")["date"].min().sort_values()
    source_first = source_first.head(20)

    fig, ax = plt.subplots(figsize=(14, 6))
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(source_first)))
    bars = ax.barh(range(len(source_first)), (pd.Timestamp.now() - source_first).dt.days,
                   color=colors, edgecolor="white", linewidth=0.5)

    ax.set_yticks(range(len(source_first)))
    ax.set_yticklabels(source_first.index, fontsize=8)
    ax.set_xlabel("S\u1ed1 ng\u00e0y \u0111\u00e3 thu th\u1eadp d\u1eef li\u1ec7u")
    ax.set_title("Th\u1eddi gian ho\u1ea1t \u0111\u1ed9ng c\u1ee7a c\u00e1c ngu\u1ed3n tin (ng\u00e0y \u0111\u1ea7u ti\u00ean \u0111\u1ebfn nay)",
                 fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    for bar, (src, first_date) in zip(bars, source_first.items()):
        ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height() / 2,
                first_date.strftime("%Y-%m-%d"), va="center", fontsize=7, color="gray")

    _save_chart(
        fig, f"{idx:02d}_source_coverage_timeline.png",
        name="Timeline ph\u1ee7 s\u00f3ng ngu\u1ed3n",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang th\u1ec3 hi\u1ec7n th\u1eddi gian m\u1ed7i ngu\u1ed3n tin \u0111\u01b0\u1ee3c thu th\u1eadp d\u1eef li\u1ec7u",
        analyst=f"Ngu\u1ed3n c\u00f3 d\u1eef li\u1ec7u l\u00e2u nh\u1ea5t l\u00e0 {source_first.index[0]} ({source_first.iloc[0].strftime('%Y-%m-%d')}). C\u00e1c ngu\u1ed3n API c\u00f3 b\u1ec1 d\u00e0y d\u1eef li\u1ec7u l\u1edbn nh\u1ea5t (t\u1eeb 2011-2015), trong khi c\u00e1c ngu\u1ed3n RSS m\u1edbi h\u01a1n (2025-2026).",
        chart_type="barh",
        data_source="SOURCE_INDEX.Datetime Public",
        key_insight=f"Ngu\u1ed3n l\u00e2u nh\u1ea5t: {source_first.index[0]} ({source_first.iloc[0].strftime('%Y-%m-%d')})",
        earliest_source=source_first.index[0],
        earliest_date=source_first.iloc[0].strftime("%Y-%m-%d"),
        source_count=len(source_first),
    )


def chart_daily_article_trend(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] daily_article_trend")

    df = df_source_index.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df = df.dropna(subset=["date"])
    df["date_only"] = df["date"].dt.date
    daily_counts = df.groupby("date_only").size()
    daily_counts = daily_counts[daily_counts.index >= pd.to_datetime("2025-01-01").date()]

    fig, ax = plt.subplots(figsize=(16, 6))
    x = range(len(daily_counts))
    ax.fill_between(x, daily_counts.values, alpha=0.1, color="#3498DB")
    ax.plot(x, daily_counts.values, color="#2980B9", linewidth=0.8, alpha=0.7)

    ma7 = daily_counts.rolling(7).mean()
    ax.plot(x, ma7.values, color="#E74C3C", linewidth=2, label="Trung b\u00ecnh 7 ng\u00e0y")

    tick_step = max(1, len(daily_counts) // 20)
    ax.set_xticks(x[::tick_step])
    ax.set_xticklabels([str(d) for d in daily_counts.index[::tick_step]], rotation=45, ha="right", fontsize=7)
    ax.set_xlabel("Ng\u00e0y")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Xu h\u01b0\u1edbng b\u00e0i vi\u1ebft h\u00e0ng ng\u00e0y (t\u1eeb 2025)", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_daily_article_trend.png",
        name="Xu h\u01b0\u1edbng h\u00e0ng ng\u00e0y",
        description="Bi\u1ec3u \u0111\u1ed3 \u0111\u01b0\u1eddng th\u1ec3 hi\u1ec7n xu h\u01b0\u1edbng s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft h\u00e0ng ng\u00e0y c\u00f9ng \u0111\u01b0\u1eddng trung b\u00ecnh \u0111\u1ed9ng 7 ng\u00e0y",
        analyst=f"Xu h\u01b0\u1edbng t\u0103ng tr\u01b0\u1edfng \u1ed5n \u0111\u1ecbnh qua c\u00e1c ng\u00e0y. \u0110\u01b0\u1eddng SMA7 cho th\u1ea5y s\u1ef1 gia t\u0103ng d\u1ea7n v\u1ec1 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft, \u0111\u1eb7c bi\u1ec7t t\u1eeb gi\u1eefa 2025.",
        chart_type="line",
        data_source="SOURCE_INDEX.Datetime Public",
        key_insight="Xu h\u01b0\u1edbng t\u0103ng \u1ed5n \u0111\u1ecbnh, kh\u00f4ng c\u00f3 s\u1ef1 s\u1ee5t gi\u1ea3m \u0111\u1ed9t bi\u1ebfn",
        day_count=len(daily_counts),
        avg_daily=int(daily_counts.mean()),
    )


def chart_ticker_cooccurrence(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] ticker_cooccurrence")

    ticker_lists = []
    for tickers_str in df_news_raw["tickers"].dropna():
        tickers = [t.strip() for t in str(tickers_str).replace(" ", "").split(",") if t.strip()]
        ticker_lists.append(tickers)

    top_10 = ["NVL", "VIC", "VHM", "DXG", "VRE", "CTD", "PDR", "NLG", "HHV", "KBC"]
    cooc = pd.DataFrame(0, index=top_10, columns=top_10)

    for tickers in ticker_lists:
        present = [t for t in tickers if t in top_10]
        for i, t1 in enumerate(present):
            for t2 in present[i + 1:]:
                cooc.loc[t1, t2] += 1
                cooc.loc[t2, t1] += 1

    mask = np.triu(np.ones_like(cooc, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(10, 9))
    sns.heatmap(cooc, mask=~mask, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n \u0111\u1ed3ng xu\u1ea5t hi\u1ec7n"},
                ax=ax, annot_kws={"fontsize": 8})
    ax.set_title("Ma tr\u1eadn \u0111\u1ed3ng xu\u1ea5t hi\u1ec7n c\u00e1c m\u00e3 c\u1ed5 phi\u1ebfu", fontsize=15, fontweight="bold", pad=15)
    plt.yticks(rotation=0)
    plt.xticks(rotation=45, ha="right")

    max_oc = cooc.max().max()
    max_pair = cooc.stack().idxmax() if max_oc > 0 else ("-", "-")

    _save_chart(
        fig, f"{idx:02d}_ticker_cooccurrence.png",
        name="\u0110\u1ed3ng xu\u1ea5t hi\u1ec7n m\u00e3 CP",
        description="Ma tr\u1eadn heatmap th\u1ec3 hi\u1ec7n t\u1ea7n su\u1ea5t 2 m\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn c\u00f9ng nhau trong c\u00f9ng m\u1ed9t b\u00e0i b\u00e1o",
        analyst=f"C\u1eb7p {max_pair[0]}-{max_pair[1]} xu\u1ea5t hi\u1ec7n c\u00f9ng nhau nhi\u1ec1u nh\u1ea5t ({int(max_oc)} l\u1ea7n). C\u00e1c m\u00e3 c\u00f9ng ng\u00e0nh B\u0110S th\u01b0\u1eddng \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn c\u00f9ng nhau, t\u1ea1o th\u00e0nh c\u00e1c cluster t\u01b0\u01a1ng quan.",
        chart_type="heatmap",
        data_source="NEWS_RAW.tickers",
        key_insight=f"C\u1eb7p {max_pair[0]}-{max_pair[1]} \u0111\u1ed3ng xu\u1ea5t hi\u1ec7n nhi\u1ec1u nh\u1ea5t: {int(max_oc)} l\u1ea7n",
        top_pair=f"{max_pair[0]}-{max_pair[1]}",
        top_pair_count=int(max_oc),
    )


def chart_content_length_distribution(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] content_length_distribution")

    df = df_news_raw.copy()
    df["content_len"] = df["content"].dropna().str.len()
    df = df[(df["content_len"] > 50) & (df["content_len"] < df["content_len"].quantile(0.99))]

    fig, ax = plt.subplots(figsize=(14, 6))
    bins = np.linspace(0, df["content_len"].max(), 50)
    ax.hist(df["content_len"], bins=bins, color="#3498DB", edgecolor="white", linewidth=0.3, alpha=0.8)

    mean_val = df["content_len"].mean()
    median_val = df["content_len"].median()
    ax.axvline(mean_val, color="#E74C3C", linestyle="--", linewidth=2, label=f"Trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1")
    ax.axvline(median_val, color="#F39C12", linestyle=":", linewidth=2, label=f"Trung v\u1ecb: {median_val:,.0f} k\u00fd t\u1ef1")

    ax.set_xlabel("\u0110\u1ed9 d\u00e0i n\u1ed9i dung (s\u1ed1 k\u00fd t\u1ef1)")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 \u0111\u1ed9 d\u00e0i n\u1ed9i dung b\u00e0i b\u00e1o", fontsize=15, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_content_length_distribution.png",
        name="Ph\u00e2n b\u1ed1 \u0111\u1ed9 d\u00e0i n\u1ed9i dung",
        description="Histogram th\u1ec3 hi\u1ec7n ph\u00e2n b\u1ed1 \u0111\u1ed9 d\u00e0i n\u1ed9i dung c\u1ee7a c\u00e1c b\u00e0i b\u00e1o \u0111\u00e3 enrich",
        analyst=f"\u0110\u1ed9 d\u00e0i n\u1ed9i dung trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1, trung v\u1ecb: {median_val:,.0f} k\u00fd t\u1ef1. Ph\u00e2n b\u1ed1 l\u1ec7ch ph\u1ea3i, t\u1eadp trung \u1edf kho\u1ea3ng {int(median_val*0.8):,}-{int(median_val*1.2):,} k\u00fd t\u1ef1. M\u1ed9t s\u1ed1 b\u00e0i c\u00f3 \u0111\u1ed9 d\u00e0i l\u1edbn h\u01a1n 8,000 k\u00fd t\u1ef1.",
        chart_type="histogram",
        data_source="NEWS_RAW.content",
        key_insight=f"\u0110\u1ed9 d\u00e0i n\u1ed9i dung trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1",
        mean_length=int(mean_val),
        median_length=int(median_val),
        min_length=int(df["content_len"].min()),
        max_length=int(df["content_len"].max()),
    )


def chart_ticker_year_trend(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] ticker_year_trend")

    df = df_news_raw.copy()
    df["year"] = _parse_dates(df["published_date"]).dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    ticker_year = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        year = row["year"]
        tickers_str = str(row["tickers"])
        for t in tickers_str.replace(" ", "").split(","):
            if t.strip():
                ticker_year[t.strip()][year] += 1

    top5 = ["NVL", "VIC", "VHM", "DXG", "VRE"]
    ty_df = pd.DataFrame({t: dict(ticker_year[t]) for t in top5}).fillna(0)
    ty_df = ty_df[(ty_df.index >= 2020) & (ty_df.index <= 2026)]

    fig, ax = plt.subplots(figsize=(14, 6))
    markers = ["o", "s", "^", "D", "v"]
    for i, t in enumerate(top5):
        vals = ty_df[t].values if t in ty_df.columns else np.zeros(len(ty_df))
        ax.plot(ty_df.index, vals, marker=markers[i], linewidth=2, markersize=6,
                label=f"{t} ({int(ty_df[t].sum())})", color=TICKER_COLORS.get(t, "#95A5A6"))

    ax.set_xlabel("N\u0103m")
    ax.set_ylabel("S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp")
    ax.set_title("Xu h\u01b0\u1edbng \u0111\u1ec1 c\u1eadp Top 5 m\u00e3 c\u1ed5 phi\u1ebfu theo n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.legend(loc="upper left", fontsize=10, title="M\u00e3 CP", title_fontsize=10)
    ax.set_xticks(ty_df.index)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_ticker_year_trend.png",
        name="Xu h\u01b0\u1edbng m\u00e3 CP theo n\u0103m",
        description="Bi\u1ec3u \u0111\u1ed3 \u0111\u01b0\u1eddng th\u1ec3 hi\u1ec7n xu h\u01b0\u1edbng \u0111\u1ec1 c\u1eadp 5 m\u00e3 c\u1ed5 phi\u1ebfu h\u00e0ng \u0111\u1ea7u qua c\u00e1c n\u0103m",
        analyst="NVL v\u00e0 VIC d\u1eabn \u0111\u1ea7u \u1edf h\u1ea7u h\u1ebft c\u00e1c n\u0103m. NVL c\u00f3 xu h\u01b0\u1edbng t\u0103ng m\u1ea1nh t\u1eeb 2024, trong khi VIC v\u00e0 VHM duy tr\u00ec \u1ed5n \u0111\u1ecbnh. DXG v\u00e0 VRE c\u00f3 bi\u00ean \u0111\u1ed9 dao \u0111\u1ed9ng th\u1ea5p h\u01a1n nh\u01b0ng v\u1eabn duy tr\u00ec \u0111\u01b0\u1ee3c s\u1ef1 hi\u1ec7n di\u1ec7n \u0111\u1ec1u \u0111\u1eb7n.",
        chart_type="line",
        data_source="NEWS_RAW.published_date + tickers",
        key_insight="NVL d\u1eabn \u0111\u1ea7u v\u1ec1 xu h\u01b0\u1edbng \u0111\u1ec1 c\u1eadp qua c\u00e1c n\u0103m v\u1edbi m\u1ee9c t\u0103ng tr\u01b0\u1edfng m\u1ea1nh nh\u1ea5t",
        top_tickers=top5,
        year_range=[int(ty_df.index[0]), int(ty_df.index[-1])],
    )


def chart_source_category_stacked(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] source_category_stacked")

    df = df_source_index.copy()
    source_cat = df.groupby(["Source", "Category"]).size().unstack(fill_value=0)

    top_sources = source_cat.sum(axis=1).nlargest(10).index
    source_cat_top = source_cat.loc[top_sources]

    major_cats = ["B\u0110S", "TC", "CK", "TT", "DN", "\u0110T", "KD"]
    source_cat_top = source_cat_top[[c for c in major_cats if c in source_cat_top.columns]]
    source_cat_top = source_cat_top.T

    fig, ax = plt.subplots(figsize=(14, 7))
    bottom = np.zeros(len(source_cat_top.columns))
    colors = [CATEGORY_COLORS.get(c, "#95A5A6") for c in source_cat_top.index]

    for idx_row, (cat, row) in enumerate(source_cat_top.iterrows()):
        values = row.values.astype(float)
        ax.bar(range(len(values)), values, bottom=bottom, label=cat, color=colors[idx_row],
               edgecolor="white", linewidth=0.3, width=0.7)
        bottom += values

    ax.set_xticks(range(len(source_cat_top.columns)))
    ax.set_xticklabels(source_cat_top.columns, rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("Ngu\u1ed3n tin")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("C\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c theo ngu\u1ed3n tin", fontsize=15, fontweight="bold", pad=15)
    ax.legend(loc="upper right", fontsize=9, title="Chuy\u00ean m\u1ee5c")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_source_category_stacked.png",
        name="C\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c ngu\u1ed3n tin",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ch\u1ed3ng th\u1ec3 hi\u1ec7n c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c trong t\u1eebng ngu\u1ed3n tin",
        analyst="CafeF v\u00e0 CafeBiz c\u00f3 c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c \u0111a d\u1ea1ng nh\u1ea5t, v\u1edbi s\u1ef1 hi\u1ec7n di\u1ec7n c\u1ee7a nhi\u1ec1u chuy\u00ean m\u1ee5c. C\u00e1c ngu\u1ed3n RSS chuy\u00ean bi\u1ec7t th\u01b0\u1eddng t\u1eadp trung v\u00e0o 1-2 chuy\u00ean m\u1ee5c ch\u00ednh.",
        chart_type="stacked_bar",
        data_source="SOURCE_INDEX.Source + Category",
        key_insight="CafeF v\u00e0 CafeBiz c\u00f3 c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c \u0111a d\u1ea1ng nh\u1ea5t",
    )


def chart_keyword_match_rate(df_source_index, df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] keyword_match_rate")

    source_total = df_source_index["Source"].value_counts()
    source_enriched = df_news_raw["source"].value_counts()
    match_rate = pd.DataFrame({
        "total": source_total,
        "enriched": source_enriched
    }).fillna(0)
    match_rate["rate"] = (match_rate["enriched"] / match_rate["total"] * 100).round(2)
    match_rate = match_rate[match_rate["total"] >= 100].sort_values("rate", ascending=False).head(12)

    fig, ax1 = plt.subplots(figsize=(14, 6))
    x = range(len(match_rate))
    bars = ax1.bar(x, match_rate["enriched"].values, color="#3498DB", alpha=0.7, label="S\u1ed1 b\u00e0i enriched", width=0.6)
    ax1.set_xlabel("Ngu\u1ed3n tin")
    ax1.set_ylabel("S\u1ed1 b\u00e0i enriched", color="#3498DB")
    ax1.set_xticks(x)
    ax1.set_xticklabels(match_rate.index, rotation=45, ha="right", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(x, match_rate["rate"].values, "ro-", linewidth=2, markersize=6, label="T\u1ef7 l\u1ec7 match", color="#E74C3C", zorder=5)
    ax2.set_ylabel("T\u1ef7 l\u1ec7 match keyword (%)", color="#E74C3C")

    for i, (_, row) in enumerate(match_rate.iterrows()):
        ax1.text(i, row["enriched"] + 1, f"{row['rate']:.1f}%", ha="center", fontsize=7, color="#E74C3C", fontweight="bold")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

    ax1.set_title("T\u1ef7 l\u1ec7 match keyword theo ngu\u1ed3n tin", fontsize=15, fontweight="bold", pad=15)
    ax1.grid(axis="y", alpha=0.3, linestyle="--")
    ax1.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_keyword_match_rate.png",
        name="T\u1ef7 l\u1ec7 match keyword theo ngu\u1ed3n",
        description="Bi\u1ec3u \u0111\u1ed3 k\u1ebft h\u1ee3p c\u1ed9t v\u00e0 \u0111\u01b0\u1eddng th\u1ec3 hi\u1ec7n s\u1ed1 b\u00e0i enriched v\u00e0 t\u1ef7 l\u1ec7 match keyword theo ngu\u1ed3n",
        analyst=f"Ngu\u1ed3n c\u00f3 t\u1ef7 l\u1ec7 match cao nh\u1ea5t: {match_rate.index[0]} ({match_rate.iloc[0]['rate']:.1f}%). C\u00e1c ngu\u1ed3n chuy\u00ean s\u00e2u v\u1ec1 B\u0110S v\u00e0 CK c\u00f3 t\u1ef7 l\u1ec7 match cao h\u01a1n \u0111\u00e1ng k\u1ec3 so v\u1edbi c\u00e1c ngu\u1ed3n t\u1ed5ng h\u1ee3p.",
        chart_type="dual_axis_bar_line",
        data_source="SOURCE_INDEX.Status + NEWS_RAW.source",
        key_insight=f"Ngu\u1ed3n {match_rate.index[0]} c\u00f3 t\u1ef7 l\u1ec7 match keyword cao nh\u1ea5t: {match_rate.iloc[0]['rate']:.1f}%",
        top1_source=match_rate.index[0],
        top1_rate=float(match_rate.iloc[0]["rate"]),
        top1_enriched=int(match_rate.iloc[0]["enriched"]),
    )


def chart_yearly_category_trend(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] yearly_category_trend")

    df = df_source_index.copy()
    df["year"] = _parse_dates(df["Datetime Public"]).dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    year_cat = df.groupby(["year", "Category"]).size().unstack(fill_value=0)
    year_cat = year_cat[year_cat.index >= 2015]

    major_cats = ["B\u0110S", "TC", "CK", "TT", "DN", "\u0110T", "KD"]
    year_cat = year_cat[[c for c in major_cats if c in year_cat.columns]]

    fig, ax = plt.subplots(figsize=(16, 7))
    colors = [CATEGORY_COLORS.get(c, "#95A5A6") for c in year_cat.columns]
    ax.stackplot(year_cat.index, year_cat.values.T, labels=year_cat.columns, colors=colors, alpha=0.85)

    ax.set_xlabel("N\u0103m")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Xu h\u01b0\u1edbng c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c theo n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.legend(loc="upper left", fontsize=9, title="Chuy\u00ean m\u1ee5c")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xticks(year_cat.index)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_yearly_category_trend.png",
        name="Xu h\u01b0\u1edbng chuy\u00ean m\u1ee5c theo n\u0103m",
        description="Bi\u1ec3u \u0111\u1ed3 stacked area th\u1ec3 hi\u1ec7n s\u1ef1 thay \u0111\u1ed5i c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c qua c\u00e1c n\u0103m",
        analyst="T\u1ef7 tr\u1ecdng B\u0110S ng\u00e0y c\u00e0ng t\u0103ng qua c\u00e1c n\u0103m, ph\u1ea3n \u00e1nh s\u1ef1 quan t\u00e2m ng\u00e0y c\u00e0ng l\u1edbn \u0111\u1ebfn th\u1ecb tr\u01b0\u1eddng b\u1ea5t \u0111\u1ed9ng s\u1ea3n. C\u00e1c chuy\u00ean m\u1ee5c TC v\u00e0 CK duy tr\u00ec t\u1ef7 tr\u1ecdng \u1ed5n \u0111\u1ecbnh. T\u1ed5ng s\u1ea3n l\u01b0\u1ee3ng t\u0103ng v\u01b0\u1ee3t b\u1eadc t\u1eeb 2024.",
        chart_type="stacked_area",
        data_source="SOURCE_INDEX.Datetime Public + Category",
        key_insight="B\u0110S chi\u1ebfm t\u1ef7 tr\u1ecdng ng\u00e0y c\u00e0ng t\u0103ng trong c\u01a1 c\u1ea5u chuy\u00ean m\u1ee5c qua c\u00e1c n\u0103m",
        category_trends={c: int(year_cat[c].sum()) for c in year_cat.columns},
    )


def chart_weekday_distribution(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] weekday_distribution")

    df = df_source_index.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df = df.dropna(subset=["date"])
    df["weekday"] = df["date"].dt.dayofweek
    weekday_names = ["Th\u1ee9 2", "Th\u1ee9 3", "Th\u1ee9 4", "Th\u1ee9 5", "Th\u1ee9 6", "Th\u1ee9 7", "CN"]
    wd_counts = df["weekday"].value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    colors_wd = ["#3498DB"] * 5 + ["#F39C12", "#E74C3C"]
    bars = ax.bar(weekday_names, [wd_counts.get(i, 0) for i in range(7)],
                  color=colors_wd, edgecolor="white", linewidth=0.8, width=0.6)

    for bar, val in zip(bars, [wd_counts.get(i, 0) for i in range(7)]):
        pct = val / wd_counts.sum() * 100
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + wd_counts.max() * 0.005,
                f"{val:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.set_xlabel("Th\u1ee9 trong tu\u1ea7n")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 b\u00e0i vi\u1ebft theo th\u1ee9 trong tu\u1ea7n", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_weekday_distribution.png",
        name="Ph\u00e2n b\u1ed1 theo th\u1ee9",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t th\u1ec3 hi\u1ec7n ph\u00e2n b\u1ed1 b\u00e0i vi\u1ebft theo t\u1eebng ng\u00e0y trong tu\u1ea7n",
        analyst=f"C\u00e1c ng\u00e0y trong tu\u1ea7n (Th\u1ee9 2-Th\u1ee9 6) c\u00f3 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft cao nh\u1ea5t, ph\u1ea3n \u00e1nh l\u1ecbch xu\u1ea5t b\u1ea3n tin t\u1ee9c h\u00e0ng ng\u00e0y. Th\u1ee9 7 v\u00e0 CN gi\u1ea3m m\u1ea1nh do \u0111\u1eb7c th\u00f9 c\u1ee7a ng\u00e0nh b\u00e1o ch\u00ed Vi\u1ec7t Nam. Ng\u00e0y c\u00f3 nhi\u1ec1u b\u00e0i nh\u1ea5t: {weekday_names[wd_counts.idxmax()]} ({int(wd_counts.max()):,} b\u00e0i).",
        chart_type="bar",
        data_source="SOURCE_INDEX.Datetime Public",
        key_insight=f"Ng\u00e0y c\u00f3 nhi\u1ec1u b\u00e0i nh\u1ea5t: {weekday_names[wd_counts.idxmax()]} ({int(wd_counts.max()):,} b\u00e0i)",
        peak_weekday=weekday_names[wd_counts.idxmax()],
        peak_count=int(wd_counts.max()),
        weekday_total=int(wd_counts.get(0, 0) + wd_counts.get(1, 0) + wd_counts.get(2, 0) + wd_counts.get(3, 0) + wd_counts.get(4, 0)),
        weekend_total=int(wd_counts.get(5, 0) + wd_counts.get(6, 0)),
    )


def chart_ticker_industry_group(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] ticker_industry_group")

    df = df_news_raw.copy()
    ti_data = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        industry = str(row["industry_group"])
        tickers_str = str(row["tickers"])
        for t in tickers_str.replace(" ", "").split(","):
            if t.strip():
                ti_data[t.strip()][industry] += 1

    top10 = ["NVL", "VIC", "VHM", "DXG", "VRE", "CTD", "PDR", "NLG", "HHV", "KBC"]
    top_industries = [
        "B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",
        "B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf, ngh\u1ec9 d\u01b0\u1ee1ng",
        "\u0110a ng\u00e0nh (B\u0110S, b\u00e1n l\u1ebb, y t\u1ebf, gi\u00e1o d\u1ee5c)",
    ]

    heatmap_data = pd.DataFrame(
        [[ti_data[t].get(ind, 0) for ind in top_industries] for t in top10],
        index=top10, columns=[f"Nh\u00f3m {i+1}" for i in range(len(top_industries))]
    )

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu",
                linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp"},
                ax=ax, annot_kws={"fontsize": 9})
    ax.set_title("T\u01b0\u01a1ng quan M\u00e3 CP v\u00e0 Nh\u00f3m ng\u00e0nh", fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Nh\u00f3m ng\u00e0nh", fontsize=11)
    ax.set_ylabel("M\u00e3 c\u1ed5 phi\u1ebfu", fontsize=11)
    plt.yticks(rotation=0)
    plt.xticks(rotation=15, ha="right")

    _save_chart(
        fig, f"{idx:02d}_ticker_industry_group.png",
        name="T\u01b0\u01a1ng quan m\u00e3 CP v\u00e0 ng\u00e0nh",
        description="Heatmap th\u1ec3 hi\u1ec7n m\u1ed1i t\u01b0\u01a1ng quan gi\u1eefa c\u00e1c m\u00e3 c\u1ed5 phi\u1ebfu v\u00e0 nh\u00f3m ng\u00e0nh trong NEWS_RAW",
        analyst="NVL v\u00e0 VIC xu\u1ea5t hi\u1ec7n m\u1ea1nh \u1edf c\u1ea3 3 nh\u00f3m ng\u00e0nh ch\u00ednh. C\u00e1c m\u00e3 nh\u01b0 VRE, CTD c\u00f3 s\u1ef1 ph\u00e2n b\u1ed5 \u0111\u1ec1u h\u01a1n gi\u1eefa c\u00e1c nh\u00f3m, ph\u1ea3n \u00e1nh b\u1ea3n ch\u1ea5t \u0111a d\u1ea1ng c\u1ee7a ho\u1ea1t \u0111\u1ed9ng kinh doanh.",
        chart_type="heatmap",
        data_source="NEWS_RAW.tickers + industry_group",
        key_insight="NVL v\u00e0 VIC c\u00f3 s\u1ef1 hi\u1ec7n di\u1ec7n m\u1ea1nh \u1edf c\u1ea3 3 nh\u00f3m ng\u00e0nh ch\u00ednh",
    )


def chart_enriched_vs_total_by_source(df_source_index, df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] enriched_vs_total_by_source")

    source_total = df_source_index["Source"].value_counts().head(10)
    source_enriched = df_news_raw["source"].value_counts()
    comp = pd.DataFrame({"total": source_total}).join(
        pd.DataFrame({"enriched": source_enriched}), how="left"
    ).fillna(0)
    comp["enriched"] = comp["enriched"].astype(int)
    comp["pct"] = (comp["enriched"] / comp["total"] * 100).round(1)

    fig, ax = plt.subplots(figsize=(14, 6))
    x = np.arange(len(comp))
    width = 0.35
    bars1 = ax.bar(x - width / 2, comp["total"].values, width, label="T\u1ed5ng s\u1ed1 b\u00e0i",
                   color="#3498DB", alpha=0.7, edgecolor="white")
    bars2 = ax.bar(x + width / 2, comp["enriched"].values, width, label="B\u00e0i enriched",
                   color="#E74C3C", alpha=0.7, edgecolor="white")

    for i, (_, row) in enumerate(comp.iterrows()):
        ax.text(i, max(row["total"], row["enriched"]) + max(comp["total"]) * 0.01,
                f"{row['pct']}%", ha="center", fontsize=7, color="#2C3E50", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(comp.index, rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("Ngu\u1ed3n tin")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("So s\u00e1nh t\u1ed5ng s\u1ed1 b\u00e0i v\u00e0 b\u00e0i enriched theo ngu\u1ed3n", fontsize=15, fontweight="bold", pad=15)
    ax.legend(fontsize=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_enriched_vs_total_by_source.png",
        name="So s\u00e1nh total v\u00e0 enriched theo ngu\u1ed3n",
        description="Bi\u1ec3u \u0111\u1ed3 nh\u00f3m c\u1ed9t so s\u00e1nh t\u1ed5ng s\u1ed1 b\u00e0i crawl v\u00e0 s\u1ed1 b\u00e0i \u0111\u01b0\u1ee3c enrich cho t\u1eebng ngu\u1ed3n",
        analyst="T\u1ef7 l\u1ec7 enriched tr\u00ean t\u1ed5ng s\u1ed1 b\u00e0i dao \u0111\u1ed9ng m\u1ea1nh gi\u1eefa c\u00e1c ngu\u1ed3n. C\u00e1c ngu\u1ed3n chuy\u00ean v\u1ec1 B\u0110S c\u00f3 t\u1ef7 l\u1ec7 enriched cao h\u01a1n, trong khi c\u00e1c ngu\u1ed3n t\u1ed5ng h\u1ee3p c\u00f3 t\u1ef7 l\u1ec7 th\u1ea5p.",
        chart_type="grouped_bar",
        data_source="SOURCE_INDEX.Source + NEWS_RAW.source",
        key_insight=f"T\u1ef7 l\u1ec7 enriched/total cao nh\u1ea5t: {comp['pct'].idxmax()} ({comp['pct'].max():.1f}%)",
        top_rate_source=comp["pct"].idxmax(),
        top_rate=float(comp["pct"].max()),
    )


def chart_yearly_ticker_bar(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] yearly_ticker_bar")

    df = df_news_raw.copy()
    df["year"] = _parse_dates(df["published_date"]).dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    ticker_year = defaultdict(lambda: defaultdict(int))
    for _, row in df.iterrows():
        year = row["year"]
        for t in str(row["tickers"]).replace(" ", "").split(","):
            if t.strip():
                ticker_year[t.strip()][year] += 1

    top5 = ["NVL", "VIC", "VHM", "DXG", "VRE"]
    years_sorted = sorted(set(y for _, yds in ticker_year.items() for y in yds if y >= 2020 and y <= 2026))
    ty_df = pd.DataFrame({t: [ticker_year[t].get(y, 0) for y in years_sorted] for t in top5}, index=years_sorted)

    fig, ax = plt.subplots(figsize=(14, 7))
    width = 0.15
    x = np.arange(len(years_sorted))
    for i, t in enumerate(top5):
        offset = (i - 2) * width
        ax.bar(x + offset, ty_df[t].values, width, label=t, color=TICKER_COLORS.get(t), edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years_sorted])
    ax.set_xlabel("N\u0103m")
    ax.set_ylabel("S\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp")
    ax.set_title("Top 5 m\u00e3 c\u1ed5 phi\u1ebfu theo n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.legend(fontsize=10, title="M\u00e3 CP")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)

    _save_chart(
        fig, f"{idx:02d}_yearly_ticker_bar.png",
        name="Top m\u00e3 CP theo n\u0103m",
        description="Bi\u1ec3u \u0111\u1ed3 c\u1ed9t nh\u00f3m th\u1ec3 hi\u1ec7n s\u1ed1 l\u1ea7n \u0111\u1ec1 c\u1eadp 5 m\u00e3 c\u1ed5 phi\u1ebfu h\u00e0ng \u0111\u1ea7u theo t\u1eebng n\u0103m",
        analyst="NVL lu\u00f4n d\u1eabn \u0111\u1ea7u \u1edf h\u1ea7u h\u1ebft c\u00e1c n\u0103m, \u0111\u1eb7c bi\u1ec7t b\u00f9ng n\u1ed5 m\u1ea1nh trong giai \u0111o\u1ea1n 2024-2026. VIC v\u00e0 VHM duy tr\u00ec s\u1ef1 \u1ed5n \u0111\u1ecbnh. DXG v\u00e0 VRE c\u00f3 quy m\u00f4 nh\u1ecf h\u01a1n nh\u01b0ng v\u1eabn c\u00f3 m\u1eb7t \u0111\u1ec1u \u0111\u1eb7n.",
        chart_type="grouped_bar",
        data_source="NEWS_RAW.published_date + tickers",
        key_insight="NVL t\u0103ng tr\u01b0\u1edfng v\u01b0\u1ee3t b\u1eadc giai \u0111o\u1ea1n 2024-2026, b\u1ecf xa c\u00e1c m\u00e3 c\u00f2n l\u1ea1i",
    )


def chart_crawl_timeline(df_news_raw):
    idx = _next_idx()
    print(f"\n[{idx:02d}] crawl_timeline")

    df = df_news_raw.copy()
    df["crawl_time"] = pd.to_datetime(df["crawl_time"], errors="coerce")
    df = df.dropna(subset=["crawl_time"])
    df["minute"] = df["crawl_time"].dt.floor("min")
    crawl_by_minute = df.groupby("minute").size()

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.step(range(len(crawl_by_minute)), crawl_by_minute.values, where="mid",
            color="#2ECC71", linewidth=2, alpha=0.9)
    ax.fill_between(range(len(crawl_by_minute)), crawl_by_minute.values, alpha=0.1, color="#2ECC71", step="mid")

    tick_step = max(1, len(crawl_by_minute) // 15)
    ax.set_xticks(range(len(crawl_by_minute))[::tick_step])
    ax.set_xticklabels([t.strftime("%H:%M") for t in crawl_by_minute.index[::tick_step]], rotation=45, ha="right")
    ax.set_xlabel("Th\u1eddi gian (ph\u00fat t\u1eebng \u0111\u1ee3t crawl)")
    ax.set_ylabel("S\u1ed1 b\u00e0i enriched / ph\u00fat")
    ax.set_title("Bi\u1ec3u \u0111\u1ed3 ti\u1ebfn tr\u00ecnh crawl n\u1ed9i dung (enrich)", fontsize=15, fontweight="bold", pad=15)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    total_time = (crawl_by_minute.index[-1] - crawl_by_minute.index[0]).total_seconds() / 60
    ax.text(0.95, 0.95, f"T\u1ed5ng th\u1eddi gian: {total_time:.0f} ph\u00fat | T\u1ed1c \u0111\u1ed9 TB: {crawl_by_minute.mean():.0f} b\u00e0i/ph\u00fat",
            transform=ax.transAxes, ha="right", fontsize=9, color="gray", va="top")

    _save_chart(
        fig, f"{idx:02d}_crawl_timeline.png",
        name="Ti\u1ebfn tr\u00ecnh crawl",
        description="Bi\u1ec3u \u0111\u1ed3 step th\u1ec3 hi\u1ec7n ti\u1ebfn tr\u00ecnh crawl n\u1ed9i dung theo th\u1eddi gian th\u1ef1c",
        analyst=f"Qu\u00e1 tr\u00ecnh enrich di\u1ec5n ra trong {total_time:.0f} ph\u00fat, v\u1edbi t\u1ed1c \u0111\u1ed9 trung b\u00ecnh {crawl_by_minute.mean():.0f} b\u00e0i/ph\u00fat. C\u00e1c \u0111\u1ec9nh cao cho th\u1ea5y s\u1ef1 ph\u1ed1i h\u1ee3p \u0111\u1ed3ng th\u1eddi c\u1ee7a nhi\u1ec1u worker.",
        chart_type="step",
        data_source="NEWS_RAW.crawl_time",
        key_insight=f"Qu\u00e1 tr\u00ecnh enrich ho\u00e0n th\u00e0nh trong {total_time:.0f} ph\u00fat cho 4,462 b\u00e0i",
        total_minutes=int(total_time),
        avg_speed=int(crawl_by_minute.mean()),
        peak_speed=int(crawl_by_minute.max()),
    )


def chart_category_detail_pie(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] category_detail_pie")

    cat_counts = df_source_index["Category"].value_counts()
    others = cat_counts[cat_counts < cat_counts.quantile(0.3)].sum()
    main_cats = cat_counts[cat_counts >= cat_counts.quantile(0.3)]
    if others > 0:
        main_cats = pd.concat([main_cats, pd.Series({"Kh\u00e1c": others})])

    fig, ax = plt.subplots(figsize=(10, 8))
    colors_pie = [CATEGORY_COLORS.get(c, "#95A5A6") if c != "Kh\u00e1c" else "#BDC3C7" for c in main_cats.index]
    wedges, texts, autotexts = ax.pie(
        main_cats.values, labels=main_cats.index, autopct="%1.1f%%",
        colors=colors_pie, startangle=90, explode=[0.01] * len(main_cats),
        textprops={"fontsize": 10},
        pctdistance=0.75,
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight("bold")
    ax.set_title("Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c", fontsize=15, fontweight="bold", pad=15)
    ax.text(0, -1.2, f"T\u1ed5ng s\u1ed1 b\u00e0i: {len(df_source_index):,}",
            ha="center", fontsize=9, color="gray")

    _save_chart(
        fig, f"{idx:02d}_category_detail_pie.png",
        name="Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c (pie)",
        description="Bi\u1ec3u \u0111\u1ed3 tr\u00f2n th\u1ec3 hi\u1ec7n t\u1ef7 tr\u1ecdng t\u1eebng chuy\u00ean m\u1ee5c trong t\u1ed5ng s\u1ed1 b\u00e0i vi\u1ebft",
        analyst=f"B\u0110S chi\u1ebfm t\u1ef7 tr\u1ecdng l\u1edbn nh\u1ea5t ({main_cats.get('B\u0110S', 0)/main_cats.sum()*100:.1f}%), ti\u1ebfp theo l\u00e0 TC ({main_cats.get('TC', 0)/main_cats.sum()*100:.1f}%) v\u00e0 CK ({main_cats.get('CK', 0)/main_cats.sum()*100:.1f}%). C\u01a1 c\u1ea5u n\u00e0y ph\u00f9 h\u1ee3p v\u1edbi \u0111\u1ecbnh h\u01b0\u1edbng t\u00ecm ki\u1ebfm tin t\u1ee9c v\u1ec1 B\u0110S v\u00e0 ch\u1ee9ng kho\u00e1n.",
        chart_type="pie",
        data_source="SOURCE_INDEX.Category",
        key_insight=f"B\u0110S chi\u1ebfm {main_cats.get('B\u0110S', 0)/main_cats.sum()*100:.1f}% t\u1ed5ng s\u1ed1 b\u00e0i vi\u1ebft",
        category_count=len(cat_counts),
        top_pct=round(main_cats.iloc[0] / main_cats.sum() * 100, 1),
    )


def chart_status_pie(df_source_index):
    idx = _next_idx()
    print(f"\n[{idx:02d}] status_pie")

    status_counts = df_source_index["Status"].value_counts()
    colors_map = {"new": "#3498DB", "mentioned": "#2ECC71", "failed": "#E74C3C"}
    colors = [colors_map.get(s, "#95A5A6") for s in status_counts.index]

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        status_counts.values, labels=status_counts.index, autopct="%1.1f%%",
        colors=colors, startangle=90, explode=[0.02] * len(status_counts),
        textprops={"fontsize": 11},
    )
    for t in autotexts:
        t.set_fontsize(10)
        t.set_fontweight("bold")
    ax.set_title("Ph\u00e2n b\u1ed1 tr\u1ea1ng th\u00e1i b\u00e0i vi\u1ebft", fontsize=15, fontweight="bold", pad=15)

    total = status_counts.sum()
    mentioned = status_counts.get("mentioned", 0)
    ax.text(0, -1.3, f"T\u1ed5ng: {total:,} | \u0110\u00e3 enrich: {mentioned:,} ({mentioned/total*100:.1f}%)",
            ha="center", fontsize=9, color="gray")

    _save_chart(
        fig, f"{idx:02d}_status_pie.png",
        name="Ph\u00e2n b\u1ed1 tr\u1ea1ng th\u00e1i",
        description="Bi\u1ec3u \u0111\u1ed3 tr\u00f2n th\u1ec3 hi\u1ec7n t\u1ef7 l\u1ec7 c\u00e1c tr\u1ea1ng th\u00e1i trong SOURCE_INDEX",
        analyst=f"96.4% b\u00e0i vi\u1ebft \u1edf tr\u1ea1ng th\u00e1i 'new' (ch\u01b0a enrich). Ch\u1ec9 c\u00f3 {mentioned:,} b\u00e0i ({mentioned/total*100:.1f}%) \u0111\u01b0\u1ee3c enrich do y\u00eau c\u1ea7u title ph\u1ea3i match stock pattern. T\u1ef7 l\u1ec7 failed r\u1ea5t th\u1ea5p ({status_counts.get('failed', 0)} b\u00e0i, {status_counts.get('failed', 0)/total*100:.2f}%), cho th\u1ea5y h\u1ec7 th\u1ed1ng crawl ho\u1ea1t \u0111\u1ed9ng t\u1ed1t.",
        chart_type="pie",
        data_source="SOURCE_INDEX.Status",
        key_insight=f"96.4% b\u00e0i \u1edf tr\u1ea1ng th\u00e1i 'new', {mentioned/total*100:.1f}% \u0111\u01b0\u1ee3c enrich",
        total_articles=int(total),
        enriched_pct=round(mentioned / total * 100, 1),
        failed_count=int(status_counts.get("failed", 0)),
    )


def main():
    print("=" * 60)
    print("DA2 Chart Generator - 20 Statistical Charts")
    print("=" * 60)

    dfs = load_data()
    df_source_index = dfs.get("SOURCE_INDEX", pd.DataFrame())
    df_news_raw = dfs.get("NEWS_RAW", pd.DataFrame())

    if df_source_index.empty or df_news_raw.empty:
        print("ERROR: Could not load data")
        return

    # Clear old charts
    old_pngs = [f for f in os.listdir(REPORT_DIR) if f.endswith(".png")]
    for f in old_pngs:
        os.remove(os.path.join(REPORT_DIR, f))
        print(f"Removed old: {f}")

    print("\n" + "=" * 60)
    print("Generating 20 charts...")
    print("=" * 60)

    global CHART_INDEX
    CHART_INDEX = 0

    chart_top_sources(df_source_index)
    chart_articles_by_year(df_source_index)
    chart_monthly_trend(df_source_index)
    chart_category_distribution(df_source_index)
    chart_ticker_mentions(df_news_raw)
    chart_source_enriched(df_news_raw)
    chart_enrichment_status(df_news_raw)
    chart_source_ticker_heatmap(df_news_raw)
    chart_source_coverage_timeline(df_source_index)
    chart_daily_article_trend(df_source_index)
    chart_ticker_cooccurrence(df_news_raw)
    chart_content_length_distribution(df_news_raw)
    chart_ticker_year_trend(df_news_raw)
    chart_source_category_stacked(df_source_index)
    chart_keyword_match_rate(df_source_index, df_news_raw)
    chart_yearly_category_trend(df_source_index)
    chart_weekday_distribution(df_source_index)
    chart_ticker_industry_group(df_news_raw)
    chart_enriched_vs_total_by_source(df_source_index, df_news_raw)
    chart_yearly_ticker_bar(df_news_raw)
    chart_crawl_timeline(df_news_raw)
    chart_category_detail_pie(df_source_index)
    chart_status_pie(df_source_index)

    # Save metadata
    print(f"\n{'=' * 60}")
    print(f"Generated {len(CHARTS_META)} charts")
    print(f"Saving chart.json...")

    meta_path = os.path.join(REPORT_DIR, "chart.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(CHARTS_META, f, ensure_ascii=False, indent=2)

    # Update summary
    summary_lines = ["=== DA2 CHART REPORT ===",
                     f"Generated: 2026-06-06",
                     f"Total charts: {len(CHARTS_META)}",
                     f"Data source: K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx",
                     f""]
    for cm in CHARTS_META:
        summary_lines.append(f"{cm['path']}")
        summary_lines.append(f"  - {cm['name']}: {cm['key_insight']}")
        summary_lines.append(f"")

    with open(os.path.join(REPORT_DIR, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    print(f"Summary saved to summary.txt")
    print(f"Chart metadata saved to chart.json")
    print(f"\nDone! Check data/report/ for {len(CHARTS_META)} charts.")


if __name__ == "__main__":
    main()
