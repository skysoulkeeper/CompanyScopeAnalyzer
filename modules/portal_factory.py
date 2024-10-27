# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/portal_factory.py

Description:
This module provides a function to dynamically retrieve a portal class based on
the state abbreviation. It uses Python's importlib to load the corresponding module
and return the appropriate class for handling portal-specific logic.
"""

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
