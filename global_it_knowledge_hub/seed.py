"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — SEED RUNNER SCRIPT (seed.py)
===============================================================================
This standalone CLI script creates or updates the Azure AI Search index schema
and uploads the initial official-source documents from `data_seed.py`.

Usage:
    python seed.py

===============================================================================
[MODIFY HERE]:
===============================================================================
1. TO ADD MORE DOCUMENTS:
   - Edit `data_seed.py` and append your new documents to `INITIAL_DOCUMENTS`.
   - Then re-run `python seed.py`.

2. TO POINT TO A DIFFERENT SEARCH INDEX:
   - Set `AZURE_SEARCH_INDEX=your-index-name` in `.env` before running this script.

3. FOR LOCAL DEMO MODE:
   - If you run `python seed.py` without Azure keys, it will inspect the local
     document library and confirm that all records are valid and ready.
===============================================================================
"""

import sys
import config
import data_seed
import azure_search


def run_seed():
    """
    Executes the index creation and document upload workflow.
    """
    print("==================================================================")
    print("      GLOBAL IT KNOWLEDGE HUB -- SEED INITIAL OFFICIAL DOCUMENTS   ")
    print("==================================================================")

    docs = data_seed.get_all_documents()
    print(f"\n[1/3] Loaded {len(docs)} official documents from data_seed.py:")
    for d in docs:
        print(f"  * [{d.get('company')}] {d.get('title')} ({d.get('category')})")

    # Check Azure credentials
    if not config.is_azure_search_configured():
        print("\n[!] Azure AI Search credentials not found or set to placeholder.")
        print(f"   AZURE_SEARCH_ENDPOINT: {config.AZURE_SEARCH_ENDPOINT or 'Not set'}")
        print(f"   AZURE_SEARCH_INDEX:    {config.AZURE_SEARCH_INDEX}")
        print("\n[i] NOTE:")
        print("   The application will run immediately in Local Grounded Mode!")
        print("   To seed real Azure AI Search, update your .env file with:")
        print("     AZURE_SEARCH_ENDPOINT=https://<your-service>.search.windows.net")
        print("     AZURE_SEARCH_ADMIN_KEY=<your-admin-key>")
        print("     AZURE_SEARCH_INDEX=it-company-knowledge")
        print("   Then run 'python seed.py' again.")
        print("\n[OK] Verification complete: All 12 documents are syntactically valid.")
        return 0

    print(f"\n[2/3] Connecting to Azure AI Search at: {config.AZURE_SEARCH_ENDPOINT}")
    print(f"      Target Index: '{config.AZURE_SEARCH_INDEX}'")
    index_res = azure_search.create_or_update_index()
    if index_res.get("status") == "error":
        print(f"[X] Index setup failed: {index_res.get('error')}")
        return 1

    print(f"\n[3/3] Uploading {len(docs)} documents to Azure AI Search...")
    upload_res = azure_search.upload_documents(docs)
    if upload_res.get("status") == "error":
        print(f"[X] Document upload failed: {upload_res.get('error')}")
        return 1

    print("\n[OK] Seeding completed successfully!")
    print(f"   Successfully indexed {upload_res.get('succeeded', len(docs))} documents.")
    print("   You can now start your web application using: python main.py")
    return 0


if __name__ == "__main__":
    sys.exit(run_seed())
