from uv_lock_report.models import LockfilePackage


class TestLockfilePackage:
    def test_valid_version(self):
        pkg_name = "pkg_name"
        pkg_version = "1.2.0"

        lfp = LockfilePackage(name=pkg_name, version=pkg_version)

        assert lfp.name == pkg_name
        assert lfp.version == pkg_version

    def test_valid_version_from_dict(self):
        pkg_name = "pkg_name"
        pkg_version = "1.2.0"

        lfp = LockfilePackage.model_validate(dict(name=pkg_name, version=pkg_version))

        assert lfp.name == pkg_name
        assert lfp.version == pkg_version

    def test_major_version_only_from_dict(self):
        d = {"name": "pkg_name", "version": "1"}

        lfp = LockfilePackage.model_validate(d)

        assert lfp.name == d["name"]
        assert lfp.version == d["version"]

    def test_major_minor_version_only_from_dict(self):
        d = {"name": "pkg_name", "version": "1.2"}

        lfp = LockfilePackage.model_validate(d)

        assert lfp.name == d["name"]
        assert lfp.version == d["version"]

    def test_malformed_post_version(self):
        ## Python Dateutil does this
        d = {"name": "pkg_name", "version": "2.9.0.post0"}
        expected_version = "2.9.0.post0"

        lfp = LockfilePackage.model_validate(d)

        assert lfp.name == d["name"]
        assert lfp.version == expected_version
