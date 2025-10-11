import re
import tomllib
from enum import StrEnum, auto
from functools import cached_property
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_serializer
from semver import Version

BASEVERSION = re.compile(
    r"""[vV]?
        (?P<major>0|[1-9]\d*)
        (\.
        (?P<minor>0|[1-9]\d*)
        (\.
        (?P<patch>0|[1-9]\d*)
        )?
        )?
    """,
    re.VERBOSE,
)


def coerce(version: str) -> tuple[Version | None, Optional[str]]:
    """
    Convert an incomplete version string into a semver-compatible Version
    object

    * Tries to detect a "basic" version string (``major.minor.patch``).
    * If not enough components can be found, missing components are
        set to zero to obtain a valid semver version.

    :param str version: the version string to convert
    :return: a tuple with a :class:`Version` instance (or ``None``
        if it's not a version) and the rest of the string which doesn't
        belong to a basic version.
    :rtype: tuple(:class:`Version` | None, str)
    """
    match = BASEVERSION.search(version)
    if not match:
        return (None, version)

    ver = {
        key: 0 if value is None else value for key, value in match.groupdict().items()
    }
    ver = Version(**ver)  # ty: ignore[missing-argument]
    rest = match.string[match.end() :]  # noqa:E203
    return ver, rest


class LockfilePackage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    version: Version | str

    def __str__(self) -> str:
        return f"{self.name}: {self.version}"

    @field_serializer("version", mode="plain")
    def ser_version(self, value: Version) -> str:
        return str(value)

    @classmethod
    def from_dict(cls, d: dict) -> "LockfilePackage":
        try:
            return cls(
                name=d["name"],
                version=Version.parse(d["version"], optional_minor_and_patch=True),
            )
        except ValueError:
            version, rest = coerce(d["version"])

            if version is not None:
                if rest is not None:
                    return cls(
                        name=d["name"],
                        version=f"{str(version)}{rest}",
                    )

                return cls(
                    name=d["name"],
                    version=version,
                )

        return cls(
            name=d["name"],
            version=d["version"],
        )

    def __eq__(self, other):
        if not isinstance(other, LockfilePackage):
            return NotImplemented
        return self.name == other.name and self.version == other.version


class UpdatedPackage(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    old_version: Version | str
    new_version: Version | str

    def __str__(self) -> str:
        return f"{self.name}: {self.old_version} -> {self.new_version}"

    @field_serializer("old_version", mode="plain")
    def ser_old_version(self, value: Version) -> str:
        return str(value)

    @field_serializer("new_version", mode="plain")
    def ser_new_version(self, value: Version) -> str:
        return str(value)


class LockfileChanges(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    added: list[LockfilePackage] = []
    removed: list[LockfilePackage] = []
    updated: list[UpdatedPackage] = []

    def __str__(self) -> str:
        all = []
        if self.added:
            all.append("Added:")
            all.extend([str(e) for e in self.added])
        if self.updated:
            all.append("Updated:")
            all.extend([str(e) for e in self.updated])
        if self.removed:
            all.append("Removed:")
            all.extend([str(e) for e in self.removed])
        return "\n".join(all)

    @computed_field
    @property
    def items(self) -> int:
        return len(self.added) + len(self.removed) + len(self.updated)

    @computed_field
    @property
    def markdown(self) -> str:
        all = ["# uv Lockfile Report"]
        if self.added:
            all.append("## Added Packages")
            all.extend(
                [
                    "| Package | Version |",
                    "|--|--|",
                ]
            )
        all.extend([f"| {added.name} | {added.version} |" for added in self.added])
        if self.updated:
            all.append("## Changed Packages")
            all.extend(
                [
                    "| Package | Old Version | New Version |",
                    "|--|--|--|",
                ]
            )
            all.extend(
                [
                    f"| {updated.name} | {updated.old_version} | {updated.new_version} |"
                    for updated in self.updated
                ]
            )

        if self.removed:
            all.append("## Removed Packages")
            all.extend(
                [
                    "| Package | Version |",
                    "|--|--|",
                ]
            )
        all.extend(
            [f"| {removed.name} | {removed.version} |" for removed in self.removed]
        )
        return "\n".join(all)


class LockFileType(StrEnum):
    UV = auto()


class LockFile(BaseModel):
    type: LockFileType
    packages: list[LockfilePackage]

    @cached_property
    def packages_by_name(self) -> dict[str, LockfilePackage]:
        return {p.name: p for p in self.packages}

    @cached_property
    def package_names(self) -> set[str]:
        return set(self.packages_by_name.keys())


class UvLockFile(LockFile):
    type: LockFileType = LockFileType.UV
    version: int
    revision: int
    packages: list[LockfilePackage] = Field(alias="package")
    requires_python: str = Field(alias="requires-python")

    @classmethod
    def from_toml_str(cls, toml_str: str) -> "UvLockFile":
        return cls.model_validate(tomllib.loads(toml_str))


class LockFileReporter:
    def __init__(
        self, old_lockfile: LockFile | None, new_lockfile: LockFile | None
    ) -> None:
        self.old_lockfile = old_lockfile
        self.new_lockfile = new_lockfile

    @cached_property
    def both_lockfile_package_names(self) -> set[str]:
        old_package_names = (
            self.old_lockfile.package_names if self.old_lockfile else set()
        )
        new_package_names = (
            self.new_lockfile.package_names if self.new_lockfile else set()
        )

        return old_package_names & new_package_names

    def get_changes(self) -> LockfileChanges:
        return LockfileChanges(
            added=self.get_added_packages(),
            removed=self.get_removed_packages(),
            updated=self.get_updated_packages(),
        )

    @cached_property
    def added_package_names(self) -> set[str]:
        if self.old_lockfile is None:
            if self.new_lockfile is None:
                return set()

            return self.new_lockfile.package_names

        if self.new_lockfile is None:
            return set()

        return self.new_lockfile.package_names.difference(
            self.old_lockfile.package_names
        )

    @cached_property
    def removed_package_names(self) -> set[str]:
        if self.new_lockfile is None:
            if self.old_lockfile is None:
                return set()

            return self.old_lockfile.package_names
        if self.old_lockfile is None:
            return set()

        return self.old_lockfile.package_names.difference(
            self.new_lockfile.package_names
        )

    def get_removed_packages(self) -> list[LockfilePackage]:
        if self.old_lockfile is None:
            return []
        return [
            pkg
            for pkg in self.old_lockfile.packages
            if pkg.name in self.removed_package_names
        ]

    def get_added_packages(self) -> list[LockfilePackage]:
        if self.new_lockfile is None:
            return []
        return [
            pkg
            for pkg in self.new_lockfile.packages
            if pkg.name in self.added_package_names
        ]

    def get_updated_packages(self) -> list[UpdatedPackage]:
        if self.old_lockfile is None or self.new_lockfile is None:
            return []
        updated_packages: list[UpdatedPackage] = []

        for pkg_name in self.both_lockfile_package_names:
            old_pkg = self.old_lockfile.packages_by_name[pkg_name]
            new_pkg = self.new_lockfile.packages_by_name[pkg_name]
            if old_pkg != new_pkg:
                updated_packages.append(
                    UpdatedPackage(
                        name=pkg_name,
                        old_version=old_pkg.version,
                        new_version=new_pkg.version,
                    )
                )
        return updated_packages
