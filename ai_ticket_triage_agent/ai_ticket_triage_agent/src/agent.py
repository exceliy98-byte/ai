from dataclasses import dataclass
from typing import Dict, List


@dataclass
class TicketResult:
    ticket_id: str
    customer: str
    category: str
    priority: str
    owner: str
    suggestion: str
    reply_draft: str


SOP: Dict[str, str] = {
    "支付问题": "核对支付流水号、订单状态和回调记录；必要时转交财务或技术同学排查。",
    "账号问题": "确认手机号/邮箱是否正确，检查验证码通道和账号风控状态。",
    "物流问题": "查询物流轨迹、预计送达时间，并同步仓储或承运商确认异常。",
    "发票咨询": "引导用户提供抬头、税号、邮箱和订单号，确认可开票范围。",
    "其他问题": "补充收集用户信息，再转交人工客服判断。",
}

OWNER: Dict[str, str] = {
    "支付问题": "财务/支付接口负责人",
    "账号问题": "账号系统负责人",
    "物流问题": "仓储物流负责人",
    "发票咨询": "运营客服负责人",
    "其他问题": "客服值班同学",
}


def classify_ticket(message: str) -> str:
    """模拟分类 Agent：根据关键词判断问题类型。"""
    rules = {
        "支付问题": ["付款", "支付", "扣款", "订单未支付"],
        "账号问题": ["登录", "验证码", "密码", "账号"],
        "物流问题": ["物流", "送到", "快递", "配送"],
        "发票咨询": ["发票", "抬头", "税号"],
    }
    for category, keywords in rules.items():
        if any(keyword in message for keyword in keywords):
            return category
    return "其他问题"


def judge_priority(message: str) -> str:
    """模拟优先级 Agent：识别紧急程度。"""
    high_words = ["无法登录", "付款成功", "投诉", "尽快", "不到账"]
    medium_words = ["超过预计", "还没", "异常", "收不到"]
    if any(word in message for word in high_words):
        return "高"
    if any(word in message for word in medium_words):
        return "中"
    return "低"


def generate_reply(customer: str, category: str, suggestion: str) -> str:
    """模拟回复生成 Agent。"""
    return (
        f"{customer}您好，我们已收到您的反馈。该问题初步判断为【{category}】。"
        f"我们会按照以下流程处理：{suggestion} 处理完成后会第一时间同步进展。"
    )


def process_tickets(tickets: List[Dict[str, str]]) -> List[TicketResult]:
    results: List[TicketResult] = []
    for ticket in tickets:
        message = ticket["message"]
        category = classify_ticket(message)
        priority = judge_priority(message)
        suggestion = SOP.get(category, SOP["其他问题"])
        owner = OWNER.get(category, OWNER["其他问题"])
        reply_draft = generate_reply(ticket["customer"], category, suggestion)

        results.append(
            TicketResult(
                ticket_id=ticket["id"],
                customer=ticket["customer"],
                category=category,
                priority=priority,
                owner=owner,
                suggestion=suggestion,
                reply_draft=reply_draft,
            )
        )
    return results
