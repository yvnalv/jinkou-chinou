#!/usr/bin/env python3
"""
Lightweight repository inventory for the the-architect skill.

Usage:
    python scripts/scan_repo.py [repo_path] [--summary]

Outputs JSON to stdout. It intentionally avoids reading file contents,
which makes it suitable as a first-pass mechanical inventory.

--summary  Omit the per-file list (use on large repositories). Categories,
           top-level counts, important files, and sub-projects are kept.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

IGNORE_DIRS = {
    # VCS / IDE
    ".git", ".hg", ".svn", ".vs", ".idea", ".vscode",
    # JavaScript / TypeScript
    "node_modules", "dist", "coverage", ".next", ".nuxt", ".svelte-kit",
    ".angular", ".turbo", ".expo", ".cache",
    # .NET / Java / Kotlin / Rust
    "bin", "obj", "target", ".gradle",
    # Python
    "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".tox", ".ipynb_checkpoints",
    # Mobile
    "Pods", "DerivedData", ".dart_tool",
    # Infrastructure
    ".terraform",
    # Systems / embedded
    ".pio",
    # Generic build output and vendored dependencies
    "build", "vendor",
}

IGNORE_DIR_PREFIXES = ("cmake-build-",)

EXTENSIONS = {
    ".cs": "csharp",
    ".csproj": "dotnet-project",
    ".fsproj": "dotnet-project",
    ".sln": "dotnet-solution",
    ".fs": "fsharp",
    ".cshtml": "razor",
    ".razor": "razor",
    ".java": "java",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".scala": "scala",
    ".py": "python",
    ".ipynb": "jupyter-notebook",
    ".go": "go",
    ".php": "php",
    ".rb": "ruby",
    ".rs": "rust",
    ".ex": "elixir",
    ".exs": "elixir",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".jsx": "javascript-react",
    ".ts": "typescript",
    ".tsx": "typescript-react",
    ".vue": "vue",
    ".svelte": "svelte",
    ".html": "html",
    ".css": "stylesheet",
    ".scss": "stylesheet",
    ".swift": "swift",
    ".m": "objective-c",
    ".dart": "dart",
    ".c": "c",
    ".h": "c-cpp-header",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "c-cpp-header",
    ".ino": "arduino",
    ".gd": "godot-script",
    ".sql": "sql",
    ".proto": "protobuf",
    ".graphql": "graphql",
    ".tf": "terraform",
    ".bicep": "bicep",
    ".sh": "shell",
    ".ps1": "powershell",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".xml": "xml",
    ".md": "markdown",
}

# Files whose presence marks a project root (used to build the sub-project map).
MANIFESTS = {
    "package.json", "pyproject.toml", "setup.py", "go.mod", "Cargo.toml",
    "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
    "Gemfile", "pubspec.yaml", "Package.swift", "mix.exs", "build.sbt",
    "dbt_project.yml", "Chart.yaml", "project.godot", "platformio.ini",
    "CMakeLists.txt", "meson.build", "Pulumi.yaml",
}
MANIFEST_SUFFIXES = {".csproj", ".fsproj", ".uproject", ".tf", ".bicep"}

IMPORTANT_FILENAMES = MANIFESTS | {
    # JavaScript / TypeScript
    "pnpm-lock.yaml", "yarn.lock", "package-lock.json", "tsconfig.json",
    "angular.json", "vite.config.ts", "vite.config.js",
    "next.config.js", "next.config.mjs", "next.config.ts",
    "nuxt.config.ts", "svelte.config.js", "metro.config.js",
    # Python
    "requirements.txt", "poetry.lock", "Pipfile", "environment.yml",
    # JVM / .NET
    "settings.gradle", "settings.gradle.kts", "global.json",
    "Directory.Build.props", "appsettings.json",
    # Mobile
    "Podfile", "AndroidManifest.xml",
    # Systems / embedded
    "CMakeLists.txt", "Makefile", "meson.build", "vcpkg.json",
    # Infrastructure / CI
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "kustomization.yaml", "serverless.yml", "host.json", "Pulumi.yaml",
    ".gitlab-ci.yml", "azure-pipelines.yml", "bitbucket-pipelines.yml",
    "Jenkinsfile",
    # Game engines
    "ProjectVersion.txt",
    # Repository hygiene and planning docs
    ".gitignore", ".env.example", "CLAUDE.md", "PROJECT_GUIDE.md",
    "PRD.md", "MIGRATION_BRIEF.md", "ARCHITECTURE.md",
    "IMPLEMENTATION_PLAN.md",
}
IMPORTANT_SUFFIXES = {".sln", ".csproj", ".fsproj", ".uproject"}
IMPORTANT_DIR_SUFFIXES = {".xcodeproj", ".xcworkspace"}
IMPORTANT_PATH_PREFIXES = (".github/workflows/",)


def is_ignored(dirname: str) -> bool:
    return dirname in IGNORE_DIRS or dirname.startswith(IGNORE_DIR_PREFIXES)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repo_path", nargs="?", default=".")
    parser.add_argument("--summary", action="store_true", help="omit the per-file list")
    args = parser.parse_args()

    root = Path(args.repo_path).resolve()
    counts: dict[str, int] = {}
    top_level: dict[str, int] = {}
    files = []
    important = []
    projects: dict[str, set[str]] = {}

    for current, dirs, names in os.walk(root):
        current_path = Path(current)
        rel_dir = current_path.relative_to(root).as_posix()
        rel_dir = "" if rel_dir == "." else rel_dir

        for d in dirs:
            if Path(d).suffix in IMPORTANT_DIR_SUFFIXES:
                important.append({"path": f"{rel_dir}/{d}".lstrip("/"), "category": "xcode-project", "size": None})
                projects.setdefault(rel_dir or ".", set()).add(d)
        dirs[:] = [d for d in dirs if not is_ignored(d) and Path(d).suffix not in IMPORTANT_DIR_SUFFIXES]

        for name in names:
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()
            category = EXTENSIONS.get(suffix, "other")
            counts[category] = counts.get(category, 0) + 1

            segment = rel.split("/", 1)[0] if "/" in rel else "(root)"
            top_level[segment] = top_level.get(segment, 0) + 1

            try:
                size = path.stat().st_size
            except OSError:  # broken symlink or permission error
                size = None

            record = {"path": rel, "category": category, "size": size}
            files.append(record)

            if (name in IMPORTANT_FILENAMES or suffix in IMPORTANT_SUFFIXES
                    or rel.startswith(IMPORTANT_PATH_PREFIXES)):
                important.append(record)

            if name in MANIFESTS or suffix in MANIFEST_SUFFIXES:
                projects.setdefault(rel_dir or ".", set()).add(name)

    result = {
        "repository": str(root),
        "file_count": len(files),
        "categories": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
        "top_level": dict(sorted(top_level.items(), key=lambda kv: -kv[1])),
        "projects": [
            {"path": p, "manifests": sorted(m)} for p, m in sorted(projects.items())
        ],
        "important_files": sorted(important, key=lambda x: x["path"]),
    }
    if not args.summary:
        result["files"] = sorted(files, key=lambda x: x["path"])

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
