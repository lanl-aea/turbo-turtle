"""Internal API module implementing the ``fetch`` subcommand behavior.

Should raise ``RuntimeError`` or a derived class of :class:`waves.exceptions.WAVESError` to allow the CLI implementation
to convert stack-trace/exceptions into STDERR message and non-zero exit codes.
"""
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

    parser.add_argument("FILE", nargs="*",
                              help=f"modsim template file or directory")
    parser.add_argument("--destination",
        help="Destination directory. Unless ``--overwrite`` is specified, conflicting file names in the " \
             "destination will not be copied. (default: PWD)",
        type=pathlib.Path,
        default=pathlib.Path().cwd())
    parser.add_argument("--overwrite",
        action="store_true",
        help="Overwrite any existing files (default: %(default)s)")
    parser.add_argument("--dry-run",
        action="store_true",
        help="Print the destination tree and exit (default: %(default)s)")
    parser.add_argument("--print-available",
        action="store_true",
        help="Print available modsim template files and exit (default: %(default)s)")

    return parser


def main(subcommand: str, root_directory: str | pathlib.Path, relative_paths: list[str | pathlib.Path],
         destination: str | pathlib.Path, requested_paths: list[str | pathlib.Path] | None = None,
         overwrite: bool = False, dry_run: bool = False,
         print_available: bool = False) -> None:
    """Thin wrapper on :meth:`waves.fetch.recursive_copy` to provide subcommand specific behavior and STDOUT/STDERR

    Recursively copy requested paths from root_directory/relative_paths directories into destination directory using
    the shortest possible shared source prefix.

    :param subcommand: name of the subcommand to report in STDOUT
    :param root_directory: String or pathlike object for the root_directory directory
    :param relative_paths: List of string or pathlike objects describing relative paths to search for in
        root_directory
    :param destination: String or pathlike object for the destination directory
    :param requested_paths: list of relative path-like objects that subset the files found in the
        ``root_directory`` ``relative_paths``
    :param overwrite: Boolean to overwrite any existing files in destination directory
    :param dry_run: Print the destination tree and exit. Short circuited by ``print_available``
    :param print_available: Print the available source files and exit. Short circuits ``dry_run``
    """
    if not requested_paths:
        requested_paths = []
    if not root_directory.is_dir():
        # During "waves fetch" sub-command, this should only be reached if the package installation
        # structure doesn't match the assumptions in _settings.py. It is used by the Conda build tests as a
        # sign-of-life that the installed directory assumptions are correct.
        raise RuntimeError(f"Could not find '{root_directory}' directory")

    print(f"{_settings._project_name_short} {subcommand}", file=sys.stdout)
    print(f"Destination directory: '{destination}'", file=sys.stdout)
    recursive_copy(root_directory, relative_paths, destination, requested_paths=requested_paths,
                   overwrite=overwrite, dry_run=dry_run,
                   print_available=print_available)


def available_files(root_directory: pathlib.Path | str,
                    relative_paths: list[str]) -> tuple[list[pathlib.Path], list[str]]:
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
            file_list = [path for path in root_directory.rglob(relative_path) if path.is_file()]
        if file_list:
            available_files.extend(file_list)
        else:
            not_found.append(relative_path)
    available_files.sort()
    not_found.sort()
    return available_files, not_found


def build_source_files(
    root_directory: str,
    relative_paths: list[str],
    exclude_patterns: list[str] = _settings._fetch_exclude_patterns
) -> tuple[list[pathlib.Path], list[str]]:
    """Wrap :meth:`available_files` and trim list based on exclude patterns

    If no source files are found, an empty list is returned.

    :param str root_directory: Relative or absolute root path to search. Relative paths are converted to absolute paths with
        respect to the current working directory before searching.
    :param list relative_paths: Relative paths to search for. Directories are searched recursively for files.
    :param list exclude_patterns: list of strings to exclude from the root_directory directory tree if the path contains a
        matching string.

    :returns: source_files, not_found
    :rtype: tuple of lists
    """
    # TODO: Save the list of excluded files and return
    source_files, not_found = available_files(root_directory, relative_paths)
    source_files = [path for path in source_files if not any(map(str(path).__contains__, exclude_patterns))]
    return source_files, not_found


