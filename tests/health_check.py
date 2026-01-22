from pathlib import Path
import json

HEALTH_DIR = Path("health")
HEALTH_DIR.mkdir(exist_ok=True)

REQUIRED_FILES = ["README.md", "LICENSE", ".gitignore"]
REQUIRED_DIRS = ["tests", ".github/workflows"]

def check_repo():
    missing_files = [f for f in REQUIRED_FILES if not Path(f).exists()]
    missing_dirs = [d for d in REQUIRED_DIRS if not Path(d).exists()]

    status = "PASS" if (not missing_files and not missing_dirs) else "FAIL"

    return {
        "status": status,
        "missing_files": missing_files,
        "missing_dirs": missing_dirs
    }

def write_reports(result):
    (HEALTH_DIR / "report.json").write_text(json.dumps(result, indent=2))

    md = "# Repo Health Report\n\n"
    md += f"**Status:** {result['status']}\n\n"

    md += "## Missing Files\n"
    md += "\n".join([f"- {x}" for x in result["missing_files"]]) or "None"
    md += "\n\n## Missing Directories\n"
    md += "\n".join([f"- {x}" for x in result["missing_dirs"]]) or "None"
    md += "\n"

    (HEALTH_DIR / "report.md").write_text(md)

def update_readme_badge(status):
    readme = Path("README.md")
    if not readme.exists():
        return

    badge = "✅ Repo Health: PASS" if status == "PASS" else "❌ Repo Health: FAIL"

    text = readme.read_text()

    # If badge line exists, replace it. Otherwise add it at top.
    lines = text.splitlines()
    if lines and lines[0].startswith(("✅ Repo Health:", "❌ Repo Health:")):
        lines[0] = badge
        new_text = "\n".join(lines)
    else:
        new_text = badge + "\n\n" + text

    readme.write_text(new_text)

if __name__ == "__main__":
    result = check_repo()
    write_reports(result)
    update_readme_badge(result["status"])

    # Fail the pipeline if FAIL
    if result["status"] == "FAIL":
        raise SystemExit("Repo health check failed")
