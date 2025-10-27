import pytest

from uv_lock_report.models import VersionChangeLevel


class TestVersionChangeLevel:
    """Test the VersionChangeLevel enum and its gitmoji property."""

    def test_major_gitmoji(self):
        """Test that MAJOR change level returns collision emoji."""
        assert VersionChangeLevel.MAJOR.gitmoji == ":collision:"

    def test_minor_gitmoji(self):
        """Test that MINOR change level returns sparkles emoji."""
        assert VersionChangeLevel.MINOR.gitmoji == ":sparkles:"

    def test_patch_gitmoji(self):
        """Test that PATCH change level returns hammer and wrench emoji."""
        assert VersionChangeLevel.PATCH.gitmoji == ":hammer_and_wrench:"

    def test_unknown_gitmoji(self):
        """Test that UNKNOWN change level returns question mark emoji."""
        assert VersionChangeLevel.UNKNOWN.gitmoji == ":question:"

    def test_all_levels_have_gitmoji(self):
        """Test that all VersionChangeLevel values have a gitmoji defined."""
        for level in VersionChangeLevel:
            # Should not raise NotImplementedError
            emoji = level.gitmoji
            assert isinstance(emoji, str)
            assert emoji.startswith(":")
            assert emoji.endswith(":")

    def test_level_values(self):
        """Test that VersionChangeLevel enum values are correctly ordered."""
        assert VersionChangeLevel.MAJOR == 0
        assert VersionChangeLevel.MINOR == 1
        assert VersionChangeLevel.PATCH == 2
        assert VersionChangeLevel.UNKNOWN == 10

    @pytest.mark.parametrize(
        "level,expected_emoji",
        [
            (VersionChangeLevel.MAJOR, ":collision:"),
            (VersionChangeLevel.MINOR, ":sparkles:"),
            (VersionChangeLevel.PATCH, ":hammer_and_wrench:"),
            (VersionChangeLevel.UNKNOWN, ":question:"),
        ],
    )
    def test_gitmoji_mapping(self, level, expected_emoji):
        """Parametrized test for all VersionChangeLevel to gitmoji mappings."""
        assert level.gitmoji == expected_emoji
