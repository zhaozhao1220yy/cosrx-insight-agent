# -*- coding: utf-8 -*-
"""
Agent ③b 修正（Planner 修订版）
职责：读取质检报告，让策划师收敛过度推断、修正口径，产出 v2 策划案
输出：output/marketing_plan_v2.md
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
        "temperature": 0.5,
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
    base = BASE
    with open(os.path.join(base, "output", "insights.json"), encoding="utf-8") as f:
        ins = json.load(f)
    with open(os.path.join(base, "output", "marketing_plan.md"), encoding="utf-8") as f:
        plan = f.read()
    with open(os.path.join(base, "output", "qa_report.md"), encoding="utf-8") as f:
        qa = f.read()

    prompt = f"""你是资深护肤品营销策划专家。你之前产出了一份营销策划案，质检 Agent 对它做了事实核查，发现了若干过度推断和口径问题。请根据质检报告，修正策划案，产出一版更严谨的 v2。

【原始洞察数据】
{json.dumps(ins, ensure_ascii=False, indent=2)}

【策划案 v1】
{plan}

【质检报告】
{qa}

请输出修正后的完整策划案 v2（Markdown），保持原结构（人群定位 / 内容选题 / 活动策划 / 关键话术），但：
1. 删除或改写所有被质检指出「过度推断」的表述；
2. 修正口径问题（如年龄占比的分母、提及率与次数）；
3. 结论必须严格可追溯到数据，不确定的地方就明确说「数据未覆盖」；
4. 仍然简洁可落地，不写空话。"""

    text, err = call_llm(prompt)
    if err:
        print("ERROR:", err)
        return

    out = os.path.join(base, "output", "marketing_plan_v2.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
