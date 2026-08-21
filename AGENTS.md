# Repository Agent Contract

## Mission

Own multiomics evidence for this repository: sequencing economics, clinical trials, regulatory approvals and other primary observations already represented by the project. Produce reproducible evidence and derived views without turning scientific/clinical milestones into investment outcomes.

## Canonical authority

- Prefer regulators, trial registries, issuer/manufacturer primary disclosures and official/public scientific sources appropriate to each field.
- Preserve entity/product/trial identity, phase/status, observation/effective period, unit, source URL, retrieval time and provenance/hash fields required by the dataset.
- Keep sequencing cost/economics, clinical-trial state, approvals and derived research conclusions separate.
- Cross-repository forecast comparison belongs in `investor2`; do not duplicate ARK forecast authority here.

## Autonomous execution

1. Inspect current `main`, README, open Issues/PRs, canonical evidence, workflows/tests and public outputs.
2. Continue one canonical workline before creating another collector, schema, branch or Issue.
3. Prefer newly verified primary records, identity/status/period corrections, reproducible comparisons, public usability, then simplification.
4. Require source/identity/period/unit compatibility before calculating growth or comparing observations.
5. Run focused deterministic checks and verify the exact reviewed revision before merge.
6. Stop at the fixed point; do not infer scientific success, approval probability, market adoption or financial value from an intermediate milestone.

## Merge and release are separate

### PR merge conditions

A PR may merge when the repository-local scientific/data contract is correct on the exact head revision: identity/status/period semantics and provenance are preserved, deterministic tests pass, generated artifacts are reproducible where affected, and no unresolved review or correctness blocker remains.

A future trial update, regulatory decision, live registry refresh after merge, public deployment, clinical outcome, or market adoption is **not** a merge condition unless the PR specifically changes the release mechanism and pre-merge validation belongs to the bounded change.

### Product/data release conditions

Release is a separate post-merge decision. Treat multiomics evidence/views as released only after the merged `main` revision is read back and the release surfaces in scope are actually verified, including fresh registry/regulatory evidence when required, published artifacts/API/UI, deployment identity, and rollback/rebuild path where applicable.

A merged PR does not prove a clinical/regulatory outcome or public release. A release/source blocker may block release without invalidating a correctly merged repository change. Report merge and release independently.

## Boundaries

- Trial registration, enrollment, endpoint results, regulatory submission and approval are distinct states.
- Do not infer unreported sequencing prices/costs, clinical outcomes, approvals, revenue or market size.
- Do not execute trades or account actions.
- Unobserved source, CI, deployment, clinical or regulatory outcomes remain unverified.

## Completion report

Report verified multiomics evidence Before -> After, primary source/canonical artifact, Issue/PR/commit/check evidence, then report `merged` and `released` separately with direct evidence for each. Include manual work removed and remaining blocker.