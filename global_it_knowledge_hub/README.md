# Global IT Knowledge Hub — Python Edition (30-Minute MVP)

> **ONE SEARCH · OFFICIAL SOURCES · ANSWERS WITH REFERENCES**
>
> A source-grounded enterprise search application built completely in **Python** (FastAPI) that answers questions using officially published information from IT companies (Microsoft, Google, AWS, IBM, Oracle, TCS, Infosys, and others).

---

## 🌟 Key Features & Architectural Highlights

1. **Global Search Across Every IT Company**:
   - Single unified search bar with real-time filtering across all companies or narrowed down to specific enterprise leaders (Microsoft, Google, AWS, IBM, Oracle, TCS, Infosys, Accenture, Wipro, Capgemini).
2. **Category-Level Drill Down**:
   - Filter by *Policies*, *Technical Documentation*, *Security & Compliance*, *Products & Services*, *Pricing*, *Brochures*, and *Careers*.
3. **Dual Execution Engine (Azure Cloud + Local Grounded Engine)**:
   - **Live Azure Cloud Mode**: Connects directly to **Azure AI Search** (`it-company-knowledge` index) and **Azure AI Foundry** (`gpt-4.1-nano` / `gpt-4o-mini`) via REST.
   - **Local Grounded Engine**: Runs immediately out of the box even without Azure keys! Uses a built-in hybrid keyword/relevance search engine with strict source-grounded answers.
4. **Strict Grounding Rules**:
   - Zero hallucination policy: The AI answers strictly using retrieved official records.
   - Cites explicit source numbers (`[SOURCE 1]`, `[SOURCE 2]`).
   - Links directly to official company URLs and displays update dates.
5. **Rich Embedded Comments**:
   - Every file contains clear `[MODIFY HERE]` sections explaining exactly how to customize companies, categories, documents, prompts, ports, and styles.

---

## 🏗️ Architecture

```mermaid
flowchart LR
    User[User Browser] -->|HTTP / SPA| FastAPI[FastAPI Server :8000]
    FastAPI -->|1. Filter & Search Query| AzureSearch[(Azure AI Search / Local Index)]
    AzureSearch -->|2. Top 5 Official Sources| FastAPI
    FastAPI -->|3. Grounded Prompt + Sources| Foundry[Azure AI Foundry Model]
    Foundry -->|4. Answer with [SOURCE #] Citations| FastAPI
    FastAPI -->|5. JSON {answer, sources}| User
```

---

## 🚀 Quick Start (Under 1 Minute)

### 1. Install Dependencies
The application uses Python 3.10+ with standard lightweight packages:
```bash
pip install fastapi uvicorn pydantic httpx python-dotenv pytest
```

### 2. Verify / Seed Document Library
Run the seed script to verify official documents and sync with Azure AI Search:
```bash
python seed.py
```

### 3. Start the Web Server
```bash
python main.py
# Or with uvicorn:
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

### 4. Run Automated Tests
```bash
python test_app.py
# Or with pytest:
# pytest test_app.py -v
```

---

## ⚙️ Configuration (`.env`)

Copy `.env.example` to `.env` to configure your Azure services:

| Environment Variable | Description | Example |
|---|---|---|
| `FOUNDRY_ENDPOINT` | Azure AI Foundry / OpenAI endpoint URL | `https://my-foundry.openai.azure.com/openai/v1/` |
| `FOUNDRY_API_KEY` | Azure AI Foundry API Key | `3a9f...` |
| `FOUNDRY_MODEL` | Deployed model name | `gpt-4.1-nano` or `gpt-4o-mini` |
| `AZURE_SEARCH_ENDPOINT` | Azure AI Search Service URL | `https://my-search.search.windows.net` |
| `AZURE_SEARCH_ADMIN_KEY` | Admin or Query key | `C1D9...` |
| `AZURE_SEARCH_INDEX` | Index name | `it-company-knowledge` |
| `PORT` | Local web server port | `8000` |

> 💡 **Tip:** If these variables are left as placeholders, the application automatically activates **Local Grounded Mode** so you can develop and test immediately offline!

---

## ✏️ Guide to Modifying the Codebase

Every code file includes explicit modification hooks with clear comments:

### 1. How to Add a New Company Tab
Open `companies.py` and locate `COMPANIES`:
```python
# In companies.py:
COMPANIES = [
    {"id": "all", "name": "All Companies"},
    {"id": "Microsoft", "name": "Microsoft"},
    # Add your new company:
    {"id": "Salesforce", "name": "Salesforce"},
    {"id": "NVIDIA", "name": "NVIDIA"},
    ...
]
```

### 2. How to Add Knowledge Categories
Open `companies.py` and locate `CATEGORIES`:
```python
# In companies.py:
CATEGORIES = [
    "All Categories",
    "Brochures",
    "Policies",
    # Add new categories:
    "AI Ethics & Governance",
    "Sustainability & ESG"
]
```

### 3. How to Add Official Documents & URLs
Open `data_seed.py` and append to `INITIAL_DOCUMENTS`:
```python
# In data_seed.py:
{
    "id": "salesforce-einstein-001",
    "company": "Salesforce",
    "category": "Policies",
    "title": "Salesforce Einstein Trust Layer Data Protection",
    "content": "Salesforce guarantees that customer data is never retained by third-party LLM providers...",
    "url": "https://www.salesforce.com/products/einstein/trust/",
    "updatedAt": "2026-07-01"
}
```
Then run `python seed.py` to index the new documents.

### 4. How to Customize the AI Persona or Prompt Rules
Open `foundry_ai.py` and locate `SYSTEM_INSTRUCTIONS`:
```python
# In foundry_ai.py:
SYSTEM_INSTRUCTIONS = """You are Global IT Knowledge Hub...
Strict Grounding Rules:
- Do not invent or assume company policies...
- ALWAYS cite your sources using [SOURCE 1]...
"""
```

### 5. How to Change Server Port or Host
Open `config.py` or `.env`:
```env
HOST=0.0.0.0
PORT=3000
```

### 6. How to Customize the UI Theme & Colors
Open `static/style.css` and modify the `:root` variables:
```css
:root {
  --primary: #1d3f91;   /* Main button and active tab color */
  --accent: #3867e8;    /* Brand accent blue */
  --bg-page: #f5f7fb;   /* Page background */
}
```

---

## 🧪 Testing Queries

Try asking these questions in the UI:

| Company Tab | Test Question | Grounded Answer Focus |
|---|---|---|
| **All Companies** | *What privacy commitments do Microsoft, AWS and Google publish for enterprise AI?* | Cross-company policy comparison |
| **Microsoft** | *Is customer data used to train Azure AI foundation models?* | Grounded in Microsoft Data Privacy docs |
| **AWS** | *What does the AWS Privacy Notice cover?* | Scope & customer content separation |
| **Google** | *Where can I find Google Cloud product terms?* | Google Terms Directory URL & guidance |
| **IBM** | *How does IBM watsonx handle client proprietary data?* | Client isolation & Granite models commitment |
