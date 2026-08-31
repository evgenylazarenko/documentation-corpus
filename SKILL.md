---
name: documentation-corpus
description: Design, scaffold, migrate, audit, and maintain sparse numbered repository documentation corpora and optional Open Knowledge Format (OKF)-aligned bundles. Use when Codex needs to organize a `documentation/` tree, separate raw evidence from maintained synthesis, define numbered taxonomy and node rules, create navigation/status/log/source maps, add lightweight concept metadata and cross-links, migrate sources without mutating originals, audit corpus integrity, or prevent documentation sprawl. For AGENTS.md-only work, prefer `maintain-agents-md`.
---

# Documentation Corpus

Build the smallest durable corpus that preserves evidence, exposes current knowledge, and stays navigable as it grows.

## Decision Rule

Use this skill for whole-corpus architecture and knowledge management. Use `maintain-agents-md` for AGENTS-only audits, draft/promotion workflows, or nested instruction maintenance. When both apply, design the corpus here and use `maintain-agents-md` only for AGENTS-specific details.

## Corpus Profiles

- **New repository corpus (default):** create sparse, two-digit numbered lanes for maintained synthesis; keep operational layers such as `_sources/` and `_meta/` unnumbered.
- **Existing repository corpus:** preserve the established taxonomy and patch gaps. Propose top-level moves or renumbering before changing stable paths.
- **Strict OKF bundle:** use only when the user explicitly requests OKF conformance or a portable OKF bundle. Read `references/okf-profile.md` first.

Repository corpora may adopt OKF ideas without claiming conformance. Do not silently turn an existing docs tree into a strict OKF bundle.

## Workflow

1. Inspect the boundary.
   - Read root and nested `AGENTS.md`, docs entry points, `.gitignore`, current tree shape, source-of-truth files, and existing taxonomy rules.
   - Use the repo's preferred search command first; otherwise use `rg` / `rg --files`.

2. Classify the work.
   - New corpus: establish the smallest useful spine and numbered lanes supported by current material.
   - Existing corpus: reuse its taxonomy and patch gaps.
   - Topic/domain expansion: read the node guide before adding pages or directories.
   - Source migration: copy or rename evidence, preserve originals, and record provenance.
   - Audit: make no content or layout edits unless the user also asks for changes.

3. Design a sparse numbered IA.
   - Use two-digit prefixes in increments of ten for maintained top-level lanes.
   - Create only lanes with current durable content; do not complete a taxonomy with placeholders.
   - Keep `00-orientation/` optional and keep the archive as the terminal numbered lane.
   - Keep `_sources/`, `_meta/`, `_templates/`, and `wip/` unnumbered.
   - After the initial taxonomy exists, request approval before adding, renaming, or renumbering a top-level lane.

4. Separate knowledge layers.
   - Keep copied evidence immutable in `_sources/` unless the user explicitly asks to replace or delete it.
   - Keep current conclusions, plans, guides, decisions, and runbooks in numbered maintained lanes.
   - Keep schema, provenance, node rules, and maintenance controls in `_meta/` or the corpus spine.
   - Treat imported active guidance differently from raw evidence: remove it and all routing references when the user marks it unsafe or explicitly requests deletion.

5. Build navigation and graph edges.
   - Give `README.md`, `INDEX.md`, `SCHEMA.md`, `STATUS.md`, `LOG.md`, and `_meta/source-map.md` distinct jobs; create only the files the durable workflow will maintain.
   - Add short folder `README.md` files for major working directories.
   - Add folder `AGENTS.md` only when local behavior differs from the parent.
   - Link maintained concepts to related sources, decisions, contracts, and replacement pages when those relationships exist.
   - Treat canonical paths as stable identities. When moving a page, update incoming links, navigation, status/log entries, and provenance in the same pass.

6. Apply lightweight metadata deliberately.
   - For new or meaningfully revised maintained concept pages, prefer compact frontmatter with `type`, `title`, and `description`, plus only useful optional fields.
   - Do not retrofit copied sources or an entire existing corpus without approval.
   - Use `references/okf-profile.md` to distinguish OKF-inspired metadata from strict conformance.

7. Define growth rules.
   - Default to one maintained page before a directory.
   - Create a directory only for multiple durable child pages, recurring work, distinct source/verification rules, or local routing.
   - List durable nodes in `INDEX.md` when the repo uses that spine.
   - Register copied, renamed, generated, derived, superseded, or removed source relationships in `_meta/source-map.md` when provenance remains useful.

8. Validate proportionally.
   - Run `scripts/audit_corpus.py <corpus-root> --profile repo` for repository corpora.
   - Run `scripts/audit_corpus.py <bundle-root> --profile okf` before claiming OKF conformance.
   - Also run repo-local checks required by current guidance. Treat warnings as review prompts and errors as blockers.

## References

- Read `references/corpus-pattern.md` when designing, restructuring, or extending a numbered repository corpus.
- Read `references/okf-profile.md` when adding portable metadata, designing a strict bundle, or evaluating OKF conformance.
