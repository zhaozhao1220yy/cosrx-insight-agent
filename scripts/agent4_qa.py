# -*- coding: utf-8 -*-
"""
Agent ④ 质检（QA / 事实核查）
职责：复核策划案的每一个数字与事实主张，是否都能追溯到真实洞察数据
输入：output/insights.json + output/marketing_plan.md
输出：output/qa_report.md
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
        "temperature": 0.2,
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
    plan_path = os.path.join(BASE, "output", "marketing_plan.md")
    if not os.path.exists(plan_path):
        print("ERROR: 先运行 agent3_planner.py 生成策划案")
        return
    with open(plan_path, encoding="utf-8") as f:
        plan = f.read()

    prompt = f"""你是严格的事实核查员。下面是一份营销策划案，以及它依据的原始洞察数据。请核查策划案中的每个数字和事实主张，是否都能在原始数据中找到依据。

【原始洞察数据】
{json.dumps(ins, ensure_ascii=False, indent=2)}

【营销策划案】
{plan}

请输出核查报告（Markdown）：
1. 可追溯的结论：逐条列出，并标注对应原始数据
2. 存疑 / 过度推断的地方：说明为什么存疑
3. 是否有编造的数据：有就明确指出
4. 总体结论：通过 / 需修改（并说明理由）

严格要求：只依据上面给出的数据核查，不要补充外部知识，不要放过任何对不上的数字。"""

    text, err = call_llm(prompt)
    if err:
        print("ERROR:", err)
        return

    out = os.path.join(BASE, "output", "qa_report.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
