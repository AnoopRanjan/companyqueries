/**
 * ============================================================================
 * GLOBAL IT KNOWLEDGE HUB — CLIENT LOGIC (app.js)
 * ============================================================================
 * Handles UI interactions, API communications, tab navigation, and grounded
 * answer rendering with official source cards.
 *
 * ✏️ HOW TO MODIFY THIS FILE:
 * 1. Default Company or Category:
 *    - Change `currentCompany` or `currentCategory` variables below.
 * 2. API Endpoints:
 *    - Update `API_CHAT_URL` or `API_COMPANIES_URL` if routing through a proxy.
 * 3. Citation Highlighting:
 *    - Customize `formatAnswerWithCitations` function to change how [SOURCE #]
 *      citations appear in the answer text.
 * ============================================================================
 */

// Application State
let currentCompany = "all";
let currentCategory = "All Categories";
let isLoading = false;

// API Endpoints
const API_CHAT_URL = "/api/chat";
const API_COMPANIES_URL = "/api/companies";
const API_HEALTH_URL = "/api/health";

// DOM Elements
const tabsContainer = document.getElementById("company-tabs-container");
const categorySelect = document.getElementById("category-select");
const searchForm = document.getElementById("search-form");
const questionInput = document.getElementById("question-input");
const charCounter = document.getElementById("char-counter");
const askButton = document.getElementById("ask-button");
const errorBox = document.getElementById("error-box");
const answerPanel = document.getElementById("answer-panel");
const answerText = document.getElementById("answer-text");
const sourcesList = document.getElementById("sources-list");
const copyBtn = document.getElementById("copy-btn");
const engineStatus = document.getElementById("engine-status");
const engineText = document.getElementById("engine-text");

// Default Fallback Lists (used if API call fails)
const DEFAULT_COMPANIES = [
  { id: "all", name: "All Companies" },
  { id: "Microsoft", name: "Microsoft" },
  { id: "Google", name: "Google" },
  { id: "AWS", name: "AWS" },
  { id: "IBM", name: "IBM" },
  { id: "Oracle", name: "Oracle" },
  { id: "Accenture", name: "Accenture" },
  { id: "TCS", name: "TCS" },
  { id: "Infosys", name: "Infosys" },
  { id: "Wipro", name: "Wipro" },
  { id: "Capgemini", name: "Capgemini" }
];

const DEFAULT_CATEGORIES = [
  "All Categories",
  "Brochures",
  "Policies",
  "Products & Services",
  "Security & Compliance",
  "Pricing",
  "Careers",
  "Technical Documentation"
];

// ----------------------------------------------------------------------------
// Initialization
// ----------------------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  initHealthCheck();
  loadCompaniesAndCategories();
  setupEventListeners();
});

/**
 * Checks system operational mode (Azure Cloud vs Local Engine)
 */
async function initHealthCheck() {
  try {
    const res = await fetch(API_HEALTH_URL);
    if (!res.ok) return;
    const data = await res.json();

    if (data.azure_search_configured && data.azure_foundry_configured) {
      engineStatus.className = "status-pill connected";
      engineText.textContent = `Azure Cloud (${data.foundry_model})`;
    } else {
      engineStatus.className = "status-pill demo";
      engineText.textContent = "Local Grounded Engine (Demo)";
    }
  } catch (err) {
    console.warn("Could not retrieve health check:", err);
  }
}

/**
 * Loads company tabs and categories from backend API
 */
async function loadCompaniesAndCategories() {
  try {
    const res = await fetch(API_COMPANIES_URL);
    if (res.ok) {
      const data = await res.json();
      renderCompanyTabs(data.companies || DEFAULT_COMPANIES);
      renderCategoryOptions(data.categories || DEFAULT_CATEGORIES);
      return;
    }
  } catch (err) {
    console.warn("Using fallback company list:", err);
  }
  renderCompanyTabs(DEFAULT_COMPANIES);
  renderCategoryOptions(DEFAULT_CATEGORIES);
}

/**
 * Renders company filter buttons with active state management
 */
function renderCompanyTabs(companies) {
  tabsContainer.innerHTML = "";
  companies.forEach(comp => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `tab ${comp.id === currentCompany ? "active" : ""}`;
    btn.textContent = comp.name;
    btn.dataset.companyId = comp.id;

    btn.addEventListener("click", () => {
      currentCompany = comp.id;
      // Update UI active class across all tabs
      document.querySelectorAll(".company-tabs .tab").forEach(t => t.classList.remove("active"));
      btn.classList.add("active");
    });

    tabsContainer.appendChild(btn);
  });
}

