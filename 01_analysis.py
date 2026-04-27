"""
PRYZM Solutions — Data Quality Assessment
UCI Online Retail II Dataset
Author: Ahmed Maala
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os
import json

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# 0. Setup
# ─────────────────────────────────────────
OUTPUT_DIR = "/home/ubuntu/pryzm-internship/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'figure.dpi': 150,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

PRYZM_BLUE  = '#1A3C5E'
PRYZM_TEAL  = '#2E9E8F'
PRYZM_AMBER = '#F5A623'
PRYZM_RED   = '#E74C3C'
PRYZM_GREY  = '#BDC3C7'

# ─────────────────────────────────────────
# 1. Load Dataset
# ─────────────────────────────────────────
print("⏳  Loading UCI Online Retail II …")
try:
    from ucimlrepo import fetch_ucirepo
    retail = fetch_ucirepo(id=502)
    df_raw = retail.data.original
    print(f"✅  Loaded via ucimlrepo: {df_raw.shape}")
except Exception as e:
    print(f"ucimlrepo failed ({e}), trying direct download …")
    url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
    import urllib.request, zipfile, io
    with urllib.request.urlopen(url, timeout=120) as r:
        zf = zipfile.ZipFile(io.BytesIO(r.read()))
    xlsx_name = [n for n in zf.namelist() if n.endswith('.xlsx')][0]
    with zf.open(xlsx_name) as f:
        df_y1 = pd.read_excel(f, sheet_name='Year 2009-2010')
        df_y2 = pd.read_excel(f, sheet_name='Year 2010-2011')
    df_raw = pd.concat([df_y1, df_y2], ignore_index=True)
    print(f"✅  Loaded via direct download: {df_raw.shape}")

# Standardise column names
df_raw.columns = [c.strip().replace(' ', '_') for c in df_raw.columns]
print("Columns:", df_raw.columns.tolist())

# ─────────────────────────────────────────
# 2. Basic Structure
# ─────────────────────────────────────────
total_rows = len(df_raw)
total_cols = len(df_raw.columns)
print(f"\n📊  Shape: {total_rows:,} rows × {total_cols} columns")
print(df_raw.dtypes)

# ─────────────────────────────────────────
# 3. Missing Values
# ─────────────────────────────────────────
missing = df_raw.isnull().sum()
missing_pct = (missing / total_rows * 100).round(2)
missing_df = pd.DataFrame({'Missing_Count': missing, 'Missing_%': missing_pct})
print("\n🔍  Missing Values:\n", missing_df[missing_df['Missing_Count'] > 0])

# ─────────────────────────────────────────
# 4. Duplicates
# ─────────────────────────────────────────
dup_count = df_raw.duplicated().sum()
dup_pct   = round(dup_count / total_rows * 100, 2)
print(f"\n🔁  Duplicates: {dup_count:,} ({dup_pct}%)")

# ─────────────────────────────────────────
# 5. Cancellations
# ─────────────────────────────────────────
invoice_col = [c for c in df_raw.columns if 'invoice' in c.lower()][0]
cancel_mask = df_raw[invoice_col].astype(str).str.startswith('C')
cancel_count = cancel_mask.sum()
cancel_pct   = round(cancel_count / total_rows * 100, 2)
print(f"\n❌  Cancellations: {cancel_count:,} ({cancel_pct}%)")

# ─────────────────────────────────────────
# 6. Negative / Zero Prices & Quantities
# ─────────────────────────────────────────
price_col = [c for c in df_raw.columns if 'price' in c.lower()][0]
qty_col   = [c for c in df_raw.columns if 'quant' in c.lower() or 'qty' in c.lower()][0]

neg_price  = (df_raw[price_col] < 0).sum()
zero_price = (df_raw[price_col] == 0).sum()
neg_qty    = (df_raw[qty_col] < 0).sum()
zero_qty   = (df_raw[qty_col] == 0).sum()

print(f"\n💰  Negative prices: {neg_price:,}  |  Zero prices: {zero_price:,}")
print(f"📦  Negative quantities: {neg_qty:,}  |  Zero quantities: {zero_qty:,}")

# ─────────────────────────────────────────
# 7. Inconsistent StockCodes
# ─────────────────────────────────────────
stock_col = [c for c in df_raw.columns if 'stock' in c.lower()][0]
std_pattern = df_raw[stock_col].astype(str).str.match(r'^\d{5}[A-Z]?$')
non_std_codes = df_raw[~std_pattern][stock_col].value_counts().head(15)
non_std_count = (~std_pattern).sum()
non_std_pct   = round(non_std_count / total_rows * 100, 2)
print(f"\n🏷️   Non-standard StockCodes: {non_std_count:,} ({non_std_pct}%)")
print(non_std_codes)

# ─────────────────────────────────────────
# 8. Country distribution
# ─────────────────────────────────────────
country_col = [c for c in df_raw.columns if 'country' in c.lower()][0]
country_dist = df_raw[country_col].value_counts().head(12)

# ─────────────────────────────────────────
# 9. Time distribution
# ─────────────────────────────────────────
date_col = [c for c in df_raw.columns if 'invoicedate' in c.lower() or 'date' in c.lower()][0]
df_raw[date_col] = pd.to_datetime(df_raw[date_col], errors='coerce')
df_raw['YearMonth'] = df_raw[date_col].dt.to_period('M')
monthly_counts = df_raw.groupby('YearMonth').size()

# ─────────────────────────────────────────
# 10. Save stats JSON for report
# ─────────────────────────────────────────
stats = {
    "total_rows": int(total_rows),
    "total_cols": int(total_cols),
    "dup_count": int(dup_count),
    "dup_pct": float(dup_pct),
    "cancel_count": int(cancel_count),
    "cancel_pct": float(cancel_pct),
    "missing_customer_id_count": int(missing.get('Customer_ID', missing.get('CustomerID', 0))),
    "missing_customer_id_pct": float(missing_pct.get('Customer_ID', missing_pct.get('CustomerID', 0))),
    "missing_description_count": int(missing.get('Description', 0)),
    "missing_description_pct": float(missing_pct.get('Description', 0)),
    "neg_price": int(neg_price),
    "zero_price": int(zero_price),
    "neg_qty": int(neg_qty),
    "zero_qty": int(zero_qty),
    "non_std_codes": int(non_std_count),
    "non_std_pct": float(non_std_pct),
    "invoice_col": invoice_col,
    "price_col": price_col,
    "qty_col": qty_col,
    "stock_col": stock_col,
    "country_col": country_col,
    "date_col": date_col,
}
with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print("\n✅  Stats saved.")

# ─────────────────────────────────────────
# 11. FIGURE 1 — Data Quality Overview (horizontal bar)
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

issues = {
    'Missing\nCustomer IDs': stats['missing_customer_id_pct'],
    'Cancellation\nRecords': stats['cancel_pct'],
    'Non-standard\nStock Codes': stats['non_std_pct'],
    'Duplicate\nRows': stats['dup_pct'],
    'Zero-price\nEntries': round(zero_price / total_rows * 100, 2),
    'Negative\nQuantities': round(neg_qty / total_rows * 100, 2),
}

colors = [PRYZM_RED if v > 10 else PRYZM_AMBER if v > 2 else PRYZM_TEAL
          for v in issues.values()]

bars = ax.barh(list(issues.keys()), list(issues.values()), color=colors,
               height=0.55, edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, issues.values()):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            f'{val:.1f}%', va='center', fontsize=10, color='#333')

ax.set_xlabel('Percentage of Total Records (%)', labelpad=8)
ax.set_title('Data Quality Issues — UCI Online Retail II\n(~540 K records, 2009–2011)',
             pad=12, color=PRYZM_BLUE)
ax.set_xlim(0, max(issues.values()) * 1.25)

legend_patches = [
    mpatches.Patch(color=PRYZM_RED,   label='Critical  (>10%)'),
    mpatches.Patch(color=PRYZM_AMBER, label='Warning  (2–10%)'),
    mpatches.Patch(color=PRYZM_TEAL,  label='Minor    (<2%)'),
]
ax.legend(handles=legend_patches, loc='lower right', fontsize=9,
          framealpha=0.9, edgecolor=PRYZM_GREY)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/fig1_quality_overview.png", bbox_inches='tight')
plt.close()
print("✅  Fig 1 saved.")

# ─────────────────────────────────────────
# 12. FIGURE 2 — Monthly Transaction Volume
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 4))

months = [str(p) for p in monthly_counts.index]
values = monthly_counts.values

ax.fill_between(range(len(months)), values, alpha=0.18, color=PRYZM_TEAL)
ax.plot(range(len(months)), values, color=PRYZM_TEAL, linewidth=2.2, marker='o',
        markersize=4)

step = max(1, len(months) // 10)
ax.set_xticks(range(0, len(months), step))
ax.set_xticklabels([months[i] for i in range(0, len(months), step)],
                   rotation=35, ha='right', fontsize=9)
ax.set_ylabel('Number of Transactions')
ax.set_title('Monthly Transaction Volume — 2009 to 2011', pad=10, color=PRYZM_BLUE)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/fig2_monthly_volume.png", bbox_inches='tight')
plt.close()
print("✅  Fig 2 saved.")

# ─────────────────────────────────────────
# 13. FIGURE 3 — Top Countries by Transactions
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))

top_countries = country_dist.head(10)
palette = [PRYZM_BLUE if i == 0 else PRYZM_TEAL if i < 4 else PRYZM_GREY
           for i in range(len(top_countries))]

bars = ax.bar(top_countries.index, top_countries.values, color=palette,
              edgecolor='white', linewidth=0.5)

for bar, val in zip(bars, top_countries.values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 500,
            f'{val:,}', ha='center', va='bottom', fontsize=8.5)

ax.set_ylabel('Number of Transactions')
ax.set_title('Top 10 Countries by Transaction Volume', pad=10, color=PRYZM_BLUE)
ax.set_xticklabels(top_countries.index, rotation=30, ha='right')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/fig3_top_countries.png", bbox_inches='tight')
plt.close()
print("✅  Fig 3 saved.")

# ─────────────────────────────────────────
# 14. FIGURE 4 — Missing Values Heatmap
# ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 3.5))

sample = df_raw.sample(min(5000, len(df_raw)), random_state=42)
missing_matrix = sample.isnull().astype(int)

sns.heatmap(missing_matrix.T, ax=ax, cmap=['#F0F4F8', PRYZM_RED],
            cbar=False, linewidths=0, yticklabels=True, xticklabels=False)

ax.set_title('Missing Value Pattern — Random Sample of 5,000 Records',
             pad=10, color=PRYZM_BLUE)
ax.set_xlabel('Records (sampled)', labelpad=6)
ax.set_ylabel('')

present_patch = mpatches.Patch(color='#F0F4F8', label='Present')
missing_patch = mpatches.Patch(color=PRYZM_RED,   label='Missing')
ax.legend(handles=[present_patch, missing_patch], loc='upper right',
          fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/fig4_missing_heatmap.png", bbox_inches='tight')
plt.close()
print("✅  Fig 4 saved.")

print("\n🎉  All analysis complete. Outputs in:", OUTPUT_DIR)
