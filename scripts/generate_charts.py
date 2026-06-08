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

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "report")
XLSX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data",
                         "K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx")
os.makedirs(REPORT_DIR, exist_ok=True)

CHARTS_META = []
CHART_INDEX = 0

SOURCE_COLORS = [
    "#3498DB", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6",
    "#1ABC9C", "#E67E22", "#2980B9", "#27AE60", "#8E44AD",
    "#D35400", "#16A085", "#C0392B", "#7F8C8D", "#2C3E50",
]
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


def _parse_dates(series):
    """Parse datetime strings, strip timezone suffixes first."""
    s = series.str.replace(r"\+.*$", "", regex=True).str.strip()
    return pd.to_datetime(s, errors="coerce")


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
    print(f"  [{CHART_INDEX:02d}] Saved: {filename}")


def load_data():
    print("Loading data from xlsx...")
    dfs = {}
    for sheet in pd.ExcelFile(XLSX_PATH).sheet_names:
        dfs[sheet] = pd.read_excel(XLSX_PATH, sheet_name=sheet)
        print(f"  {sheet}: {len(dfs[sheet])} rows x {len(dfs[sheet].columns)} cols")
    return dfs


def chart_01_top_sources(df_source_index):
    """Top 15 nguồn tin có nhiều bài viết nhất"""
    idx = _next_idx()
    source_counts = df_source_index["Source"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(12, 6.5))
    bars = ax.barh(range(len(source_counts)), source_counts.values,
                   color=SOURCE_COLORS[:len(source_counts)], edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(source_counts)))
    ax.set_yticklabels(source_counts.index, fontsize=9)
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Top 15 ngu\u1ed3n tin c\u00f3 nhi\u1ec1u b\u00e0i vi\u1ebft nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, source_counts.values):
        ax.text(val + max(source_counts.values) * 0.005, bar.get_y() + bar.get_height() / 2,
                f"{val:,}", va="center", fontsize=8, color="#2C3E50")
    ax.set_xlim(0, source_counts.values[0] * 1.15)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.set_axisbelow(True)
    _save_chart(fig, f"{idx:02d}_top_nguon_tin.png", "Top ngu\u1ed3n tin",
        "Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang: 15 ngu\u1ed3n tin c\u00f3 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft nhi\u1ec1u nh\u1ea5t trong h\u1ec7 th\u1ed1ng",
        f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u v\u1edbi {source_counts.iloc[0]:,} b\u00e0i chi\u1ebfm {source_counts.iloc[0]/len(df_source_index)*100:.1f}%. Ba ngu\u1ed3n \u0111\u1ea7u (CafeBiz B\u0110S, CafeBiz TC, CafeF DN) chi\u1ebfm {(source_counts.iloc[:3].sum()/len(df_source_index)*100):.1f}% t\u1ed5ng s\u1ed1 b\u00e0i, cho th\u1ea5y s\u1ef1 t\u1eadp trung cao \u1edf c\u00e1c ngu\u1ed3n API l\u1edbn.",
        "barh", "SOURCE_INDEX.Source",
        f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u: {source_counts.iloc[0]:,} b\u00e0i",
        total_sources=df_source_index["Source"].nunique(),
        top1=source_counts.index[0], top1_count=int(source_counts.iloc[0]),
        top3_pct=round(source_counts.iloc[:3].sum()/len(df_source_index)*100, 1))


def chart_02_articles_by_year(df_source_index):
    """Số lượng bài viết theo từng năm"""
    idx = _next_idx()
    df = df_source_index.copy()
    df["year"] = _parse_dates(df["Datetime Public"]).dt.year.dropna().astype(int)
    year_counts = df["year"].value_counts().sort_index()
    year_counts = year_counts[year_counts.index >= 2015]
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ["#2ECC71" if y <= 2022 else "#F39C12" if y == 2023 else "#E74C3C" if y >= 2025 else "#3498DB" for y in year_counts.index]
    bars = ax.bar(year_counts.index.astype(str), year_counts.values, color=colors, edgecolor="white", linewidth=0.8, width=0.7)
    for bar, val in zip(bars, year_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(year_counts.values)*0.01,
                f"{val:,}", ha="center", va="bottom", fontsize=8, rotation=45)
    ax.set_xlabel("N\u0103m"); ax.set_ylabel("S\u1ed1 b\u00e0i vi\u1ebft")
    ax.set_title("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo t\u1eebng n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    peak = year_counts.idxmax()
    ax.annotate(f"\u0110\u1ec9nh: {peak} ({year_counts.max():,})",
                xy=(list(year_counts.index).index(peak), year_counts.max()),
                xytext=(list(year_counts.index).index(peak)-0.3, year_counts.max()*0.85),
                fontsize=9, color="#E74C3C", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=1.5))
    _save_chart(fig, f"{idx:02d}_bai_viet_theo_nam.png", "B\u00e0i vi\u1ebft theo n\u0103m",
        "Bi\u1ec3u \u0111\u1ed3 c\u1ed9t: s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft ph\u00e2n b\u1ed5 theo t\u1eebng n\u0103m, t\u1eeb 2015 \u0111\u1ebfn 2026",
        f"N\u0103m {peak} d\u1eabn \u0111\u1ea7u ({year_counts.max():,} b\u00e0i). S\u1ea3n l\u01b0\u1ee3ng t\u0103ng m\u1ea1nh t\u1eeb 2023, \u0111\u1eb7c bi\u1ec7t n\u0103m 2025 v\u00e0 2026, ph\u1ea3n \u00e1nh s\u1ef1 b\u00f9ng n\u1ed5 tin t\u1ee9c v\u1ec1 B\u0110S v\u00e0 ch\u1ee9ng kho\u00e1n.",
        "bar", "SOURCE_INDEX.Datetime Public",
        f"N\u0103m {peak} c\u00f3 s\u1ed1 b\u00e0i cao nh\u1ea5t: {year_counts.max():,}",
        peak_year=int(peak), peak_count=int(year_counts.max()),
        year_range=[int(year_counts.index[0]), int(year_counts.index[-1])])


