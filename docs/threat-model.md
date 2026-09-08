# Mobile Threat Model

## Protected assets

- Authentication/session material
- User PII and application data
- Device capabilities exposed through permissions
- Application network traffic
- Android application components and inter-process boundaries
- Release-build integrity

## Relevant threat conditions

| Threat condition | Security consequence | Primary control |
|---|---|---|
| Debuggable release configuration | Reduced runtime resistance and information exposure | MOB-001 |
| Backup of sensitive application state | Stored-data exposure | MOB-002 |
| Cleartext network traffic | Loss of confidentiality/integrity in transit | MOB-003 |
| Unprotected exported component | Unauthorized external invocation | MOB-004 |
| Excessive sensitive permissions | Expanded privacy/device impact | MOB-005 |
| Missing explicit network policy | Weaker transport governance | MOB-006 |
| Legacy target SDK | Reduced benefit from current platform protections | MOB-007 |

## MITRE ATT&CK Mobile context

This project uses ATT&CK only as defensive context; it does not emulate these behaviors.

- **T1409 – Access Stored Application Data**: relevant to stored/backup data exposure.
- **T1437 – Application Layer Protocol**: transport-policy controls help protect application communications.
- **T1417 – Input Capture**: application permissions and sensitive-data handling should minimize opportunities for capture or misuse.

## Out of scope

Exploit development, credential theft, malware development, persistence, bypass techniques, unauthorized instrumentation, production scanning, and targeting of third-party applications are outside this project.
