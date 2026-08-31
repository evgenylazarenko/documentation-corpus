# Numbered Corpus Pattern

Use sparse numbered lanes for maintained synthesis and unnumbered operational layers for evidence and governance. Adapt lane names to the repo; do not create empty folders to imitate an example.

## Contents

- Core layers
- Navigation spine
- Numbered taxonomy rules
- Taxonomy profiles
- Node and path rules
- Source and retention rules
- Maintenance checks

## Core Layers

| Layer | Purpose |
| --- | --- |
| `_sources/` | Raw copied evidence; immutable by default. |
| Numbered lanes | Current conclusions, strategy, product, architecture, engineering, operations, decisions, and other maintained knowledge. |
| `_meta/` | Corpus schema, source map, node rules, and maintenance controls. |
| `_templates/` | Reusable shapes only after repetition appears. |
| `wip/` | Temporary notes and handoffs; never hidden source of truth. |
| Terminal archive lane | Superseded but historically useful maintained material. |

## Navigation Spine

Use these files only when each has a distinct maintained job:

- `README.md`: human entry point and directory map.
- `INDEX.md`: content-oriented map and shortest canonical reading paths.
- `SCHEMA.md`: taxonomy, naming, metadata, lifecycle, and maintenance contract.
- `STATUS.md`: current project/corpus state, open decisions, and next useful work.
- `LOG.md`: chronological record of material corpus changes.
- `_meta/source-map.md`: provenance for copied, renamed, generated, derived, superseded, or removed material.
- `_meta/node-creation-guide.md`: rules for future pages, directories, domains, and decisions.

Do not duplicate the same directory listing across every spine file.

## Numbered Taxonomy Rules

- Default new maintained lanes to two-digit prefixes in increments of ten.
- Create only lanes supported by current durable content.
- Keep gaps available for later domains; do not renumber merely to close a gap.
- Use `00-orientation/` only when first-read context deserves its own lane.
- Keep the archive last. Preserve an established `70-archive/` or `90-archive/` convention instead of normalizing it casually.
- Require approval before adding, renaming, or renumbering a top-level lane after the initial taxonomy exists.
- Treat a canonical path as a stable identity; moves are migrations, not cosmetic cleanup.

## Taxonomy Profiles

### Product And Engineering

- `00-orientation/`: first-read context and product promises.
- `10-product/`: requirements, UX, positioning, research, and user-facing truth.
- `20-architecture/`: system overview, contracts, ADRs, and technical boundaries.
- `30-engineering/`: developer guides, component designs, and implementation plans.
- `40-operations/`: runbooks and operational procedures.
- `50-quality-security/`: testing, incidents, privacy, compliance, risk, and security.
- `60-decisions/`: durable cross-domain decisions when they need a dedicated lane.
- `90-archive/`: superseded technical or product material.

### Strategy And Portfolio

- `00-orientation/`: entry context.
- `10-strategy/`: thesis, constraints, and studio/company strategy.
- `20-portfolio/`: product selection, lifecycle, sequencing, and portfolio policy.
- `30-research/`: synthesized market, user, competitor, channel, and regulatory research.
- `40-brand-goto-market/`: brand, positioning, pricing, launch, and channels.
- `50-operations/`: cadence, budget, resourcing, tooling, and workflow.
- `60-decisions/`: durable commitments and their consequences.
- `70-archive/`: superseded strategies and snapshots.

### Sparse App

Start with only the lanes that have content, for example:

- `10-product/`
- `30-engineering/`
- `60-decisions/` when the first durable decision exists
- a terminal archive lane when something actually needs archiving

Do not create missing decades as placeholders.

## Node And Path Rules

- Default to one maintained page.
- Create a directory only for multiple durable child pages, recurring work, distinct source/verification rules, or local routing.
- Put new directories under the nearest existing numbered lane.
- Avoid `misc`, `ideas`, `random`, `notes`, and unclassified buckets.
- Add a concise `README.md` for a durable directory.
- Add `AGENTS.md` only for local behavior, not repeated global rules.
- Update links, navigation, logs, and provenance whenever a canonical page moves.

## Source And Retention Rules

- Copy source evidence into `_sources/` with clear names and provenance.
- Do not rewrite copied evidence to match current conclusions.
- Add a dated or clearly named replacement when a source materially changes.
- Do not preserve obsolete active guidance merely because raw evidence is normally retained.
- When the user requests safety removal, delete the active artifact and every routing reference; retain a source copy only if the user wants it and it cannot be mistaken for active guidance.

## Maintenance Checks

- Run the bundled auditor with the appropriate profile.
- Review key local links and navigation paths.
- Check source-map coverage for copied evidence.
- Keep folder README and AGENTS files map-like.
- Reconcile `INDEX.md`, `STATUS.md`, and `LOG.md` after material corpus changes.