def chart_03_category_distribution(df_source_index):
    """Phân bố bài viết theo chuyên mục (dạng barh, không pie để tránh chồng label)"""
    idx = _next_idx()
    cat_counts = df_source_index["Category"].value_counts()
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(range(len(cat_counts)), cat_counts.values,
                   color=[CATEGORY_COLORS.get(c, "#95A5A6") for c in cat_counts.index],
                   edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(cat_counts)))
    ax.set_yticklabels(cat_counts.index, fontsize=11)
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 b\u00e0i vi\u1ebft theo chuy\u00ean m\u1ee5c", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, cat_counts.values):
        pct = val / len(df_source_index) * 100
        ax.text(val + max(cat_counts.values)*0.003, bar.get_y() + bar.get_height()/2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=9)
    ax.set_xlim(0, cat_counts.values[0] * 1.15)
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    _save_chart(fig, f"{idx:02d}_phan_bo_chuyen_muc.png", "Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c",
        "Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang: t\u1ef7 l\u1ec7 b\u00e0i vi\u1ebft ph\u00e2n theo t\u1eebng chuy\u00ean m\u1ee5c (B\u0110S, TC, CK, TT, DN...)",
        f"B\u0110S chi\u1ebfm {(cat_counts['B\u0110S']/len(df_source_index)*100):.1f}% v\u1edbi {cat_counts['B\u0110S']:,} b\u00e0i. TC ({cat_counts.get('TC',0):,}) v\u00e0 CK ({cat_counts.get('CK',0):,}) l\u1ea7n l\u01b0\u1ee3t x\u1ebfp sau. Ba chuy\u00ean m\u1ee5c n\u00e0y ph\u1ea3n \u00e1nh \u0111\u00fang tr\u1ecdng t\u00e2m ph\u00e2n t\u00edch.",
        "barh", "SOURCE_INDEX.Category",
        f"B\u0110S chi\u1ebfm {(cat_counts['B\u0110S']/len(df_source_index)*100):.1f}% t\u1ed5ng s\u1ed1 b\u00e0i",
        top1=cat_counts.index[0], top1_pct=round(cat_counts.iloc[0]/len(df_source_index)*100, 1),
        total_categories=len(cat_counts))


