from uv_lock_report.models import LockfileChanges, OutputFormat, RequiresPythonChanges

from .conftest import (
    ADDED_PACKAGES,
    EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE,
    EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE_WITH_LINK,
    EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_TABLE,
    EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE,
    EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE_WITH_LINK,
    EXPECTED_LOCKFILE_CHANGES_FULL_TABLE,
    REMOVED_PACKAGES,
    UPDATED_PACKAGES,
)


class TestLockfileChanges:
    def test_empty_markdown(self):
        lfc = LockfileChanges(
            requires_python=RequiresPythonChanges(old=None, new=None),
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )
        assert lfc.markdown == "## uv Lockfile Report"

    def test_full_markdown_table(self):
        lfc = LockfileChanges(
            requires_python=RequiresPythonChanges(old=None, new=None),
            added=ADDED_PACKAGES,
            updated=UPDATED_PACKAGES,
            removed=REMOVED_PACKAGES,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )
        assert lfc.markdown == EXPECTED_LOCKFILE_CHANGES_FULL_TABLE
        assert lfc.items == len(ADDED_PACKAGES) + len(UPDATED_PACKAGES) + len(
            REMOVED_PACKAGES
        )
        assert lfc.model_dump() == EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_TABLE

    def test_full_markdown_simple(self):
        lfc = LockfileChanges(
            requires_python=RequiresPythonChanges(old=None, new=None),
            added=ADDED_PACKAGES,
            updated=UPDATED_PACKAGES,
            removed=REMOVED_PACKAGES,
            output_format=OutputFormat.SIMPLE,
            show_learn_more_link=False,
        )
        assert lfc.markdown == EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE
        assert lfc.items == len(ADDED_PACKAGES) + len(UPDATED_PACKAGES) + len(
            REMOVED_PACKAGES
        )
        assert lfc.model_dump() == EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE

    def test_full_markdown_simple_with_learn_more_link(self):
        lfc = LockfileChanges(
            requires_python=RequiresPythonChanges(old=None, new=None),
            added=ADDED_PACKAGES,
            updated=UPDATED_PACKAGES,
            removed=REMOVED_PACKAGES,
            output_format=OutputFormat.SIMPLE,
            show_learn_more_link=True,
        )
        assert lfc.markdown == EXPECTED_LOCKFILE_CHANGES_FULL_SIMPLE_WITH_LINK
        assert lfc.items == len(ADDED_PACKAGES) + len(UPDATED_PACKAGES) + len(
            REMOVED_PACKAGES
        )
        assert (
            lfc.model_dump()
            == EXPECTED_LOCKFILE_CHANGES_FULL_MODEL_DUMP_SIMPLE_WITH_LINK
        )
