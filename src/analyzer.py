from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .controls import CONTROLS, HIGH_RISK_PERMISSIONS, SEVERITY_SCORES
from .manifest_parser import ManifestProfile, parse_manifest


@dataclass(frozen=True)
class Finding:
    control_id: str
    title: str
    severity: str
    evidence: str
    remediation: str
    standard: str
    attack_context: str | None = None


def analyze_profile(profile: ManifestProfile, minimum_target_sdk: int = 35) -> list[Finding]:
    finding_ids: list[tuple[str, str]] = []

    if profile.debuggable:
        finding_ids.append(("MOB-001", "android:debuggable=true"))
    if profile.allow_backup:
        finding_ids.append(("MOB-002", "android:allowBackup=true or not explicitly disabled"))
    if profile.uses_cleartext_traffic:
        finding_ids.append(("MOB-003", "android:usesCleartextTraffic=true"))

    for component in profile.components:
        if component.exported is True and not component.permission:
            finding_ids.append(("MOB-004", f"{component.kind}:{component.name} exported without permission"))

    for permission in sorted(set(profile.permissions) & HIGH_RISK_PERMISSIONS):
        finding_ids.append(("MOB-005", f"requested permission: {permission}"))

    if not profile.network_security_config:
        finding_ids.append(("MOB-006", "android:networkSecurityConfig not declared"))

    if profile.target_sdk is None or profile.target_sdk < minimum_target_sdk:
        finding_ids.append(("MOB-007", f"targetSdkVersion={profile.target_sdk!r}; lab baseline={minimum_target_sdk}"))

    findings: list[Finding] = []
    for control_id, evidence in finding_ids:
        control = CONTROLS[control_id]
        findings.append(
            Finding(
                control_id=control.control_id,
                title=control.title,
                severity=control.severity,
                evidence=evidence,
                remediation=control.remediation,
                standard=control.masvs_area,
                attack_context=control.attack_context,
            )
        )
    return findings


def risk_score(findings: list[Finding]) -> int:
    if not findings:
        return 0
    raw = sum(SEVERITY_SCORES[f.severity] for f in findings)
    theoretical_max = max(1, len(findings) * 10)
    return min(100, round((raw / theoretical_max) * 100))


def analyze_manifest(path: str | Path) -> tuple[ManifestProfile, list[Finding], int]:
    profile = parse_manifest(path)
    findings = analyze_profile(profile)
    return profile, findings, risk_score(findings)