def chart_04_ticker_mentions(df_news_raw):
    """Mã cổ phiếu được nhắc đến nhiều nhất"""
    idx = _next_idx()
    ticker_counts = Counter()
    for t_str in df_news_raw["tickers"].dropna():
        for t in str(t_str).replace(" ", "").split(","):
            if t: ticker_counts[t.strip()] += 1
    ticker_df = pd.DataFrame(ticker_counts.most_common(17), columns=["Ticker", "Count"]).sort_values("Count")
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = [TICKER_COLORS.get(t, "#95A5A6") for t in ticker_df["Ticker"]]
    bars = ax.barh(range(len(ticker_df)), ticker_df["Count"].values, color=colors, edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(ticker_df)))
    ax.set_yticklabels(ticker_df["Ticker"].values, fontsize=11, fontweight="bold")
    ax.set_xlabel("S\u1ed1 l\u1ea7n \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn")
    ax.set_title("M\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn nhi\u1ec1u nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, ticker_df["Count"].values):
        pct = val / ticker_df["Count"].sum() * 100
        ax.text(val + ticker_df["Count"].max()*0.005, bar.get_y() + bar.get_height()/2,
                f"{val:,} l\u1ea7n ({pct:.1f}%)", va="center", fontsize=8)
    ax.set_xlim(0, ticker_df["Count"].max() * 1.18)
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    total = int(ticker_df["Count"].sum())
    _save_chart(fig, f"{idx:02d}_ma_co_phieu_noi_bat.png", "M\u00e3 c\u1ed5 phi\u1ebfu n\u1ed5i b\u1eadt",
        "Bi\u1ec3u \u0111\u1ed3 c\u1ed9t ngang: 17 m\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn nhi\u1ec1u nh\u1ea5t trong c\u00e1c b\u00e0i b\u00e1o \u0111\u00e3 ph\u00e2n t\u00edch",
        f"NVL d\u1eabn \u0111\u1ea7u v\u1edbi {int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0]):,} l\u1ea7n ({int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0])/total*100:.1f}%). Top 3 (NVL, VIC, VHM) chi\u1ebfm {ticker_df.iloc[-3:]['Count'].sum()/total*100:.1f}% t\u1ed5ng l\u01b0\u1ee3ng \u0111\u1ec1 c\u1eadp.",
        "barh", "NEWS_RAW.tickers",
        f"NVL \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn nhi\u1ec1u nh\u1ea5t: {int(ticker_df[ticker_df['Ticker']=='NVL']['Count'].iloc[0]):,} l\u1ea7n",
        top1=ticker_df.iloc[-1]["Ticker"], top1_count=int(ticker_df.iloc[-1]["Count"]),
        top3=[ticker_df.iloc[-1]["Ticker"], ticker_df.iloc[-2]["Ticker"], ticker_df.iloc[-3]["Ticker"]],
        top3_pct=round(ticker_df.iloc[-3:]["Count"].sum()/total*100, 1), total_mentions=total)


def chart_05_source_match_rate(df_source_index, df_news_raw):
    """Nguồn tin có tỷ lệ bài trúng mã cổ phiếu cao nhất (kết hợp cột + đường)"""
    idx = _next_idx()
    total_s = df_source_index["Source"].value_counts()
    matched_s = df_news_raw["source"].value_counts()
    rate_df = pd.DataFrame({"total": total_s, "matched": matched_s}).fillna(0).astype({"matched": int})
    rate_df["rate"] = (rate_df["matched"] / rate_df["total"] * 100).round(2)
    rate_df = rate_df[rate_df["total"] >= 500].sort_values("rate", ascending=False).head(12)
    fig, ax1 = plt.subplots(figsize=(13, 6))
    x = np.arange(len(rate_df))
    bars = ax1.bar(x, rate_df["matched"].values, color="#3498DB", alpha=0.65, width=0.6, label="S\u1ed1 b\u00e0i tr\u00fang m\u00e3 CP")
    ax1.set_xticks(x); ax1.set_xticklabels(rate_df.index, rotation=45, ha="right", fontsize=8)
    ax1.set_xlabel("Ngu\u1ed3n tin"); ax1.set_ylabel("S\u1ed1 b\u00e0i tr\u00fang m\u00e3 CP", color="#3498DB")
    ax2 = ax1.twinx()
    line = ax2.plot(x, rate_df["rate"].values, "o-", color="#E74C3C", linewidth=2, markersize=7, zorder=5, label="T\u1ef7 l\u1ec7 tr\u00fang (%)")
    ax2.set_ylabel("T\u1ef7 l\u1ec7 tr\u00fang m\u00e3 CP (%)", color="#E74C3C")
    for i, (_, r) in enumerate(rate_df.iterrows()):
        ax1.text(i, r["matched"] + max(rate_df["matched"])*0.01, f"{r['rate']:.1f}%", ha="center", fontsize=7.5, color="#E74C3C", fontweight="bold")
    l1, la1 = ax1.get_legend_handles_labels(); l2, la2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, la1 + la2, loc="upper left", fontsize=9)
    ax1.set_title("Ngu\u1ed3n tin c\u00f3 t\u1ef7 l\u1ec7 b\u00e0i tr\u00fang m\u00e3 c\u1ed5 phi\u1ebfu cao nh\u1ea5t",
                  fontsize=15, fontweight="bold", pad=15)
    ax1.grid(axis="y", alpha=0.3, linestyle="--"); ax1.set_axisbelow(True)
    _save_chart(fig, f"{idx:02d}_nguon_tin_trung_ma_cp.png", "Ngu\u1ed3n tin tr\u00fang m\u00e3 CP",
        "Bi\u1ec3u \u0111\u1ed3 k\u1ebft h\u1ee3p c\u1ed9t v\u00e0 \u0111\u01b0\u1eddng: s\u1ed1 b\u00e0i ph\u00f9 h\u1ee3p v\u00e0 t\u1ef7 l\u1ec7 ph\u00f9 h\u1ee3p c\u1ee7a t\u1eebng ngu\u1ed3n tin",
        f"Ngu\u1ed3n {rate_df.index[0]} c\u00f3 t\u1ef7 l\u1ec7 tr\u00fang cao nh\u1ea5t ({rate_df.iloc[0]['rate']:.1f}%). C\u00e1c ngu\u1ed3n chuy\u00ean s\u00e2u v\u1ec1 B\u0110S v\u00e0 CK c\u00f3 t\u1ef7 l\u1ec7 cao h\u01a1n \u0111\u00e1ng k\u1ec3 so v\u1edbi ngu\u1ed3n t\u1ed5ng h\u1ee3p.",
        "dual_axis", "SOURCE_INDEX.Status + NEWS_RAW.source",
        f"Ngu\u1ed3n {rate_df.index[0]} c\u00f3 t\u1ef7 l\u1ec7 tr\u00fang cao nh\u1ea5t: {rate_df.iloc[0]['rate']:.1f}%",
        top1_source=rate_df.index[0], top1_rate=float(rate_df.iloc[0]["rate"]),
        top1_matched=int(rate_df.iloc[0]["matched"]))


