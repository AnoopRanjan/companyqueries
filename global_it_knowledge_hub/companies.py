"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — COMPANIES & CATEGORIES DEFINITION (companies.py)
===============================================================================
This module defines the official company tabs and knowledge categories available
in the Global IT Knowledge Hub user interface and search filters.

===============================================================================
✏️ HOW TO MODIFY THIS FILE:
===============================================================================
1. TO ADD A NEW COMPANY TAB:
   Simply add a new dictionary to the `COMPANIES` list below:
       {"id": "Salesforce", "name": "Salesforce"}
   - `id`: The internal identifier used for database filtering and Azure search.
     (Must match the "company" field value in your document records).
   - `name`: The user-friendly label displayed on the tab button in the UI.

2. TO ADD A NEW KNOWLEDGE CATEGORY:
   Simply append a string to the `CATEGORIES` list below:
       "AI Ethics & Governance"
   - Make sure to keep "All Categories" as the first option.
   - Any document seeded with this category can then be filtered by the user.

3. TO CHANGE THE DISPLAY ORDER:
   - Drag or move the entries up or down in the lists.
===============================================================================
"""

from typing import List, Dict


# =============================================================================
# ✏️ MODIFY HERE: Company Tabs List
# =============================================================================
# The "id" field is used to filter documents in Azure AI Search.
# Note: Keep {"id": "all", "name": "All Companies"} at the top to allow global search.
COMPANIES: List[Dict[str, str]] = [
    {"id": "all", "name": "All Companies"},
    {"id": "Microsoft", "name": "Microsoft"},
    {"id": "Google", "name": "Google"},
    {"id": "AWS", "name": "AWS"},
    {"id": "IBM", "name": "IBM"},
    {"id": "Oracle", "name": "Oracle"},
    {"id": "Accenture", "name": "Accenture"},
    {"id": "TCS", "name": "TCS"},
    {"id": "Infosys", "name": "Infosys"},
    {"id": "Wipro", "name": "Wipro"},
    {"id": "Capgemini", "name": "Capgemini"},
    # Examples of how you can add more companies anytime:
    # {"id": "Salesforce", "name": "Salesforce"},
    # {"id": "Cisco", "name": "Cisco"},
    # {"id": "SAP", "name": "SAP"},
    # {"id": "NVIDIA", "name": "NVIDIA"}
]


# =============================================================================
# ✏️ MODIFY HERE: Document Categories List
# =============================================================================
# These categories appear in the search panel dropdown filter.
# "All Categories" must remain the default (index 0) to search across all types.
CATEGORIES: List[str] = [
    "All Categories",
    "Brochures",
    "Policies",
    "Products & Services",
    "Security & Compliance",
    "Pricing",
    "Careers",
    "Technical Documentation",
    # You can add more categories here as your document library grows:
    # "AI Ethics & Governance",
    # "Sustainability & ESG",
    # "Whitepapers & Case Studies"
]


def get_company_ids() -> List[str]:
    """Returns a list of all valid company identifiers."""
    return [comp["id"] for comp in COMPANIES]


def is_valid_company(company_id: str) -> bool:
    """Checks whether the requested company ID is recognized."""
    return company_id in get_company_ids()


def is_valid_category(category_name: str) -> bool:
    """Checks whether the requested category is recognized."""
    return category_name in CATEGORIES
