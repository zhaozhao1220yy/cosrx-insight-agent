# -*- coding: utf-8 -*-
"""
Agent ③ 策划师（Planner）
职责：把分析师产出的真实洞察，翻译成可落地的营销策划案（调用模型 API）
输入：output/insights.json
输出：output/marketing_plan.md
"""
import os
import json
import urllib.request

BASE = os.path.join(os.path.dirname(__file__), "..")


def call_llm(prompt):
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        return None, "缺少 DEEPSEEK_API_KEY 环境变量（需先配置）"
    body = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"], None


def main():
    with open(os.path.join(BASE, "output", "insights.json"), encoding="utf-8") as f:
        ins = json.load(f)

    context = json.dumps(
        {
            "产品": ins["产品"],
            "评论总数": ins["评论总数"],
            "满意度4维度均分": ins["满意度_4维度均分_1到5"],
            "推荐率百分比": ins["推荐率_百分比"],
            "复购意愿率百分比": ins["复购意愿率_百分比"],
            "年龄分布": ins["年龄分布"],
            "肤质Top10": ins["肤质Top10"],
            "好评关键词Top15": ins["好评关键词Top15"],
            "差评关键词Top15": ins["差评关键词Top15"],
        },
        ensure_ascii=False,
        indent=2,
    )

    prompt = f"""你是资深护肤品营销策划专家。下面是韩国品牌 COSRX 两款产品在电商平台（印尼市场）的真实消费者评论洞察数据。请严格基于这些真实数据，产出一份可落地执行的营销策划案。

【真实洞察数据】
{context}

请用 Markdown 输出以下结构：
1. 人群定位：核心目标人群画像（年龄 / 肤质 / 核心诉求）
2. 内容选题：5 个基于真实痛点的内容选题（每条注明它对应上面哪条数据洞察）
3. 活动策划：1 个活动方案（目标 / 形式 / 核心卖点 / 预期指标）
4. 关键话术：3 条基于「隐藏痛点」的营销话术（例如好评区高频出现的「黏腻/油腻」这类被好评掩盖的痛点）

硬性要求：
- 所有结论必须能追溯到上面真实数据，不编造任何数字或事实；
- 语言简洁、具体、可落地，不用空话套话；
- 不要虚构产品功效，不要写医疗宣称。"""

    text, err = call_llm(prompt)
    if err:
        print("ERROR:", err)
        return

    out = os.path.join(BASE, "output", "marketing_plan.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
