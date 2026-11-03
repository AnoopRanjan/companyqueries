"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — TEST SUITE (test_app.py)
===============================================================================
Automated test suite verifying:
1. Company tabs and category metadata (/api/companies)
2. API health check and configuration status (/api/health)
3. Question answering retrieval pipeline (/api/chat)
4. Company filtering (Microsoft, AWS, Google, All)
5. Category filtering (Policies, Technical Documentation, etc.)
6. Input validation (400 Bad Request on empty or >1,500 character queries)
7. Source document grounding and [SOURCE #] citations

Usage:
    python test_app.py
    # or
    pytest test_app.py -v
===============================================================================
"""

import sys
from pathlib import Path

# Add project root to sys.path so tests can run from any directory
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import app, get_companies_and_categories, get_health_status, chat_endpoint, ChatRequest
import companies
import data_seed
import azure_search
import foundry_ai


def test_companies_endpoint():
    """Verifies that company tabs and categories are served correctly."""
    data = get_companies_and_categories()
    assert "companies" in data
    assert "categories" in data
    assert len(data["companies"]) >= 10
    assert data["companies"][0]["id"] == "all"
    assert "Policies" in data["categories"]
    print("  [PASS] test_companies_endpoint")


def test_health_endpoint():
    """Verifies health check status format."""
    data = get_health_status()
    assert "azure_search_configured" in data
    assert "azure_foundry_configured" in data
    assert "mode" in data
    assert "search_index" in data
    print("  [PASS] test_health_endpoint")


def test_chat_microsoft_query():
    """
    Tests answering a query specific to Microsoft Azure AI policy.
    Verifies that Microsoft sources are returned and cited.
    """
    req = ChatRequest(
        question="Is customer data used to train Azure AI foundation models?",
        company="Microsoft",
        category="All Categories"
    )
    resp = chat_endpoint(req)
    assert hasattr(resp, "answer")
    assert hasattr(resp, "sources")
    assert len(resp.sources) > 0

    # Ensure all returned sources belong to Microsoft
    for src in resp.sources:
        assert src.company == "Microsoft"

    # Ensure citation format is present
    assert "[SOURCE 1]" in resp.answer
    print("  [PASS] test_chat_microsoft_query")


def test_chat_aws_query():
    """Tests query filtered to AWS."""
    req = ChatRequest(
        question="What does the AWS Privacy Notice cover?",
        company="AWS",
        category="All Categories"
    )
    resp = chat_endpoint(req)
    assert len(resp.sources) > 0
    assert any("AWS" in s.company for s in resp.sources)
    print("  [PASS] test_chat_aws_query")


def test_chat_google_query():
    """Tests query filtered to Google Cloud."""
    req = ChatRequest(
        question="Where can I find Google Cloud product terms?",
        company="Google",
        category="Policies"
    )
    resp = chat_endpoint(req)
    assert len(resp.sources) > 0
    assert any(s.company == "Google" for s in resp.sources)
    assert any(s.category == "Policies" for s in resp.sources)
    print("  [PASS] test_chat_google_query")


def test_chat_all_companies_global_query():
    """Tests global search across all companies from a single search query."""
    req = ChatRequest(
        question="What privacy policies do Microsoft, AWS and Google publish?",
        company="all",
        category="All Categories"
    )
    resp = chat_endpoint(req)
    assert len(resp.sources) >= 3
    companies_present = {s.company for s in resp.sources}
    assert "Microsoft" in companies_present or "AWS" in companies_present or "Google" in companies_present
    print("  [PASS] test_chat_all_companies_global_query")


def test_validation_empty_question():
    """Verifies that an empty question is rejected with 400 Bad Request."""
    req = ChatRequest(question="   ", company="all")
    resp = chat_endpoint(req)
    assert resp.status_code == 400
    print("  [PASS] test_validation_empty_question")


def test_validation_exceeding_character_limit():
    """Verifies that questions longer than 1,500 characters are rejected with 400."""
    long_question = "A" * 1501
    req = ChatRequest(question=long_question, company="all")
    resp = chat_endpoint(req)
    assert resp.status_code == 400
    print("  [PASS] test_validation_exceeding_character_limit")


def test_local_search_scoring():
    """Directly tests the tokenization and scoring of local hybrid search."""
    results = azure_search.search_local("customer data train", company="Microsoft")
    assert len(results) > 0
    assert results[0]["company"] == "Microsoft"
    assert "ms-privacy-001" == results[0]["id"]
    print("  [PASS] test_local_search_scoring")


def run_all_tests():
    """Runs all test cases and reports results."""
    print("==================================================================")
    print("      RUNNING GLOBAL IT KNOWLEDGE HUB AUTOMATED TEST SUITE        ")
    print("==================================================================")
    tests = [
        test_companies_endpoint,
        test_health_endpoint,
        test_chat_microsoft_query,
        test_chat_aws_query,
        test_chat_google_query,
        test_chat_all_companies_global_query,
        test_validation_empty_question,
        test_validation_exceeding_character_limit,
        test_local_search_scoring
    ]

    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {t.__name__}: {e}")
            failed += 1

    print("==================================================================")
    print(f"Test Summary: {passed} passed, {failed} failed.")
    print("==================================================================")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
