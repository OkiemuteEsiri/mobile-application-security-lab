from __future__ import annotations

from collections import Counter
from pathlib import Path
import sys

from .analyzer import analyze_manifest


def render_report(path: str | Path) -> str:
    profile, findings, score = analyze_manifest(path)
    counts = Counter(f.severity for f in findings)
    lines = [
        f"Application: {profile.package}",
        f"Risk score: {score}/100",
        f"High findings: {counts.get('High', 0)}",
        f"Medium findings: {counts.get('Medium', 0)}",
        f"Total findings: {len(findings)}",
        f"Status: {'remediation required' if findings else 'baseline controls passed'}",
        "",
        "Findings:",
    ]
    if not findings:
        lines.append("- None")
    for finding in findings:
        lines.extend([
            f"- [{finding.severity}] {finding.control_id}: {finding.title}",
            f"  Evidence: {finding.evidence}",
            f"  Standard: {finding.standard}",
            f"  ATT&CK context: {finding.attack_context or 'Not mapped'}",
            f"  Remediation: {finding.remediation}",
        ])
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m src.reporting <AndroidManifest.xml>")
        return 2
    print(render_report(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
