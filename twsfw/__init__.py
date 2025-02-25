from . import _version

__version__ = _version.get_versions()["version"]

from .game import Game  # noqa: F401
