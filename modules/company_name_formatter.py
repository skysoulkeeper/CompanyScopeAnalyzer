# modules/company_name_formatter.py
import re
from utils.logger import logger


def format_company_name_to_domain(name: str) -> str:
    """
    Formats the company name into a format suitable for domain name generation.
    """
    try:
        name = re.sub(r'\b(LLC|L\.L\.C\.)\b', '', name, flags=re.IGNORECASE)
        formatted_name = re.sub(r'\s+|[^a-zA-Z0-9]', '', name)
        return formatted_name.lower()
    except Exception as e:
        logger.error(f"Error formatting name to domain: {e}")
        raise


def format_company_name_for_portal(name: str) -> str:
    """
    Formats the company name for a specific portal's naming conventions.
    """
    try:
        name = re.sub(r'\b(LLC|L\.L\.C\.|INC|I\.N\.C\.)\b', '', name, flags=re.IGNORECASE)
        return name.strip()
    except Exception as e:
        logger.error(f"Error formatting name for portal: {e}")
        raise
