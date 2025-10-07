## uv Lock Report
## Description

<!-- AUTO-DOC-DESCRIPTION:START - Do not remove or modify this section -->

Parses any changes to uv.lock in a Pull Request and
creates a PR comment with details of any new, removed, or
updated packages

<!-- AUTO-DOC-DESCRIPTION:END -->


## Example
```yaml
on:
  pull_request:

permissions:
  contents: read
  pull-requests: write

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@08c6903cd8c0fde910a37f88322edcfb5dd907a8 # v5.0.0
        with:
          fetch-depth: 0

      - name: Report
        uses: mw-root/uv-lock-report@v1.0.0
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

<!-- AUTO-DOC-INPUT:START - Do not remove or modify this section -->

|    INPUT     |  TYPE  | REQUIRED | DEFAULT | DESCRIPTION  |
|--------------|--------|----------|---------|--------------|
| github-token | string |   true   |         | GitHub Token |

<!-- AUTO-DOC-INPUT:END -->
