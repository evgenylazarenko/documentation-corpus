#!/usr/bin/env python3
"""Read-only audit for repository documentation corpora and strict OKF bundles."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - environment dependent
    yaml = None


EXCLUDED_PARTS = {
    ".git",
    ".build",
    "DerivedData",
    "node_modules",
    "vendor",
}
NUMBERED_LANE_RE = re.compile(r"^(\d{2})-[a-z0-9][a-z0-9-]*$")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
DATE_HEADING_RE = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}\s*$")
TOP_LEVEL_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")
SPINE_FILES = {"README.md", "INDEX.md", "SCHEMA.md", "STATUS.md", "LOG.md"}
NON_CONTENT_FILES = SPINE_FILES | {"AGENTS.md"}
NON_MAINTAINED_DIRS = {"_meta", "_sources", "_templates", "wip"}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("corpus_root", type=Path, help="Documentation or OKF bundle root")
    parser.add_argument(
        "--profile",
        choices=("repo", "okf"),
        default="repo",
        help="Audit an ordinary repository corpus or strict OKF bundle",
    )
    parser.add_argument(
        "--max-agents-lines",
        type=int,
        default=80,
        help="Warn when an AGENTS.md file exceeds this line count",
    )
    return parser.parse_args()


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDED_PARTS for part in path.relative_to(root).parts)
    )


def split_frontmatter(text: str) -> tuple[str | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :])
    return "", text


def parse_frontmatter(block: str, path: Path, report: Report) -> dict[str, object] | None:
    if yaml is not None:
        try:
            value = yaml.safe_load(block)
        except Exception as exc:  # noqa: BLE001 - report parser detail
            report.error(f"{path}: invalid YAML frontmatter: {exc}")
            return None
        if value is None:
            return {}
        if not isinstance(value, dict):
            report.error(f"{path}: frontmatter must be a YAML mapping")
            return None
        return value

    data: dict[str, object] = {}
    for line in block.splitlines():
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = TOP_LEVEL_KEY_RE.match(line)
        if match:
            data[match.group(1)] = (match.group(2) or "").strip().strip('"\'')
    return data


def resolve_local_target(root: Path, source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split("#", 1)[0].strip()
    if not target or target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "app://")):
        return None
    target = unquote(target)
    if " " in target and not target.startswith("/"):
        target = target.split(" ", 1)[0]
    if target.startswith(("/Users/", "/private/", "/tmp/")):
        target = re.sub(r":\d+(?::\d+)?$", "", target)
        return Path(target).resolve()
    if target.startswith("/"):
        return (root / target.lstrip("/")).resolve()
    return (source.parent / target).resolve()


def audit_common(root: Path, files: list[Path], max_agents_lines: int, report: Report) -> None:
    root_resolved = root.resolve()
    trailing: list[str] = []
    broken_links: list[str] = []
    for path in files:
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        preserved_material = bool(relative.parts) and (
            relative.parts[0] == "_sources" or "archive" in relative.parts[0].lower()
        )
        if not preserved_material:
            for number, line in enumerate(text.splitlines(), start=1):
                markdown_hard_break = line.endswith("  ") and not line.endswith("   ")
                if line.rstrip() != line and not markdown_hard_break:
                    trailing.append(f"{relative}:{number}")
        if path.name == "AGENTS.md":
            line_count = len(text.splitlines())
            if line_count > max_agents_lines:
                report.warn(f"{relative}: {line_count} lines exceeds AGENTS.md limit {max_agents_lines}")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = resolve_local_target(root, path, raw_target)
            if target is None:
                continue
            try:
                target.relative_to(root_resolved)
            except ValueError:
                # Links outside the corpus may point at code, source repos, or
                # renderer-specific file targets. Corpus mode does not own them.
                continue
            if not target.exists():
                broken_links.append(f"{relative} -> {raw_target}")

    if trailing:
        sample = ", ".join(trailing[:10])
        suffix = "" if len(trailing) <= 10 else f" (+{len(trailing) - 10} more)"
        report.warn(f"trailing whitespace at {sample}{suffix}")
    if broken_links:
        sample = ", ".join(broken_links[:10])
        suffix = "" if len(broken_links) <= 10 else f" (+{len(broken_links) - 10} more)"
        report.warn(f"broken local links: {sample}{suffix}")


def audit_repo(root: Path, files: list[Path], report: Report) -> None:
    top_dirs = sorted(path for path in root.iterdir() if path.is_dir() and not path.name.startswith("."))
    numbered: list[tuple[int, Path]] = []
    unnumbered: list[str] = []
    prefixes: dict[int, list[str]] = {}

    for path in top_dirs:
        match = NUMBERED_LANE_RE.match(path.name)
        if match:
            prefix = int(match.group(1))
            numbered.append((prefix, path))
            prefixes.setdefault(prefix, []).append(path.name)
            durable = [
                item
                for item in path.rglob("*.md")
                if item.name not in {"README.md", "AGENTS.md"}
            ]
            if not durable:
                report.warn(f"{path.name}/: numbered lane has no durable pages beyond routing files")
        elif path.name not in NON_MAINTAINED_DIRS:
            unnumbered.append(path.name)

    if numbered:
        report.note("numbered lanes: " + ", ".join(path.name for _, path in numbered))
    else:
        report.note("no numbered maintained lanes found; preserve an established unnumbered taxonomy or plan a migration")
    if unnumbered:
        report.note("unnumbered top-level directories preserved for review: " + ", ".join(unnumbered))
    for prefix, names in sorted(prefixes.items()):
        if len(names) > 1:
            report.warn(f"duplicate numbered prefix {prefix:02d}: {', '.join(names)}")

    if not (root / "README.md").exists():
        report.warn("README.md is missing from the corpus root")
    missing_spine = sorted(name for name in SPINE_FILES if not (root / name).exists())
    if missing_spine:
        report.note("optional spine files not present: " + ", ".join(missing_spine))

    index_path = root / "INDEX.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        missing_index: list[str] = []
        for path in files:
            relative = path.relative_to(root)
            if path.name in NON_CONTENT_FILES:
                continue
            if relative.parts and (
                relative.parts[0] in NON_MAINTAINED_DIRS
                or "archive" in relative.parts[0].lower()
            ):
                continue
            relative_text = relative.as_posix()
            if relative_text not in index_text and path.name not in index_text:
                missing_index.append(relative_text)
        if missing_index:
            sample = ", ".join(missing_index[:10])
            suffix = "" if len(missing_index) <= 10 else f" (+{len(missing_index) - 10} more)"
            report.note(f"INDEX.md is curated and does not list every maintained page: {sample}{suffix}")

    sources_root = root / "_sources"
    if sources_root.exists():
        source_map = root / "_meta" / "source-map.md"
        if not source_map.exists():
            report.warn("_sources/ exists but _meta/source-map.md is missing")
        else:
            source_map_text = source_map.read_text(encoding="utf-8")
            source_files = [
                path
                for path in sources_root.rglob("*")
                if path.is_file() and path.name not in {".DS_Store", "README.md", "AGENTS.md"}
            ]
            if "_sources" not in source_map_text:
                report.warn("_meta/source-map.md does not mention the _sources evidence layer")
            else:
                report.note(f"source map present for _sources/ ({len(source_files)} evidence files)")


def audit_okf(root: Path, files: list[Path], report: Report) -> None:
    if yaml is None:
        report.warn("PyYAML is unavailable; frontmatter key presence is checked but full YAML parsing is not verified")

    root_index = root / "index.md"
    if not root_index.exists():
        report.note("root index.md is optional and not present")

    for path in files:
        relative = path.relative_to(root)
        text = path.read_text(encoding="utf-8")
        block, body = split_frontmatter(text)

        if path.name == "index.md":
            if block is not None:
                if relative != Path("index.md"):
                    report.error(f"{relative}: frontmatter is permitted only on bundle-root index.md")
                else:
                    data = parse_frontmatter(block, relative, report)
                    if data is not None and "okf_version" not in data:
                        report.error(f"{relative}: root index.md frontmatter may only be used to declare okf_version")
            if not body.strip():
                report.warn(f"{relative}: index.md is empty")
            continue

        if path.name == "log.md":
            if block is not None:
                report.error(f"{relative}: log.md must not contain frontmatter")
            for line in body.splitlines():
                if line.startswith("## ") and not DATE_HEADING_RE.match(line):
                    report.error(f"{relative}: log date heading must use YYYY-MM-DD: {line}")
            continue

        if block is None:
            report.error(f"{relative}: concept document is missing YAML frontmatter")
            continue
        if block == "":
            report.error(f"{relative}: frontmatter opening delimiter has no closing delimiter")
            continue
        data = parse_frontmatter(block, relative, report)
        if data is None:
            continue
        concept_type = data.get("type")
        if not isinstance(concept_type, str) or not concept_type.strip():
            report.error(f"{relative}: concept frontmatter requires a non-empty type field")


def print_report(root: Path, profile: str, files: list[Path], report: Report) -> None:
    print(f"Corpus audit: root={root} profile={profile} markdown={len(files)}")
    for label, messages in (
        ("ERROR", report.errors),
        ("WARN", report.warnings),
        ("NOTE", report.notes),
    ):
        for message in messages:
            print(f"{label}: {message}")
    print(
        f"Summary: errors={len(report.errors)} warnings={len(report.warnings)} notes={len(report.notes)}"
    )


def main() -> int:
    args = parse_args()
    root = args.corpus_root.expanduser().resolve()
    report = Report()

    if not root.is_dir():
        print(f"ERROR: corpus root is not a directory: {root}", file=sys.stderr)
        return 2

    files = markdown_files(root)
    if not files:
        report.warn("no Markdown files found")

    audit_common(root, files, args.max_agents_lines, report)
    if args.profile == "repo":
        audit_repo(root, files, report)
    else:
        audit_okf(root, files, report)

    print_report(root, args.profile, files, report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
