# Copilot Instructions for `uv-lock-report`

## Project Overview
- **Purpose:** Parses `uv.lock` changes and generates a Markdown report for Pull Request comments, summarizing added, removed, and updated Python packages.
- **Main Components:**
  - `main.py`: CLI entrypoint, parses arguments and invokes the report logic.
  - `uv_lock_report/report.py`: Orchestration layer that fetches lockfiles (via git or filesystem) and delegates to `LockFileReporter`.
  - `uv_lock_report/models.py`: Pydantic models for lockfile packages, change sets, and reporter logic.
  - `uv_lock_report/tests/`: Pytest-based tests for core logic and models.
- **GitHub Action:** Defined in `action.yml` to automate report generation and PR commenting.

## Architecture
- **Lockfile Abstraction:**
  - `LockFile` base class with `UvLockFile` implementation for `uv.lock` parsing.
  - Uses `cached_property` for efficient lookups (`packages_by_name`, `package_names`).
  - `LockFile.from_toml_str()` factory method parses TOML into structured models.
- **Reporter Pattern:**
  - `LockFileReporter` compares old/new lockfiles and computes diffs.
  - Handles edge cases: missing lockfiles (None), packages without versions.
  - Change detection via set operations on package names.

## Key Workflows
- **Run Locally:**
  - `uv run main.py <base_sha> <base_path> <output_path>`
    - Compares current `uv.lock` with the one at `<base_sha>` and writes a JSON report to `<output_path>`.
- **Run Tests:**
  - `uv run pytest` or `uv run pytest --cov` for coverage.
- **GitHub Action:**
  - Installs dependencies with `uv sync`.
  - Runs the report and posts a Markdown summary as a PR comment (see `action.yml`).

## Conventions & Patterns
- **Version Handling:**
  - Uses `semver.Version` for structured version parsing.
  - Custom `coerce()` function handles malformed versions (e.g., `2.9.0.post0`).
  - Falls back to string representation when parsing fails.
- **Models:**
  - All lockfile data is modeled with Pydantic (`LockfilePackage`, `UpdatedPackage`, `LockfileChanges`).
  - Markdown output is generated via the `markdown` computed property on `LockfileChanges`.
  - Package equality based on `name` and `version` (see `LockfilePackage.__eq__`).
- **Testing:**
  - Use pytest; test data and expectations are in `tests/conftest.py`.
  - Tests cover version edge cases (major-only, minor-only, post-releases).
- **Python Version:** Requires Python >=3.13 (see `pyproject.toml`).
- **Dependencies:** Uses `pydantic` for modeling, `semver` for version parsing.

## Integration Points
- **GitHub API:** Comments are posted using `actions/github-script` in the workflow.
- **External Tools:**
  - `uv` is used for dependency management and running the app.
  - `git show` fetches historical `uv.lock` content for comparison.

## Examples
- **Run report locally:**
  ```sh
  uv run main.py <base_sha> <base_path> <output_path>
  ```
- **Run tests with coverage:**
  ```sh
  uv run pytest --cov=uv_lock_report
  ```
- **Add a new lockfile type:**
  - Subclass `LockFile` in `models.py` (see `UvLockFile` example).
  - Implement `from_toml_str()` or equivalent parser.

## References
- See `README.md` for usage and action configuration examples.
- See `action.yml` for CI/CD and PR integration details.
- See `uv_lock_report/models.py` for:
  - `LockFileReporter` - core diff logic.
  - `UvLockFile` - uv.lock parsing.
  - `LockfileChanges.markdown` - Markdown rendering.
