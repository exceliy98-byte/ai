import json
from collections import Counter
from pathlib import Path

from agent import process_tickets

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "tickets.json"
OUTPUT_PATH = ROOT / "outputs" / "report.md"


def main() -> None:
    tickets = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    results = process_tickets(tickets)

    category_stats = Counter(item.category for item in results)
    priority_stats = Counter(item.priority for item in results)

    lines = ["# AI 工单分诊日报", ""]
    lines.append(f"共处理工单：{len(results)} 条")
    lines.append("")
    lines.append("## 分类统计")
    for category, count in category_stats.items():
        lines.append(f"- {category}：{count} 条")
    lines.append("")
    lines.append("## 优先级统计")
    for priority, count in priority_stats.items():
        lines.append(f"- {priority}优先级：{count} 条")
    lines.append("")
    lines.append("## 明细")

    for item in results:
        lines.extend(
            [
                f"### {item.ticket_id} - {item.customer}",
                f"- 分类：{item.category}",
                f"- 优先级：{item.priority}",
                f"- 负责人：{item.owner}",
                f"- 处理建议：{item.suggestion}",
                f"- 回复草稿：{item.reply_draft}",
                "",
            ]
        )

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"已生成报告：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
