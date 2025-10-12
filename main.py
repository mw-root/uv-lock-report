from argparse import ArgumentParser, Namespace

from uv_lock_report.models import OutputFormat
from uv_lock_report.report import report


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--base-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument(
        "--format",
        choices=list(OutputFormat),
        default=OutputFormat.TABLE.value,
        required=False,
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    base_sha = args.base_sha
    base_path = args.base_path
    output_path = args.output_path
    format = OutputFormat(args.format)
    report(base_sha, base_path, output_path, output_format=format)


if __name__ == "__main__":
    main()
