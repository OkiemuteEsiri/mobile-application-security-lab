# Architecture

## Components

The lab separates collection, analysis, policy, and reporting so each responsibility can be tested independently.

1. **Manifest parser** converts Android XML into a normalized `ManifestProfile`.
2. **Control catalogue** defines control identifiers, severity, standards context, and remediation text.
3. **Analyzer** evaluates the normalized profile and produces deterministic findings.
4. **Risk engine** calculates an explainable normalized score.
5. **Reporter** converts findings into human-readable engineering evidence.

## Trust boundaries

The analyzer operates only on local files supplied by the user. It performs no network calls, does not install applications, and does not execute application code.

## Design decisions

- Standard library only to minimize dependency risk.
- Deterministic rules rather than opaque scoring.
- Synthetic data to avoid confidential artifacts.
- Separate secure/insecure manifests to support regression validation.
- Remediation text is stored alongside each control so engineering guidance remains traceable to the failed rule.

## Extension points

Future modules can add iOS plist/entitlement analysis, SARIF output, JSON schemas, SBOM ingestion, and mobile CI release gates without changing the core manifest parser.
