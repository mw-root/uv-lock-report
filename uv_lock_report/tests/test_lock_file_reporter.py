from typing import Any, cast

from uv_lock_report.models import (
    LockfilePackage,
    LockFileReporter,
    LockFileType,
    OutputFormat,
    UpdatedPackage,
    UvLockFile,
    VersionChangeLevel,
)


class TestLockFileReporter:
    """Test the LockFileReporter class for comparing lockfiles and detecting changes."""

    def test_both_lockfiles_none(self):
        """Test when both old and new lockfiles are None."""
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
        ]
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
            LockfilePackage(name="pkg3", version="3.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
            LockfilePackage(name="pkg3", version="3.0.0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="1.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="1.5.0"),
            LockfilePackage(name="pkg2", version="3.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
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
        assert updates_by_name["pkg1"].old_version == "1.0.0"
        assert updates_by_name["pkg1"].new_version == "1.5.0"
        assert updates_by_name["pkg2"].old_version == "2.0.0"
        assert updates_by_name["pkg2"].new_version == "3.0.0"

    def test_mixed_changes(self):
        """Test when packages are added, removed, and updated."""
        old_packages = [
            LockfilePackage(name="pkg1", version="1.0.0"),
            LockfilePackage(name="pkg2", version="2.0.0"),
            LockfilePackage(name="pkg3", version="3.0.0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="1.5.0"),  # Updated
            LockfilePackage(name="pkg3", version="3.0.0"),  # Unchanged
            LockfilePackage(name="pkg4", version="4.0.0"),  # Added
        ]
        # pkg2 is removed

        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
        assert changes.updated[0].old_version == "1.0.0"
        assert changes.updated[0].new_version == "1.5.0"

        assert changes.items == 3

    def test_package_version_string_handling(self):
        """Test packages with string versions (malformed versions)."""
        old_packages = [
            LockfilePackage(name="pkg1", version="2.9.0.post0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg1", version="2.10.0.post0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
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
            LockfilePackage(name="zebra", version="1.0.0"),
            LockfilePackage(name="alpha", version="2.0.0"),
            LockfilePackage(name="beta", version="3.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=True,
        )

        changes = reporter.get_changes()
        # Order should be preserved from new_packages
        assert [pkg.name for pkg in changes.added] == ["zebra", "alpha", "beta"]

    def test_cached_properties(self):
        """Test that cached properties work correctly."""
        old_packages = [
            LockfilePackage(name="pkg1", version="1.0.0"),
        ]
        new_packages = [
            LockfilePackage(name="pkg2", version="2.0.0"),
        ]
        old_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": old_packages, "requires-python": ">=3.9"}),
        )
        new_lockfile = UvLockFile(
            type=LockFileType.UV,
            version=1,
            revision=1,
            **cast(Any, {"package": new_packages, "requires-python": ">=3.9"}),
        )

        reporter = LockFileReporter(
            old_lockfile=old_lockfile,
            new_lockfile=new_lockfile,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
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
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )

        # Create packages with different change levels
        major_update = UpdatedPackage(
            name="major-pkg", old_version="1.0.0", new_version="2.0.0"
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version="1.0.0", new_version="1.1.0"
        )
        patch_update = UpdatedPackage(
            name="patch-pkg", old_version="1.0.0", new_version="1.0.1"
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
        """Test sorting when multiple packages have the same change level - should be alphabetical by name."""
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )

        # Create multiple packages with same change level but different names
        major_update_zebra = UpdatedPackage(
            name="zebra-pkg", old_version="1.0.0", new_version="2.0.0"
        )
        major_update_alpha = UpdatedPackage(
            name="alpha-pkg", old_version="1.5.3", new_version="3.0.0"
        )
        major_update_beta = UpdatedPackage(
            name="beta-pkg", old_version="2.0.0", new_version="5.0.0"
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version="2.1.0", new_version="2.2.0"
        )

        # Pass in non-alphabetical order
        packages = [
            major_update_zebra,
            minor_update,
            major_update_beta,
            major_update_alpha,
        ]

        sorted_packages = reporter.sort_packages_by_change_level(packages)

        # All major updates should come before minor update, and be sorted alphabetically
        assert len(sorted_packages) == 4
        assert sorted_packages[0].name == "alpha-pkg"  # MAJOR, alphabetically first
        assert sorted_packages[1].name == "beta-pkg"  # MAJOR, alphabetically second
        assert sorted_packages[2].name == "zebra-pkg"  # MAJOR, alphabetically third
        assert sorted_packages[3].name == "minor-pkg"  # MINOR, comes after all major

    def test_sort_packages_by_change_level_empty_list(self):
        """Test sorting an empty list of packages."""
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )

        sorted_packages = reporter.sort_packages_by_change_level([])

        assert sorted_packages == []

    def test_sort_packages_by_change_level_verifies_change_levels(self):
        """Test that the sorted packages have the correct change levels and names in correct order."""
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )

        # Create packages with all possible change levels
        major_update = UpdatedPackage(
            name="major-pkg", old_version="1.0.0", new_version="2.0.0"
        )
        minor_update = UpdatedPackage(
            name="minor-pkg", old_version="1.0.0", new_version="1.1.0"
        )
        patch_update = UpdatedPackage(
            name="patch-pkg", old_version="1.0.0", new_version="1.0.1"
        )
        post_patch_update = UpdatedPackage(
            name="post-pkg", old_version="1.0.0.post0", new_version="1.0.1.post0"
        )

        packages = [patch_update, post_patch_update, major_update, minor_update]

        sorted_packages = reporter.sort_packages_by_change_level(packages)

        # Verify the change levels are in correct order (MAJOR=0, MINOR=1, PATCH=2)
        # Note: .post0 versions are correctly parsed as PATCH changes by packaging.version
        assert sorted_packages[0].change_level() == VersionChangeLevel.MAJOR  # 0
        assert sorted_packages[1].change_level() == VersionChangeLevel.MINOR  # 1
        assert sorted_packages[2].change_level() == VersionChangeLevel.PATCH  # 2
        assert sorted_packages[3].change_level() == VersionChangeLevel.PATCH  # 2

    def test_sort_packages_by_change_level_alphabetical_within_levels(self):
        """Test comprehensive sorting: by change level first, then alphabetically by name."""
        reporter = LockFileReporter(
            old_lockfile=None,
            new_lockfile=None,
            output_format=OutputFormat.TABLE,
            show_learn_more_link=False,
        )

        # Create multiple packages at each change level with non-alphabetical names
        packages = [
            # PATCH updates
            UpdatedPackage(
                name="zulu-patch",
                old_version="1.0.0",
                new_version="1.0.1",
            ),
            UpdatedPackage(
                name="alpha-patch",
                old_version="1.0.0",
                new_version="1.0.2",
            ),
            # MINOR updates
            UpdatedPackage(
                name="yankee-minor",
                old_version="1.0.0",
                new_version="1.1.0",
            ),
            UpdatedPackage(
                name="bravo-minor",
                old_version="1.0.0",
                new_version="1.2.0",
            ),
            # MAJOR updates
            UpdatedPackage(
                name="whiskey-major",
                old_version="1.0.0",
                new_version="2.0.0",
            ),
            UpdatedPackage(
                name="charlie-major",
                old_version="1.0.0",
                new_version="3.0.0",
            ),
            # POST PATCH updates (also PATCH level with packaging.version)
            UpdatedPackage(
                name="victor-post",
                old_version="1.0.0.post0",
                new_version="2.0.0.post0",
            ),
            UpdatedPackage(
                name="delta-post",
                old_version="1.0.0.post0",
                new_version="1.1.0.post0",
            ),
        ]

        sorted_packages = reporter.sort_packages_by_change_level(packages)

        # Verify correct order: MAJOR (alphabetical), MINOR (alphabetical), PATCH (alphabetical)
        # Note: .post versions are now correctly parsed, so victor-post is MAJOR and delta-post is MINOR
        expected_order = [
            "charlie-major",  # MAJOR, alphabetically first
            "victor-post",  # MAJOR (2.0.0.post0), alphabetically second
            "whiskey-major",  # MAJOR, alphabetically third
            "bravo-minor",  # MINOR, alphabetically first
            "delta-post",  # MINOR (1.1.0.post0), alphabetically second
            "yankee-minor",  # MINOR, alphabetically third
            "alpha-patch",  # PATCH, alphabetically first
            "zulu-patch",  # PATCH, alphabetically second
        ]

        actual_order = [pkg.name for pkg in sorted_packages]
        assert actual_order == expected_order
