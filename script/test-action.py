from argparse import ArgumentParser, Namespace

from uv_lock_report.models import (
    LockFileReporter,
    OutputFormat,
    UvLockFile,
)
from uv_lock_report.report import write_changes_file

old_lockfile = UvLockFile.model_validate(
    {
        "version": 1,
        "revision": 3,
        "requires-python": ">=3.14",
        "package": [
            {"name": "upgraded_major", "version": "2.0.0"},
            {"name": "upgraded_minor", "version": "2.0.0"},
            {"name": "upgraded_patch", "version": "2.0.0"},
            {"name": "downgraded_major", "version": "4.20.1"},
            {"name": "downgraded_minor", "version": "4.20.1"},
            {"name": "downgraded_patch", "version": "4.20.1"},
            {"name": "removed_1", "version": "1.0.0"},
        ],
    }
)
new_lockfile = UvLockFile.model_validate(
    {
        "version": 1,
        "revision": 3,
        "requires-python": ">=3.14",
        "package": [
            {"name": "upgraded_major", "version": "3.2.0"},
            {"name": "upgraded_minor", "version": "2.2.0"},
            {"name": "upgraded_patch", "version": "2.0.1"},
            {"name": "downgraded_major", "version": "3.14.0"},
            {"name": "downgraded_minor", "version": "4.10.0"},
            {"name": "downgraded_patch", "version": "4.20.0"},
            {"name": "added_1", "version": "3.7.0"},
        ],
    }
)


output_path = "report.json"


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "--output-format",
        choices=list(OutputFormat),
        default=OutputFormat.TABLE.value,
        required=False,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    reporter = LockFileReporter(
        old_lockfile=old_lockfile,
        new_lockfile=new_lockfile,
        output_format=args.output_format,
        show_learn_more_link=False,
    )

    write_changes_file(
        lockfile_changes=reporter.get_changes(),
        output_path=output_path,
    )


if __name__ == "__main__":
    main()
