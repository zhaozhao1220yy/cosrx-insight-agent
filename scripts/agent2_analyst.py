# -*- coding: utf-8 -*-
"""
Agent ② 分析师（Analyst）
职责：对清洗后的评论做洞察挖掘 -> 满意度 / 忠诚度 / 人群画像 / 痛点 vs 好评点
只用 pandas + 词频统计，0 成本。
"""
import pandas as pd
import os
import json
import re
from collections import Counter

BASE = os.path.join(os.path.dirname(__file__), "..")

# 印尼语停用词（简化版，够 demo 用）
STOPWORDS = set("""yang dan di ke dari untuk dengan tidak ini itu saya aku kamu anda dia
kita mereka adalah karena juga sangat sudah tapi atau pada lebih kurang sih kok gak ga
nggak nya yg aja deh ya udah kalau kalo jadi tp pas pake pakai kulit wajah cream produk
banget cocok recommended bagus""".split())


def tokenize(text):
    words = re.findall(r"[a-zA-Z]+", str(text).lower())
    return [w for w in words if len(w) > 3 and w not in STOPWORDS]


def main():
    df = pd.read_csv(os.path.join(BASE, "data", "clean", "reviews_clean.csv"))

    dims = ["star_effectiveness", "star_packaging", "star_texture", "star_value_for_money"]
    satisfaction = df[dims].mean().round(2).to_dict()

    rec_rate = float((df["is_recommended"] == "yes").mean())
    rep_rate = float((df["is_repurchase"] == "yes").mean())

    age_dist = df["age_range"].value_counts(dropna=True).to_dict()

    skin_counter = Counter()
    for v in df["skin_types"].dropna():
        for s in str(v).split(";"):
            s = s.strip()
            if s:
                skin_counter[s] += 1

    pos = df[df["star_effectiveness"] >= 4]
    neg = df[df["star_effectiveness"] <= 2]
    pos_words, neg_words = Counter(), Counter()
    for t in pos["details"]:
        pos_words.update(tokenize(t))
    for t in neg["details"]:
        neg_words.update(tokenize(t))

    result = {
        "产品": df["product_name"].unique().tolist(),
        "评论总数": int(len(df)),
        "正面评论(效果>=4星)": int(len(pos)),
        "负面评论(效果<=2星)": int(len(neg)),
        "满意度_4维度均分_1到5": satisfaction,
        "推荐率_百分比": round(rec_rate * 100, 1),
        "复购意愿率_百分比": round(rep_rate * 100, 1),
        "年龄分布": age_dist,
        "肤质Top10": [[k, v] for k, v in skin_counter.most_common(10)],
        "好评关键词Top15": [[k, v] for k, v in pos_words.most_common(15)],
        "差评关键词Top15": [[k, v] for k, v in neg_words.most_common(15)],
    }

    with open(os.path.join(BASE, "output", "insights.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
