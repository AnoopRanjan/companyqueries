"""
===============================================================================
GLOBAL IT KNOWLEDGE HUB — SEED DOCUMENTS LIBRARY (data_seed.py)
===============================================================================
This module contains the initial official-source documents for the Knowledge Hub.
These records are indexed in Azure AI Search and used by the AI model to generate
grounded answers with official references.

===============================================================================
✏️ HOW TO MODIFY THIS FILE:
===============================================================================
1. TO ADD A NEW DOCUMENT RECORD:
   Append a dictionary to the `INITIAL_DOCUMENTS` list below with these fields:
       {
           "id": "unique-slug-001",            # Required: unique document identifier
           "company": "Microsoft",             # Required: must match a company ID
           "category": "Policies",             # Required: must match a category name
           "title": "Document Title",          # Required: official document title
           "content": "Official summary...",   # Required: searchable text summary
           "url": "https://company.com/doc",   # Required: official source URL
           "updatedAt": "2026-05-19"           # Required: publication or check date
       }

2. TO UPDATE AN EXISTING DOCUMENT:
   Locate its dictionary by "id" and update the "content", "title", or "updatedAt".
   Then re-run `python seed.py` to push changes to Azure AI Search.

3. NOTE ON CONTENT:
   Keep content concise, factual, and strictly aligned with the company's
   officially published wording. Avoid subjective interpretations.
===============================================================================
"""

from typing import List, Dict, Any


