import os
import sys
import shutil
import typing
import filecmp
import pathlib
import argparse

from turbo_turtle import _settings


_exclude_from_namespace = set(globals().keys())


def get_parser() -> argparse.ArgumentParser:
    """Return a 'no-help' parser for the fetch subcommand

    :return: parser
    """
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "FILE",
        nargs="*",
        help=f"modsim template file or directory",
    )
    parser.add_argument(
        "--destination",
        # fmt: off
        help="Destination directory. Unless ``--overwrite`` is specified, conflicting file names in the "
             "destination will not be copied. (default: PWD)",
        # fmt: on
        type=pathlib.Path,
        default=pathlib.Path().cwd(),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite any existing files (default: %(default)s)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the destination tree and exit (default: %(default)s)",
    )
    parser.add_argument(
        "--print-available",
        action="store_true",
        help="Print available modsim template files and exit (default: %(default)s)",
    )

    return parser


def main(
    subcommand: str,
    root_directory: typing.Union[str, pathlib.Path],
    relative_paths: typing.Iterable[typing.Union[str, pathlib.Path]],
    destination: typing.Union[str, pathlib.Path],
    requested_paths: typing.List[pathlib.Path] = [],
    overwrite: bool = False,
    dry_run: bool = False,
    print_available: bool = False,
) -> None:
    """Thin wrapper on :meth:`turbo_turtle.fetch.recursive_copy` to provide subcommand specific behavior and
    STDOUT/STDERR

    Recursively copy requested paths from root_directory/relative_paths directories into destination directory using
    the shortest possible shared source prefix.

    :param subcommand: name of the subcommand to report in STDOUT
    :param root_directory: String or pathlike object for the root_directory directory
    :param relative_paths: List of string or pathlike objects describing relative paths to search for in
        root_directory
    :param destination: String or pathlike object for the destination directory
    :param requested_paths: list of Path objects that subset the files found in the
        ``root_directory`` ``relative_paths``
    :param overwrite: Boolean to overwrite any existing files in destination directory
    :param dry_run: Print the destination tree and exit. Short circuited by ``print_available``
    :param print_available: Print the available source files and exit. Short circuits ``dry_run``
    """
    root_directory = pathlib.Path(root_directory)
    if not root_directory.is_dir():
        # During "turbo-turtle fetch" sub-command, this should only be reached if the package installation
        # structure doesn't match the assumptions in _settings.py. It is used by the Conda build tests as a
        # sign-of-life that the installed directory assumptions are correct.
        raise RuntimeError(f"Could not find '{root_directory}' directory")

    print(f"{_settings._project_name_short} {subcommand}", file=sys.stdout)
    print(f"Destination directory: '{destination}'", file=sys.stdout)
    recursive_copy(
        root_directory,
        relative_paths,
        destination,
        requested_paths=requested_paths,
        overwrite=overwrite,
        dry_run=dry_run,
        print_available=print_available,
    )


def available_files(
    root_directory: typing.Union[str, pathlib.Path], relative_paths: typing.Iterable[typing.Union[str, pathlib.Path]]
) -> typing.Tuple[typing.List[pathlib.Path], typing.List[typing.Union[str, pathlib.Path]]]:
    """Build a list of files at ``relative_paths`` with respect to the root ``root_directory`` directory

    Returns a list of absolute paths and a list of any relative paths that were not found. Falls back to a full
    recursive search of ``relative_paths`` with ``pathlib.Path.rglob`` to enable pathlib style pattern matching.

    :param root_directory: Relative or absolute root path to search. Relative paths are converted to absolute paths with
        respect to the current working directory before searching.
    :param relative_paths: Relative paths to search for. Directories are searched recursively for files.

    :returns: available_files, not_found
    """
    root_directory = pathlib.Path(root_directory).resolve()
    if isinstance(relative_paths, str):
        relative_paths = [relative_paths]

    available_files = []
    not_found = []
    for relative_path in relative_paths:
        file_list = []
        absolute_path = root_directory / relative_path
        if absolute_path.is_file():
            file_list.append(absolute_path)
        elif absolute_path.is_dir():
            file_list = [path for path in absolute_path.rglob("*") if path.is_file()]
        else:
            file_list = [path for path in root_directory.rglob(str(relative_path)) if path.is_file()]
        if file_list:
            available_files.extend(file_list)
        else:
            not_found.append(relative_path)
    available_files.sort()
    not_found.sort()
    return available_files, not_found


def build_source_files(
    root_directory: typing.Union[str, pathlib.Path],
    relative_paths: typing.Iterable[typing.Union[str, pathlib.Path]],
    exclude_patterns: typing.Iterable[str] = _settings._fetch_exclude_patterns,
) -> typing.Tuple[typing.List[pathlib.Path], typing.List[typing.Union[str, pathlib.Path]]]:
    """Wrap :meth:`available_files` and trim list based on exclude patterns

    If no source files are found, an empty list is returned.

    :param str root_directory: Relative or absolute root path to search. Relative paths are converted to absolute paths
        with respect to the current working directory before searching.
    :param list relative_paths: Relative paths to search for. Directories are searched recursively for files.
    :param list exclude_patterns: list of strings to exclude from the root_directory directory tree if the path contains
        a matching string.

    :returns: source_files, not_found
    :rtype: tuple of lists
    """
    # TODO: Save the list of excluded files and return
    source_files, not_found = available_files(root_directory, relative_paths)
    source_files = [path for path in source_files if not any(map(str(path).__contains__, exclude_patterns))]
    return source_files, not_found


