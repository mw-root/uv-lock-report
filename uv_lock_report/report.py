import subprocess
from pathlib import Path

from uv_lock_report.models import (
    LockfileChanges,
    LockFileReporter,
    OutputFormat,
    UvLockFile,
)

CURRENT_UV_LOCK = Path("uv.lock")


def get_new_uv_lock_file(base_path: str) -> UvLockFile | None:
    path = Path(base_path)
    uv_lock_path = path / CURRENT_UV_LOCK
    if not uv_lock_path.exists():
        print("uv.lock not found in current working directory")
        return None
    return UvLockFile.from_toml_str(uv_lock_path.read_text())


def get_old_uv_lock_file(base_sha: str, base_path: str) -> UvLockFile | None:
    cmd = ["git", "show", f"{base_sha}:uv.lock"]

    run = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=base_path,
    )

    if run.returncode != 0:
        print("uv.lock not found in base commit")
        print(run.stderr)
        print(run.stdout)
        print(run.args)
        return None

    print("Found uv.lock in base commit.")
    return UvLockFile.from_toml_str(run.stdout)


def write_changes_file(lockfile_changes: LockfileChanges, output_path: str) -> None:
    Path(output_path).write_text(lockfile_changes.model_dump_json())


def report(
    base_sha: str,
    base_path: str,
    output_path: str,
    output_format: OutputFormat = OutputFormat.TABLE,
    show_learn_more_link: bool = True,
) -> None:
    old_lockfile = get_old_uv_lock_file(base_sha, base_path)
    new_lockfile = get_new_uv_lock_file(base_path)

    reporter = LockFileReporter(
        old_lockfile=old_lockfile,
        new_lockfile=new_lockfile,
        output_format=output_format,
        show_learn_more_link=show_learn_more_link,
    )

    write_changes_file(
        lockfile_changes=reporter.get_changes(),
        output_path=output_path,
    )
