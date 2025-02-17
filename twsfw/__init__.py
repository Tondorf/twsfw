from . import _version

__version__ = _version.get_versions()["version"]

from twsfwphysx import Engine  # noqa: F401
