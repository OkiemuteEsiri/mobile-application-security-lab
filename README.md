# Mobile Application Security Lab

A defensive mobile application security engineering project for assessing Android application configuration and security posture in an authorized laboratory environment.

## Purpose

Mobile applications frequently expose risk through insecure platform configuration rather than sophisticated exploitation: exported components, weak backup settings, cleartext traffic, excessive permissions, debuggable builds, unsafe WebView choices, and weak network security configuration. This project turns those controls into a repeatable static assessment and remediation workflow.

The repository uses only synthetic manifests and intentionally non-sensitive examples. It does not target production applications, contain credentials, or provide exploit payloads.

## Security engineering objectives

- Parse Android manifest metadata safely.
- Identify high-risk application configuration patterns.
- Assign deterministic severity and risk scores.
- Map findings to OWASP MASVS / Mobile Top 10 concepts and MITRE ATT&CK Mobile where useful.
- Produce evidence-oriented reports for engineering teams.
- Validate remediation by rescanning corrected configuration.
- Demonstrate how mobile security checks can operate as CI quality gates.

## Architecture

```text
Synthetic Android Manifest
          |
          v
   Manifest Parser
          |
          v
  Security Control Engine
     |            |
     v            v
 Findings      Risk Score
     |            |
     +-------> Reporter
                  |
                  v
        Remediation / Re-test
```

## Repository structure

```text
.
├── src/
│   ├── manifest_parser.py
│   ├── controls.py
│   ├── analyzer.py
│   └── reporting.py
├── data/
│   ├── synthetic_insecure_manifest.xml
│   └── synthetic_hardened_manifest.xml
├── tests/
│   ├── test_parser.py
│   └── test_analyzer.py
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── threat-model.md
│   └── remediation-validation.md
├── reports/
│   └── example-assessment.md
└── .github/workflows/
    └── tests.yml
```

## Implemented controls

| Control | Example risk | Default severity |
|---|---|---:|
| Debuggable production build | Runtime inspection and reduced hardening | High |
| Application backup enabled | Sensitive application data exposure | Medium |
| Cleartext traffic allowed | Network confidentiality degradation | High |
| Exported component without permission | Unauthorized component invocation | High |
| Excessive high-risk permissions | Expanded privilege / privacy exposure | Medium |
| Missing network security config | Reduced transport-policy control | Medium |
| Legacy target SDK | Missing modern platform protections | Medium |

## Risk model

Each finding receives a base severity score:

- Critical: 10
- High: 8
- Medium: 5
- Low: 2

The application risk score is the severity-weighted total normalized to 0–100. The model is deliberately explainable rather than predictive; teams can see exactly which controls contribute to the score.

## Usage

```bash
python -m src.reporting data/synthetic_insecure_manifest.xml
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

No third-party Python packages are required.

## Example output

```text
Application: com.example.synthetic
Risk score: 78/100
High findings: 3
Medium findings: 4
Status: remediation required
```

See `reports/example-assessment.md` for a synthetic management-facing result.

## Standards mapping

The assessment methodology aligns conceptually with:

- OWASP Mobile Application Security Verification Standard (MASVS)
- OWASP Mobile Application Security Testing Guide (MASTG)
- OWASP Mobile Top 10
- Android platform security guidance
- MITRE ATT&CK Mobile, where configuration weaknesses relate to attacker behaviors

ATT&CK references are contextual mappings, not claims that a technique has been executed.

## Defensive ATT&CK context

Examples include:

- **T1417 – Input Capture**: sensitive UI/data handling and platform exposure should be minimized.
- **T1437 – Application Layer Protocol**: transport controls reduce exposure of application communications.
- **T1409 – Access Stored Application Data**: backup and storage configuration can affect data exposure.

## Remediation lifecycle

1. Identify the insecure configuration.
2. Record evidence and affected component.
3. Assign engineering owner and severity.
4. Apply the secure configuration change.
5. Re-run the analyzer against the corrected manifest.
6. Confirm the original control no longer fails.
7. Run regression tests before closure.
8. Retain evidence of the validated state.

A finding is not considered closed merely because a change ticket exists.

## CI/CD use

The included GitHub Actions workflow runs the unit-test suite. In a mature pipeline, the analyzer can additionally gate releases when new High-severity mobile configuration findings are introduced.

## Skills demonstrated

- Mobile application security engineering
- Android manifest security analysis
- Python security automation
- Risk scoring and reporting
- Secure configuration validation
- OWASP mobile security methodology
- Threat modeling
- Test-driven security controls
- DevSecOps security gates
- Remediation verification

## Limitations

This is a static, configuration-focused lab. It does not claim to replace dynamic instrumentation, source-code review, SAST, DAST, binary analysis, cryptographic review, API testing, device-level assessment, or manual application penetration testing.

All samples are synthetic. No employer, client, commercial application, credential, or production endpoint is represented.

## Roadmap

- Add iOS entitlement/plist configuration checks.
- Add SARIF output for code-scanning platforms.
- Add JSON report export and trend comparison.
- Add certificate/network-security-policy checks.
- Add SBOM/mobile dependency risk ingestion.
- Add a lightweight release security gate.

## Ethical scope

Use this project only for applications and environments you own or are explicitly authorized to assess. The implementation is intentionally defensive and avoids exploit delivery, credential theft, persistence, bypass techniques, and production targeting.
