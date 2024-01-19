# modules/company_name_formatter.py
import re
from utils.logger import logger


# Define a function to format a company name for domain name generation
def format_company_name_to_domain(name: str) -> str:
    try:
        # Remove common business entity suffixes (e.g., LLC, L.L.C.) and non-alphanumeric characters
        name = re.sub(r'\b(LLC|L\.L\.C\.|LLC\.|INC|I\.N\.C\.|INC\.)\b', '', name, flags=re.IGNORECASE)
        formatted_name = re.sub(r'\s+|[^a-zA-Z0-9]', '', name)
        return formatted_name.lower()
    except Exception as e:
        logger.error(f"Error formatting name to domain: {e}")
        raise


# Define a function to format a company name for a specific portal's naming conventions
def format_company_name_for_portal(name: str, remove_suffix: bool = True) -> str:
    try:
        logger.info(f"format_company_name_for_portal: input: {name}, remove_suffix: {remove_suffix}")
        if remove_suffix:
            name = re.sub(r'\b(LLC|L\.L\.C\.|INC|I\.N\.C\.)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[^\w\s]', '', name)
        formatted_name = name.strip()
        logger.info(f"format_company_name_for_portal: output: {formatted_name}")
        return formatted_name
    except Exception as e:
        logger.error(f"Error formatting name for portal: {e}")
        raise

