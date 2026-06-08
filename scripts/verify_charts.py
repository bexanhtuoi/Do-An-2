import json

with open("data/report/chart.json", "r", encoding="utf-8") as f:
    charts = json.load(f)

print(f"{'#':>2} | {'Filename':35s} | {'Type':15s} | {'Size':>6s} | {'Name':25s}")
print("-" * 90)
for i, c in enumerate(charts):
    fn = c["path"].split("/")[-1]
    print(f"{i+1:2d} | {fn:35s} | {c['chart_type']:15s} | {c['file_size_kb']:>5.1f}KB | {c['name']:25s}")

total_kb = sum(c["file_size_kb"] for c in charts)
print("-" * 90)
print(f"Total: {len(charts)} charts, {total_kb:.0f} KB")

print("\n=== CHART TYPES ===")
types = {}
for c in charts:
    types[c["chart_type"]] = types.get(c["chart_type"], 0) + 1
for t, n in sorted(types.items(), key=lambda x: -x[1]):
    print(f"  {t:20s}: {n}")
