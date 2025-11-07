from argparse import ArgumentParser, Namespace

from uv_lock_report.models import OutputFormat
from uv_lock_report.report import report


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--base-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument(
        "--output-format",
        choices=list(OutputFormat),
        default=OutputFormat.TABLE.value,
        required=False,
    )
    parser.add_argument(
        "--show-learn-more-link",
        choices=["true", "false"],
        default="true",
        required=False,
        help='Whether to show a "Learn More" link in the report comment.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    base_sha = args.base_sha
    base_path = args.base_path
    output_path = args.output_path
    output_format = OutputFormat(args.output_format)
    report(
        base_sha=base_sha,
        base_path=base_path,
        output_path=output_path,
        output_format=output_format,
        show_learn_more_link=args.show_learn_more_link == "true",
    )
