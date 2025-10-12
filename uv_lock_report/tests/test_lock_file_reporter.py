from semver import Version

from uv_lock_report.models import (
    LockFile,
    LockfilePackage,
    LockFileReporter,
    LockFileType,
    OutputFormat,
)


class TestLockFileReporter:
    """Test the LockFileReporter class for comparing lockfiles and detecting changes."""

    def test_both_lockfiles_none(self):
        """Test when both old and new lockfiles are None."""
        reporter = LockFileReporter(
            old_lockfile=None, new_lockfile=None, output_format=OutputFormat.TABLE
        )

        assert reporter.added_package_names == set()
        assert reporter.removed_package_names == set()
        assert reporter.both_lockfile_package_names == set()

        changes = reporter.get_changes()
        assert changes.added == []
        assert changes.removed == []
        assert changes.updated == []
        assert changes.items == 0

    def test_old_lockfile_none_new_lockfile_has_packages(self):
        """Test when old lockfile is None and new lockfile has packages (initial lockfile)."""
        new_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
        ]
        new_lockfile = LockFile(
            type=LockFileType.UV,
            packages=new_packages,
        )
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == {"pkg1", "pkg2"}
        assert reporter.removed_package_names == set()
        assert reporter.both_lockfile_package_names == set()

        changes = reporter.get_changes()
        assert len(changes.added) == 2
        assert changes.removed == []
        assert changes.updated == []
        assert changes.items == 2

    def test_new_lockfile_none_old_lockfile_has_packages(self):
        """Test when new lockfile is None and old lockfile has packages (lockfile deleted)."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
        ]
        old_lockfile = LockFile(
            type=LockFileType.UV,
            packages=old_packages,
        )
        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == set()
        assert reporter.removed_package_names == {"pkg1", "pkg2"}
        assert reporter.both_lockfile_package_names == set()

        changes = reporter.get_changes()
        assert changes.added == []
        assert len(changes.removed) == 2
        assert changes.updated == []
        assert changes.items == 2

    def test_no_changes(self):
        """Test when both lockfiles are identical."""
        packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == set()
        assert reporter.removed_package_names == set()
        assert reporter.both_lockfile_package_names == {"pkg1", "pkg2"}

        changes = reporter.get_changes()
        assert changes.added == []
        assert changes.removed == []
        assert changes.updated == []
        assert changes.items == 0

    def test_added_packages_only(self):
        """Test when only new packages are added."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
            LockfilePackage(name="pkg3", version=Version(3, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == {"pkg2", "pkg3"}
        assert reporter.removed_package_names == set()
        assert reporter.both_lockfile_package_names == {"pkg1"}

        changes = reporter.get_changes()
        assert len(changes.added) == 2
        assert {pkg.name for pkg in changes.added} == {"pkg2", "pkg3"}
        assert changes.removed == []
        assert changes.updated == []
        assert changes.items == 2

    def test_removed_packages_only(self):
        """Test when only packages are removed."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
            LockfilePackage(name="pkg3", version=Version(3, 0, 0)),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == set()
        assert reporter.removed_package_names == {"pkg2", "pkg3"}
        assert reporter.both_lockfile_package_names == {"pkg1"}

        changes = reporter.get_changes()
        assert changes.added == []
        assert len(changes.removed) == 2
        assert {pkg.name for pkg in changes.removed} == {"pkg2", "pkg3"}
        assert changes.updated == []
        assert changes.items == 2

    def test_updated_packages_only(self):
        """Test when only package versions are updated."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 5, 0)),
            LockfilePackage(name="pkg2", version=Version(3, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == set()
        assert reporter.removed_package_names == set()
        assert reporter.both_lockfile_package_names == {"pkg1", "pkg2"}

        changes = reporter.get_changes()
        assert changes.added == []
        assert changes.removed == []
        assert len(changes.updated) == 2
        assert changes.items == 2

        # Verify the update details
        updates_by_name = {pkg.name: pkg for pkg in changes.updated}
        assert updates_by_name["pkg1"].old_version == Version(1, 0, 0)
        assert updates_by_name["pkg1"].new_version == Version(1, 5, 0)
        assert updates_by_name["pkg2"].old_version == Version(2, 0, 0)
        assert updates_by_name["pkg2"].new_version == Version(3, 0, 0)

    def test_mixed_changes(self):
        """Test when packages are added, removed, and updated."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
            LockfilePackage(name="pkg3", version=Version(3, 0, 0)),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 5, 0)),  # Updated
            LockfilePackage(name="pkg3", version=Version(3, 0, 0)),  # Unchanged
            LockfilePackage(name="pkg4", version=Version(4, 0, 0)),  # Added
        ]
        # pkg2 is removed

        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        assert reporter.added_package_names == {"pkg4"}
        assert reporter.removed_package_names == {"pkg2"}
        assert reporter.both_lockfile_package_names == {"pkg1", "pkg3"}

        changes = reporter.get_changes()
        assert len(changes.added) == 1
        assert changes.added[0].name == "pkg4"

        assert len(changes.removed) == 1
        assert changes.removed[0].name == "pkg2"

        assert len(changes.updated) == 1
        assert changes.updated[0].name == "pkg1"
        assert changes.updated[0].old_version == Version(1, 0, 0)
        assert changes.updated[0].new_version == Version(1, 5, 0)

        assert changes.items == 3

    def test_package_version_string_handling(self):
        """Test packages with string versions (malformed versions)."""
        old_packages = [
            LockfilePackage(name="pkg1", version="2.9.0.post0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="2.10.0.post0"),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        changes = reporter.get_changes()
        assert len(changes.updated) == 1
        assert changes.updated[0].name == "pkg1"
        assert str(changes.updated[0].old_version) == "2.9.0.post0"
        assert str(changes.updated[0].new_version) == "2.10.0.post0"

    def test_get_added_packages_order_preserved(self):
        """Test that the order of added packages is preserved from the new lockfile."""
        old_packages = []
        new_packages = [
            LockfilePackage(name="zebra", version=Version(1, 0, 0)),
            LockfilePackage(name="alpha", version=Version(2, 0, 0)),
            LockfilePackage(name="beta", version=Version(3, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        changes = reporter.get_changes()
        # Order should be preserved from new_packages
        assert [pkg.name for pkg in changes.added] == ["zebra", "alpha", "beta"]

    def test_cached_properties(self):
        """Test that cached properties work correctly."""
        old_packages = [
            LockfilePackage(name="pkg1", version=Version(1, 0, 0)),
        ]
        new_packages = [
            LockfilePackage(name="pkg2", version=Version(2, 0, 0)),
        ]
        old_lockfile = LockFile(type=LockFileType.UV, packages=old_packages)
        new_lockfile = LockFile(type=LockFileType.UV, packages=new_packages)

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
        )

        # Access cached properties multiple times
        assert reporter.added_package_names == {"pkg2"}
        assert reporter.added_package_names == {"pkg2"}  # Should use cached value

        assert reporter.removed_package_names == {"pkg1"}
        assert reporter.removed_package_names == {"pkg1"}  # Should use cached value

        assert reporter.both_lockfile_package_names == set()
        assert reporter.both_lockfile_package_names == set()  # Should use cached value
