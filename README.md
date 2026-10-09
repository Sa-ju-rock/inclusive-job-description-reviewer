# ⚖️ EquiText: Bias-Free Job Description Reviewer
### *UN Sustainable Development Goal 5 (SDG 5): Gender Equality*

> **Problem Statement:**  
> *"Unconscious gender bias in job descriptions prevents diverse talent from applying to technical roles."*  
>  
> **Solution:**  
> A rule-based NLP web application built with **Python**, **Django**, and **Tailwind CSS** that detects gender-coded wording in job postings, calculates a **Gender Neutrality Index (0–100%)**, and provides concrete inclusive replacement suggestions in real time.

---

## 🌟 Key Features

1. **Rule-Based NLP Analyzer (`bias_analyzer/utils/analyzer.py`):**
   - Screens text against peer-reviewed gendered lexicons (grounded in *Gaucher, Friesen, & Kay, 2011*).
   - Flags **Masculine-coded terms** (e.g., *"ninja"*, *"rockstar"*, *"dominant"*, *"competitive"*, *"enforce"*, *"crush"*).
   - Flags **Feminine-coded terms** (e.g., *"nurturing"*, *"supportive"*, *"collaborative"*, *"interpersonal"*, *"compassionate"*).
   - Computes masculine and feminine wording density (% of total text).
   - Calculates a **Gender Neutrality Index (0–100%)** factoring in both asymmetry and bias concentration.
   - Categorizes findings into clear severity levels (*Strongly Neutral*, *Mild Bias*, *Moderate Bias*, *High Bias*).

2. **Interactive Results Dashboard (`result.html`):**
   - **SVG Neutrality Score Ring**: Visual circular score gauge with dynamic color themes.
   - **Annotated Text View**: Original text with interactive color-coded badges (`M` / `F`) with hover tooltips showing why each term was flagged.
   - **One-Click Revised Version**: Automated inclusive rewritten text with a *"Copy to Clipboard"* button.
   - **Actionable Replacements Catalog**: Side-by-side cards displaying occurrence counts, psychological context, and concrete inclusive alternatives.

3. **Beginner-Friendly Architecture:**
   - Full Django MTV (Model-Template-View) pattern.
   - SQLite database (zero configuration required).
   - Tailwind CSS via CDN (no Node.js / npm build steps needed).
   - Built-in one-click sample presets on the landing page for quick testing.

---

## 📂 Project Directory Layout

```text
bo final project/
├── manage.py                          # Django administrative CLI runner
├── requirements.txt                   # Project dependencies (Django, gunicorn, etc.)
├── README.md                          # Documentation and setup guide
│
├── job_reviewer_project/              # Core Django project configuration
│   ├── __init__.py
│   ├── asgi.py                        # ASGI configuration
│   ├── settings.py                    # App settings, templates, static config
│   ├── urls.py                        # Root URL router
│   └── wsgi.py                        # WSGI production entrypoint
│
└── bias_analyzer/                     # Main application
    ├── __init__.py
    ├── admin.py                       # Django admin configuration
    ├── apps.py                        # App metadata
    ├── forms.py                       # Form with input validation & Tailwind styling
    ├── models.py                      # JobDescriptionReview SQLite model
    ├── tests.py                       # 9 unit tests covering NLP logic & views
    ├── urls.py                        # App route handlers
    ├── views.py                       # Request controllers & template renderers
    │
    ├── utils/                         # NLP & Lexicon Engine
    │   ├── __init__.py
    │   ├── words_database.py          # Research dictionaries & sample postings
    │   └── analyzer.py                # Regex tokenization, scoring formula, highlighter
    │
    ├── templates/
    │   └── bias_analyzer/
    │       ├── base.html              # Base layout (Tailwind CSS, SDG 5 banner, footer)
    │       ├── index.html             # Landing page with textarea & sample presets
    │       ├── result.html            # Results dashboard with score ring & badges
    │       ├── history.html           # Historical audit log table
    │       └── about.html             # SDG 5 research context & formula explanation
    │
    └── static/
        └── bias_analyzer/
            ├── css/custom.css         # Print & tooltip styles
            └── js/main.js             # UI helpers
```

