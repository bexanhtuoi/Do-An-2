import os
import json
import warnings
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
CATEGORY_EXPLAIN = {
    "B\u0110S": "B\u1ea5t \u0111\u1ed9ng s\u1ea3n", "TC": "T\u00e0i ch\u00ednh", "CK": "Ch\u1ee9ng kho\u00e1n",
    "TT": "Th\u1ecb tr\u01b0\u1eddng", "DN": "Doanh nghi\u1ec7p", "\u0110T": "\u0110\u1ea7u t\u01b0",
    "KD": "Kinh doanh", "DT": "\u0110\u00e0o t\u1ea1o", "SX": "S\u1ea3n xu\u1ea5t",
    "TG": "Th\u1ebf gi\u1edbi", "XD": "X\u00e2y d\u1ef1ng",
}

INDUSTRY_GROUPS = [
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n nh\u00e0 \u1edf, ngh\u1ec9 d\u01b0\u1ee1ng",
    "\u0110a ng\u00e0nh (B\u0110S, b\u00e1n l\u1ebb, y t\u1ebf, gi\u00e1o d\u1ee5c)",
    "H\u1ea1 t\u1ea7ng KCN",
    "X\u00e2y d\u1ef1ng",
    "X\u00e2y d\u1ef1ng h\u1ea1 t\u1ea7ng",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n KCN",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n, h\u1ea1 t\u1ea7ng",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n, x\u00e2y d\u1ef1ng",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n KCN, h\u1ea1 t\u1ea7ng",
    "B\u1ea5t \u0111\u1ed9ng s\u1ea3n, d\u1ecbch v\u1ee5",
    "D\u1ecbch v\u1ee5 x\u00e2y d\u1ef1ng",
]


def _parse_dates(series):
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


# ─── CHART 01: Top 15 nguồn tin ───────────────────────────────────
def chart_01_top_sources(df_si):
    idx = _next_idx()
    sc = df_si["Source"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(12, 6.5))
    bars = ax.barh(range(len(sc)), sc.values, color=SOURCE_COLORS[:len(sc)], edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(sc)))
    ax.set_yticklabels(sc.index, fontsize=9)
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Top 15 ngu\u1ed3n tin c\u00f3 nhi\u1ec1u b\u00e0i vi\u1ebft nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, sc.values):
        ax.text(val + sc.values[0]*0.005, bar.get_y()+bar.get_height()/2, f"{val:,}", va="center", fontsize=8, color="#2C3E50")
    ax.set_xlim(0, sc.values[0]*1.15)
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)

    api_pct = df_si[df_si["Source"].str.startswith("API", na=False)].shape[0]/len(df_si)*100
    rss_pct = df_si[df_si["Source"].str.startswith("RSS", na=False)].shape[0]/len(df_si)*100

    _save_chart(fig, f"{idx:02d}_top_nguon_tin.png", "Top ngu\u1ed3n tin",
        "C\u1ed9t ngang: 15 ngu\u1ed3n c\u00f3 s\u1ed1 b\u00e0i nhi\u1ec1u nh\u1ea5t. Th\u1ec3 hi\u1ec7n s\u1ef1 ph\u00e2n b\u1ed1 ngu\u1ed3n tin trong h\u1ec7 th\u1ed1ng.",
        f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u tuy\u1ec7t \u0111\u1ed1i ({sc.iloc[0]:,} b\u00e0i). Ba ngu\u1ed3n \u0111\u1ea7u chi\u1ebfm {sc.iloc[:3].sum()/len(df_si)*100:.1f}%. Ngu\u1ed3n API chi\u1ebfm {api_pct:.0f}%, RSS chi\u1ebfm {rss_pct:.0f}%. CafeF v\u00e0 CafeBiz l\u00e0 hai t\u00ean mi\u1ec1n ch\u00ednh cung c\u1ea5p d\u1eef li\u1ec7u.",
        "barh", "SOURCE_INDEX.Source",
        f"CafeBiz B\u0110S d\u1eabn \u0111\u1ea7u: {sc.iloc[0]:,} b\u00e0i ({sc.iloc[0]/len(df_si)*100:.1f}%), API chi\u1ebfm {api_pct:.0f}% t\u1ed5ng d\u1eef li\u1ec7u",
        api_pct=round(api_pct, 1), rss_pct=round(rss_pct, 1),
        top1=sc.index[0], top1_count=int(sc.iloc[0]),
        top3_pct=round(sc.iloc[:3].sum()/len(df_si)*100, 1),
        total_sources=df_si["Source"].nunique())


