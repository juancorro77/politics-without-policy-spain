# Politics without Policy? Measuring Agenda Shift and Executive Evasion in the Spanish Congress of Deputies (2019-2026)

This repository contains the replication package, raw data, computational pipeline, and draft manuscript for the paper: 

> **Politics without Policy? Measuring Agenda Shift and Executive Evasion in the Spanish Congress of Deputies (2019-2026)**
> *Author: Juan Corro*
> *Preprint / Publication Year: 2026*

---

## Abstract

Do parliamentary control sessions serve to hold the executive accountable for public administration, or do they function as a mere arena for partisan confrontation? Using a hybrid computational approach combining rule-based text parsing and Large Language Model (LLM) classification (Gemini API), we audit **2,275 oral Q&A segments** from the weekly control sessions (*Preguntas Orales en Pleno*) of the Spanish Congress of Deputies, covering the **XIV (2019-2023)** and **XV (2023-Present)** Legislatures. 

We operationalize two key metrics:
1. **Agenda Shift Rate (ASR)**: The percentage of the debate dedicated to partisan conflict or territorial legitimacy (*politics*) instead of the registered sectorial policy topic (*policy*).
2. **Evasion Rate (ER)**: The percentage of the minister's response spent on partisan confrontation instead of addressing the technical question.

Our findings reveal a systemic degradation of deliberative quality: **83.8%** of control questions are registered directly on *politics*. For the remaining **16.2%** of questions registered on *policy* (housing, energy, health, etc.), **over 69% (XIV) and 71% (XV)** of the actual debate time is shifted to partisan politics. Furthermore, ministers evade technical questions by dedicating **69.8% (XIV) and 68.9% (XV)** of their response turn to partisan counterattacks.

---

## Repository Structure

```text
politics-without-policy-spain/
├── README.md                  # This file
├── LICENSE                    # MIT License for code
├── .gitignore                 # Files excluded from Git
│
├── paper/                     # Manuscript folder
│   └── draft_manuscript.md    # Draft version of the paper/report
│
├── methodology/               # Theoretical and coding guidelines
│   └── methodological_framework.md # Definitions, variables, and CAP codes
│
├── data/                      # Dataset files
│   ├── raw/                   # Scraped intermediate JSON files
│   │   ├── initiatives_list.json   # 2,558 scraped initiatives
│   │   └── transcripts_dataset.json # 2,275 extracted Q&A segments
│   └── processed/             # Final analyzed files
│       ├── classified_dataset.csv  # Sentiment, classification, turns, and variables
│       └── summary_stats.json      # Aggregated metrics for both legislatures
│
└── scripts/                   # Python pipeline
    ├── 01_scrape_initiatives.py    # Scrapes the Congreso search portal
    ├── 02_scrape_transcripts.py     # Downloads PDFs and extracts text turns
    └── 03_classify_and_analyze.py  # Performs tokenization, dictionary rules, and LLM classification
```

---

## Data Description

*   `data/raw/initiatives_list.json`: Metadata of all registered questions of type "Pregunta oral en Pleno" for the XIV and XV Legislatures (scraped via headless browser to bypass Liferay pagination limits).
*   `data/raw/transcripts_dataset.json`: Full text transcripts matching the initiatives, divided by speaker turns.
*   `data/processed/classified_dataset.csv`: The main replication dataset. Each row corresponds to a single sentence or Speech Unit coded as `policy` or `politics`, with its corresponding speaker, party, legislature, and computed ASR and ER values.

---

## Methodology & Ceding Rules

The text classification utilizes a **hybrid classifier**:
1.  **Rule-based Dictionary**: Speech units are evaluated against a localized dictionary of Spanish political terms (e.g., *amnistía*, *corrupción*, *tránsfuga* for `politics`; *alquiler*, *megavatios*, *carretera* for `policy`).
2.  **LLM Refinement (Gemini API)**: Ambiguous sentences that do not match the dictionary are classified using `gemini-pro`/`gemini-1.5-flash` with a strict zero-shot classification prompt.
3.  **Variables**:
    *   **ASR** is calculated as the ratio of `politics` speech units over the total speech units in a Q&A debate.
    *   **ER** is the ratio of `politics` speech units in the minister's response turns.

For full mathematical formulations and reference literature, see [methodological_framework.md](methodology/methodological_framework.md).

---

## Replication Instructions

### Prerequisites
*   Python 3.10+
*   A Gemini API Key (optional, only if you want to re-run the LLM classification rather than using the cached classifications)

### Setup
1.  Clone the repository:
    ```bash
    git clone https://github.com/juancorro77/politics-without-policy-spain.git
    cd politics-without-policy-spain
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    # If requirements.txt is not present, install core dependencies:
    # pip install playwright beautifulsoup4 pandas requests python-dotenv
    # playwright install chromium
    ```

### Execution Pipeline
*   **Step 1: Scrape Initiatives List**
    ```bash
    python3 scripts/01_scrape_initiatives.py
    ```
*   **Step 2: Scrape Transcripts & Speeches**
    ```bash
    python3 scripts/02_scrape_transcripts.py
    ```
*   **Step 3: Run Classification & Statistical Generation**
    *   To run with the heuristic dictionary fallback (offline/no API key):
        ```bash
        python3 scripts/03_classify_and_analyze.py
        ```
    *   To run with LLM active refinement:
        Create a `.env` file with `GEMINI_API_KEY=your_key` and run:
        ```bash
        python3 scripts/03_classify_and_analyze.py --llm
        ```

---

## License

*   The Python **code** is licensed under the **MIT License**.
*   The **datasets** and **manuscript/reports** are licensed under a **Creative Commons Attribution 4.0 International License (CC-BY 4.0)**.

---

## Citation

If you use this dataset or replication code in your academic work, please cite it as follows:

```bibtex
@dataset{corro_politics_without_policy_2026,
  author    = {Corro, Juan},
  title     = {Replication Package for: Politics without Policy? Measuring Agenda Shift and Executive Evasion in the Spanish Congress of Deputies (2019-2026)},
  year      = {2026},
  publisher = {GitHub},
  journal   = {GitHub Repository},
  howpublished = {\url{https://github.com/juancorro77/politics-without-policy-spain}}
}
```