def chart_06_crawl_success_rate(df_news_raw):
    """Tỷ lệ tải bài thành công (dùng label thay vì autopct để tránh chồng)"""
    idx = _next_idx()
    status_counts = df_news_raw["crawl_status"].value_counts()
    labels_map = {"success": "Th\u00e0nh c\u00f4ng", "short_content": "N\u1ed9i dung ng\u1eafn", "failed": "Th\u1ea5t b\u1ea1i"}
    colors_map = {"success": "#2ECC71", "short_content": "#F39C12", "failed": "#E74C3C"}
    labels = [labels_map.get(s, s) for s in status_counts.index]
    colors = [colors_map.get(s, "#95A5A6") for s in status_counts.index]
    fig, ax = plt.subplots(figsize=(9, 7))
    wedges, texts, autotexts = ax.pie(
        status_counts.values, labels=labels, autopct=lambda p: f"{p:.1f}%" if p > 5 else "",
        colors=colors, startangle=90, explode=[0.02]*len(status_counts),
        textprops={"fontsize": 11}, pctdistance=0.75)
    for t, a in zip(texts, autotexts):
        t.set_fontsize(11)
        if a: a.set_fontsize(11); a.set_fontweight("bold")
    # Add small count labels for small slices outside
    for i, (val, label) in enumerate(zip(status_counts.values, labels)):
        if val / status_counts.sum() < 0.05:
            ang = (wedges[i].theta2 + wedges[i].theta1) / 2
            x = 1.25 * np.cos(np.deg2rad(ang))
            y = 1.25 * np.sin(np.deg2rad(ang))
            ax.annotate(f"{label}: {val:,}", xy=(1.05*np.cos(np.deg2rad(ang)), 1.05*np.sin(np.deg2rad(ang))),
                       fontsize=9, ha="center", va="center")
    ax.set_title("T\u1ef7 l\u1ec7 t\u1ea3i b\u00e0i th\u00e0nh c\u00f4ng", fontsize=15, fontweight="bold", pad=15)
    success = status_counts.get("success", 0); total = status_counts.sum()
    ax.text(0, -1.25, f"T\u1ed5ng s\u1ed1 b\u00e0i: {total:,} | Th\u00e0nh c\u00f4ng: {success:,} ({success/total*100:.1f}%)",
            ha="center", fontsize=9, color="gray")
    _save_chart(fig, f"{idx:02d}_ty_le_tai_bai.png", "T\u1ef7 l\u1ec7 t\u1ea3i b\u00e0i",
        "Bi\u1ec3u \u0111\u1ed3 tr\u00f2n: t\u1ef7 l\u1ec7 t\u1ea3i b\u00e0i th\u00e0nh c\u00f4ng, n\u1ed9i dung ng\u1eafn v\u00e0 th\u1ea5t b\u1ea1i",
        f"T\u1ef7 l\u1ec7 t\u1ea3i th\u00e0nh c\u00f4ng: {success/total*100:.1f}%. Ch\u1ec9 {status_counts.get('failed',0)} b\u00e0i th\u1ea5t b\u1ea1i (0.3%) v\u00e0 {status_counts.get('short_content',0)} b\u00e0i n\u1ed9i dung ng\u1eafn. H\u1ec7 th\u1ed1ng ho\u1ea1t \u0111\u1ed9ng \u1ed5n \u0111\u1ecbnh.",
        "pie", "NEWS_RAW.crawl_status",
        f"T\u1ef7 l\u1ec7 t\u1ea3i th\u00e0nh c\u00f4ng: {success/total*100:.1f}%",
        success_rate=round(success/total*100, 1), total_articles=int(total),
        failed=int(status_counts.get("failed", 0)))


