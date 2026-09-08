from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Control:
    control_id: str
    title: str
    severity: str
    description: str
    remediation: str
    masvs_area: str
    attack_context: str | None = None


CONTROLS = {
    "MOB-001": Control(
        "MOB-001", "Debuggable application build", "High",
        "The application is marked debuggable, reducing runtime hardening.",
        "Disable android:debuggable for release builds and enforce release build configuration in CI.",
        "MASVS-RESILIENCE"
    ),
    "MOB-002": Control(
        "MOB-002", "Application backup enabled", "Medium",
        "Application backup is enabled and may expand exposure of locally stored application data.",
        "Disable backup where business requirements do not require it and validate storage behavior.",
        "MASVS-STORAGE", "T1409"
    ),
    "MOB-003": Control(
        "MOB-003", "Cleartext traffic permitted", "High",
        "The application permits cleartext network traffic.",
        "Disable cleartext traffic and enforce TLS through platform network security configuration.",
        "MASVS-NETWORK", "T1437"
    ),
    "MOB-004": Control(
        "MOB-004", "Exported component lacks permission protection", "High",
        "An exported Android component does not declare a protecting permission.",
        "Set exported=false unless external invocation is required; otherwise enforce least-privilege permissions and validate callers.",
        "MASVS-PLATFORM"
    ),
    "MOB-005": Control(
        "MOB-005", "High-risk permission exposure", "Medium",
        "The manifest requests a permission associated with sensitive device or user data.",
        "Remove unnecessary permissions and apply least privilege with runtime justification where required.",
        "MASVS-PRIVACY"
    ),
    "MOB-006": Control(
        "MOB-006", "Network security configuration missing", "Medium",
        "No explicit Android network security configuration is declared.",
        "Define a network security configuration appropriate to application trust and certificate requirements.",
        "MASVS-NETWORK"
    ),
    "MOB-007": Control(
        "MOB-007", "Legacy target SDK", "Medium",
        "The target SDK is below the lab baseline and may not benefit from current platform protections.",
        "Upgrade target SDK after compatibility testing and address deprecated security-sensitive behaviors.",
        "MASVS-PLATFORM"
    ),
}

HIGH_RISK_PERMISSIONS = {
    "android.permission.READ_SMS",
    "android.permission.RECORD_AUDIO",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.READ_CONTACTS",
    "android.permission.CAMERA",
}

SEVERITY_SCORES = {"Critical": 10, "High": 8, "Medium": 5, "Low": 2}
