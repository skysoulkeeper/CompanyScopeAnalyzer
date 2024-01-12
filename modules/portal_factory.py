# modules/portal_factory.py
import importlib


def get_portal_class(state_abbr):
    try:
        portal_module = importlib.import_module(f".portals.{state_abbr.lower()}_portal",
                                                package="modules")
        return getattr(portal_module, f"{state_abbr.upper()}Portal")
    except (ImportError, AttributeError):
        raise ValueError(f"No portal class found for state: {state_abbr}")
