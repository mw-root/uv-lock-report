from uv_lock_report.models import LockfilePackage, OutputFormat, UpdatedPackage

ADDED_PACKAGES: list[LockfilePackage] = [
    LockfilePackage(name="added_1", version="1.0.0"),
    LockfilePackage(name="added_2", version="4.2.0"),
]
REMOVED_PACKAGES: list[LockfilePackage] = [
    LockfilePackage(name="removed_1", version="1.0.0"),
    LockfilePackage(name="removed_2", version="4.2.0"),
]
UPDATED_PACKAGES: list[UpdatedPackage] = [
    UpdatedPackage(name="updated_1", old_version="1.0.0", new_version="2.0.0"),
    UpdatedPackage(name="updated_2", old_version="1.0.0", new_version="2.0.0"),
]

EXPECTED_LOCKFILE_CHANGES_FULL_TABLE = """
## uv Lockfile Report
### Added Packages
| Package | Version |
|--|--|
| added_1 | 1.0.0 |
| added_2 | 4.2.0 |
### Changed Packages
| Package | Old Version | New Version |
|--|--|--|
| updated_1 | 1.0.0 | 2.0.0 |
| updated_2 | 1.0.0 | 2.0.0 |
### Removed Packages
| Package | Version |
|--|--|
| removed_1 | 1.0.0 |
| removed_2 | 4.2.0 |
""".strip()

EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE = """
## uv Lockfile Report
### Added Packages
\\`added_1\\`: \\`1.0.0\\`
\\`added_2\\`: \\`4.2.0\\`
### Changed Packages
:collision: \\`updated_1\\`: \\`1.0.0\\` -> \\`2.0.0\\`
:collision: \\`updated_2\\`: \\`1.0.0\\` -> \\`2.0.0\\`
### Removed Packages
\\`removed_1\\`: \\`1.0.0\\`
\\`removed_2\\`: \\`4.2.0\\`
""".strip()


EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE_WITH_LINK = """
## uv Lockfile Report
### Added Packages
\\`added_1\\`: \\`1.0.0\\`
\\`added_2\\`: \\`4.2.0\\`
### Changed Packages
:collision: \\`updated_1\\`: \\`1.0.0\\` -> \\`2.0.0\\`
:collision: \\`updated_2\\`: \\`1.0.0\\` -> \\`2.0.0\\`
### Removed Packages
\\`removed_1\\`: \\`1.0.0\\`
\\`removed_2\\`: \\`4.2.0\\`

---
Learn more about this report at https://github.com/mw-root/uv-lock-report
""".strip()


EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_TABLE = {
    "added": [
        {"name": "added_1", "version": "1.0.0"},
        {"name": "added_2", "version": "4.2.0"},
    ],
    "items": 6,
    "learn_more_link_text": "\n---\nLearn more about this report at https://github.com/mw-root/uv-lock-report",
    "markdown": EXPECTED_LOCKFILE_CHANGES_FULL_TABLE,
    "markdown_simple": EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE,
    "markdown_table": EXPECTED_LOCKFILE_CHANGES_FULL_TABLE,
    "output_format": OutputFormat.TABLE,
    "removed": [
        {"name": "removed_1", "version": "1.0.0"},
        {"name": "removed_2", "version": "4.2.0"},
    ],
    "requires_python": {"new": None, "old": None},
    "show_learn_more_link": False,
    "updated": [
        {"name": "updated_1", "new_version": "2.0.0", "old_version": "1.0.0"},
        {"name": "updated_2", "new_version": "2.0.0", "old_version": "1.0.0"},
    ],
}


EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE = {
    "added": [
        {"name": "added_1", "version": "1.0.0"},
        {"name": "added_2", "version": "4.2.0"},
    ],
    "items": 6,
    "learn_more_link_text": "\n---\nLearn more about this report at https://github.com/mw-root/uv-lock-report",
    "markdown": EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE,
    "markdown_simple": EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE,
    "markdown_table": EXPECTED_LOCKFILE_CHANGES_FULL_TABLE,
    "output_format": OutputFormat.SIMPLE,
    "removed": [
        {"name": "removed_1", "version": "1.0.0"},
        {"name": "removed_2", "version": "4.2.0"},
    ],
    "requires_python": {"new": None, "old": None},
    "show_learn_more_link": False,
    "updated": [
        {"name": "updated_1", "new_version": "2.0.0", "old_version": "1.0.0"},
        {"name": "updated_2", "new_version": "2.0.0", "old_version": "1.0.0"},
    ],
}

EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE_WITH_LINK = {
    "added": [
        {"name": "added_1", "version": "1.0.0"},
        {"name": "added_2", "version": "4.2.0"},
    ],
    "items": 6,
    "learn_more_link_text": "\n---\nLearn more about this report at https://github.com/mw-root/uv-lock-report",
    "markdown": EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE_WITH_LINK,
    "markdown_simple": EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE_WITH_LINK,
    "markdown_table": EXPECTED_LOCKFILE_CHANGES_FULL_TABLE,
    "output_format": OutputFormat.SIMPLE,
    "removed": [
        {"name": "removed_1", "version": "1.0.0"},
        {"name": "removed_2", "version": "4.2.0"},
    ],
    "requires_python": {"new": None, "old": None},
    "show_learn_more_link": True,
    "updated": [
        {"name": "updated_1", "new_version": "2.0.0", "old_version": "1.0.0"},
        {"name": "updated_2", "new_version": "2.0.0", "old_version": "1.0.0"},
    ],
}
