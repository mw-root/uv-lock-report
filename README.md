## uv Lock Report

[![codecov](https://codecov.io/gh/mw-root/uv-lock-report/graph/badge.svg?token=QQFK62PQ8G)](https://codecov.io/gh/mw-root/uv-lock-report)

## Description

<!-- AUTO-DOC-DESCRIPTION:START - Do not remove or modify this section -->

Digests complex `uv.lock` diffs in Pull Requests and provides a
simple summary of dependency changes as a PR comment.

<!-- AUTO-DOC-DESCRIPTION:END -->

Pull Requests with lockfile changes can be difficult to evaluate at a quick glance
and diffs are usually hidden by default.

This GitHub Action transforms complex `uv.lock` diffs into a clean, easy-to-read report.
It analyzes the changes between your base and head lockfiles, then posts a formatted comment showing exactly which packages were added, updated, or removed—including version changes and their severity (major, minor, or patch).

No more parsing through hundreds of lines of TOML diffs to understand what changed.


## Example Gitlab Actions Usage

```yaml
name: uv Lockfile Report

on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
        with:
          fetch-depth: 0

      - name: Report
        uses: mw-root/uv-lock-report@v0.7.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

|        INPUT         |  TYPE  | REQUIRED |  DEFAULT   |                           DESCRIPTION                           |
|----------------------|--------|----------|------------|-----------------------------------------------------------------|
|     github-token     | string |   true   |            |                          GitHub Token                           |
|    output-format     | string |  false   | `"simple"` |   The output format of the report. <br>One of: simple, table    |
| show-learn-more-link | string |  false   |  `"true"`  | Whether to show a "Learn More" <br>link in the report comment.  |

<!-- AUTO-DOC-INPUT:END -->



### Output Format Examples

The formatting can be chosen with the `output-format` input.

#### Simple Format ( Default )
![Example Comment](images/uv-lock-report-simple-comment.png "Simple Format")


#### Table Format
![Example Comment](images/uv-lock-report-table-comment.png "Table Format")

## CLI Usage

You can also use `uv-lock-report` as a standalone CLI tool for local development or in custom CI/CD pipelines.

### Installation

Install the package using uv:

```bash
uv build
pip install ./dist/uv_lock_report-0.1.0-py3-none-any.whl
```

### Usage

```bash
uv-lock-report --base-sha <git-sha> --base-path <path-to-base-lockfile> --output-path <output-file>
```

#### Arguments

- `--base-sha`: Git SHA of the base commit to compare against
- `--base-path`: Path to the base lockfile (usually `uv.lock`)
- `--output-path`: Path where the JSON report will be written
- `--output-format`: Output format (`table` or `simple`, default: `table`)
- `--show-learn-more-link`: Whether to show "Learn More" link (`true` or `false`, default: `true`)

#### Example

```bash
# Compare current uv.lock with the one from main branch
uv-lock-report \
  --base-sha main \
  --base-path uv.lock \
  --output-path report.json \
  --output-format table
```

### Testing the installation

You can test that the CLI is properly installed:

```bash
# Test with a built wheel
uv run --with ./dist/uv_lock_report-0.1.0-py3-none-any.whl uv-lock-report --help

# Or run the included test script
uv run python test_cli_install.py
```
