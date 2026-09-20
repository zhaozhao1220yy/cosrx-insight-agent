#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
一键跑完整流程：数据工 → 分析师 → LDA → 策划师 → 质检 → 修正
本地段（数据工/分析师/LDA）不需要 API key；策划师/质检/修正需要 DEEPSEEK_API_KEY。
用法：python3 run_all.py
"""
import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

STEPS = [
    ("① 数据工", "scripts/agent1_data_cleaner.py", False),
    ("② 分析师", "scripts/agent2_analyst.py", False),
    ("②b LDA 主题挖掘", "scripts/agent2_lda.py", False),
    ("③ 策划师", "scripts/agent3_planner.py", True),
    ("④ 质检", "scripts/agent4_qa.py", True),
    ("③b 修正", "scripts/agent3_revise.py", True),
    ("③c 执行方案", "scripts/agent3_campaign.py", True),
]


def main():
    need_key = os.environ.get("DEEPSEEK_API_KEY") is None
    if need_key:
        print("提示：未检测到 DEEPSEEK_API_KEY，策划师/质检/修正将跳过（本地段照常跑）。\n")
    for name, script, requires_key in STEPS:
        if requires_key and need_key:
            print(f"[跳过] {name}（需要 DEEPSEEK_API_KEY）")
            continue
        print(f"[运行] {name}")
        r = subprocess.run([sys.executable, os.path.join(BASE, script)], cwd=BASE)
        if r.returncode != 0:
            print(f"[失败] {name}，退出。")
            sys.exit(1)
    print("\n全部完成，产出在 output/ 目录。")


if __name__ == "__main__":
    main()
