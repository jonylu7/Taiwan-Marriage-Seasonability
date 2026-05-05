"""
Taiwan Marriage Seasonality Analysis
Data: MOI Table 1.2 - Monthly marriage registrations, 2000-2025
"""

import re
import statistics
import xlrd
from python_calamine import CalamineWorkbook

DATA_OLD = "data/m1-02_2000-2016.xls"
DATA_NEW = "data/m1-02_2017-2026.xlsx"

MONTH_ZH = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,
            '七':7,'八':8,'九':9,'十':10}
MONTH_LABELS = ['1月','2月','3月','4月','5月','6月',
                '7月','8月','9月','10月','11月','12月']


def parse_month(label):
    if '十一月' in label: return 11
    if '十二月' in label: return 12
    if '十月'   in label: return 10
    return next((n for ch, n in MONTH_ZH.items() if label.lstrip().startswith(ch)), None)


def load_old(path):
    wb = xlrd.open_workbook(path)
    sh = wb.sheet_by_index(0)
    records, current_year = [], None
    for i in range(6, sh.nrows):
        label = str(sh.cell_value(i, 0)).strip()
        val   = sh.cell_value(i, 15)
        if not label or not val:
            continue
        if re.search(r'\d{4}', label) and '年' in label and '月' not in label:
            current_year = int(re.search(r'(\d{4})', label).group(1))
        elif '月' in label and current_year:
            m = parse_month(label)
            if m:
                records.append((current_year, m, int(val)))
    return records


def load_new(path, from_year=2017):
    wb = CalamineWorkbook.from_path(path)
    ws = wb.get_sheet_by_name('年月monthly')
    records, current_year = [], None
    for row in ws.to_python():
        label = str(row[0]).strip() if row[0] else ''
        val   = row[15] if len(row) > 15 else None
        if not label or not val:
            continue
        if re.search(r'\d{4}', label) and '年' in label and '月' not in label:
            current_year = int(re.search(r'(\d{4})', label).group(1))
        elif '月' in label and current_year and current_year >= from_year:
            m = parse_month(label)
            if m:
                records.append((current_year, m, int(val)))
    return records


def skewness(data):
    n, mu, s = len(data), statistics.mean(data), statistics.stdev(data)
    return sum(((x - mu) / s) ** 3 for x in data) * n / ((n-1) * (n-2))


def kurtosis(data):
    n, mu, s = len(data), statistics.mean(data), statistics.stdev(data)
    k = sum(((x - mu) / s) ** 4 for x in data) * n*(n+1) / ((n-1)*(n-2)*(n-3))
    return k - 3*(n-1)**2 / ((n-2)*(n-3))


def main():
    records = sorted(load_old(DATA_OLD) + load_new(DATA_NEW))
    records = [(y, m, v) for y, m, v in records if y <= 2025]
    print(f"Records loaded: {len(records)}  ({records[0][0]}–{records[-1][0]})")

    all_vals   = [v for _, _, v in records]
    grand_mean = statistics.mean(all_vals)

    # ── Monthly descriptive statistics ──────────────────────────────────────
    print("\n" + "="*95)
    print(f"{'月份':<8}{'平均':>9}{'中位數':>9}{'標準差':>9}{'最小':>9}{'最大':>9}{'CV%':>8}{'偏態':>8}{'峰態':>8}{'季節指數':>10}")
    print("="*95)
    monthly = {}
    for m in range(1, 13):
        vals = [v for _, mo, v in records if mo == m]
        avg  = statistics.mean(vals)
        med  = statistics.median(vals)
        std  = statistics.stdev(vals)
        cv   = std / avg * 100
        skew = skewness(vals)
        kurt = kurtosis(vals)
        idx  = avg / grand_mean
        monthly[m] = dict(avg=avg, med=med, std=std, min=min(vals),
                          max=max(vals), cv=cv, skew=skew, kurt=kurt, idx=idx)
        print(f"{MONTH_LABELS[m-1]:<8}{avg:>9,.0f}{med:>9,.0f}{std:>9,.0f}"
              f"{min(vals):>9,.0f}{max(vals):>9,.0f}{cv:>7.1f}%"
              f"{skew:>+8.3f}{kurt:>+8.3f}{idx:>10.3f}")
    print("="*95)

    peak   = max(monthly, key=lambda x: monthly[x]['avg'])
    trough = min(monthly, key=lambda x: monthly[x]['avg'])
    print(f"\n最高月: {peak}月  (avg {monthly[peak]['avg']:,.0f}，idx {monthly[peak]['idx']:.3f})")
    print(f"最低月: {trough}月  (avg {monthly[trough]['avg']:,.0f}，idx {monthly[trough]['idx']:.3f})")

    # ── Seasonal index bar chart (text) ──────────────────────────────────────
    print("\n── 季節指數 ──")
    for m in range(1, 13):
        idx = monthly[m]['idx']
        bar = '█' * int(idx * 20)
        marker = ' ◀ 最高' if m == peak else (' ◀ 最低' if m == trough else '')
        print(f"  {MONTH_LABELS[m-1]:5s}  {idx:.3f}  {bar}{marker}")

    # ── Annual trend ──────────────────────────────────────────────────────────
    print("\n── 年度結婚對數 ──")
    for y in range(2000, 2026):
        total = sum(v for yr, _, v in records if yr == y)
        bar   = '▓' * (total // 5000)
        print(f"  {y}: {total:>7,}  {bar}")

    # ── Monthly share ─────────────────────────────────────────────────────────
    avg_annual = statistics.mean(
        [sum(v for yr, _, v in records if yr == y) for y in range(2000, 2026)]
    )
    print(f"\n── 各月占全年比例  (年均結婚對數 {avg_annual:,.0f}) ──")
    for m in range(1, 13):
        share = monthly[m]['avg'] / avg_annual * 100
        print(f"  {MONTH_LABELS[m-1]:5s}: {share:.1f}%")


if __name__ == "__main__":
    main()
