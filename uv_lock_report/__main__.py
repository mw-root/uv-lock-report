"""
Entry point for running uv_lock_report as a module.

This allows the package to be executed with:
    python -m uv_lock_report
"""

from uv_lock_report.cli import main

if __name__ == "__main__":
    main()
