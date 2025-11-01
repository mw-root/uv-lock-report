from uv_lock_report.models import UpdatedPackage


class TestUpdatedPackage:
    def test_valid_versions(self):
        up = UpdatedPackage(name="steve", old_version="1.0.0", new_version="2.0.0")
        assert up.model_dump() == {
            "name": "steve",
            "new_version": "2.0.0",
            "old_version": "1.0.0",
        }
