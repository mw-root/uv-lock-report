from semver import Version

from uv_lock_report.models import LockfilePackage, UpdatedPackage

ADDED_PACKAGES: list[LockfilePackage] = [
    LockfilePackage(name="added_1", version=Version(1, 0, 0)),
    LockfilePackage(name="added_2", version=Version(4, 2, 0)),
]
REMOVED_PACKAGES: list[LockfilePackage] = [
    LockfilePackage(name="removed_1", version=Version(1, 0, 0)),
    LockfilePackage(name="removed_2", version=Version(4, 2, 0)),
]
UPDATED_PACKAGES: list[UpdatedPackage] = [
    UpdatedPackage(
        name="updated_1", old_version=Version(1, 0, 0), new_version=Version(2, 0, 0)
    ),
    UpdatedPackage(
        name="updated_2", old_version=Version(1, 0, 0), new_version=Version(2, 0, 0)
    ),
]

EXPECTED_LOCKFILE_CHANGES_FULL_MARKDOWN = """
# uv Lockfile Report
## Added Packages
| Package | Version |
|--|--|
| added_1 | 1.0.0 |
| added_2 | 4.2.0 |
## Changed Packages
| Package | Old Version | New Version |
|--|--|--|
| updated_1 | 1.0.0 | 2.0.0 |
| updated_2 | 1.0.0 | 2.0.0 |
## Removed Packages
| Package | Version |
|--|--|
| removed_1 | 1.0.0 |
| removed_2 | 4.2.0 |
""".strip()


EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP = {
    "added": [
        {"name": "added_1", "version": "1.0.0"},
        {"name": "added_2", "version": "4.2.0"},
    ],
    "items": 6,
    "markdown": "# uv Lockfile Report\n"
    "## Added Packages\n"
    "| Package | Version |\n"
    "|--|--|\n"
    "| added_1 | 1.0.0 |\n"
    "| added_2 | 4.2.0 |\n"
    "## Changed Packages\n"
    "| Package | Old Version | New Version |\n"
    "|--|--|--|\n"
    "| updated_1 | 1.0.0 | 2.0.0 |\n"
    "| updated_2 | 1.0.0 | 2.0.0 |\n"
    "## Removed Packages\n"
    "| Package | Version |\n"
    "|--|--|\n"
    "| removed_1 | 1.0.0 |\n"
    "| removed_2 | 4.2.0 |",
    "removed": [
        {"name": "removed_1", "version": "1.0.0"},
        {"name": "removed_2", "version": "4.2.0"},
    ],
    "updated": [
        {"name": "updated_1", "new_version": "2.0.0", "old_version": "1.0.0"},
        {"name": "updated_2", "new_version": "2.0.0", "old_version": "1.0.0"},
    ],
}
