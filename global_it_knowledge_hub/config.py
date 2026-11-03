"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — CONFIGURATION SETTINGS (config.py)
===============================================================================
This module manages all configuration variables for the application:
1. Azure AI Foundry (Model Endpoint, API Key, Deployment Model Name)
2. Azure AI Search (Search Endpoint, Admin Key, Index Name)
3. Server Configuration (Host, Port, Debug Mode)

===============================================================================
✏️ HOW TO MODIFY THIS FILE:
===============================================================================
1. To change default ports or hosts:
   - Modify the `DEFAULT_HOST` or `DEFAULT_PORT` constants below.
2. To configure your Azure services:
   - Copy `.env.example` to `.env` and paste your actual Azure keys there.
   - Do NOT hardcode secrets directly in this file for production safety.
3. To test immediately without Azure credentials:
   - Leave the keys as empty or placeholders. The application will automatically
     activate its built-in local hybrid search and response synthesis engine!
===============================================================================
"""

import os
from pathlib import Path
from typing import Dict, Any


# -----------------------------------------------------------------------------
# Base Directory and .env file discovery
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


def load_env_file(filepath: Path) -> None:
    """
    Lightweight, dependency-free .env file loader.
    Reads key=value pairs into os.environ without requiring external packages.
    Preserves any pre-existing environment variables.
    """
    if not filepath.exists():
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    # Do not overwrite environment variables passed from the OS
                    if key not in os.environ:
                        os.environ[key] = val
    except Exception as e:
        print(f"[Config] Warning: Could not read {filepath}: {e}")


# Load .env file automatically when config is imported
load_env_file(ENV_FILE)


# =============================================================================
# ✏️ MODIFY HERE: Default Server & Azure Settings
# =============================================================================

# Server Host & Port
# Change DEFAULT_PORT to 3000, 8080, etc., if port 8000 is occupied on your machine
DEFAULT_HOST = os.getenv("HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("PORT", "8000"))

# Azure AI Foundry Configuration
# - FOUNDRY_ENDPOINT: Your Azure OpenAI or AI Foundry model endpoint
#   Format: https://YOUR-RESOURCE.openai.azure.com/openai/v1/
# - FOUNDRY_API_KEY: Your Azure AI Foundry secret key
# - FOUNDRY_MODEL: The exact deployment name you assigned in AI Foundry
#   Example: "gpt-4.1-nano", "gpt-4o", or "gpt-4o-mini"
FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_ENDPOINT", "").strip()
FOUNDRY_API_KEY = os.getenv("FOUNDRY_API_KEY", "").strip()
FOUNDRY_MODEL = os.getenv("FOUNDRY_MODEL", "gpt-4.1-nano").strip()

# Azure AI Search Configuration
# - AZURE_SEARCH_ENDPOINT: The Search service URL
#   Format: https://YOUR-SEARCH.search.windows.net
# - AZURE_SEARCH_ADMIN_KEY: The Admin key or Query key from Azure Portal
# - AZURE_SEARCH_INDEX: The index name where documents will be stored
AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT", "").strip()
AZURE_SEARCH_ADMIN_KEY = os.getenv("AZURE_SEARCH_ADMIN_KEY", "").strip()
AZURE_SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX", "it-company-knowledge").strip()

# Azure API Version for Search REST calls
AZURE_SEARCH_API_VERSION = os.getenv("AZURE_SEARCH_API_VERSION", "2023-11-01")


def is_azure_search_configured() -> bool:
    """
    Checks if Azure AI Search has valid credentials configured.
    Returns True if an endpoint and key are set (and not placeholder text).
    """
    endpoint = AZURE_SEARCH_ENDPOINT
    key = AZURE_SEARCH_ADMIN_KEY
    if not endpoint or not key:
        return False
    if "YOUR-SEARCH" in endpoint or "YOUR_SEARCH_ADMIN_KEY" in key:
        return False
    return True


def is_azure_foundry_configured() -> bool:
    """
    Checks if Azure AI Foundry has valid credentials configured.
    Returns True if an endpoint and key are set (and not placeholder text).
    """
    endpoint = FOUNDRY_ENDPOINT
    key = FOUNDRY_API_KEY
    if not endpoint or not key:
        return False
    if "YOUR-RESOURCE" in endpoint or "YOUR_FOUNDRY_API_KEY" in key:
        return False
    return True


def get_status_summary() -> Dict[str, Any]:
    """
    Returns an overview of the current configuration status.
    Useful for health checks and UI status indicators.
    """
    search_ready = is_azure_search_configured()
    foundry_ready = is_azure_foundry_configured()
    
    return {
        "azure_search_configured": search_ready,
        "azure_foundry_configured": foundry_ready,
        "mode": "Live Azure Cloud" if (search_ready and foundry_ready) else "Local Grounded Engine (Demo Mode)",
        "search_index": AZURE_SEARCH_INDEX,
        "foundry_model": FOUNDRY_MODEL,
        "endpoint_configured": bool(AZURE_SEARCH_ENDPOINT)
    }
