from unittest.mock import MagicMock, patch

import pytest

from uv_lock_report.models import UvLockFile
from uv_lock_report.report import get_new_uv_lock_file, get_old_uv_lock_file

# Sample minimal valid uv.lock content for testing
SAMPLE_UV_LOCK = """version = 1
revision = 3
requires-python = ">=3.13"

[[package]]
name = "test-package"
version = "1.0.0"
source = { registry = "https://pypi.org/simple" }
"""

SAMPLE_UV_LOCK_UPDATED = """version = 1
revision = 3
requires-python = ">=3.13"

[[package]]
name = "test-package"
version = "2.0.0"
source = { registry = "https://pypi.org/simple" }

[[package]]
name = "new-package"
version = "1.5.0"
source = { registry = "https://pypi.org/simple" }
"""


class TestGetNewUvLockFile:
    """Test the get_new_uv_lock_file function for reading current uv.lock files."""

    def test_lockfile_exists(self, tmp_path):
        """Test when uv.lock exists in the base_path."""
        # Create a uv.lock file in the temporary directory
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text(SAMPLE_UV_LOCK)

        # Call the function
        result = get_new_uv_lock_file(str(tmp_path))

        # Verify the result
        assert result is not None
        assert isinstance(result, UvLockFile)
        assert result.version == 1
        assert result.revision == 3
        assert result.requires_python == ">=3.13"
        assert len(result.packages) == 1
        assert result.packages[0].name == "test-package"
        assert str(result.packages[0].version) == "1.0.0"

    def test_lockfile_not_exists(self, tmp_path, capsys):
        """Test when uv.lock does not exist in the base_path."""
        # Call the function without creating a uv.lock file
        result = get_new_uv_lock_file(str(tmp_path))

        # Verify the result
        assert result is None

        # Verify the error message was printed
        captured = capsys.readouterr()
        assert "uv.lock not found in current working directory" in captured.out

    def test_lockfile_with_multiple_packages(self, tmp_path):
        """Test parsing a lockfile with multiple packages."""
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text(SAMPLE_UV_LOCK_UPDATED)

        result = get_new_uv_lock_file(str(tmp_path))

        assert result is not None
        assert len(result.packages) == 2
        package_names = {pkg.name for pkg in result.packages}
        assert package_names == {"test-package", "new-package"}

    def test_lockfile_with_relative_path(self, tmp_path):
        """Test when base_path is a relative path."""
        # Create a subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        uv_lock_path = subdir / "uv.lock"
        uv_lock_path.write_text(SAMPLE_UV_LOCK)

        # Call with relative path components
        result = get_new_uv_lock_file(str(subdir))

        assert result is not None
        assert isinstance(result, UvLockFile)

    def test_lockfile_malformed_toml(self, tmp_path):
        """Test when uv.lock contains malformed TOML."""
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text("this is not valid toml {{{")

        # Should raise an exception when parsing
        with pytest.raises(Exception):  # tomllib.TOMLDecodeError or similar
            get_new_uv_lock_file(str(tmp_path))

    def test_lockfile_empty(self, tmp_path):
        """Test when uv.lock is empty."""
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text("")

        # Should raise an exception when parsing
        with pytest.raises(Exception):
            get_new_uv_lock_file(str(tmp_path))


