# -*- coding: utf-8 -*-
"""
Agent ① 数据工（Data Cleaner）
职责：读原始评论 -> 去重、去噪、规范化 -> 输出干净数据 + 数据质量报告
不依赖 sklearn，只用 pandas。
"""
import pandas as pd
import glob
import os
import json

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
CLEAN_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "clean")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")
os.makedirs(CLEAN_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    # 1) 读入两个评论文件，合并
    files = sorted(glob.glob(os.path.join(RAW_DIR, "review_*.csv")))
    dfs = []
    for f in files:
        d = pd.read_csv(f)
        d["_source_file"] = os.path.basename(f)
        dfs.append(d)
    raw = pd.concat(dfs, ignore_index=True)
    n_raw = len(raw)

    # 2) 去重：同一用户对同一产品写了相同文本，视为重复
    before = len(raw)
    df = raw.drop_duplicates(subset=["user_id", "product_id", "details"]).copy()
    n_dup = before - len(df)

    # 3) 规范化关键字段
    for c in ["is_repurchase", "is_recommended"]:
        if c in df.columns:
            df[c] = df[c].astype(str).str.lower().str.strip()
    for c in ["star_effectiveness", "star_packaging", "star_texture", "star_value_for_money"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # 4) 评论文本清洗：去首尾空白、去空评论
    df["details"] = df["details"].astype(str).str.strip()
    n_empty_text = int((df["details"].isin(["", "nan", "None"])).sum())
    df = df[~df["details"].isin(["", "nan", "None"])].copy()

    # 5) 落盘
    df.to_csv(os.path.join(CLEAN_DIR, "reviews_clean.csv"), index=False)

    # 6) 数据质量报告
    report = {
        "原始评论条数": n_raw,
        "去重删除条数": int(n_dup),
        "空文本删除条数": n_empty_text,
        "清洗后条数": len(df),
        "覆盖产品数": int(df["product_name"].nunique()),
        "各字段缺失率": {c: round(float(df[c].isna().mean()), 4) for c in df.columns},
    }
    with open(os.path.join(OUT_DIR, "data_quality_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
