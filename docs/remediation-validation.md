# Remediation and Validation Playbook

This workflow turns a mobile-security observation into an auditable remediation decision. All examples are synthetic and intended for authorized defensive assessment.

## Engineering lifecycle

1. **Triage** — confirm the failed control, affected component, evidence quality and severity.
2. **Assign** — identify an accountable engineering/product owner. Missing ownership remains a governance gap.
3. **Plan** — record the corrective control, target date and any approved exception. Risk acceptance does not erase the technical observation.
4. **Remediate** — implement the smallest durable change that addresses the root control weakness.
5. **Re-test** — repeat the relevant static/configuration assessment using the same control definition.
6. **Validate closure** — close only when the expected secure state is demonstrated. The risk-register model requires validation evidence for `validated_closed` items.
7. **Monitor regression** — retain the control in CI/release assurance where practical.

## Evidence standard

Useful closure evidence can include a sanitized manifest/configuration diff, repeatable unit-test output, a static-analysis result, a release-policy check, or an architecture decision showing that risky behavior was removed. Never store credentials, production tokens, signing material, customer data or confidential application artifacts in this repository.

## Control-specific validation

| Control theme | Remediation objective | Revalidation signal |
|---|---|---|
| Debuggable production build | Disable debugging in release configuration | Release manifest/config reports debugging disabled |
| Backup exposure | Apply a backup policy appropriate to data sensitivity | Release configuration and backup rules match policy |
| Cleartext transport | Enforce encrypted transport | Network-security configuration denies cleartext |
| Exported component | Restrict unnecessary external access | Component is non-exported or protected by an appropriate permission |
| Sensitive local storage | Use platform-backed protected storage and minimize persistence | Static/config review shows sensitive values are not stored unprotected |
| Excessive permission | Remove capabilities not required by product functionality | Permission inventory contains only justified capabilities |

## Risk register

`src/risk_register.py` provides deterministic finding identifiers, accountable ownership, due dates, lifecycle status, bounded exposure metrics and Markdown output. The model deliberately distinguishes `risk_accepted` from `validated_closed`: an accepted risk is still an open technical exposure for reporting purposes.

## Risk acceptance

Exceptions should be time-bounded, owned, justified and reviewed. An exception changes treatment status; it does not mean the control weakness disappeared. Revalidation is required after an exception expires or a compensating control changes.

## Closure standard

A ticket, pull request, stated intent, or deployment claim is not closure evidence. Closure requires the corrected configuration plus repeatable security revalidation. Before/after evidence should be retained outside this public lab when it contains organizational information.

## Safety boundary

This project does not bypass mobile controls, intercept credentials, defeat certificate pinning, exploit applications, access live devices, or target production services. It models defensive assurance and remediation governance only.
