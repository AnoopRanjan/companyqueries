"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — AZURE AI SEARCH CLIENT (azure_search.py)
===============================================================================
This module handles all communication with Azure AI Search:
1. Creating or updating the search index schema (`it-company-knowledge`)
2. Uploading official company documents (seeding)
3. Executing keyword / semantic search queries with company & category filters
4. Built-in fallback search engine (runs automatically when Azure is not configured)

===============================================================================
✏️ HOW TO MODIFY THIS FILE:
===============================================================================
1. TO CHANGE THE NUMBER OF RETURNED DOCUMENTS:
   - Modify the `DEFAULT_TOP_RESULTS` constant (default is 5).

2. TO ADD NEW SEARCHABLE FIELDS (e.g., tags, region, author):
   - Add the field definition to `INDEX_FIELDS` below.
   - Update `SELECT_FIELDS` so the new field is returned in search responses.

3. TO SWITCH BETWEEN AZURE CLOUD & LOCAL DEMO ENGINE:
   - Set valid Azure keys in `.env` to use live Azure AI Search.
   - Leave them blank to use the built-in local search index immediately.
===============================================================================
"""

import re
from typing import List, Dict, Any, Optional
import httpx

import config
from data_seed import INITIAL_DOCUMENTS


# =============================================================================
# ✏️ MODIFY HERE: Search Index Fields Schema
# =============================================================================
INDEX_FIELDS = [
    {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
    {"name": "company", "type": "Edm.String", "filterable": True, "facetable": True, "searchable": True},
    {"name": "category", "type": "Edm.String", "filterable": True, "facetable": True, "searchable": True},
    {"name": "title", "type": "Edm.String", "searchable": True},
    {"name": "content", "type": "Edm.String", "searchable": True},
    {"name": "url", "type": "Edm.String", "searchable": False},
    {"name": "updatedAt", "type": "Edm.String", "filterable": True}
]

# The fields returned in search result documents
SELECT_FIELDS = "id, company, category, title, content, url, updatedAt"

# Default number of relevant sources to retrieve for question answering
DEFAULT_TOP_RESULTS = 5


# =============================================================================
# Azure AI Search REST API Client
# =============================================================================

def _build_azure_headers() -> Dict[str, str]:
    """Builds standard HTTP headers for Azure AI Search REST API requests."""
    return {
        "Content-Type": "application/json",
        "api-key": config.AZURE_SEARCH_ADMIN_KEY
    }


def create_or_update_index() -> Dict[str, Any]:
    """
    Creates or updates the Azure AI Search index schema.
    Uses Azure Search REST API: PUT /indexes/{index_name}?api-version=...
    """
    if not config.is_azure_search_configured():
        return {
            "status": "skipped",
            "message": "Azure Search not configured. Local fallback index will be used."
        }

    endpoint = config.AZURE_SEARCH_ENDPOINT.rstrip("/")
    url = f"{endpoint}/indexes/{config.AZURE_SEARCH_INDEX}?api-version={config.AZURE_SEARCH_API_VERSION}"
    payload = {
        "name": config.AZURE_SEARCH_INDEX,
        "fields": INDEX_FIELDS
    }

    print(f"[AzureSearch] Creating/updating index '{config.AZURE_SEARCH_INDEX}' at {url}...")
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.put(url, headers=_build_azure_headers(), json=payload)
            if resp.status_code in [200, 201, 204]:
                print("[AzureSearch] Index created/updated successfully!")
                return {"status": "success", "code": resp.status_code}
            else:
                error_msg = f"HTTP {resp.status_code}: {resp.text}"
                print(f"[AzureSearch] Index creation failed: {error_msg}")
                return {"status": "error", "error": error_msg}
    except Exception as e:
        print(f"[AzureSearch] Error contacting Azure: {e}")
        return {"status": "error", "error": str(e)}


def upload_documents(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Uploads or merges documents into the Azure AI Search index.
    Uses Azure Search REST API: POST /indexes/{index_name}/docs/index?api-version=...
    """
    if not config.is_azure_search_configured():
        return {
            "status": "skipped",
            "count": len(documents),
            "message": "Azure Search not configured. Seed documents saved in local index."
        }

    endpoint = config.AZURE_SEARCH_ENDPOINT.rstrip("/")
    url = f"{endpoint}/indexes/{config.AZURE_SEARCH_INDEX}/docs/index?api-version={config.AZURE_SEARCH_API_VERSION}"

    payload = {
        "value": [
            {
                "@search.action": "mergeOrUpload",
                **doc
            }
            for doc in documents
        ]
    }

    print(f"[AzureSearch] Uploading {len(documents)} documents to '{config.AZURE_SEARCH_INDEX}'...")
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, headers=_build_azure_headers(), json=payload)
            if resp.status_code in [200, 201]:
                data = resp.json()
                succeeded = sum(1 for item in data.get("value", []) if item.get("status") is True)
                print(f"[AzureSearch] Successfully uploaded {succeeded}/{len(documents)} documents.")
                return {"status": "success", "succeeded": succeeded, "results": data.get("value", [])}
            else:
                error_msg = f"HTTP {resp.status_code}: {resp.text}"
                print(f"[AzureSearch] Document upload failed: {error_msg}")
                return {"status": "error", "error": error_msg}
    except Exception as e:
        print(f"[AzureSearch] Error uploading documents: {e}")
        return {"status": "error", "error": str(e)}


