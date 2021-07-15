import os
import py_compile
import sys

IGNORE_DIRS = ["__pycache__"]


def main(dest):
    # type: (str) -> None
    for root, _, files in os.walk(dest):
        if os.path.basename(root) in IGNORE_DIRS:
            continue
        for filename in files:
            if not filename.endswith(".py"):
                continue
            src_file = os.path.join(root, filename)
            dest_file = src_file + "c"
            py_compile.compile(src_file, dest_file)


if __name__ == "__main__":
    main(sys.argv[1])
