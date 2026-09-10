"""Risk-register and remediation validation utilities for synthetic mobile findings."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from hashlib import sha256
from typing import Iterable

SEVERITY_WEIGHT = {"critical": 4, "high": 3, "medium": 2, "low": 1}


@dataclass(frozen=True)
class RiskItem:
    control_id: str
    title: str
    severity: str
    component: str
    owner: str
    status: str = "open"
    due_date: str | None = None
    evidence: str = ""
    remediation: str = ""
    validation: str = ""

    def __post_init__(self) -> None:
        severity = self.severity.lower()
        if severity not in SEVERITY_WEIGHT:
            raise ValueError(f"unsupported severity: {self.severity}")
        if self.status not in {"open", "in_progress", "risk_accepted", "validated_closed"}:
            raise ValueError(f"unsupported status: {self.status}")
        if not self.control_id.strip() or not self.title.strip() or not self.component.strip():
            raise ValueError("control_id, title and component are required")
        if self.status == "validated_closed" and not self.validation.strip():
            raise ValueError("validated_closed items require validation evidence")
        if self.due_date:
            datetime.strptime(self.due_date, "%Y-%m-%d")

    @property
    def finding_id(self) -> str:
        raw = f"{self.control_id}|{self.component}|{self.title}".lower().encode()
        return f"MOB-{sha256(raw).hexdigest()[:12].upper()}"

    @property
    def overdue(self) -> bool:
        if not self.due_date or self.status == "validated_closed":
            return False
        return date.fromisoformat(self.due_date) < date.today()


def summarize(items: Iterable[RiskItem]) -> dict[str, object]:
    records = list(items)
    open_items = [x for x in records if x.status != "validated_closed"]
    weighted = sum(SEVERITY_WEIGHT[x.severity.lower()] for x in open_items)
    max_weight = max(1, len(records) * 4)
    exposure_score = round(100 * weighted / max_weight, 1)
    return {
        "total": len(records),
        "open": len(open_items),
        "validated_closed": len(records) - len(open_items),
        "overdue": sum(x.overdue for x in open_items),
        "exposure_score": exposure_score,
        "by_severity": {
            severity: sum(x.severity.lower() == severity and x.status != "validated_closed" for x in records)
            for severity in SEVERITY_WEIGHT
        },
    }


def render_markdown(items: Iterable[RiskItem]) -> str:
    records = sorted(items, key=lambda x: (-SEVERITY_WEIGHT[x.severity.lower()], x.finding_id))
    metrics = summarize(records)
    lines = [
        "# Mobile Security Risk Register",
        "",
        "> Synthetic assessment output. This report is not evidence of a production compromise.",
        "",
        f"- Open findings: **{metrics['open']}**",
        f"- Validated closed: **{metrics['validated_closed']}**",
        f"- Overdue: **{metrics['overdue']}**",
        f"- Exposure score: **{metrics['exposure_score']}/100**",
        "",
        "| ID | Severity | Control | Component | Owner | Status | Due |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in records:
        lines.append(
            f"| {item.finding_id} | {item.severity.title()} | {item.control_id} | "
            f"{item.component} | {item.owner or 'Unassigned'} | {item.status} | {item.due_date or '-'} |"
        )
    lines.extend(["", "## Validation requirements", ""])
    for item in records:
        if item.status != "validated_closed":
            lines.extend([
                f"### {item.finding_id} — {item.title}",
                f"- Remediation: {item.remediation or 'Define and implement a corrective control.'}",
                f"- Revalidation: {item.validation or 'Re-run the relevant static/configuration control and retain evidence.'}",
                "",
            ])
    return "\n".join(lines)