---

## 🚀 Step-by-Step Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed:
```bash
python --version
```

### 2. (Recommended) Create & Activate a Virtual Environment
```bash
# On Windows (PowerShell / Command Prompt):
python -m venv venv
.\venv\Scripts\activate

# On macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
Create the SQLite database tables:
```bash
python manage.py migrate
```

### 5. (Optional) Create an Admin Superuser
To inspect saved reviews in the Django Admin portal:
```bash
python manage.py createsuperuser
```

### 6. Run the Local Development Server
```bash
python manage.py runserver
```

Now open your web browser and navigate to:  
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Running Automated Tests

To run the unit test suite covering the NLP analyzer, form validation, and view routing:
```bash
python manage.py test
```
*Expected output: `Ran 9 tests in 0.2s - OK`*

---

## 🧠 How the Rule-Based NLP Analyzer Works

### 1. Linguistic Lexicons (`utils/words_database.py`)
Rooted in occupational psychology research (*Gaucher et al., 2011*):
- **Masculine-Coded Terms:** Agentic words emphasizing individual competition, hierarchy, or aggression (`rockstar`, `ninja`, `dominant`, `competitive`, `enforce`, `crush`, `authoritative`, etc.).
- **Feminine-Coded Terms:** Communal words emphasizing caregiving, accommodation, or subordinate traits (`nurturing`, `supportive`, `collaborative`, `interpersonal`, `compassionate`, `gentle`, etc.).

### 2. Gender Neutrality Index (GNI) Formula
$$\text{GNI} = \max\Big(0, 100 - \text{Imbalance Penalty} - \text{Density Penalty}\Big)$$

- **Imbalance Penalty ($0 \dots 40$ points):** Penalizes one-sided gender skew:
  $$\text{Imbalance} = \frac{|M - F|}{M + F} \times 40$$
- **Density Penalty ($0 \dots 60$ points):** Penalizes high saturation of coded buzzwords relative to total document length:
  $$\text{Density} = \min\left(60, \frac{M + F}{N} \times 750\right)$$
- If zero coded words are present, $\text{GNI} = 100\%$.

### 3. Concrete Inclusive Replacements
| Flagged Word | Recommended Inclusive Alternatives | Rationale |
| :--- | :--- | :--- |
| `rockstar` / `ninja` | *skilled professional*, *senior engineer* | Replaces exclusionary bravado with professional competency. |
| `dominant` | *leading*, *prominent*, *influential* | Shifts tone from authoritarian control to market leadership. |
| `competitive` | *growth-oriented*, *motivated*, *high-achieving* | Avoids zero-sum framing that discourages team players. |
| `enforce` | *maintain*, *uphold*, *ensure compliance* | Replaces policing connotations with stewardship. |
| `nurturing` | *fostering*, *mentoring*, *developing* | Retains developmental intent without maternal stereotyping. |
| `supportive` | *collaborative*, *enabling*, *constructive* | Prevents framing technical roles as administrative support. |

---

## 🎯 Testing with Included Sample Presets

On the landing page, click any of the preset buttons in the top bar:
1. **"Rockstar" Tech Job (Biased):** Loads a typical Silicon Valley post saturated with masculine buzzwords (`rockstar`, `ninja`, `dominate`, `crush`, `fearless`, `workaholic`). Result score: **0% (High Bias)**.
2. **Feminine Coded Sample:** Loads a community lead posting loaded with communal terms (`nurture`, `supportive`, `compassionate`, `gentle`, `caring`). Result score: **0% (Feminine-Skewed)**.
3. **Inclusive Job Sample:** Loads a balanced software engineering posting focused on technical outcomes, deliverables, and collaboration. Result score: **100% (Strongly Gender-Neutral)**.

---

## 🌐 Alignment with UN SDG 5

- **Target 5.5:** *"Ensure women's full and effective participation and equal opportunities for leadership at all levels of decision-making in political, economic and public life."*
- **Impact:** By neutralizing language in job descriptions, companies increase female applicant rates to technical and leadership roles by **up to 42%**, breaking systemic occupational segregation in STEM.
