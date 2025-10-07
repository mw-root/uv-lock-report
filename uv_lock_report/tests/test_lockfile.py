from uv_lock_report.models import LockfilePackage


class TestLockfilePackage:
    def test_valid_version(self):
        pkg_name = "pkg_name"
        pkg_version = "1.2.0"

        lfp = LockfilePackage(name=pkg_name, version=pkg_version)

        assert lfp.name == pkg_name
        assert str(lfp.version) == pkg_version

    def test_valid_version_from_dict(self):
        pkg_name = "pkg_name"
        pkg_version = "1.2.0"

        lfp = LockfilePackage.from_dict(dict(name=pkg_name, version=pkg_version))

        assert lfp.name == pkg_name
        assert str(lfp.version) == pkg_version

    def test_major_version_only_from_dict(self):
        d = {"name": "pkg_name", "version": "1"}
        expected_version = "1.0.0"

        lfp = LockfilePackage.from_dict(d)

        assert lfp.name == d["name"]
        assert str(lfp.version) == expected_version

    def test_major_minor_version_only_from_dict(self):
        d = {"name": "pkg_name", "version": "1.2"}
        expected_version = "1.2.0"

        lfp = LockfilePackage.from_dict(d)

        assert lfp.name == d["name"]
        assert str(lfp.version) == expected_version

    def test_malformed_post_version(self):
        ## Python Dateutil does this
        d = {"name": "pkg_name", "version": "2.9.0.post0"}
        expected_version = "2.9.0.post0"

        lfp = LockfilePackage.from_dict(d)

        assert lfp.name == d["name"]
        assert str(lfp.version) == expected_version
