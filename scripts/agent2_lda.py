# -*- coding: utf-8 -*-
"""
Agent ②b LDA 主题挖掘（分析师增强）
职责：对评论文本做 LDA 主题模型，自动发现消费者在讨论哪些主题
输出：output/lda_topics.json
"""
import pandas as pd
import os
import json
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

BASE = os.path.join(os.path.dirname(__file__), "..")

STOPWORDS = set("""yang dan di ke dari untuk dengan tidak ini itu saya aku kamu anda dia
kita mereka adalah karena juga sangat sudah tapi atau pada lebih kurang sih kok gak ga
nggak nya yg aja deh ya udah kalau kalo jadi tp pas pake pakai kulit wajah cream produk
banget cocok recommended bagus""".split())


def tokenize(text):
    words = re.findall(r"[a-zA-Z]+", str(text).lower())
    return " ".join([w for w in words if len(w) > 3 and w not in STOPWORDS])


def main():
    df = pd.read_csv(os.path.join(BASE, "data", "clean", "reviews_clean.csv"))
    docs = df["details"].map(tokenize).tolist()

    vec = CountVectorizer(max_df=0.7, min_df=10, max_features=5000)
    X = vec.fit_transform(docs)

    lda = LatentDirichletAllocation(n_components=6, random_state=42, max_iter=20)
    lda.fit(X)

    words = vec.get_feature_names_out()
    topics = []
    for i, comp in enumerate(lda.components_):
        top = [words[j] for j in comp.argsort()[-10:][::-1]]
        weight = float(comp.sum() / lda.components_.sum())
        topics.append({"主题编号": i + 1, "关键词Top10": top, "占比": round(weight, 4)})

    with open(os.path.join(BASE, "output", "lda_topics.json"), "w", encoding="utf-8") as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)
    print(json.dumps(topics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
