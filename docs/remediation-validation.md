# Remediation and Validation Playbook

## Engineering workflow

For every mobile security finding:

1. Record the failed control, evidence, affected component, and severity.
2. Assign an engineering owner and remediation target.
3. Implement the smallest secure configuration change that resolves the issue.
4. Re-run the analyzer against the updated manifest.
5. Run the full unit-test suite to detect regression.
6. Compare before/after evidence.
7. Confirm no new High-severity finding was introduced.
8. Retain the corrected artifact and validation output before closure.

## Control-specific validation

### MOB-001 — Debuggable build

Remediation: release builds must not set `android:debuggable=true`.

Validation: analyzer no longer reports MOB-001 and the release build pipeline confirms a non-debuggable build profile.

### MOB-002 — Backup exposure

Remediation: disable application backup when not explicitly required by the product design.

Validation: verify `android:allowBackup=false` and confirm application data lifecycle requirements remain satisfied.

### MOB-003 — Cleartext traffic

Remediation: set `android:usesCleartextTraffic=false` and enforce an appropriate network security policy.

Validation: MOB-003 no longer appears and transport tests confirm expected HTTPS/TLS behavior.

### MOB-004 — Exported component

Remediation: make the component non-exported unless external invocation is a business requirement. If exposure is required, apply a suitable permission and validate caller authorization.

Validation: verify the corrected component configuration and repeat component-security review.

### MOB-005 — Sensitive permission

Remediation: remove permissions that are not necessary for a defined feature.

Validation: confirm application functionality still works without the permission and document justified permissions.

## Closure evidence

A ticket, pull request, or stated intent to remediate is not closure evidence. Closure requires the corrected configuration plus successful security revalidation.
