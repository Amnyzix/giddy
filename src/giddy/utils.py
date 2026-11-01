import re
from pathlib import Path


def clean_branch_name(branch_type: str, raw_name: str) -> str:
    """
    Clean the feature name to create a valid Git branch name.
    """
    clean_name = raw_name.strip().lower().replace(" ", "-").replace("_", "-")
    clean_name = re.sub(r"[^a-z0-9-]", "", clean_name)  # Remove special characters
    clean_name = re.sub(r"-+", "-", clean_name)  # Prevent multiple consecutive dashes
    clean_name = clean_name.strip("-")  # Remove leading/trailing dashes

    if not clean_name:
        return ""

    return f"{branch_type}/{clean_name}"


def append_to_gitignore(file_path: str) -> None:
    """Append a file or folder path to the .gitignore file safely."""
    gitignore_path = Path(".gitignore")

    # if the file already exists, check if it's not already there to avoid duplicates
    if gitignore_path.is_file():
        with open(gitignore_path, "r", encoding="utf-8") as f:
            existing_lines = [line.strip() for line in f.readlines()]
        if file_path in existing_lines:
            return  # Already present, nothing to do!

    # add it properly to the end of the file
    with open(gitignore_path, "a", encoding="utf-8") as f:
        f.write(f"\n{file_path}\n")


def parse_version(tag: str) -> tuple[int, int, int]:
    """Parse a tag string (like 'v1.2.3' or '1.2.3') into major, minor, patch."""
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", tag)
    if match:
        return int(match.group(1)), int(match.group(2)), int(match.group(3))
    return 0, 0, 0  # Fallback if the last tag was formatted badly