/**
 * Populates the category selector dropdown
 */
function renderCategoryOptions(categories) {
  categorySelect.innerHTML = "";
  categories.forEach(cat => {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = cat;
    categorySelect.appendChild(opt);
  });
}

/**
 * Attaches form, chip, and input event handlers
 */
function setupEventListeners() {
  // Question input character counter
  questionInput.addEventListener("input", () => {
    const count = questionInput.value.length;
    charCounter.textContent = `${count.toLocaleString()} / 1,500`;
  });

  // Category select change
  categorySelect.addEventListener("change", (e) => {
    currentCategory = e.target.value;
  });

  // Example Question Chips
  document.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const company = chip.dataset.company || "all";
      const question = chip.dataset.question || "";

      // Switch company tab
      currentCompany = company;
      const targetTab = document.querySelector(`.tab[data-company-id="${company}"]`);
      if (targetTab) {
        document.querySelectorAll(".company-tabs .tab").forEach(t => t.classList.remove("active"));
        targetTab.classList.add("active");
      }

      // Populate textarea
      questionInput.value = question;
      questionInput.dispatchEvent(new Event("input"));
      questionInput.focus();
    });
  });

  // Form submission
  searchForm.addEventListener("submit", handleSearchSubmit);

  // Copy Answer button
  copyBtn.addEventListener("click", () => {
    const text = answerText.innerText;
    if (!text) return;
    navigator.clipboard.writeText(text).then(() => {
      const original = copyBtn.textContent;
      copyBtn.textContent = "✅ Copied!";
      setTimeout(() => { copyBtn.textContent = original; }, 2000);
    });
  });
}

/**
 * Handles question submission and API communication
 */
async function handleSearchSubmit(e) {
  e.preventDefault();
  const question = questionInput.value.trim();
  if (!question || isLoading) return;

  // Set loading UI
  setLoadingState(true);
  hideError();
  answerPanel.classList.add("hidden");

  try {
    const response = await fetch(API_CHAT_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        company: currentCompany,
        category: currentCategory
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to retrieve answers from the Knowledge Hub.");
    }

    // Display AI Answer
    displayAnswer(data.answer || "", data.sources || []);

  } catch (err) {
    showError(err.message || "Network error. Please verify the server is running.");
  } finally {
    setLoadingState(false);
  }
}

/**
 * Formats and renders the answer and source cards
 */
function displayAnswer(rawAnswer, sources) {
  // Format citations like [SOURCE 1] into badge pills
  answerText.innerHTML = formatAnswerWithCitations(rawAnswer);

  // Render Official Source Document Cards
  sourcesList.innerHTML = "";
  if (!sources || sources.length === 0) {
    sourcesList.innerHTML = "<p class='no-sources'>No matching official source documents found.</p>";
  } else {
    sources.forEach((src, idx) => {
      const card = document.createElement("article");
      card.className = "source-card";
      card.innerHTML = `
        <div class="source-card-header">
          <strong class="source-title">${idx + 1}. ${escapeHtml(src.title)}</strong>
        </div>
        <p class="source-meta">
          <strong>${escapeHtml(src.company)}</strong> · 
          <span>${escapeHtml(src.category)}</span> · 
          <span>Updated: ${escapeHtml(src.updatedAt)}</span>
        </p>
        ${src.content ? `<p class="source-content-preview">"${escapeHtml(src.content)}"</p>` : ""}
        <a href="${escapeHtml(src.url)}" target="_blank" rel="noopener noreferrer" class="source-link">
          Open official document ↗
        </a>
      `;
      sourcesList.appendChild(card);
    });
  }

  answerPanel.classList.remove("hidden");
  answerPanel.scrollIntoView({ behavior: "smooth", block: "start" });
}

/**
 * Converts markdown-style bullets and [SOURCE #] into styled HTML
 */
function formatAnswerWithCitations(text) {
  let escaped = escapeHtml(text);

  // Replace [SOURCE X] with styled pills
  escaped = escaped.replace(/\[SOURCE\s*(\d+)\]/gi, (match, num) => {
    return `<span class="citation-pill">Source ${num}</span>`;
  });

  // Convert markdown bold **text** to <strong>
  escaped = escaped.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  return escaped;
}

function setLoadingState(loading) {
  isLoading = loading;
  askButton.disabled = loading;
  const btnText = askButton.querySelector(".btn-text");
  if (loading) {
    btnText.textContent = "Searching official sources...";
  } else {
    btnText.textContent = "Search & Ask AI →";
  }
}

function showError(msg) {
  errorBox.textContent = msg;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
