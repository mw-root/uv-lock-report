from argparse import ArgumentParser, Namespace

from uv_lock_report.report import report


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("base_sha")
    parser.add_argument("base_path")
    parser.add_argument("output_path")
    return parser.parse_args()


def main():
    args = parse_args()
    base_sha = args.base_sha
    base_path = args.base_path
    output_path = args.output_path
    report(base_sha, base_path, output_path)


if __name__ == "__main__":
    main()