def search_azure(query: str, company: str = "all", category: str = "All Categories", top: int = DEFAULT_TOP_RESULTS) -> List[Dict[str, Any]]:
    """
    Queries Azure AI Search with company & category OData filters.
    """
    endpoint = config.AZURE_SEARCH_ENDPOINT.rstrip("/")
    url = f"{endpoint}/indexes/{config.AZURE_SEARCH_INDEX}/docs/search?api-version={config.AZURE_SEARCH_API_VERSION}"

    # Build OData filter expressions
    filters = []
    if company and company.lower() != "all":
        safe_company = company.replace("'", "''")
        filters.append(f"company eq '{safe_company}'")

    if category and category != "All Categories":
        safe_category = category.replace("'", "''")
        filters.append(f"category eq '{safe_category}'")

    filter_expr = " and ".join(filters) if filters else None

    payload: Dict[str, Any] = {
        "search": query if query.strip() else "*",
        "top": top,
        "select": SELECT_FIELDS
    }
    if filter_expr:
        payload["filter"] = filter_expr

    with httpx.Client(timeout=20.0) as client:
        resp = client.post(url, headers=_build_azure_headers(), json=payload)
        if resp.status_code == 200:
            data = resp.json()
            return [item for item in data.get("value", [])]
        else:
            print(f"[AzureSearch] Query failed with code {resp.status_code}: {resp.text}")
            return []


# =============================================================================
# Built-in Local Hybrid Search (Zero-Dependency Offline Fallback)
# =============================================================================

def _tokenize(text: str) -> List[str]:
    """Extracts lowercase alphanumeric tokens for local search scoring."""
    return re.findall(r"\w+", text.lower())


def search_local(query: str, company: str = "all", category: str = "All Categories", top: int = DEFAULT_TOP_RESULTS) -> List[Dict[str, Any]]:
    """
    Intelligent built-in search engine for local testing.
    Filters by company and category, and scores relevance using term frequency
    across title (weighted 3x) and content (weighted 1x).
    """
    filtered_docs = []
    for doc in INITIAL_DOCUMENTS:
        # Company tab filter
        if company and company.lower() != "all":
            if doc.get("company", "").lower() != company.lower():
                continue
        # Category dropdown filter
        if category and category != "All Categories":
            if doc.get("category", "").lower() != category.lower():
                continue
        filtered_docs.append(doc)

    if not query.strip():
        return filtered_docs[:top]

    query_tokens = _tokenize(query)
    scored_docs = []

    for doc in filtered_docs:
        title_tokens = _tokenize(doc.get("title", ""))
        content_tokens = _tokenize(doc.get("content", ""))
        company_tokens = _tokenize(doc.get("company", ""))

        score = 0.0
        for token in query_tokens:
            # Title matches are prioritized
            score += title_tokens.count(token) * 3.0
            # Content matches
            score += content_tokens.count(token) * 1.0
            # Company name matches
            score += company_tokens.count(token) * 2.0

        if score > 0 or not query_tokens:
            scored_docs.append((score, doc))

    # Sort descending by relevance score
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for _, doc in scored_docs[:top]]


# =============================================================================
# Unified Search Entrypoint
# =============================================================================

def search_documents(query: str, company: str = "all", category: str = "All Categories", top: int = DEFAULT_TOP_RESULTS) -> List[Dict[str, Any]]:
    """
    Main search function:
    - If Azure AI Search is configured, queries Azure cloud index.
    - Otherwise (or if Azure fails), seamlessly uses local hybrid search.
    """
    if config.is_azure_search_configured():
        try:
            results = search_azure(query, company, category, top)
            if results:
                return results
            print("[Search] Azure search returned no results, falling back to local library.")
        except Exception as e:
            print(f"[Search] Azure Search exception ({e}), falling back to local search.")

    return search_local(query, company, category, top)
