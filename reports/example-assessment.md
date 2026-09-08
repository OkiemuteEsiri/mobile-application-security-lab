# Example Mobile Security Assessment

**Artifact:** `data/synthetic_insecure_manifest.xml`  
**Environment:** Synthetic lab only  
**Assessment type:** Static Android manifest security review

## Executive summary

The synthetic application contains multiple configuration weaknesses that would warrant remediation before release. The highest-priority issues are the debuggable release configuration, cleartext traffic allowance, and an exported activity without permission protection.

## Key findings

| ID | Severity | Finding | Recommended action |
|---|---|---|---|
| MOB-001 | High | Debuggable application build | Disable debugging in release builds |
| MOB-003 | High | Cleartext traffic permitted | Enforce TLS and network security policy |
| MOB-004 | High | Exported component lacks permission protection | Remove unnecessary export or enforce authorization |
| MOB-002 | Medium | Application backup enabled | Disable backup where not required |
| MOB-005 | Medium | Sensitive permissions requested | Apply least privilege and feature justification |
| MOB-006 | Medium | Network security config missing | Add explicit network security configuration |
| MOB-007 | Medium | Legacy target SDK | Upgrade after compatibility testing |

## Risk interpretation

The report is intended to demonstrate prioritization and engineering remediation. The synthetic score is not a production risk rating and should not be used without application context.

## Recommended remediation order

1. Remove debuggable release behavior.
2. Disable cleartext transport and define network security policy.
3. Correct exported component access control.
4. Review sensitive permissions and backup behavior.
5. Upgrade the target SDK.
6. Re-run the analyzer and unit tests.

## Validation expectation

The supplied `synthetic_hardened_manifest.xml` represents the target control state and is used by the tests to verify that baseline controls can pass after remediation.