def chart_07_source_ticker_heatmap(df_news_raw):
    """Mối liên hệ giữa nguồn tin và mã cổ phiếu"""
    idx = _next_idx()
    ts = defaultdict(lambda: defaultdict(int))
    for _, row in df_news_raw.iterrows():
        for t in str(row["tickers"]).replace(" ", "").split(","):
            if t.strip(): ts[t.strip()][str(row["source"])] += 1
    top_ticks = ["NVL", "VIC", "VHM", "DXG", "VRE", "CTD", "PDR", "NLG", "HHV", "KBC"]
    top_srcs = sorted(set(s for t in top_ticks for s in ts.get(t, {})),
                      key=lambda s: sum(ts[t].get(s, 0) for t in top_ticks), reverse=True)[:8]
    hm = pd.DataFrame([[ts[t].get(s, 0) for s in top_srcs] for t in top_ticks],
                      index=top_ticks, columns=top_srcs)
    fig, ax = plt.subplots(figsize=(13, 8))
    sns.heatmap(hm, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n xu\u1ea5t hi\u1ec7n"}, ax=ax, annot_kws={"fontsize": 8})
    ax.set_title("Ngu\u1ed3n tin n\u00e0o th\u01b0\u1eddng nh\u1eafc \u0111\u1ebfn m\u00e3 c\u1ed5 phi\u1ebfu n\u00e0o?",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Ngu\u1ed3n tin", fontsize=11); ax.set_ylabel("M\u00e3 c\u1ed5 phi\u1ebfu", fontsize=11)
    plt.yticks(rotation=0); plt.xticks(rotation=30, ha="right")
    _save_chart(fig, f"{idx:02d}_ma_tran_nguon_ma_cp.png", "Ma tr\u1eadn ngu\u1ed3n v\u00e0 m\u00e3 CP",
        "Heatmap: th\u1ec3 hi\u1ec7n ngu\u1ed3n tin n\u00e0o th\u01b0\u1eddng \u0111\u01b0a tin v\u1ec1 m\u00e3 c\u1ed5 phi\u1ebfu n\u00e0o",
        "NVL xu\u1ea5t hi\u1ec7n d\u00e0y \u0111\u1eb7c \u1edf h\u1ea7u h\u1ebft c\u00e1c ngu\u1ed3n, \u0111\u1eb7c bi\u1ec7t CafeBiz B\u0110S v\u00e0 CafeF DN. M\u1ed7i ngu\u1ed3n c\u00f3 th\u1ebf m\u1ea1nh ri\u00eang v\u1ec1 m\u1ed9t s\u1ed1 m\u00e3 nh\u1ea5t \u0111\u1ecbnh.",
        "heatmap", "NEWS_RAW.tickers + source",
        "NVL \u0111\u01b0\u1ee3c nh\u1eafc nhi\u1ec1u nh\u1ea5t \u1edf h\u1ea7u h\u1ebft ngu\u1ed3n tin")


def chart_08_ticker_cooccurrence(df_news_raw):
    """Các mã cổ phiếu thường xuất hiện cùng nhau"""
    idx = _next_idx()
    tick_lists = [[t.strip() for t in str(t_str).replace(" ", "").split(",") if t.strip()]
                  for t_str in df_news_raw["tickers"].dropna()]
    top10 = ["NVL", "VIC", "VHM", "DXG", "VRE", "CTD", "PDR", "NLG", "HHV", "KBC"]
    cooc = pd.DataFrame(0, index=top10, columns=top10)
    for ticks in tick_lists:
        present = [t for t in ticks if t in top10]
        for i, t1 in enumerate(present):
            for t2 in present[i+1:]:
                cooc.loc[t1, t2] += 1; cooc.loc[t2, t1] += 1
    mask = np.triu(np.ones_like(cooc, dtype=bool), k=1)
    fig, ax = plt.subplots(figsize=(9, 8))
    sns.heatmap(cooc, mask=~mask, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n xu\u1ea5t hi\u1ec7n c\u00f9ng nhau"}, ax=ax, annot_kws={"fontsize": 8})
    ax.set_title("M\u00e3 c\u1ed5 phi\u1ebfu n\u00e0o hay \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn c\u00f9ng nhau?",
                 fontsize=15, fontweight="bold", pad=15)
    plt.yticks(rotation=0); plt.xticks(rotation=45, ha="right")
    max_pair = cooc.stack().idxmax()
    max_val = int(cooc.max().max())
    _save_chart(fig, f"{idx:02d}_cap_ma_cp_cung_xuat_hien.png", "C\u1eb7p m\u00e3 CP c\u00f9ng xu\u1ea5t hi\u1ec7n",
        "Heatmap (n\u1eeda tr\u00ean): t\u1ea7n su\u1ea5t hai m\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn trong c\u00f9ng m\u1ed9t b\u00e0i b\u00e1o",
        f"C\u1eb7p {max_pair[0]}-{max_pair[1]} th\u01b0\u1eddng xu\u1ea5t hi\u1ec7n c\u00f9ng nhau nh\u1ea5t ({max_val} l\u1ea7n). C\u00e1c m\u00e3 trong c\u00f9ng t\u1eadp \u0111o\u00e0n (VIC-VHM) ho\u1eb7c c\u00f9ng ng\u00e0nh th\u01b0\u1eddng \u0111i k\u00e8m, gi\u00fap ph\u00e1t hi\u1ec7n m\u1ed1i quan h\u1ec7 th\u1ecb tr\u01b0\u1eddng.",
        "heatmap", "NEWS_RAW.tickers",
        f"C\u1eb7p {max_pair[0]}-{max_pair[1]} xu\u1ea5t hi\u1ec7n c\u00f9ng nhau nhi\u1ec1u nh\u1ea5t: {max_val} l\u1ea7n",
        top_pair=f"{max_pair[0]}-{max_pair[1]}", top_pair_count=max_val)


def chart_09_weekday_distribution(df_source_index):
    """Ngày nào trong tuần có nhiều tin tức nhất"""
    idx = _next_idx()
    df = df_source_index.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df["weekday"] = df["date"].dt.dayofweek
    wd_names = ["Th\u1ee9 Hai", "Th\u1ee9 Ba", "Th\u1ee9 T\u01b0", "Th\u1ee9 N\u0103m", "Th\u1ee9 S\u00e1u", "Th\u1ee9 B\u1ea3y", "Ch\u1ee7 Nh\u1eadt"]
    df = df.dropna(subset=["weekday"])
    wd_counts = df["weekday"].value_counts().sort_index()
    colors_wd = ["#2ECC71"] * 5 + ["#F39C12", "#E74C3C"]
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(wd_names, [wd_counts.get(i, 0) for i in range(7)],
                  color=colors_wd, edgecolor="white", linewidth=0.8, width=0.65)
    for bar, val in zip(bars, [wd_counts.get(i, 0) for i in range(7)]):
        pct = val / wd_counts.sum() * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + wd_counts.max()*0.005,
                f"{val:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_xlabel("Ng\u00e0y trong tu\u1ea7n"); ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("B\u00e0i vi\u1ebft \u0111\u01b0\u1ee3c \u0111\u0103ng v\u00e0o ng\u00e0y n\u00e0o trong tu\u1ea7n?",
                 fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    peak_idx = int(wd_counts.idxmax())
    _save_chart(fig, f"{idx:02d}_phan_bo_trong_tuan.png", "Ph\u00e2n b\u1ed1 trong tu\u1ea7n",
        "Bi\u1ec3u \u0111\u1ed3 c\u1ed9t: ph\u00e2n b\u1ed1 s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo ng\u00e0y trong tu\u1ea7n",
        f"C\u00e1c ng\u00e0y trong tu\u1ea7n c\u00f3 s\u1ed1 b\u00e0i cao h\u01a1n h\u1eb3n cu\u1ed1i tu\u1ea7n ({wd_names[peak_idx]} nhi\u1ec1u nh\u1ea5t: {int(wd_counts.max()):,} b\u00e0i). Th\u1ee9 B\u1ea3y v\u00e0 Ch\u1ee7 Nh\u1eadt gi\u1ea3m m\u1ea1nh do \u0111\u1eb7c th\u00f9 b\u00e1o ch\u00ed Vi\u1ec7t Nam.",
        "bar", "SOURCE_INDEX.Datetime Public",
        f"{wd_names[peak_idx]} c\u00f3 nhi\u1ec1u b\u00e0i nh\u1ea5t: {int(wd_counts.max()):,} b\u00e0i",
        peak_weekday=wd_names[peak_idx], peak_count=int(wd_counts.max()),
        weekday_total=int(sum(wd_counts.get(i, 0) for i in range(5))),
        weekend_total=int(sum(wd_counts.get(i, 0) for i in [5, 6])))


def chart_10_content_length_distribution(df_news_raw):
    """Độ dài bài viết phổ biến"""
    idx = _next_idx()
    df = df_news_raw.copy()
    df["len"] = df["content"].dropna().str.len()
    df = df[(df["len"] > 50) & (df["len"] < df["len"].quantile(0.99))]
    fig, ax = plt.subplots(figsize=(13, 6))
    n_bins = 40
    bins = np.linspace(df["len"].min(), df["len"].max(), n_bins)
    ax.hist(df["len"], bins=bins, color="#3498DB", edgecolor="white", linewidth=0.3, alpha=0.8)
    mean_val, median_val = df["len"].mean(), df["len"].median()
    ax.axvline(mean_val, color="#E74C3C", linestyle="--", linewidth=2,
               label=f"Trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1")
    ax.axvline(median_val, color="#F39C12", linestyle=":", linewidth=2,
               label=f"Trung v\u1ecb: {median_val:,.0f} k\u00fd t\u1ef1")
    ax.set_xlabel("\u0110\u1ed9 d\u00e0i b\u00e0i vi\u1ebft (s\u1ed1 k\u00fd t\u1ef1)")
    ax.set_ylabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 \u0111\u1ed9 d\u00e0i c\u1ee7a c\u00e1c b\u00e0i b\u00e1o \u0111\u00e3 t\u1ea3i", fontsize=15, fontweight="bold", pad=15)
    ax.legend(fontsize=10); ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    _save_chart(fig, f"{idx:02d}_do_dai_bai_viet.png", "\u0110\u1ed9 d\u00e0i b\u00e0i vi\u1ebft",
        "Histogram: ph\u00e2n b\u1ed1 \u0111\u1ed9 d\u00e0i n\u1ed9i dung c\u00e1c b\u00e0i b\u00e1o \u0111\u00e3 t\u1ea3i th\u00e0nh c\u00f4ng",
        f"\u0110\u1ed9 d\u00e0i trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1, trung v\u1ecb: {median_val:,.0f} k\u00fd t\u1ef1. H\u1ea7u h\u1ebft b\u00e0i vi\u1ebft c\u00f3 \u0111\u1ed9 d\u00e0i t\u1eeb 3,000-8,000 k\u00fd t\u1ef1, ph\u00f9 h\u1ee3p v\u1edbi \u0111\u1eb7c th\u00f9 b\u00e1o ch\u00ed Vi\u1ec7t Nam.",
        "histogram", "NEWS_RAW.content",
        f"\u0110\u1ed9 d\u00e0i trung b\u00ecnh: {mean_val:,.0f} k\u00fd t\u1ef1",
        mean_length=int(mean_val), median_length=int(median_val))


def generate_statistic_json(df_source_index, df_news_raw, df_company_info, df_source_list, df_news_raw_unfiltered):
    """Create comprehensive statistic.json"""
    print("\nGenerating statistic.json...")

    # Basic stats
    total_links = len(df_source_index)
    total_enriched = len(df_news_raw)
    total_failed = len(df_news_raw[df_news_raw["crawl_status"] == "failed"]) if "crawl_status" in df_news_raw.columns else 0

    # Date range
    dates = pd.to_datetime(df_source_index["Datetime Public"].str.replace(r"\+.*$", "", regex=True), errors="coerce")
    date_min = dates.min()
    date_max = dates.max()

    # Sources
    total_sources = df_source_index["Source"].nunique()
    source_types = {}
    type_col = next((c for c in df_source_list.columns if "Lo\u1ea1i" in c), None)
    if type_col:
        source_types = df_source_list[type_col].value_counts().to_dict()

    # Categories
    cat_counts = df_source_index["Category"].value_counts().to_dict()
    cat_counts_clean = {str(k): int(v) for k, v in cat_counts.items()}

    # Companies
    companies = []
    ticker_col = next((c for c in df_company_info.columns if "M\u00e3" in c), None)
    name_col = next((c for c in df_company_info.columns if "T\u00ean \u0111\u1ea7" in c or "t\u00ean" in c.lower()), None)
    exchange_col = next((c for c in df_company_info.columns if "S\u00e0n" in c), None)
    industry_col = next((c for c in df_company_info.columns if "Ng\u00e0nh" in c), None)
    if ticker_col:
        for _, row in df_company_info.iterrows():
            companies.append({
                "ticker": row[ticker_col],
                "name": row.get(name_col, "") if name_col else "",
                "exchange": row.get(exchange_col, "") if exchange_col else "",
                "industry": row.get(industry_col, "") if industry_col else "",
            })

    # Ticker mentions
    ticker_counts = Counter()
    for t_str in df_news_raw["tickers"].dropna():
        for t in str(t_str).replace(" ", "").split(","):
            if t: ticker_counts[t.strip()] += 1

    # Source type breakdown
    total_rss = df_source_index[df_source_index["Source"].str.startswith("RSS", na=False)].shape[0]
    total_api = df_source_index[df_source_index["Source"].str.startswith("API", na=False)].shape[0]

    # RSS vs API source names
    rss_sources = sorted(df_source_index[df_source_index["Source"].str.startswith("RSS", na=False)]["Source"].unique())
    api_sources = sorted(df_source_index[df_source_index["Source"].str.startswith("API", na=False)]["Source"].unique())

    # Status
    status_counts = df_source_index["Status"].value_counts().to_dict()

    # Enrichment rate
    matched_status = status_counts.get("mentioned", 0)
    new_status = status_counts.get("new", 0)
    failed_status = status_counts.get("failed", 0)

    stat = {
        "project": "DA2 - Crawl tin t\u1ee9c B\u0110S & CK",
        "generated_at": "2026-06-06",
        "data_source": "K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx",
        "sheets": 10,
        "overview": {
            "total_links_crawled": int(total_links),
            "total_links_enriched": int(total_enriched),
            "enrichment_rate_pct": round(total_enriched / total_links * 100, 2),
            "total_failed_fetches": int(total_failed),
            "date_range": {
                "from": str(date_min.date()) if hasattr(date_min, 'date') else str(date_min),
                "to": str(date_max.date()) if hasattr(date_max, 'date') else str(date_max),
                "total_days": int((date_max - date_min).days) if hasattr(date_min, 'date') else 0,
            },
        },
        "sources": {
            "total_unique_sources": int(total_sources),
            "by_type": {str(k): int(v) for k, v in source_types.items()},
            "total_rss_feeds": len(rss_sources),
            "total_api_zones": len(api_sources),
            "rss_sources_list": rss_sources[:20],
            "api_sources_list": api_sources,
            "source_names_list": sorted(df_source_list["T\u00ean trang"].dropna().unique().tolist()) if "T\u00ean trang" in df_source_list.columns else [],
        },
        "categories": {
            "total_categories": len(cat_counts_clean),
            "by_category": {
                k: {"count": v, "pct": round(v / total_links * 100, 1)}
                for k, v in sorted(cat_counts_clean.items(), key=lambda x: -x[1])
            },
        },
        "articles": {
            "total_source_index": int(total_links),
            "total_news_raw": int(total_enriched),
            "by_status": {
                "new_unprocessed": int(new_status),
                "mentioned_enriched": int(matched_status),
                "failed": int(failed_status),
            },
            "status_pct": {
                "new_pct": round(new_status / total_links * 100, 1),
                "mentioned_pct": round(matched_status / total_links * 100, 1),
                "failed_pct": round(failed_status / total_links * 100, 1),
            },
            "rss_vs_api": {
                "rss_articles": int(total_rss),
                "api_articles": int(total_api),
                "rss_pct": round(total_rss / total_links * 100, 1),
                "api_pct": round(total_api / total_links * 100, 1),
            },
        },
        "companies_and_tickers": {
            "total_companies": len(companies),
            "companies": companies,
            "ticker_mentions": {
                str(k): int(v) for k, v in sorted(ticker_counts.items(), key=lambda x: -x[1])
            },
            "total_mentions": int(sum(ticker_counts.values())),
        },
        "top_statistics": {
            "top_5_sources": [
                {"rank": i+1, "name": s, "count": int(c)}
                for i, (s, c) in enumerate(
                    sorted(df_source_index["Source"].value_counts().head(5).items(), key=lambda x: -x[1])
                )
            ],
            "top_5_tickers": [
                {"rank": i+1, "ticker": t, "count": int(c)}
                for i, (t, c) in enumerate(ticker_counts.most_common(5))
            ],
            "top_3_categories": [
                {"rank": i+1, "name": k, "count": int(v)}
                for i, (k, v) in enumerate(
                    sorted(cat_counts_clean.items(), key=lambda x: -x[1])[:3]
                )
            ],
        },
    }

    path = os.path.join(REPORT_DIR, "statistic.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stat, f, ensure_ascii=False, indent=2)
    print(f"  Saved: statistic.json ({os.path.getsize(path)/1024:.0f} KB)")
    return stat


def main():
    print("=" * 60)
    print("DA2 Chart Generator v2 - 10 Quality Charts")
    print("=" * 60)

    dfs = load_data()
    df_si = dfs.get("SOURCE_INDEX", pd.DataFrame())
    df_nr = dfs.get("NEWS_RAW", pd.DataFrame())
    df_ci = dfs.get("COMPANY_INFO", pd.DataFrame())
    df_sl = dfs.get("SOURCE_LIST", pd.DataFrame())

    if df_si.empty or df_nr.empty:
        print("ERROR: Could not load data")
        return

    # Clear old charts
    for f in os.listdir(REPORT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(REPORT_DIR, f))
            print(f"Removed old: {f}")

    print("\n" + "=" * 60)
    print("Generating 10 charts...")
    print("=" * 60)

    global CHART_INDEX
    CHART_INDEX = 0

    chart_01_top_sources(df_si)
    chart_02_articles_by_year(df_si)
    chart_03_category_distribution(df_si)
    chart_04_ticker_mentions(df_nr)
    chart_05_source_match_rate(df_si, df_nr)
    chart_06_crawl_success_rate(df_nr)
    chart_07_source_ticker_heatmap(df_nr)
    chart_08_ticker_cooccurrence(df_nr)
    chart_09_weekday_distribution(df_si)
    chart_10_content_length_distribution(df_nr)

    # Save chart.json
    print(f"\n{'=' * 60}")
    print(f"Generated {len(CHARTS_META)} charts")
    print(f"Saving chart.json...")
    meta_path = os.path.join(REPORT_DIR, "chart.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(CHARTS_META, f, ensure_ascii=False, indent=2)

    # Generate statistic.json
    generate_statistic_json(df_si, df_nr, df_ci, df_sl, df_nr)

    # Summary
    total_kb = sum(c["file_size_kb"] for c in CHARTS_META)
    print(f"\nDone! {len(CHARTS_META)} charts ({total_kb:.0f} KB total)")
    for c in CHARTS_META:
        print(f"  {c['path'].split('/')[-1]:40s} {c['chart_type']:15s} {c['file_size_kb']:>5.1f}KB  {c['name']}")


if __name__ == "__main__":
    main()