class TestGetOldUvLockFile:
    """Test the get_old_uv_lock_file function for reading historical uv.lock files via git."""

    def test_git_show_success(self, tmp_path, capsys):
        """Test when git show successfully retrieves the lockfile."""
        base_sha = "abc123"

        # Mock subprocess.run to return a successful result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK
        mock_result.stderr = ""

        with patch(
            "uv_lock_report.report.subprocess.run", return_value=mock_result
        ) as mock_run:
            result = get_old_uv_lock_file(base_sha, str(tmp_path))

            # Verify subprocess.run was called correctly
            mock_run.assert_called_once_with(
                ["git", "show", f"{base_sha}:uv.lock"],
                capture_output=True,
                text=True,
                cwd=str(tmp_path),
            )

            # Verify the result
            assert result is not None
            assert isinstance(result, UvLockFile)
            assert result.version == 1
            assert len(result.packages) == 1
            assert result.packages[0].name == "test-package"

            # Verify success message was printed
            captured = capsys.readouterr()
            assert "Found uv.lock in base commit." in captured.out

    def test_git_show_file_not_found(self, tmp_path, capsys):
        """Test when git show fails because the file doesn't exist in the commit."""
        base_sha = "abc123"

        # Mock subprocess.run to return a failure
        mock_result = MagicMock()
        mock_result.returncode = 128
        mock_result.stdout = ""
        mock_result.stderr = "fatal: path 'uv.lock' does not exist in 'abc123'"
        mock_result.args = ["git", "show", "abc123:uv.lock"]

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            result = get_old_uv_lock_file(base_sha, str(tmp_path))

            # Verify the result
            assert result is None

            # Verify error messages were printed
            captured = capsys.readouterr()
            assert "uv.lock not found in base commit" in captured.out
            assert "fatal: path 'uv.lock' does not exist" in captured.out

    def test_git_show_invalid_commit(self, tmp_path, capsys):
        """Test when git show fails because the commit SHA is invalid."""
        base_sha = "invalidsha"

        # Mock subprocess.run to return a failure
        mock_result = MagicMock()
        mock_result.returncode = 128
        mock_result.stdout = ""
        mock_result.stderr = "fatal: invalid object name 'invalidsha'"
        mock_result.args = ["git", "show", "invalidsha:uv.lock"]

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            result = get_old_uv_lock_file(base_sha, str(tmp_path))

            # Verify the result
            assert result is None

            # Verify error messages were printed
            captured = capsys.readouterr()
            assert "uv.lock not found in base commit" in captured.out

    def test_git_show_with_different_sha_formats(self, tmp_path):
        """Test with various SHA formats (full SHA, short SHA, branch name, tag)."""
        test_cases = [
            "a1b2c3d4e5f6",  # Short SHA
            "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",  # Full SHA
            "main",  # Branch name
            "v1.0.0",  # Tag
            "HEAD~1",  # Relative reference
        ]

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK

        for sha in test_cases:
            with patch(
                "uv_lock_report.report.subprocess.run", return_value=mock_result
            ) as mock_run:
                result = get_old_uv_lock_file(sha, str(tmp_path))

                # Verify subprocess.run was called with the correct SHA
                mock_run.assert_called_once_with(
                    ["git", "show", f"{sha}:uv.lock"],
                    capture_output=True,
                    text=True,
                    cwd=str(tmp_path),
                )

                # Verify the result
                assert result is not None

    def test_git_show_with_updated_lockfile(self, tmp_path):
        """Test parsing an updated lockfile from git."""
        base_sha = "def456"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK_UPDATED

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            result = get_old_uv_lock_file(base_sha, str(tmp_path))

            assert result is not None
            assert len(result.packages) == 2
            package_names = {pkg.name for pkg in result.packages}
            assert package_names == {"test-package", "new-package"}

    def test_git_show_malformed_output(self, tmp_path):
        """Test when git show returns malformed TOML."""
        base_sha = "abc123"

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "this is not valid toml {[["

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            # Should raise an exception when parsing
            with pytest.raises(Exception):
                get_old_uv_lock_file(base_sha, str(tmp_path))

    def test_git_command_construction(self, tmp_path):
        """Test that the git command is constructed correctly."""
        base_sha = "test-sha"
        base_path = str(tmp_path)

        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK

        with patch(
            "uv_lock_report.report.subprocess.run", return_value=mock_result
        ) as mock_run:
            get_old_uv_lock_file(base_sha, base_path)

            # Verify the exact command structure
            call_args = mock_run.call_args
            assert call_args[0][0] == ["git", "show", f"{base_sha}:uv.lock"]
            assert call_args[1]["capture_output"] is True
            assert call_args[1]["text"] is True
            assert call_args[1]["cwd"] == base_path


class TestGetLockfilesIntegration:
    """Integration tests comparing get_new_uv_lock_file and get_old_uv_lock_file."""

    def test_same_lockfile_content(self, tmp_path):
        """Test that both functions can parse the same lockfile content."""
        # Write current lockfile
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text(SAMPLE_UV_LOCK)

        # Mock git show to return the same content
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK

        new_lockfile = get_new_uv_lock_file(str(tmp_path))

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            old_lockfile = get_old_uv_lock_file("abc123", str(tmp_path))

        # Both should return valid lockfiles with identical content
        assert new_lockfile is not None
        assert old_lockfile is not None
        assert new_lockfile.version == old_lockfile.version
        assert new_lockfile.revision == old_lockfile.revision
        assert len(new_lockfile.packages) == len(old_lockfile.packages)
        assert new_lockfile.packages[0].name == old_lockfile.packages[0].name
        assert new_lockfile.packages[0].version == old_lockfile.packages[0].version

    def test_different_lockfile_content(self, tmp_path):
        """Test that functions correctly handle different lockfile versions."""
        # Write current lockfile
        uv_lock_path = tmp_path / "uv.lock"
        uv_lock_path.write_text(SAMPLE_UV_LOCK_UPDATED)

        # Mock git show to return the old content
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = SAMPLE_UV_LOCK

        new_lockfile = get_new_uv_lock_file(str(tmp_path))

        with patch("uv_lock_report.report.subprocess.run", return_value=mock_result):
            old_lockfile = get_old_uv_lock_file("abc123", str(tmp_path))

        # Both should be valid but with different content
        assert new_lockfile is not None
        assert old_lockfile is not None
        assert len(new_lockfile.packages) == 2
        assert len(old_lockfile.packages) == 1