# ─── CHART 02: Bài viết theo năm ──────────────────────────────────
def chart_02_articles_by_year(df_si):
    idx = _next_idx()
    df = df_si.copy()
    df["year"] = _parse_dates(df["Datetime Public"]).dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    yc = df["year"].value_counts().sort_index()
    yc = yc[yc.index >= 2015]
    fig, ax = plt.subplots(figsize=(14, 6))
    colors = ["#2ECC71" if y <= 2022 else "#F39C12" if y == 2023 else "#E74C3C" if y >= 2025 else "#3498DB" for y in yc.index]
    bars = ax.bar([str(y) for y in yc.index], yc.values, color=colors, edgecolor="white", linewidth=0.8, width=0.7)
    for bar, val in zip(bars, yc.values):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+max(yc.values)*0.01,
                f"{val:,}", ha="center", va="bottom", fontsize=8, rotation=45)
    ax.set_xlabel("N\u0103m"); ax.set_ylabel("S\u1ed1 b\u00e0i vi\u1ebft")
    ax.set_title("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo t\u1eebng n\u0103m", fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)

    growth_24_25 = ((yc.get(2025,0)-yc.get(2024,0))/yc.get(2024,1)*100)
    peak = yc.idxmax()
    ax.annotate(f"\u0110\u1ec9nh: {peak} ({yc.max():,})",
                xy=(list(yc.index).index(peak), yc.max()),
                xytext=(list(yc.index).index(peak)-0.3, yc.max()*0.85),
                fontsize=9, color="#E74C3C", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#E74C3C", lw=1.5))

    _save_chart(fig, f"{idx:02d}_bai_viet_theo_nam.png", "B\u00e0i vi\u1ebft theo n\u0103m",
        "C\u1ed9t \u0111\u1ee9ng: s\u1ed1 b\u00e0i vi\u1ebft ph\u00e2n theo n\u0103m, t\u1eeb 2015 \u0111\u1ebfn nay. M\u00e0u s\u1eafc ph\u00e2n bi\u1ec7t giai \u0111o\u1ea1n: xanh (2015-2022), v\u00e0ng (2023), xanh d\u01b0\u01a1ng (2024), \u0111\u1ecf (2025-2026).",
        f"N\u0103m {peak} d\u1eabn \u0111\u1ea7u ({yc.max():,} b\u00e0i). T\u0103ng tr\u01b0\u1edfng n\u00f3ng t\u1eeb 2024: 2025 t\u0103ng {growth_24_25:.0f}% so v\u1edbi 2024. L\u0169y k\u1ebf 2024-2026 chi\u1ebfm {yc.loc[2024:2026].sum()/yc.sum()*100:.1f}% t\u1ed5ng s\u1ed1 b\u00e0i, cho th\u1ea5y s\u1ef1 b\u00f9ng n\u1ed5 tin t\u1ee9c B\u0110S-CK giai \u0111o\u1ea1n g\u1ea7n \u0111\u00e2y.",
        "bar", "SOURCE_INDEX.Datetime Public",
        f"N\u0103m {peak} \u0111\u1ec9nh: {yc.max():,} b\u00e0i. 2025 t\u0103ng {growth_24_25:.0f}% so 2024",
        peak_year=int(peak), peak_count=int(yc.max()),
        growth_24_25=round(growth_24_25, 1),
        total_2015_2026=int(yc.sum()),
        year_range=[int(yc.index[0]), int(yc.index[-1])])


# ─── CHART 03: Phân bố chuyên mục ─────────────────────────────────
def chart_03_category_distribution(df_si):
    idx = _next_idx()
    cc = df_si["Category"].value_counts()
    fig, ax = plt.subplots(figsize=(13, 7))
    bars = ax.barh(range(len(cc)), cc.values,
                   color=[CATEGORY_COLORS.get(c, "#95A5A6") for c in cc.index],
                   edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(cc)))
    ax.set_yticklabels(cc.index, fontsize=11, fontweight="bold")
    ax.set_xlabel("S\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft")
    ax.set_title("Ph\u00e2n b\u1ed1 b\u00e0i vi\u1ebft theo chuy\u00ean m\u1ee5c", fontsize=15, fontweight="bold", pad=15)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, cc.values):
        pct = val/len(df_si)*100
        ax.text(val+cc.values[0]*0.003, bar.get_y()+bar.get_height()/2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=9)
    ax.set_xlim(0, cc.values[0]*1.18)
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)

    # Legend box explaining category abbreviations
    legend_items = [f"{k} = {v}" for k, v in CATEGORY_EXPLAIN.items()]
    legend_text = "\n".join(legend_items)
    ax.text(0.98, 0.02, legend_text, transform=ax.transAxes, fontsize=7.5,
            va="bottom", ha="right", family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#BDC3C7", alpha=0.85))

    bds_pct = cc.get("B\u0110S", 0)/len(df_si)*100
    ck_pct = cc.get("CK", 0)/len(df_si)*100
    tc_pct = cc.get("TC", 0)/len(df_si)*100

    _save_chart(fig, f"{idx:02d}_phan_bo_chuyen_muc.png", "Ph\u00e2n b\u1ed1 chuy\u00ean m\u1ee5c",
        "C\u1ed9t ngang: ph\u00e2n b\u1ed5 b\u00e0i vi\u1ebft theo 11 chuy\u00ean m\u1ee5c. H\u1ed9p ch\u00fa th\u00edch g\u00f3c ph\u1ea3i gi\u1ea3i ngh\u0129a c\u00e1c k\u00fd hi\u1ec7u vi\u1ebft t\u1eaft.",
        f"B\u0110S chi\u1ebfm {bds_pct:.1f}% ({cc['B\u0110S']:,} b\u00e0i), TC {tc_pct:.1f}%, CK {ck_pct:.1f}%. Ba chuy\u00ean m\u1ee5c n\u00e0y chi\u1ebfm {(bds_pct+tc_pct+ck_pct):.1f}% t\u1ed5ng d\u1eef li\u1ec7u, kh\u1eb3ng \u0111\u1ecbnh tr\u1ecdng t\u00e2m ph\u00e2n t\u00edch B\u0110S - T\u00e0i ch\u00ednh - Ch\u1ee9ng kho\u00e1n.",
        "barh", "SOURCE_INDEX.Category",
        f"B\u0110S chi\u1ebfm {bds_pct:.1f}%, TC {tc_pct:.1f}%, CK {ck_pct:.1f}% - ba chuy\u00ean m\u1ee5c ch\u00ednh",
        categories_legend=CATEGORY_EXPLAIN,
        bds_pct=round(bds_pct,1), ck_pct=round(ck_pct,1), tc_pct=round(tc_pct,1),
        top1=cc.index[0], total_categories=len(cc))


# ─── CHART 04: Mã cổ phiếu nổi bật ────────────────────────────────
def chart_04_ticker_mentions(df_nr):
    idx = _next_idx()
    tc = Counter()
    for t_str in df_nr["tickers"].dropna():
        for t in str(t_str).replace(" ", "").split(","):
            if t: tc[t.strip()] += 1
    tdf = pd.DataFrame(tc.most_common(17), columns=["Ticker","Count"]).sort_values("Count")
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = [TICKER_COLORS.get(t, "#95A5A6") for t in tdf["Ticker"]]
    bars = ax.barh(range(len(tdf)), tdf["Count"].values, color=colors, edgecolor="white", linewidth=0.5, height=0.7)
    ax.set_yticks(range(len(tdf)))
    ax.set_yticklabels(tdf["Ticker"].values, fontsize=11, fontweight="bold")
    ax.set_xlabel("S\u1ed1 l\u1ea7n \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn")
    ax.set_title("M\u00e3 c\u1ed5 phi\u1ebfu \u0111\u01b0\u1ee3c nh\u1eafc \u0111\u1ebfn nhi\u1ec1u nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    for bar, val in zip(bars, tdf["Count"].values):
        pct = val/tdf["Count"].sum()*100
        ax.text(val+tdf["Count"].max()*0.005, bar.get_y()+bar.get_height()/2,
                f"{val:,} ({pct:.1f}%)", va="center", fontsize=8)
    ax.set_xlim(0, tdf["Count"].max()*1.18)
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    total = int(tdf["Count"].sum())
    nvl_cnt = int(tdf[tdf["Ticker"]=="NVL"]["Count"].iloc[0]) if "NVL" in tdf["Ticker"].values else 0
    vic_cnt = int(tdf[tdf["Ticker"]=="VIC"]["Count"].iloc[0]) if "VIC" in tdf["Ticker"].values else 0
    vhm_cnt = int(tdf[tdf["Ticker"]=="VHM"]["Count"].iloc[0]) if "VHM" in tdf["Ticker"].values else 0
    _save_chart(fig, f"{idx:02d}_ma_co_phieu_noi_bat.png", "M\u00e3 c\u1ed5 phi\u1ebfu n\u1ed5i b\u1eadt",
        "C\u1ed9t ngang: 17 m\u00e3 CP \u0111\u01b0\u1ee3c nh\u1eafc nhi\u1ec1u nh\u1ea5t trong 4.462 b\u00e0i b\u00e1o \u0111\u00e3 ph\u00e2n t\u00edch.",
        f"NVL d\u1eabn \u0111\u1ea7u ({nvl_cnt:,} l\u1ea7n, {nvl_cnt/total*100:.1f}%), VIC ({vic_cnt:,}), VHM ({vhm_cnt:,}). Top 3 chi\u1ebfm {tdf.iloc[-3:]['Count'].sum()/total*100:.1f}%. NVL v\u01b0\u1ee3t tr\u1ed9i nh\u1edd quy m\u00f4 d\u01b0 n\u1ee3 v\u00e0 t\u00e1i c\u1ea5u tr\u00fac li\u00ean t\u1ee5c \u0111\u01b0\u1ee3c b\u00e1o ch\u00ed nh\u1eafc \u0111\u1ebfn.",
        "barh", "NEWS_RAW.tickers",
        f"NVL d\u1eabn \u0111\u1ea7u: {nvl_cnt:,} l\u1ea7n ({nvl_cnt/total*100:.1f}%). Top 3 (NVL-VIC-VHM) chi\u1ebfm {tdf.iloc[-3:]['Count'].sum()/total*100:.1f}%",
        top1="NVL", top1_count=nvl_cnt, top2="VIC", top2_count=vic_cnt, top3="VHM", top3_count=vhm_cnt,
        total_mentions=total, unique_tickers=len(tdf))


# ─── CHART 05: Nguồn tin trúng mã CP ──────────────────────────────
def chart_05_source_match_rate(df_si, df_nr):
    idx = _next_idx()
    tot = df_si["Source"].value_counts()
    mat = df_nr["source"].value_counts()
    rd = pd.DataFrame({"total": tot, "matched": mat}).fillna(0).astype({"matched": int})
    rd["rate"] = (rd["matched"]/rd["total"]*100).round(2)
    rd = rd[rd["total"] >= 500].sort_values("rate", ascending=False).head(12)
    fig, ax1 = plt.subplots(figsize=(13, 6))
    x = np.arange(len(rd))
    bars = ax1.bar(x, rd["matched"].values, color="#3498DB", alpha=0.65, width=0.6, label="S\u1ed1 b\u00e0i tr\u00fang m\u00e3 CP")
    ax1.set_xticks(x); ax1.set_xticklabels(rd.index, rotation=45, ha="right", fontsize=8)
    ax1.set_xlabel("Ngu\u1ed3n tin"); ax1.set_ylabel("S\u1ed1 b\u00e0i tr\u00fang m\u00e3 CP", color="#3498DB")
    ax2 = ax1.twinx()
    ax2.plot(x, rd["rate"].values, "o-", color="#E74C3C", linewidth=2, markersize=7, zorder=5, label="T\u1ef7 l\u1ec7 tr\u00fang (%)")
    ax2.set_ylabel("T\u1ef7 l\u1ec7 tr\u00fang m\u00e3 CP (%)", color="#E74C3C")
    for i, (_, r) in enumerate(rd.iterrows()):
        ax1.text(i, r["matched"]+max(rd["matched"])*0.01, f"{r['rate']:.1f}%", ha="center", fontsize=7.5, color="#E74C3C", fontweight="bold")
    l1, la1 = ax1.get_legend_handles_labels(); l2, la2 = ax2.get_legend_handles_labels()
    ax1.legend(l1+l2, la1+la2, loc="upper left", fontsize=9)
    ax1.set_title("Ngu\u1ed3n tin c\u00f3 t\u1ef7 l\u1ec7 b\u00e0i tr\u00fang m\u00e3 c\u1ed5 phi\u1ebfu cao nh\u1ea5t", fontsize=15, fontweight="bold", pad=15)
    ax1.grid(axis="y", alpha=0.3, linestyle="--"); ax1.set_axisbelow(True)
    _save_chart(fig, f"{idx:02d}_nguon_tin_trung_ma_cp.png", "Ngu\u1ed3n tin tr\u00fang m\u00e3 CP",
        "K\u1ebft h\u1ee3p c\u1ed9t v\u00e0 \u0111\u01b0\u1eddng: s\u1ed1 b\u00e0i ph\u00f9 h\u1ee3p (c\u1ed9t) v\u00e0 t\u1ef7 l\u1ec7 ph\u00f9 h\u1ee3p (\u0111\u01b0\u1eddng) theo t\u1eebng ngu\u1ed3n tin.",
        f"Ngu\u1ed3n {rd.index[0]} c\u00f3 t\u1ef7 l\u1ec7 tr\u00fang cao nh\u1ea5t ({rd.iloc[0]['rate']:.1f}%). C\u00e1c ngu\u1ed3n chuy\u00ean B\u0110S v\u00e0 CK lu\u00f4n c\u00f3 t\u1ef7 l\u1ec7 tr\u00fang cao h\u01a1n ngu\u1ed3n t\u1ed5ng h\u1ee3p. T\u1ef7 l\u1ec7 trung b\u00ecnh chung: {len(df_nr)/len(df_si)*100:.2f}% (4.462/124.792).",
        "dual_axis", "SOURCE_INDEX.Status + NEWS_RAW.source",
        f"Ngu\u1ed3n {rd.index[0]} tr\u00fang cao nh\u1ea5t: {rd.iloc[0]['rate']:.1f}%. T\u1ef7 l\u1ec7 TB to\u00e0n h\u1ec7 th\u1ed1ng: {len(df_nr)/len(df_si)*100:.2f}%",
        top1_source=rd.index[0], top1_rate=float(rd.iloc[0]["rate"]), top1_matched=int(rd.iloc[0]["matched"]),
        system_avg_rate=round(len(df_nr)/len(df_si)*100, 2))


# ─── CHART 06: Xu hướng theo tháng (3-5 năm) ──────────────────────
def chart_06_monthly_trend(df_si):
    idx = _next_idx()
    df = df_si.copy()
    df["date"] = _parse_dates(df["Datetime Public"])
    df["year"] = df["date"].dt.year
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)
    df["month"] = df["date"].dt.month.astype(int)
    df = df[df["year"] >= 2022]
    df["ym"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)
    order = sorted(df["ym"].unique())
    mc = df["ym"].value_counts().reindex(order).fillna(0)

    fig, ax = plt.subplots(figsize=(15, 6))
    x = np.arange(len(mc))
    ax.fill_between(x, mc.values, alpha=0.12, color="#3498DB")
    ax.plot(x, mc.values, color="#2980B9", linewidth=1.8, marker="o", markersize=3.5)
    ma3 = mc.rolling(3, min_periods=1).mean()
    ax.plot(x, ma3.values, color="#E74C3C", linewidth=2.2, linestyle="-", label="TB tr\u01b0\u1ee3t 3 th\u00e1ng")

    tick_step = max(1, len(mc)//12)
    ax.set_xticks(x[::tick_step])
    ax.set_xticklabels([mc.index[i] for i in range(0, len(mc), tick_step)], rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("Th\u00e1ng"); ax.set_ylabel("S\u1ed1 b\u00e0i vi\u1ebft")
    ax.set_title("Xu h\u01b0\u1edbng s\u1ed1 l\u01b0\u1ee3ng b\u00e0i vi\u1ebft theo th\u00e1ng (2022-2026)",
                 fontsize=15, fontweight="bold", pad=15)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.axhline(mc.mean(), color="#2C3E50", linestyle=":", linewidth=1, alpha=0.5, label=f"TB: {mc.mean():,.0f}/th\u00e1ng")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.3, linestyle="--"); ax.set_axisbelow(True)

    growth_24 = (mc.loc[[m for m in mc.index if m.startswith("2025")]].sum() - mc.loc[[m for m in mc.index if m.startswith("2024")]].sum())/mc.loc[[m for m in mc.index if m.startswith("2024")]].sum()*100 if any(m.startswith("2024") for m in mc.index) and any(m.startswith("2025") for m in mc.index) else 0

    _save_chart(fig, f"{idx:02d}_xu_huong_theo_thang.png", "Xu h\u01b0\u1edbng theo th\u00e1ng",
        "\u0110\u01b0\u1eddng line: xu h\u01b0\u1edbng s\u1ed1 b\u00e0i theo th\u00e1ng t\u1eeb 2022 \u0111\u1ebfn nay, k\u00e8m \u0111\u01b0\u1eddng trung b\u00ecnh tr\u01b0\u1ee3t 3 th\u00e1ng (MA3) v\u00e0 \u0111\u01b0\u1eddng trung b\u00ecnh t\u1ed5ng th\u1ec3.",
        f"T\u1ed5ng s\u1ed1 b\u00e0i 2022-2026: {int(mc.sum()):,}. T\u0103ng tr\u01b0\u1edfng 2024-2025: {growth_24:.0f}%. Xu h\u01b0\u1edbng t\u0103ng m\u1ea1nh t\u1eeb \u0111\u1ea7u 2024, duy tr\u00ec \u1ed5n \u0111\u1ecbnh \u1edf m\u1ee9c cao n\u0103m 2025-2026. Trung b\u00ecnh {mc.mean():,.0f} b\u00e0i/th\u00e1ng.",
        "line", "SOURCE_INDEX.Datetime Public",
        f"T\u0103ng tr\u01b0\u1edfng 2024-2025: {growth_24:.0f}%. TB {mc.mean():,.0f} b\u00e0i/th\u00e1ng",
        growth_rate=round(growth_24, 1), monthly_avg=int(mc.mean()),
        year_range=[2022, 2026], total_months=len(mc))


# ─── CHART 07: Ma trận nguồn × mã CP ──────────────────────────────
def chart_07_source_ticker_heatmap(df_nr):
    idx = _next_idx()
    ts = defaultdict(lambda: defaultdict(int))
    for _, row in df_nr.iterrows():
        for t in str(row["tickers"]).replace(" ", "").split(","):
            if t.strip(): ts[t.strip()][str(row["source"])] += 1
    top_ticks = ["NVL","VIC","VHM","DXG","VRE","CTD","PDR","NLG","HHV","KBC"]
    top_srcs = sorted(set(s for t in top_ticks for s in ts.get(t,{})),
                      key=lambda s: sum(ts[t].get(s,0) for t in top_ticks), reverse=True)[:8]
    hm = pd.DataFrame([[ts[t].get(s,0) for s in top_srcs] for t in top_ticks],
                      index=top_ticks, columns=top_srcs)
    fig, ax = plt.subplots(figsize=(13, 8))
    sns.heatmap(hm, annot=True, fmt="d", cmap="YlOrRd", linewidths=0.5, linecolor="white",
                cbar_kws={"label": "S\u1ed1 l\u1ea7n xu\u1ea5t hi\u1ec7n"}, ax=ax, annot_kws={"fontsize": 8})
    ax.set_title("Ngu\u1ed3n tin n\u00e0o th\u01b0\u1eddng nh\u1eafc \u0111\u1ebfn m\u00e3 c\u1ed5 phi\u1ebfu n\u00e0o?",
                 fontsize=15, fontweight="bold", pad=15)
    ax.set_xlabel("Ngu\u1ed3n tin", fontsize=11); ax.set_ylabel("M\u00e3 c\u1ed5 phi\u1ebfu", fontsize=11)
    plt.yticks(rotation=0); plt.xticks(rotation=30, ha="right")
    _save_chart(fig, f"{idx:02d}_ma_tran_nguon_ma_cp.png", "Ma tr\u1eadn ngu\u1ed3n v\u00e0 m\u00e3 CP",
        "Heatmap: th\u1ec3 hi\u1ec7n ngu\u1ed3n tin n\u00e0o th\u01b0\u1eddng \u0111\u01b0a tin v\u1ec1 m\u00e3 c\u1ed5 phi\u1ebfu n\u00e0o. M\u00e0u c\u00e0ng \u0111\u1eadm = t\u1ea7n su\u1ea5t c\u00e0ng cao.",
        "NVL xu\u1ea5t hi\u1ec7n d\u00e0y \u0111\u1eb7c \u1edf h\u1ea7u h\u1ebft ngu\u1ed3n, \u0111\u1eb7c bi\u1ec7t CafeBiz B\u0110S v\u00e0 CafeF DN. CafeBiz B\u0110S l\u00e0 ngu\u1ed3n duy nh\u1ea5t bao ph\u1ee7 t\u1ed1t c\u1ea3 10 m\u00e3. CafeF TC thi\u00ean v\u1ec1 VIC-VHM, CafeBiz CK thi\u00ean v\u1ec1 DXG-VRE.",
        "heatmap", "NEWS_RAW.tickers + source",
        "NVL \u0111\u01b0\u1ee3c nh\u1eafc nhi\u1ec1u nh\u1ea5t \u1edf h\u1ea7u h\u1ebft ngu\u1ed3n. CafeBiz B\u0110S bao ph\u1ee7 t\u1ed1t nh\u1ea5t 10 m\u00e3 CP.")


# ─── CHART 08: Phễu crawl tổng quan ───────────────────────────────
def chart_08_crawl_funnel(df_si, df_nr):
    idx = _next_idx()
    total_links = len(df_si)
    mentioned = len(df_si[df_si["Status"] == "mentioned"]) if "Status" in df_si.columns else len(df_nr)
    enriched_ok = len(df_nr[df_nr["crawl_status"] == "success"]) if "crawl_status" in df_nr.columns else len(df_nr)
    failed_cnt = len(df_nr[df_nr["crawl_status"] == "failed"]) if "crawl_status" in df_nr.columns else 0

    stages = [
        ("T\u1ed5ng s\u1ed1 link \u0111\u00e3 crawl", total_links, f"96 RSS + 22 API"),
        ("B\u00e0i tr\u00fang m\u00e3 c\u1ed5 phi\u1ebfu", mentioned, f"{(mentioned/total_links*100):.2f}%"),
        ("T\u1ea3i n\u1ed9i dung th\u00e0nh c\u00f4ng", enriched_ok, f"{(enriched_ok/mentioned*100):.1f}%"),
    ]
    labels = [s[0] for s in stages]
    values = [s[1] for s in stages]
    details = [s[2] for s in stages]
    colors_bar = ["#3498DB", "#E74C3C", "#2ECC71"]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    bar_width = 0.6
    positions = np.arange(len(stages))
    bars = ax.barh(positions, values, height=bar_width, color=colors_bar, edgecolor="white", linewidth=1)

    max_val = max(values)
    ax.barh(positions, values, height=bar_width, color=colors_bar, edgecolor="white", linewidth=1)

    for i, (bar, val, label, detail) in enumerate(zip(bars, values, labels, details)):
        ax.text(bar.get_width() + max_val*0.01, bar.get_y() + bar.get_height()/2,
                f"{val:,}", va="center", fontsize=13, fontweight="bold", color="#2C3E50")
        ax.text(bar.get_width() + max_val*0.01, bar.get_y() + bar.get_height()/2 - 0.22,
                detail, va="top", fontsize=8, color="#7F8C8D")

    # Arrow connections
    for i in range(len(stages)-1):
        y_pos = (positions[i] + positions[i+1]) / 2
        ax.annotate("", xy=(values[i+1]*0.98, positions[i+1]), xytext=(values[i]*0.98, positions[i]),
                    arrowprops=dict(arrowstyle="->", color="#BDC3C7", lw=2))

    # Retention rate on arrows
    ret_1_2 = mentioned/total_links*100
    ret_2_3 = enriched_ok/mentioned*100
    ax.text(values[0]*0.5, positions[0]-0.5, f"Gi\u1eef l\u1ea1i: {ret_1_2:.1f}%",
            ha="center", fontsize=8, color="#E74C3C", fontweight="bold")
    ax.text(values[1]*0.5, positions[1]-0.5, f"Gi\u1eef l\u1ea1i: {ret_2_3:.1f}%",
            ha="center", fontsize=8, color="#2ECC71", fontweight="bold")

    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, max_val*1.25)
    ax.set_title("T\u1ed5ng quan Pipeline: T\u1eeb crawl \u0111\u1ebfn ph\u00e2n t\u00edch n\u1ed9i dung",
                 fontsize=15, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="x", alpha=0.3, linestyle="--"); ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)

    _save_chart(fig, f"{idx:02d}_phieu_crawl_tong_quan.png", "Ph\u1ec5u crawl t\u1ed5ng quan",
        "Bi\u1ec3u \u0111\u1ed3 ph\u1ec5u: tr\u1ef1c quan h\u00f3a lu\u1ed3ng d\u1eef li\u1ec7u t\u1eeb crawl link -> l\u1ecdc theo m\u00e3 CP -> t\u1ea3i n\u1ed9i dung th\u00e0nh c\u00f4ng. T\u1ef7 l\u1ec7 gi\u1eef l\u1ea1i qua m\u1ed7i giai \u0111o\u1ea1n cho th\u1ea5y hi\u1ec7u qu\u1ea3 pipeline.",
        f"Pipeline: {total_links:,} links \u2192 {mentioned:,} tr\u00fang m\u00e3 CP ({ret_1_2:.1f}%) \u2192 {enriched_ok:,} t\u1ea3i th\u00e0nh c\u00f4ng ({ret_2_3:.1f}%). Ch\u1ec9 {failed_cnt} b\u00e0i th\u1ea5t b\u1ea1i. H\u1ec7 th\u1ed1ng ho\u1ea1t \u0111\u1ed9ng hi\u1ec7u qu\u1ea3 cao.",
        "funnel", "SOURCE_INDEX.Status + NEWS_RAW.crawl_status",
        f"{total_links:,} links \u2192 {mentioned:,} tr\u00fang CP ({ret_1_2:.1f}%) \u2192 {enriched_ok:,} t\u1ea3i OK ({ret_2_3:.1f}%)",
        total_links=int(total_links), matched=int(mentioned), enriched_ok=int(enriched_ok),
        retention_1=round(ret_1_2, 1), retention_2=round(ret_2_3, 1),
        failed=int(failed_cnt))


