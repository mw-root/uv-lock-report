import subprocess
import tomllib
from pathlib import Path

from uv_lock_report.models import LockfileChanges, LockfilePackage, UpdatedPackage

CURRENT_UV_LOCK = Path("uv.lock")


def read_uv_lock(base_path: str) -> dict:
    path = Path(base_path)
    return tomllib.loads((path / CURRENT_UV_LOCK).read_text())


def read_old_uv_lock(base_sha: str, base_path: str) -> dict:
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
        return {"package": []}

    print("Found uv.lock in base commit.")
    return tomllib.loads(run.stdout)


def write_changes_file(lockfile_changes: LockfileChanges, output_path: str) -> None:
    Path(output_path).write_text(lockfile_changes.model_dump_json())


def report(base_sha: str, base_path: str, output_path: str) -> None:
    old_lockfile = read_old_uv_lock(base_sha, base_path)
    new_lockfile = read_uv_lock(base_path)

    old_lockfile_package_names = set(p["name"] for p in old_lockfile["package"])
    new_lockfile_package_names = set(p["name"] for p in new_lockfile["package"])

    added_package_names = new_lockfile_package_names.difference(
        old_lockfile_package_names
    )
    removed_package_names = old_lockfile_package_names.difference(
        new_lockfile_package_names
    )

    packages_in_both = old_lockfile_package_names & new_lockfile_package_names

    lockfile_changes = LockfileChanges()

    for pkg in old_lockfile["package"]:
        if pkg["name"] in removed_package_names:
            lockfile_changes.removed.append(LockfilePackage.from_dict(pkg))

    for pkg in new_lockfile["package"]:
        if pkg["name"] in added_package_names:
            lockfile_changes.added.append(LockfilePackage.from_dict(pkg))

    for pkg in new_lockfile["package"]:
        ## Editable and Local packages don't have versions
        if "version" not in pkg:
            continue

        new_package = LockfilePackage.from_dict(pkg)
        if new_package.name in packages_in_both:
            old_package_dict = next(
                p for p in old_lockfile["package"] if p["name"] == new_package.name
            )
            old_package = LockfilePackage.from_dict(old_package_dict)
            if old_package.version == new_package.version:
                continue

            lockfile_changes.updated.append(
                UpdatedPackage(
                    name=new_package.name,
                    old_version=old_package.version,
                    new_version=new_package.version,
                )
            )

    write_changes_file(lockfile_changes, output_path)
