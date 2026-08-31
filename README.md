# Documentation Corpus

Documentation Corpus is a Codex skill for organizing repository documentation into a small knowledge base with an intent to make the repo easier for AI agents to understand.

It keeps raw sources separate from authoritative documentation, creates only the navigation files a project will use, and leaves room to grow without filling the repository with empty folders. It can establish a new documentation tree, repair an existing one, migrate source material, or audit a corpus for structural problems.

## What it does

- Organizes maintained documentation into sparse, numbered sections.
- Keeps copied evidence immutable in `_sources/` by default.
- Records provenance for copied, moved, generated, or superseded material.
- Maintains useful entry points such as `README.md`, `INDEX.md`, and `_meta/source-map.md` when the repository needs them.
- Audits ordinary repository corpora and optional strict Open Knowledge Format bundles.

The default is an ordinary repository corpus. Strict Open Knowledge Format conformance is opt-in and uses a separate profile.

## Install

Install the skill:

```bash
npx skills add evgenylazarenko/documentation-corpus
```

Or clone the repository into your Codex skills directory:

```bash
git clone https://github.com/evgenylazarenko/documentation-corpus.git ~/.codex/skills/documentation-corpus
```

Then ask Codex to use the skill, for example:

```text
Use $documentation-corpus to organize this repository's documentation.
```

## What's included

- [`SKILL.md`](SKILL.md): the workflow and decision rules.
- [`references/corpus-pattern.md`](references/corpus-pattern.md): the default numbered repository pattern.
- [`references/okf-profile.md`](references/okf-profile.md): guidance for OKF-inspired metadata and strict bundles.
- [`scripts/audit_corpus.py`](scripts/audit_corpus.py): a read-only structural auditor.

## Inspirations

This skill was inspired by [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), especially its separation of immutable sources from a maintained, interlinked wiki.

It also draws on Google's [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), a portable format for knowledge stored as Markdown with structured frontmatter. The skill borrows those ideas where they help ordinary repositories without requiring every corpus to become a strict OKF bundle.
