import argparse
import importlib


def get_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Import modules of a package. Always performs package import.")
    parser.add_argument(
        "-p", "--package",
        required=True,
        help="Name of base package. Will always be imported"
    )
    parser.add_argument(
        "-m", "--module",
        nargs="*",
        default=[],
        help="Optional submodule names to also import from package"
    )
    return parser


def main() -> None:
    parser = get_parser()
    args = parser.parse_args()

    importlib.import_module(args.package)
    for module in args.module:
        importlib.import_module(f"{args.package}.{module}")


if __name__ == "__main__":
    main()
