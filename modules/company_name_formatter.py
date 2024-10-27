# MIT License
# Copyright (c) 2024 skysoulkeeper
# See LICENSE file for more details.

"""
Module: modules/company_name_formatter.py

Description:
This module provides functions to format company names for domain name generation
and for specific portal naming conventions. It removes common legal suffixes and
non-alphanumeric characters to ensure compatibility with various formats.
"""

import re
from utils.logger import logger


# Define a function to format a company name for domain name generation
def format_company_name_to_domain(name: str) -> str:
    try:
        # Regular expression to remove common business entity suffixes (e.g., LLC, L.L.C.) and non-alphanumeric characters.
        # 're.IGNORECASE' makes the pattern case-insensitive.
        name = re.sub(r'\b(LLC|L\.L\.C\.|LLC\.|INC|I\.N\.C\.|INC\.)\b', '', name, flags=re.IGNORECASE)
        # Regular expression to remove spaces and any characters that are not letters or numbers.
        formatted_name = re.sub(r'\s+|[^a-zA-Z0-9]', '', name)
        return formatted_name.lower()  # Returning the formatted name in lowercase.
    except Exception as e:
        logger.error(f"Error formatting name to domain: {e}")
        raise


# Define a function to format a company name for a specific portal's naming conventions
def format_company_name_for_portal(name: str, remove_suffix: bool = True) -> str:
    try:
        logger.info(f"format_company_name_for_portal: input: {name}, remove_suffix: {remove_suffix}")
        if remove_suffix:
            # Removing common legal suffixes from the company name if 'remove_suffix' is True.
            name = re.sub(r'\b(LLC|L\.L\.C\.|INC|I\.N\.C\.)\b', '', name, flags=re.IGNORECASE)
        # Removing all non-word characters (anything other than letter, digit, underscore) and spaces.
        name = re.sub(r'[^\w\s]', '', name)
        formatted_name = name.strip()  # Stripping leading and trailing whitespace from the name.
        logger.info(f"format_company_name_for_portal: output: {formatted_name}")
        return formatted_name  # Returning the formatted name.
    except Exception as e:
        logger.error(f"Error formatting name for portal: {e}")
        raise
