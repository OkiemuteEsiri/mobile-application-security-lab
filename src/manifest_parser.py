from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import xml.etree.ElementTree as ET

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"


@dataclass
class Component:
    kind: str
    name: str
    exported: bool | None
    permission: str | None = None


@dataclass
class ManifestProfile:
    package: str
    target_sdk: int | None
    debuggable: bool
    allow_backup: bool
    uses_cleartext_traffic: bool
    network_security_config: str | None
    permissions: list[str] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)


def _bool_attr(element: ET.Element, name: str, default: bool = False) -> bool:
    raw = element.get(f"{ANDROID_NS}{name}")
    if raw is None:
        return default
    return raw.strip().lower() == "true"


def parse_manifest(path: str | Path) -> ManifestProfile:
    root = ET.parse(path).getroot()
    application = root.find("application")
    if application is None:
        raise ValueError("manifest does not contain an application element")

    target_sdk = None
    uses_sdk = root.find("uses-sdk")
    if uses_sdk is not None:
        raw_target = uses_sdk.get(f"{ANDROID_NS}targetSdkVersion")
        if raw_target and raw_target.isdigit():
            target_sdk = int(raw_target)

    permissions = [
        item.get(f"{ANDROID_NS}name", "")
        for item in root.findall("uses-permission")
        if item.get(f"{ANDROID_NS}name")
    ]

    components: list[Component] = []
    for kind in ("activity", "service", "receiver", "provider"):
        for element in application.findall(kind):
            exported_raw = element.get(f"{ANDROID_NS}exported")
            exported = None if exported_raw is None else exported_raw.lower() == "true"
            components.append(
                Component(
                    kind=kind,
                    name=element.get(f"{ANDROID_NS}name", "<unnamed>"),
                    exported=exported,
                    permission=element.get(f"{ANDROID_NS}permission"),
                )
            )

    return ManifestProfile(
        package=root.get("package", "<unknown>"),
        target_sdk=target_sdk,
        debuggable=_bool_attr(application, "debuggable"),
        allow_backup=_bool_attr(application, "allowBackup", default=True),
        uses_cleartext_traffic=_bool_attr(application, "usesCleartextTraffic"),
        network_security_config=application.get(f"{ANDROID_NS}networkSecurityConfig"),
        permissions=permissions,
        components=components,
    )
