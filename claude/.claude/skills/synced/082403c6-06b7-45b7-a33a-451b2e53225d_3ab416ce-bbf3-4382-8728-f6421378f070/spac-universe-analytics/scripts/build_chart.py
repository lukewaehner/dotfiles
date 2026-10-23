#!/usr/bin/env python3
"""
build_chart.py — standard chart renderer for spac-universe-analytics.

Produces a fast, consistent static PNG chart from a ranked result set.
Two shapes are supported:

  ranking   one bar per category, sorted descending (top-N)
  by_period one small-multiple / grouped panel per period (e.g. per year),
            each panel showing that period's top-N categories

Usage:
  python build_chart.py --input data.csv --category-col director --value-col total_spacs \
      --shape ranking --title "Directors by number of SPACs" --output chart.png --top-n 15

  python build_chart.py --input data.csv --category-col director --value-col spacs_that_year \
      --period-col ipo_year --shape by_period --title "Directors by SPACs, by IPO year" \
      --output chart.png --top-n 5 --max-periods 8

Input CSV must have a header row. This script has no network/DB access —
run the universe-query SQL first, save the result to CSV, then call this.
"""
import argparse
import csv
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# A small, colorblind-safe categorical palette. Swap freely, but keep it
# consistent across a single chart so repeat categories read the same way.
PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2",
           "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]


def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def render_ranking(rows, category_col, value_col, title, output, top_n):
    rows = sorted(rows, key=lambda r: to_float(r[value_col]), reverse=True)[:top_n]
    rows = list(reversed(rows))  # so the top item plots at the top of a barh
    labels = [r[category_col] for r in rows]
    values = [to_float(r[value_col]) for r in rows]

    fig_height = max(3, 0.35 * len(labels) + 1.2)
    fig, ax = plt.subplots(figsize=(9, fig_height), dpi=150)
    bars = ax.barh(labels, values, color=PALETTE[0])
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_xlabel(value_col.replace("_", " "))
    ax.set_title(title, fontsize=13, fontweight="bold", loc="left")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output)
    print(f"wrote {output} ({len(labels)} bars)")


def render_by_period(rows, category_col, value_col, period_col, title, output,
                      top_n, max_periods):
    periods = sorted({r[period_col] for r in rows if r[period_col]})
    if max_periods and len(periods) > max_periods:
        periods = periods[-max_periods:]  # keep the most recent periods

    n = len(periods)
    ncols = min(4, n) or 1
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.2 * ncols, 3.2 * nrows), dpi=150)
    axes = axes.flatten() if n > 1 else [axes]

    for i, period in enumerate(periods):
        period_rows = [r for r in rows if r[period_col] == period]
        period_rows = sorted(period_rows, key=lambda r: to_float(r[value_col]), reverse=True)[:top_n]
        period_rows = list(reversed(period_rows))
        labels = [r[category_col] for r in period_rows]
        values = [to_float(r[value_col]) for r in period_rows]
        ax = axes[i]
        ax.barh(labels, values, color=PALETTE[i % len(PALETTE)])
        ax.set_title(str(period), fontsize=10, fontweight="bold")
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)

    for j in range(n, len(axes)):
        axes[j].axis("off")

    fig.suptitle(title, fontsize=13, fontweight="bold", x=0.02, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(output)
    print(f"wrote {output} ({n} period panels)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="CSV with a header row")
    p.add_argument("--category-col", required=True)
    p.add_argument("--value-col", required=True)
    p.add_argument("--period-col", help="required when --shape by_period")
    p.add_argument("--shape", choices=["ranking", "by_period"], default="ranking")
    p.add_argument("--title", default="")
    p.add_argument("--output", required=True, help="output PNG path")
    p.add_argument("--top-n", type=int, default=15)
    p.add_argument("--max-periods", type=int, default=8,
                    help="cap panels in by_period mode; keeps the most recent periods")
    args = p.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no rows in input", file=sys.stderr)
        sys.exit(1)

    if args.shape == "ranking":
        render_ranking(rows, args.category_col, args.value_col, args.title,
                        args.output, args.top_n)
    else:
        if not args.period_col:
            print("--period-col is required for --shape by_period", file=sys.stderr)
            sys.exit(1)
        render_by_period(rows, args.category_col, args.value_col, args.period_col,
                          args.title, args.output, args.top_n, args.max_periods)


if __name__ == "__main__":
    main()
