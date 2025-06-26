import sys

import parver


def bump_version(version: str, pre=None, major=False, minor=False, patch=True):
    if not any([major, minor, patch]):
        patch = True
    if len([v for v in [major, minor, patch] if v]) != 1:
        print(
            "Only one option should be provided among (--major, --minor, --patch)",
            file=sys.stderr,
        )
        sys.exit(1)
    current_version = parver.Version.parse(version)
    if not pre:
        version_idx = [major, minor, patch].index(True)
        new_version = current_version.bump_release(index=version_idx).replace(
            pre=None, post=None
        )
    else:
        new_version = current_version.bump_pre(pre)
    new_version = new_version.replace(local=None, dev=None)
    return str(new_version)


if __name__ == "__main__":
    import json

    input_data = json.loads(sys.argv[1])
    print(bump_version(**input_data))
