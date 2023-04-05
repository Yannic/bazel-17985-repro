#!/usr/bin/env python3

import argparse
import io
import json
import sys
import zipfile

from typing import List


class JarArtifact:
    def __init__(self, s: str):
        parts = s.split(',')

        self.path = parts[0]
        self.label = parts[1]


def _run(args) -> int:
    with io.open(args.allowlist) as file:
        allowlist = json.load(file)

    files = {}
    warnings = []
    for artifact in args.inputs:
        with zipfile.ZipFile(artifact.path) as file:
            for name in file.namelist():
                if not name.endswith('.class'):
                    # We only check class files.
                    continue

                if (name in files) and (name not in allowlist):
                    warnings.append(
                        "Found duplicate file: '{}', originally provided by '{}', also provided by '{}'.".format(
                            name, files[name], artifact.label))
                    continue
                files[name] = artifact.label

    with io.open(args.output, 'w') as output:
        for warning in warnings:
            print(warning, file=sys.stderr)
            print(warning, file=output)

    if (len(warnings) > 0) and (not args.succeed_on_found_violations):
        return 1

    return 0


def main(argv: List[str]) -> int:
    """Main program.

    Args:
      argv: command-line arguments, such as sys.argv (including the program name
      in argv[0]).

    Returns:
      Zero if there are no duplicate class files in `--inputs`, non-zero otherwise.
    """

    parser = argparse.ArgumentParser(
        description='Tool for enforcing oneversion requirement on jars.',
        fromfile_prefix_chars='@'
    )

    # Arguments from
    # https://cs.opensource.google/bazel/bazel/+/master:src/main/java/com/google/devtools/build/lib/rules/java/OneVersionCheckActionBuilder.java;l=73;drc=4843f29a445761c31761152ab4e7d4cad9c346d2
    parser.add_argument('--output',
                        required=True,
                        type=str,
                        help='The output file.')
    parser.add_argument('--succeed_on_found_violations',
                        required=False,
                        default=False,
                        action='store_true',
                        help='Whether to succeed if any violations are found.')
    parser.add_argument('--whitelist',
                        required=True,
                        dest='allowlist',
                        type=str,
                        help='Path to the allowlist file.')
    parser.add_argument('--inputs',
                        required=True,
                        type=JarArtifact,
                        nargs='+',
                        help='List of inputs.')

    return _run(parser.parse_args(argv[1:]))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