def longest_common_path_prefix(file_list: str | pathlib.Path | list[str | pathlib.Path]) -> pathlib.Path:
    """Return the longest common file path prefix.

    The edge case of a single path is handled by returning the parent directory

    :param file_list: List of path-like objects

    :returns: longest common path prefix

    :raises RuntimeError: When file list is empty
    """
    if isinstance(file_list, str) or isinstance(file_list, pathlib.Path):
        file_list = [file_list]
    file_list = [pathlib.Path(path) for path in file_list]
    number_of_files = len(file_list)
    if number_of_files < 1:
        raise RuntimeError("No files in 'file_list'")
    elif number_of_files == 1:
        longest_common_path = file_list[0].parent
    else:
        longest_common_path = pathlib.Path(os.path.commonpath(file_list))
    return longest_common_path


def build_destination_files(destination: str | pathlib.Path,
                            requested_paths: list[str | pathlib.Path]) -> tuple[list, list]:
    """Build destination file paths from the requested paths, truncating the longest possible source prefix path

    :param destination: String or pathlike object for the destination directory
    :param requested_paths: List of requested file paths

    :returns: destination files, existing files
    """
    destination = pathlib.Path(destination).resolve()
    longest_common_requested_path = longest_common_path_prefix(requested_paths)
    destination_files = [destination / path.relative_to(longest_common_requested_path) for path in requested_paths]
    existing_files = [path for path in destination_files if path.exists()]
    return destination_files, existing_files


def build_copy_tuples(destination: str | pathlib.Path, requested_paths_resolved: list,
                      overwrite: bool = False) -> tuple[tuple]:
    """
    :param destination: String or pathlike object for the destination directory
    :param requested_paths_resolved: List of absolute requested file paths

    :returns: requested and destination file path pairs
    """
    destination_files, existing_files = build_destination_files(destination, requested_paths_resolved)
    copy_tuples = tuple(zip(requested_paths_resolved, destination_files))
    if not overwrite and existing_files:
        copy_tuples = tuple((requested_path, destination_file) for requested_path, destination_file in copy_tuples if
                            destination_file not in existing_files)
    return copy_tuples


def conditional_copy(copy_tuples: tuple[tuple]) -> None:
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


def recursive_copy(root_directory: str | pathlib.Path, relative_paths: list[str | pathlib.Path],
                   destination: str | pathlib.Path, requested_paths: list[str | pathlib.Path] | None = None,
                   overwrite: bool = False, dry_run: bool = False,
                   print_available: bool = False) -> None:
    """Recursively copy requested paths from root_directory/relative_paths directories into destination directory using
    the shortest possible shared source prefix.

    If destination files exist, copy non-conflicting files unless overwrite is specified.

    :param root_directory: String or pathlike object for the root_directory directory
    :param relative_paths: List of string or pathlike objects describing relative paths to search for in
        root_directory
    :param destination: String or pathlike object for the destination directory
    :param requested_paths: list of relative path-like objects that subset the files found in the
        ``root_directory`` ``relative_paths``
    :param overwrite: Boolean to overwrite any existing files in destination directory
    :param dry_run: Print the destination tree and exit. Short circuited by ``print_available``
    :param print_available: Print the available source files and exit. Short circuits ``dry_run``

    :raises RuntimeError: If the no requested files exist in the longest common source path
    """
    if not requested_paths:
        requested_paths = []

    # Build source tree
    source_files, missing_relative_paths = build_source_files(root_directory, relative_paths)
    longest_common_source_path = longest_common_path_prefix(source_files)
    if print_available:
        print("Available source files:")
        print_list([path.relative_to(longest_common_source_path) for path in source_files])

    # Down select to requested file list
    if requested_paths:
        requested_paths_resolved, missing_requested_paths = build_source_files(longest_common_source_path, requested_paths)
    else:
        requested_paths_resolved = source_files
        missing_requested_paths = []
    if not requested_paths_resolved:
        raise RuntimeError(f"Did not find any requested files in '{longest_common_source_path}'")

    # Build source/destination pairs
    destination = pathlib.Path(destination).resolve()
    copy_tuples = build_copy_tuples(destination, requested_paths_resolved, overwrite=overwrite)
    if len(copy_tuples) != len(requested_paths_resolved):
        print(f"Found conflicting files in destination '{destination}'. Use '--overwrite' to replace existing files.",
              file=sys.stderr)

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