def generate_statistic_json(df_si, df_nr, df_ci, df_sl):
    print("\nGenerating statistic.json...")
    total_links = len(df_si)
    dates = _parse_dates(df_si["Datetime Public"])
    date_min, date_max = dates.min(), dates.max()

    ticker_counts = Counter()
    for t_str in df_nr["tickers"].dropna():
        for t in str(t_str).replace(" ", "").split(","):
            if t: ticker_counts[t.strip()] += 1
    status_counts = df_si["Status"].value_counts().to_dict()
    total_rss = df_si[df_si["Source"].str.startswith("RSS", na=False)].shape[0]
    total_api = df_si[df_si["Source"].str.startswith("API", na=False)].shape[0]

    companies = []
    ticker_col = next((c for c in df_ci.columns if "M\u00e3" in c), None)
    name_col = next((c for c in df_ci.columns if "T\u00ean \u0111\u1ea7" in c or "t\u00ean" in c.lower()), None)
    exchange_col = next((c for c in df_ci.columns if "S\u00e0n" in c), None)
    industry_col = next((c for c in df_ci.columns if "Ng\u00e0nh" in c), None)
    if ticker_col:
        for _, row in df_ci.iterrows():
            companies.append({
                "ticker": row[ticker_col], "name": row.get(name_col, ""),
                "exchange": row.get(exchange_col, ""), "industry": row.get(industry_col, ""),
            })

    source_types = {}
    type_col = next((c for c in df_sl.columns if "Lo\u1ea1i" in c), None)
    if type_col:
        source_types = df_sl[type_col].value_counts().to_dict()

    matched_status = status_counts.get("mentioned", 0)
    new_status = status_counts.get("new", 0)
    failed_status = status_counts.get("failed", 0)
    enriched_ok = len(df_nr[df_nr["crawl_status"]=="success"]) if "crawl_status" in df_nr.columns else 0
    enriched_fail = len(df_nr[df_nr["crawl_status"]=="failed"]) if "crawl_status" in df_nr.columns else 0

    stat = {
        "project": "DA2 - Crawl tin t\u1ee9c B\u0110S & CK",
        "generated_at": "2026-06-06",
        "data_source": "K4_CRAWL_NHOM_2_BAT_DONG_SAN_XAY_DUNG_KCN.xlsx",
        "sheets": 10,
        "overview": {
            "total_links_crawled": int(total_links),
            "total_articles_enriched": int(len(df_nr)),
            "enrichment_rate_pct": round(len(df_nr)/total_links*100, 2),
            "date_range": {"from": str(date_min.date()), "to": str(date_max.date()),
                           "total_days": int((date_max-date_min).days)},
        },
        "sources": {
            "total_unique_source_channels": int(df_si["Source"].nunique()),
            "by_type": {str(k): int(v) for k, v in source_types.items()},
            "rss_feeds": int(total_rss),
            "api_zones": int(total_api),
            "rss_pct": round(total_rss/total_links*100, 1),
            "api_pct": round(total_api/total_links*100, 1),
        },
        "categories": {
            "total_categories": int(df_si["Category"].nunique()),
            "by_category": {
                str(k): {"count": int(v), "pct": round(v/total_links*100, 1)}
                for k, v in sorted(df_si["Category"].value_counts().to_dict().items(), key=lambda x: -x[1])
            },
        },
        "articles_pipeline": {
            "stage_1_links_crawled": int(total_links),
            "stage_2_title_matched": int(matched_status),
            "stage_3_content_fetched_ok": int(enriched_ok),
            "stage_4_content_failed": int(enriched_fail),
            "retention_rate_1_to_2_pct": round(matched_status/total_links*100, 2),
            "retention_rate_2_to_3_pct": round(enriched_ok/matched_status*100, 1) if matched_status else 0,
            "status_breakdown": {
                "new_unprocessed": int(new_status), "mentioned": int(matched_status), "failed": int(failed_status),
            },
        },
        "companies_and_tickers": {
            "total_companies": len(companies),
            "companies": companies,
            "ticker_mentions": {str(k): int(v) for k, v in sorted(ticker_counts.items(), key=lambda x: -x[1])},
            "top_3_tickers": [
                {"ticker": t, "count": int(c)} for t, c in ticker_counts.most_common(3)
            ],
            "ticker_diversity": len(ticker_counts),
        },
        "industry_coverage": {
            "total_industry_groups": int(df_nr["industry_group"].nunique()) if "industry_group" in df_nr.columns else 0,
            "groups": sorted(df_nr["industry_group"].value_counts().to_dict().items(), key=lambda x: -x[1])[:10] if "industry_group" in df_nr.columns else [],
            "domains_covered": [
                "B\u1ea5t \u0111\u1ed9ng s\u1ea3n",
                "X\u00e2y d\u1ef1ng",
                "Khu c\u00f4ng nghi\u1ec7p",
            ],
        },
    }
    path = os.path.join(REPORT_DIR, "statistic.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(stat, f, ensure_ascii=False, indent=2)
    print(f"  Saved: statistic.json ({os.path.getsize(path)/1024:.0f} KB)")


def main():
    print("="*60)
    print("DA2 Chart Generator v3 - 8 Quality Charts")
    print("="*60)
    dfs = load_data()
    si, nr, ci, sl = dfs["SOURCE_INDEX"], dfs["NEWS_RAW"], dfs["COMPANY_INFO"], dfs["SOURCE_LIST"]

    for f in os.listdir(REPORT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(REPORT_DIR, f))
            print(f"Removed old: {f}")

    print("\n"+"="*60+"\nGenerating 8 charts...\n"+"="*60)
    global CHART_INDEX; CHART_INDEX = 0

    chart_01_top_sources(si)
    chart_02_articles_by_year(si)
    chart_03_category_distribution(si)
    chart_04_ticker_mentions(nr)
    chart_05_source_match_rate(si, nr)
    chart_06_monthly_trend(si)
    chart_07_source_ticker_heatmap(nr)
    chart_08_crawl_funnel(si, nr)

    print(f"\n{'='*60}\nSaving chart.json...")
    with open(os.path.join(REPORT_DIR, "chart.json"), "w", encoding="utf-8") as f:
        json.dump(CHARTS_META, f, ensure_ascii=False, indent=2)

    generate_statistic_json(si, nr, ci, sl)

    total_kb = sum(c["file_size_kb"] for c in CHARTS_META)
    print(f"\nDone! {len(CHARTS_META)} charts ({total_kb:.0f} KB total)")
    for c in CHARTS_META:
        print(f"  {c['path'].split('/')[-1]:40s} {c['chart_type']:15s} {c['file_size_kb']:>5.1f}KB  {c['name']}")


if __name__ == "__main__":
    main()