def longest_common_path_prefix(file_list: typing.List[pathlib.Path]) -> pathlib.Path:
    """Return the longest common file path prefix.

    The edge case of a single path is handled by returning the parent directory

    :param file_list: List of path-like objects

    :returns: longest common path prefix

    :raises RuntimeError: When file list is empty
    """
    number_of_files = len(file_list)
    if number_of_files < 1:
        raise RuntimeError("No files in 'file_list'")
    elif number_of_files == 1:
        longest_common_path = file_list[0].parent
    else:
        longest_common_path = pathlib.Path(os.path.commonpath(file_list))
    return longest_common_path


def build_destination_files(
    destination: typing.Union[str, pathlib.Path], requested_paths: typing.List[pathlib.Path]
) -> typing.Tuple[typing.List[pathlib.Path], typing.List[pathlib.Path]]:
    """Build destination file paths from the requested paths, truncating the longest possible source prefix path

    :param destination: String or pathlike object for the destination directory
    :param requested_paths: List of requested files as path-objects

    :returns: destination files, existing files
    """
    destination = pathlib.Path(destination).resolve()
    longest_common_requested_path = longest_common_path_prefix(requested_paths)
    destination_files = [destination / path.relative_to(longest_common_requested_path) for path in requested_paths]
    existing_files = [path for path in destination_files if path.exists()]
    return destination_files, existing_files


def build_copy_tuples(
    destination: typing.Union[str, pathlib.Path],
    requested_paths_resolved: typing.List[pathlib.Path],
    overwrite: bool = False,
) -> typing.List[typing.Tuple[pathlib.Path, pathlib.Path]]:
    """
    :param destination: String or pathlike object for the destination directory
    :param requested_paths_resolved: List of absolute requested files as path-objects

    :returns: requested and destination file path pairs
    """
    destination_files, existing_files = build_destination_files(destination, requested_paths_resolved)
    copy_tuples = [
        (requested_path, destination_file)
        for requested_path, destination_file in zip(requested_paths_resolved, destination_files)
    ]
    if not overwrite and existing_files:
        copy_tuples = [
            (requested_path, destination_file)
            for requested_path, destination_file in copy_tuples
            if destination_file not in existing_files
        ]
    return copy_tuples


def conditional_copy(copy_tuples: typing.List[typing.Tuple[pathlib.Path, pathlib.Path]]) -> None:
    """Copy when destination file doesn't exist or doesn't match source file content

    Uses Python ``shutil.copyfile``, so meta data isn't preserved. Creates intermediate parent directories prior to
    copy, but doesn't raise exceptions on existing parent directories.

    :param copy_tuples: Tuple of source, destination pathlib.Path pairs, e.g. ``((source, destination), ...)``
    """
    for source_file, destination_file in copy_tuples:
        # If the root_directory and destination file contents are the same, don't perform unnecessary file I/O
        if not destination_file.exists() or not filecmp.cmp(source_file, destination_file, shallow=False):
            destination_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_file, destination_file)


def print_list(things_to_print: list, prefix: str = "\t", stream=sys.stdout) -> None:
    """Print a list to the specified stream, one line per item

    :param list things_to_print: List of items to print
    :param str prefix: prefix to print on each line before printing the item
    :param file-like stream: output stream. Defaults to ``sys.stdout``.
    """
    for item in things_to_print:
        print(f"{prefix}{item}", file=stream)


def recursive_copy(
    root_directory: typing.Union[str, pathlib.Path],
    relative_paths: typing.Iterable[typing.Union[str, pathlib.Path]],
    destination: typing.Union[str, pathlib.Path],
    requested_paths: typing.List[pathlib.Path] = [],
    overwrite: bool = False,
    dry_run: bool = False,
    print_available: bool = False,
) -> None:
    """Recursively copy requested paths from root_directory/relative_paths directories into destination directory using
    the shortest possible shared source prefix.

    If destination files exist, copy non-conflicting files unless overwrite is specified.

    :param root_directory: String or pathlike object for the root_directory directory
    :param relative_paths: List of string or pathlike objects describing relative paths to search for in
        root_directory
    :param destination: String or pathlike object for the destination directory
    :param requested_paths: list of relative path-objects that subset the files found in the
        ``root_directory`` ``relative_paths``
    :param overwrite: Boolean to overwrite any existing files in destination directory
    :param dry_run: Print the destination tree and exit. Short circuited by ``print_available``
    :param print_available: Print the available source files and exit. Short circuits ``dry_run``

    :raises RuntimeError: If the no requested files exist in the longest common source path
    """

    # Build source tree
    source_files, missing_relative_paths = build_source_files(root_directory, relative_paths)
    longest_common_source_path = longest_common_path_prefix(source_files)
    if print_available:
        print("Available source files:")
        print_list([path.relative_to(longest_common_source_path) for path in source_files])

    # Down select to requested file list
    if len(requested_paths) > 0:
        requested_paths_resolved, missing_requested_paths = build_source_files(
            longest_common_source_path, requested_paths
        )
    else:
        requested_paths_resolved = source_files
        missing_requested_paths = []
    if not requested_paths_resolved:
        raise RuntimeError(f"Did not find any requested files in '{longest_common_source_path}'")

    # Build source/destination pairs
    destination = pathlib.Path(destination).resolve()
    copy_tuples = build_copy_tuples(destination, requested_paths_resolved, overwrite=overwrite)
    if len(copy_tuples) != len(requested_paths_resolved):
        print(
            f"Found conflicting files in destination '{destination}'. Use '--overwrite' to replace existing files.",
            file=sys.stderr,
        )

    # User I/O
    if dry_run:
        print("Files to create:")
        print_list([destination for _, destination in copy_tuples])
    if print_available or dry_run:
        return

    # Do the work if there are any files left to copy
    conditional_copy(copy_tuples)


# Limit help() and 'from module import *' behavior to the module's public API
_module_objects = set(globals().keys()) - _exclude_from_namespace
__all__ = [name for name in _module_objects if not name.startswith("_")]
