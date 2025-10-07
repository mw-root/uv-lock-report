from uv_lock_report.models import LockfileChanges

from .conftest import (
    ADDED_PACKAGES,
    EXPECTED_LOCKFILE_CHANGES_FULL_MARKDOWN,
    EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP,
    REMOVED_PACKAGES,
    UPDATED_PACKAGES,
)


class TestLockfileChanges:
    def test_empty_markdown(self):
        lfc = LockfileChanges()
        assert lfc.markdown == "# uv Lockfile Report"

    def test_full_markdown(self):
        lfc = LockfileChanges(
            added=ADDED_PACKAGES, updated=UPDATED_PACKAGES, removed=REMOVED_PACKAGES
        )
        assert lfc.markdown == EXPECTED_LOCKFILE_CHANGES_FULL_MARKDOWN
        assert lfc.items == len(ADDED_PACKAGES) + len(UPDATED_PACKAGES) + len(
            REMOVED_PACKAGES
        )
        assert lfc.model_dump() == EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP
