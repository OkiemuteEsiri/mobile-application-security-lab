# Assessment Methodology

## Scope

This lab performs static Android manifest configuration analysis against synthetic or explicitly authorized application artifacts.

## Workflow

1. Confirm authorization and artifact provenance.
2. Parse the manifest into a normalized application profile.
3. Evaluate each security control independently.
4. Record failed control, evidence, severity, standards context, and remediation.
5. Calculate a transparent aggregate risk score.
6. Prioritize High findings before Medium/Low observations.
7. Apply remediation in the engineering branch.
8. Re-run the analyzer and unit tests.
9. Retain before/after evidence for closure.

## Evidence quality

Every finding must identify the exact manifest condition that caused the failure. Findings should be reproducible from the supplied artifact and should not depend on unverifiable assumptions.

## Severity model

- **High**: configuration can materially reduce application confidentiality, integrity, or component isolation.
- **Medium**: configuration weakens platform hardening, privacy, or defense in depth.
- **Low**: minor hardening or hygiene issue with limited direct impact.

Severity is distinct from business risk. Production risk should additionally consider application sensitivity, exposed data, user population, compensating controls, and threat context.

## Closure criteria

A finding is closed only when the insecure configuration is corrected, the analyzer no longer reports it, regression tests pass, and evidence of the corrected state is retained.
