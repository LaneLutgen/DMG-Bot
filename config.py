from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

_config = None
CONFIG_FILE = "config.yaml"


def get_section(name):
    global _config
    if not _config:
        with open(CONFIG_FILE, "r") as f:
            _config = load(f, Loader=Loader)

    section = _config.get(name)

    if not section:
        raise KeyError(f"Section {name} not found in {CONFIG_FILE}")

    return _config.get(name)


__all__ = ['get_section']
