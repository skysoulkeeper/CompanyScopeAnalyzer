# modules/portal_factory.py
import importlib


# Define a function to dynamically get a portal class based on the state abbreviation
def get_portal_class(state_abbr):
    try:
        # Construct the module name using the state abbreviation and import the module
        portal_module = importlib.import_module(f".portals.{state_abbr.lower()}_portal",
                                                package="modules")

        # Get the class name based on the state abbreviation (e.g., "CAPortal" for "CA")
        portal_class_name = f"{state_abbr.upper()}Portal"

        # Get and return the portal class from the module
        return getattr(portal_module, portal_class_name)
    except (ImportError, AttributeError):
        # Handle exceptions if the module or class is not found
        raise ValueError(f"No portal class found for state: {state_abbr}")
