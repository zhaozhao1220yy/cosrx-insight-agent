# -*- coding: utf-8 -*-
"""
Agent ③c 执行方案（Campaign Execution Plan）
职责：基于真实洞察 + 用户提供的假设约束，生成详细可执行的活动方案
输出：output/campaign_plan.md
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
        "temperature": 0.6,
    }
    req = urllib.request.Request(
        "https://api.deepseek.com/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
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

    prompt = f"""你是资深护肤品整合营销专家，擅长把消费者洞察落成可执行的活动方案。下面是一份真实消费者评论洞察数据，以及一组【假设】的活动约束。请产出一份详细、可落地的活动执行方案。

【真实洞察数据】（印尼市场，COSRX 两款产品）
{context}

【活动约束（均为假设值，模拟练习用，不是真实执行）】
- 预算：10 万人民币（约 2.2 亿印尼盾）
- 周期：3 周
- 主阵地：Instagram（印尼市场）
- 目标：品牌曝光 + 销量转化（双目标，需平衡）

请用 Markdown 输出，结构如下：
1. 活动目标拆解（把「曝光+销量」拆成可量化的指标，标注目标值为假设）
2. 时间线（3 周，分预热/爆发/收尾三阶段，具体到每周做什么）
3. 渠道策略（Instagram 内 Reels/Stories/Feed/达人合作/付费广告怎么配，分别为什么）
4. 预算分配表（10 万人民币分配到各模块，给出比例和金额）
5. KPI 与复盘指标（哪些指标衡量曝光、哪些衡量销量转化，含计算公式）
6. 物料清单（文案/视频/图片/落地页各需要什么）
7. 执行分工（角色与职责）
8. 风险预案（至少 3 个风险 + 应对）

硬性要求：
- 洞察相关的结论必须能追溯到上面的真实数据，引用具体数字；
- 预算、周期、目标量都是假设值，方案开头和每个数字处都要明确标注「假设」；
- 不编造任何真实业绩数据、不虚构产品功效、不写医疗宣称；
- 语言具体、可落地，不用空话套话。"""

    text, err = call_llm(prompt)
    if err:
        print("ERROR:", err)
        return

    out = os.path.join(BASE, "output", "campaign_plan.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
