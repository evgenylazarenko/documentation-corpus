# Open Knowledge Format Profile

Use this reference to borrow OKF principles safely or to build a strict OKF bundle. The official sources are the [Google Cloud introduction](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) and the [OKF specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

## Contents

- Choose a mode
- Repository profile
- Strict OKF profile
- Frontmatter fields
- Paths, links, and citations
- Navigation filename rules
- Migration and versioning
- Validation

## Choose A Mode

### Repository Corpus (Default)

Use OKF ideas inside an ordinary repo documentation corpus:

- one durable concept per maintained page
- compact YAML frontmatter on new or meaningfully revised maintained pages
- stable paths
- normal Markdown cross-links
- claim-level citations
- progressive navigation through `README.md`, `INDEX.md`, and folder maps

Keep established uppercase spine files and AGENTS conventions. Call this **OKF-inspired**, not OKF-conformant.

### Strict OKF Bundle (Explicit)

Use a self-contained bundle root when the user explicitly asks for OKF conformance or portable exchange. Avoid mixing unrelated repo governance files into the bundle unless they are valid concept documents.

A strict v0.1 bundle requires:

- UTF-8 Markdown concept files with YAML frontmatter
- a non-empty `type` field in every non-reserved Markdown document
- lowercase `index.md` and `log.md` reserved for their specified purposes
- parseable frontmatter
- best-effort consumption of unknown types, extra keys, missing optional fields, and broken links

Do not claim conformance until the entire selected bundle passes these rules.

## Frontmatter Fields

Use the smallest useful metadata block:

```yaml
---
type: Product Scope
title: Dog Poop Tracker MLP Scope
description: Defines the current MLP product boundary.
resource: https://example.com/canonical-resource
tags: [product, mlp]
timestamp: 2026-07-11T00:00:00Z
status: active
source_refs:
  - _sources/product-brief.md
supersedes: []
superseded_by: []
---
```

Field responsibilities:

- `type`: required in strict OKF; recommended for maintained repository concepts. Keep type values descriptive and repo-local.
- `title`: human-readable display name.
- `description`: one-sentence summary used by indexes, previews, and retrieval.
- `resource`: canonical URI for the underlying asset described by the concept, when one exists.
- `tags`: cross-cutting classification that should not be encoded only in directory names.
- `timestamp`: ISO 8601 time of the last meaningful change.
- `status`: repo-local lifecycle extension such as draft, active, canonical, superseded, archived, or evidence.
- `source_refs`: repo-local paths or source IDs used to derive the maintained page.
- `supersedes` / `superseded_by`: repo-local lifecycle links.

OKF consumers must tolerate producer-defined extra fields. Do not create a global registry of allowed `type` values.

## Paths, Links, And Citations

- Treat the relative file path without `.md` as concept identity in strict bundles.
- Prefer stable paths. A move changes identity and requires link/provenance reconciliation.
- Use standard relative Markdown links or bundle-root links beginning with `/`.
- Express relationship meaning in nearby prose; links themselves are untyped graph edges.
- Warn about broken links during authoring, but do not treat them as strict OKF malformation.
- Put externally supported claims under a `# Citations` section when useful.

Keep these provenance surfaces distinct:

- `resource`: identity of the described external asset.
- `source_refs`: inputs used for synthesis.
- `# Citations`: support for claims in the body.
- `_meta/source-map.md`: corpus copy, rename, derivation, supersession, and removal history.

## Navigation Filename Rules

Repository profile:

- Keep `README.md`, `INDEX.md`, and `LOG.md` when that is the established convention.
- Do not create lowercase duplicates merely to look like OKF.

Strict OKF profile:

- Use lowercase `index.md` for optional directory listings and progressive disclosure.
- Use lowercase `log.md` for optional date-grouped update history.
- Permit `okf_version: "0.1"` frontmatter only on the bundle-root `index.md`.
- Treat uppercase `INDEX.md`, `LOG.md`, `README.md`, and `AGENTS.md` as ordinary concept documents; they therefore require valid frontmatter and `type` if placed inside the strict bundle.

## Migration And Versioning

- Adopt metadata incrementally for ordinary repository corpora.
- Do not retrofit immutable copied sources merely to increase frontmatter coverage.
- Do not mass-move existing concepts without an approved migration plan.
- Preserve incoming links or leave an explicit replacement/tombstone concept when consumers may still use the old identity.
- Pin strict bundles to the targeted OKF version and re-audit before upgrading.

## Validation

Run:

```bash
python3 scripts/audit_corpus.py /path/to/corpus --profile repo
python3 scripts/audit_corpus.py /path/to/bundle --profile okf
```

The repository profile reports navigation, numbering, link, source-map, and maintenance warnings. The OKF profile additionally blocks missing or invalid concept frontmatter, empty `type`, and misuse of reserved filenames.
