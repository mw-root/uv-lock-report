import re
from typing import Optional

from pydantic import BaseModel, ConfigDict, computed_field, field_serializer
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
