from semver import Version

from uv_lock_report.models import (
    LockFile,
    LockfilePackage,
    LockFileReporter,
    LockFileType,
    OutputFormat,
    UpdatedPackage,
    VersionChangeLevel,
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

    def test_sort_packages_by_change_level(self):
        """Test that sort_packages_by_change_level returns packages sorted by change level (major first, then minor, then patch)."""
        reporter = LockFileReporter(
            old_lockfile=None, new_lockfile=None, output_format=OutputFormat.TABLE
        )

        # Create packages with different change levels
        major_update = UpdatedPackage(
            name="major-pkg", old_version=Version(1, 0, 0), new_version=Version(2, 0, 0)
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version=Version(1, 0, 0), new_version=Version(1, 1, 0)
        )
        patch_update = UpdatedPackage(
            name="patch-pkg", old_version=Version(1, 0, 0), new_version=Version(1, 0, 1)
        )
        string_version_update = UpdatedPackage(
            name="string-pkg", old_version="1.0.0.post0", new_version="1.0.1.post0"
        )

        # Test packages in mixed order
        unsorted_packages = [
            patch_update,
            major_update,
            string_version_update,
            minor_update,
        ]

        sorted_packages = reporter.sort_packages_by_change_level(unsorted_packages)

        # Verify order: major first, then minor, then patch, then unknown (string versions)
        assert len(sorted_packages) == 4
        assert sorted_packages[0].name == "major-pkg"  # MAJOR = 2
        assert sorted_packages[1].name == "minor-pkg"  # MINOR = 1
        assert sorted_packages[2].name == "patch-pkg"  # PATCH = 0
        assert sorted_packages[3].name == "string-pkg"  # UNKNOWN = -1

    def test_sort_packages_by_change_level_same_level(self):
        """Test sorting when multiple packages have the same change level."""
        reporter = LockFileReporter(
            old_lockfile=None, new_lockfile=None, output_format=OutputFormat.TABLE
        )

        # Create multiple packages with same change level
        major_update_1 = UpdatedPackage(
            name="alpha-pkg", old_version=Version(1, 0, 0), new_version=Version(2, 0, 0)
        )
        major_update_2 = UpdatedPackage(
            name="beta-pkg", old_version=Version(1, 5, 3), new_version=Version(3, 0, 0)
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version=Version(2, 1, 0), new_version=Version(2, 2, 0)
        )

        packages = [minor_update, major_update_1, major_update_2]

        sorted_packages = reporter.sort_packages_by_change_level(packages)

        # Both major updates should come before minor update
        assert len(sorted_packages) == 3
        assert sorted_packages[0].name in [
            "alpha-pkg",
            "beta-pkg",
        ]  # Either major update
        assert sorted_packages[1].name in [
            "alpha-pkg",
            "beta-pkg",
        ]  # The other major update
        assert sorted_packages[2].name == "minor-pkg"  # Minor update last

    def test_sort_packages_by_change_level_empty_list(self):
        """Test sorting an empty list of packages."""
        reporter = LockFileReporter(
            old_lockfile=None, new_lockfile=None, output_format=OutputFormat.TABLE
        )

        sorted_packages = reporter.sort_packages_by_change_level([])

        assert sorted_packages == []

    def test_sort_packages_by_change_level_verifies_change_levels(self):
        """Test that the sorted packages actually have the correct change levels in descending order."""
        reporter = LockFileReporter(
            old_lockfile=None, new_lockfile=None, output_format=OutputFormat.TABLE
        )

        # Create packages with all possible change levels
        major_update = UpdatedPackage(
            name="major-pkg", old_version=Version(1, 0, 0), new_version=Version(2, 0, 0)
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version=Version(1, 0, 0), new_version=Version(1, 1, 0)
        )
        patch_update = UpdatedPackage(
            name="patch-pkg", old_version=Version(1, 0, 0), new_version=Version(1, 0, 1)
        )
        unknown_update = UpdatedPackage(
            name="unknown-pkg", old_version="1.0.0.post0", new_version="1.0.1.post0"
        )

        packages = [patch_update, unknown_update, major_update, minor_update]

        sorted_packages = reporter.sort_packages_by_change_level(packages)

        # Verify the change levels are in descending order
        assert sorted_packages[0].change_level() == VersionChangeLevel.MAJOR  # 2
        assert sorted_packages[1].change_level() == VersionChangeLevel.MINOR  # 1
        assert sorted_packages[2].change_level() == VersionChangeLevel.PATCH  # 0
        assert sorted_packages[3].change_level() == VersionChangeLevel.UNKNOWN  # -1
