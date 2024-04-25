import argparse
import importlib


def get_parser() -> argparse.Namspace:
    parser = argparse.ArgumentParser("Import modules of turbo turtle. Always performs package import")
    parser.add_argument(
        "MODULE",
        nargs="*",
        help="turbo_turtle case-sensitive module names"
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    import turbo_turtle
    for module in args.MODULE:
        importlib.import_module(f"turbo_turtle.{module}")


if __name__ == "__main__":
    main()