# =============================================================================
# ✏️ MODIFY HERE: Official Knowledge Base Documents
# =============================================================================
INITIAL_DOCUMENTS: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # MICROSOFT OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "ms-privacy-001",
        "company": "Microsoft",
        "category": "Policies",
        "title": "Microsoft Foundry Models - Data Privacy and Security",
        "content": (
            "Microsoft states that prompts, completions, embeddings and training data "
            "for Models sold by Azure are not made available to other customers or "
            "model providers, and are not used to train generative AI foundation "
            "models without customer permission or instruction. The document also "
            "describes processing, storage, abuse monitoring and deployment geography."
        ),
        "url": "https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy",
        "updatedAt": "2026-05-19"
    },
    {
        "id": "ms-openai-faq-001",
        "company": "Microsoft",
        "category": "Technical Documentation",
        "title": "Azure OpenAI Frequently Asked Questions",
        "content": (
            "Microsoft's Azure OpenAI FAQ states that customer data is not used to "
            "retrain the models. Refer to the linked FAQ and the current data privacy "
            "documentation for details and applicable conditions."
        ),
        "url": "https://learn.microsoft.com/en-us/azure/cognitive-services/openai/faq",
        "updatedAt": "Check official page"
    },
    {
        "id": "ms-copilot-security-001",
        "company": "Microsoft",
        "category": "Security & Compliance",
        "title": "Microsoft Copilot Architecture and Enterprise Data Protection",
        "content": (
            "Enterprise data protection (EDP) for Microsoft Copilot ensures that "
            "customer prompts and responses are not logged or retained by underlying "
            "model providers, honoring tenant boundaries, Microsoft Entra ID access controls, "
            "and Purview compliance policies."
        ),
        "url": "https://learn.microsoft.com/en-us/copilot/microsoft-365/enterprise-data-protection",
        "updatedAt": "2026-04-12"
    },

    # -------------------------------------------------------------------------
    # AWS OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "aws-privacy-001",
        "company": "AWS",
        "category": "Policies",
        "title": "AWS Privacy Notice",
        "content": (
            "The AWS Privacy Notice describes how AWS collects and uses personal "
            "information in connection with AWS websites, applications, products, "
            "services, events and experiences. It distinguishes this notice from "
            "the terms governing customer content stored or processed using AWS."
        ),
        "url": "https://aws.amazon.com/privacy/",
        "updatedAt": "2026-05-18"
    },
    {
        "id": "aws-bedrock-security-001",
        "company": "AWS",
        "category": "Security & Compliance",
        "title": "Amazon Bedrock Data Protection and Governance",
        "content": (
            "Amazon Bedrock does not use customer prompts or completions to train "
            "the base foundation models, and does not share customer data with third-party "
            "model providers. Customer data is encrypted in transit using TLS 1.2+ and "
            "at rest with AWS KMS customer-managed keys."
        ),
        "url": "https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html",
        "updatedAt": "2026-06-01"
    },

    # -------------------------------------------------------------------------
    # GOOGLE OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "google-cloud-privacy-001",
        "company": "Google",
        "category": "Policies",
        "title": "Google Cloud Privacy Notice",
        "content": (
            "The Google Cloud Privacy Notice describes how Google collects and "
            "processes personal information in relation to Google Cloud Platform, "
            "Google Workspace, Marketplace, Cloud Identity and related services. "
            "Consult the current notice for its complete scope and terms."
        ),
        "url": "https://cloud.google.com/terms/cloud-privacy-notice",
        "updatedAt": "2026-10-15"
    },
    {
        "id": "google-terms-001",
        "company": "Google",
        "category": "Policies",
        "title": "Google Cloud Terms Directory",
        "content": (
            "Google Cloud publishes a directory of product terms and policies, "
            "including Google Cloud Platform terms of service, acceptable use "
            "policy and cloud data processing addendum."
        ),
        "url": "https://cloud.google.com/product-terms",
        "updatedAt": "Check official page"
    },
    {
        "id": "google-vertex-privacy-001",
        "company": "Google",
        "category": "Technical Documentation",
        "title": "Google Cloud Vertex AI Data Governance and Customer Data Privacy",
        "content": (
            "Google Cloud Vertex AI guarantees that customer data (including prompts, "
            "generated outputs, cache, and fine-tuning datasets) is never used to train "
            "Google foundation models without explicit customer instruction. Customer data "
            "stays within the customer's defined cloud region."
        ),
        "url": "https://cloud.google.com/vertex-ai/docs/generative-ai/data-governance",
        "updatedAt": "2026-08-20"
    },

    # -------------------------------------------------------------------------
    # IBM OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "ibm-watsonx-gov-001",
        "company": "IBM",
        "category": "Security & Compliance",
        "title": "IBM watsonx Governance and Data Protection Framework",
        "content": (
            "IBM watsonx provides transparent AI model lifecycle tracking, risk "
            "management, and regulatory compliance. IBM commits that client proprietary "
            "data and intellectual property remain isolated, encrypted, and are not utilized "
            "for training public IBM Granite foundation models."
        ),
        "url": "https://www.ibm.com/products/watsonx-governance",
        "updatedAt": "2026-03-10"
    },

    # -------------------------------------------------------------------------
    # ORACLE OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "oracle-cloud-security-001",
        "company": "Oracle",
        "category": "Security & Compliance",
        "title": "Oracle Cloud Infrastructure (OCI) Generative AI Security Architecture",
        "content": (
            "Oracle Cloud Generative AI ensures complete tenant isolation with dedicated "
            "AI clusters. Oracle does not retain customer prompts or model responses, and "
            "third-party model providers have zero access to customer data or fine-tuned weights."
        ),
        "url": "https://www.oracle.com/artificial-intelligence/generative-ai/security/",
        "updatedAt": "2026-05-02"
    },

    # -------------------------------------------------------------------------
    # TCS OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "tcs-ai-framework-001",
        "company": "TCS",
        "category": "Products & Services",
        "title": "TCS AI WisdomNext and Enterprise Responsible AI Framework",
        "content": (
            "Tata Consultancy Services (TCS) AI WisdomNext aggregates multiple generative "
            "AI models into a unified enterprise orchestration plane with embedded safety, "
            "cost optimization, and strict multi-cloud governance rules."
        ),
        "url": "https://www.tcs.com/what-we-do/services/artificial-intelligence",
        "updatedAt": "2026-07-11"
    },

    # -------------------------------------------------------------------------
    # INFOSYS OFFICIAL RECORDS
    # -------------------------------------------------------------------------
    {
        "id": "infosys-topaz-001",
        "company": "Infosys",
        "category": "Products & Services",
        "title": "Infosys Topaz: AI-first Services, Solutions and Platforms",
        "content": (
            "Infosys Topaz leverages generative AI technologies with an applied "
            "responsible-by-design framework, offering enterprise blueprints for cognitive "
            "automation, secure cloud migrations, and customer experience enhancements."
        ),
        "url": "https://www.infosys.com/services/generative-ai/topaz.html",
        "updatedAt": "2026-06-25"
    }
]


def get_all_documents() -> List[Dict[str, Any]]:
    """Returns the complete list of seed documents."""
    return INITIAL_DOCUMENTS
