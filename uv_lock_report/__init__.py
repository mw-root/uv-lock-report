"""
uv-lock-report: Parses uv.lock changes and generates Markdown reports.
"""

from uv_lock_report.cli import main as cli_main
from uv_lock_report.report import report
from uv_lock_report.models import (
    LockFile,
    UvLockFile,
    LockFileReporter,
    LockfileChanges,
    LockfilePackage,
    UpdatedPackage,
    OutputFormat,
)

__all__ = [
    "cli_main",
    "report",
    "LockFile",
    "UvLockFile",
    "LockFileReporter",
    "LockfileChanges",
    "LockfilePackage",
    "UpdatedPackage",
    "OutputFormat",
]

try:
    from uv_lock_report._version import __version__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"