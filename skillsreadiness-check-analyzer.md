---
name: readiness-check-analyzer
description: >-
  Analyzes SAP Readiness Check (RC) documents for S/4HANA migration planning. Generates per-module executive reports (.docx + interactive .html) covering simplification items, compatibility scope analysis, EWA findings, and Fiori app recommendations. Use when the user says: "analyze readiness check", "RC analysis", "analyze RC", "process readiness check", "run RC analysis", "readiness check results", "new MPW client", "MPW analysis", "new RC client", "start RC for [client]", "analyze RC for [client]", "RC analysis PS", "readiness check PM", "analyze module", "S/4HANA readiness", "generate RC report", "create readiness check report", "migration readiness check", "analiza RC", "análisis de módulo", "análisis readiness check", "nuevo cliente MPW", "generar reporte RC".
allowed-tools: web_search execute write_file read_file edit_file
metadata:
  author: "camilo.cifuentes@sap.com  Global Delivery HUB SCM Americas"
  version: 1.6.1
  tags: sap s4hana readiness-check migration mpw rc-analysis consulting ecc-to-s4hana simplification-items fiori ewa americas gdh
---

# Readiness Check Analyzer

Automated analysis of SAP Readiness Check documents for clients transitioning to S/4HANA. Generates per-module executive reports (.docx + interactive .html) following the MPW (Migration Planning Workshop) methodology.

---

## Activation

Trigger on any of these phrases:

**Direct activation:**
- `analyze readiness check`, `RC analysis`, `analyze RC`
- `process readiness check`, `run RC analysis`, `readiness check results`

**By client / MPW context:**
- `new MPW client`, `MPW analysis`, `new RC client`, `new RC`
- `start RC for [client]`, `analyze RC for [client]`

**By SAP module:**
- `RC analysis PS`, `readiness check PM`, `analyze module [X]`
- `S/4HANA readiness for [module]`

**By output / action:**
- `generate RC report`, `create readiness check report`
- `S/4HANA migration readiness`, `migration readiness check`

**Spanish (backward compatible):**
- `analiza RC`, `análisis de módulo`, `análisis readiness check`
- `nuevo cliente MPW`, `generar reporte RC`

---

## Output Language

**ALL generated content in the .docx and .html reports MUST be written in English**, regardless of the language of the source RC document.

English label reference:
- Resumen Ejecutivo → **Management Summary** | Tabla Resumen → **Summary Table**
- Detalle por Ítem → **Finding Detail** | Resumen de Acciones → **Action Summary**
- Apps Fiori Recomendadas → **Recommended Fiori Apps** | Hallazgos EWA → **EWA Findings**
- Alta/Media/Baja → **High/Medium/Low** | Esfuerzo → **Effort** | Impacto → **Impact**

---

## Output Destination (MANDATORY)

All generated files MUST be saved to the **Joule conversation working directory** — the default folder where Joule stores the current conversation's files.

```python
from pathlib import Path

# Uses the current working directory of the Joule conversation
# This is the default folder Joule uses for every conversation
OUTPUT_DIR = Path.cwd()
print(f"Output folder: {OUTPUT_DIR}")

docx_path = OUTPUT_DIR / f"RC Analysis {MOD} {CLIENT_NAME}.docx"
html_path = OUTPUT_DIR / f"RC Analysis {MOD} {CLIENT_NAME}.html"

def to_file_uri(path: Path) -> str:
    return path.as_uri()

docx_uri = to_file_uri(docx_path)
html_uri  = to_file_uri(html_path)
```

Before generating, inform the user of the resolved output path:
> `📂 Output folder: <OUTPUT_DIR>`

---

## SAP Note & Fiori App Links (MANDATORY)

Every SAP Note number and Fiori App ID **must be verified and hyperlinked** in both .docx and .html outputs.

### Verified URL Patterns

| Type | URL |
|---|---|
| SAP Note | `https://me.sap.com/notes/<NOTE_NUMBER>` |
| Fiori App | `https://fioriappslibrary.hana.ondemand.com/sap/fix/externalViewer/?appId=<APP_ID>` |

Use `fiori_library_url(app_id)` from `scripts/fiori_catalog.py`.
Verify each SAP Note via `web_search` → flag `[verify]` if not found.
Verify each Fiori App via `web_search` → omit link if not found.

### Embedding in .docx

```python
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import docx

def add_hyperlink(paragraph, text, url):
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0070F2')
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(color); rPr.append(u)
    new_run.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink
```

### Embedding in .html
```html
<a href="https://me.sap.com/notes/1234567" target="_blank" class="sap-link">SAP Note 1234567</a>
<a href="https://fioriappslibrary.hana.ondemand.com/sap/fix/externalViewer/?appId=F1234" target="_blank" class="fiori-link">F1234 — App Name</a>
```
```css
.sap-link   { color: #0070F2; text-decoration: underline; font-weight: 500; }
.fiori-link { color: #27ae60; text-decoration: underline; font-weight: 500; }
```

---

## Prerequisites

Python packages: `python-docx`, `openpyxl`, `pandas`, `lxml`
Shared libraries in `plantillas/`: `ewa_lib.py`, `fiori_catalog.py`

```
pip install python-docx openpyxl pandas lxml
```

---

## Source of Truth

```
plantillas/Master_context.md
```

**CRITICAL:** Always read `plantillas/Master_context.md` FIRST (~1538 lines, read in chunks). Follow exactly — override Spanish labels with English equivalents.

---

## Shared Libraries

```python
import sys
from pathlib import Path
WORKSPACE = Path.cwd()
sys.path.insert(0, str(WORKSPACE / "plantillas"))
from ewa_lib import extract_ewa_text, build_ewa_block_for_module
from fiori_catalog import FIORI_CATALOG, fiori_library_url
```

---

## High-Level Workflow

### Step 0 — Welcome Introduction (MANDATORY — show FIRST, ALWAYS)

Fixed. Display EXACTLY as written. No prior context.

---

> ## 📦 SAP Readiness Check Analyzer
>
> ---
>
> Welcome! This skill transforms your SAP Readiness Check results into a clear, executive-ready report — automatically.
>
> **What I do**
> I analyze the SAP Readiness Check (RC) package downloaded from SAP and generate a module-specific report that covers:
> - Simplification Items and their business impact
> - Compatibility Scope analysis
> - EarlyWatch Alert (EWA) findings
> - Recommended Fiori Apps with direct links
> - All SAP Notes with clickable references
>
> **How it works — 3 steps**
>
> | Step | What happens |
> |---|---|
> | 1️⃣ You attach the ZIP | The SAP RC package downloaded from the Readiness Check tool |
> | 2️⃣ I scan and detect | I identify which SAP modules are covered in your RC |
> | 3️⃣ You pick a module | I generate the full report automatically |
>
> **Where your output files will be saved**
> Both files are saved in the **Joule conversation folder** — the same place where Joule keeps your conversation files.
>
> | Output file | Format |
> |---|---|
> | `RC Analysis <MODULE> <CLIENT>.docx` | Word — ready for presentations and reviews |
> | `RC Analysis <MODULE> <CLIENT>.html` | Interactive — clickable SAP Notes, Fiori App links, and copy buttons |
>
> ---
> **Ready to start?**
> Please attach your SAP Readiness Check ZIP file below.
> *(Usually named: `SAP S4HANA Conversion RC_ClientName_XXXX.zip`)*

---

Wait for ZIP. Do NOT proceed until received.

---

### Step 0.1 — Extract the ZIP

```python
import zipfile
from pathlib import Path

rc_zip = Path(RC_ZIP)
extract_dir = rc_zip.parent / rc_zip.stem
extract_dir.mkdir(parents=True, exist_ok=True)

with zipfile.ZipFile(rc_zip, 'r') as z:
    z.extractall(extract_dir)

children = [c for c in extract_dir.iterdir() if not c.name.startswith('.')]
if len(children) == 1 and children[0].is_dir():
    extract_dir = children[0]

print(f"RC_FOLDER: {extract_dir}")
for f in sorted(extract_dir.rglob("*")):
    if f.is_file(): print(f"  {f.relative_to(extract_dir)}")
```

Set `RC_FOLDER`. Stop if corrupted or password-protected.

---

### Step 0.2 — Auto-Detect Client Name

Never ask. Priority:
1. ZIP filename (strip SAP/S4HANA/Conversion/RC/year tokens)
2. Word RC cover page (`Customer:`, `Client:`, `Prepared for:`)
3. `doc.core_properties.company`
4. Excel filenames (non-SAP words)

Store as `CLIENT_NAME`. Show: *"Client detected: GrupoNutresa"*. Ask only if all fail.

---

### Step 0.5 — Detect Modules (DUAL SOURCE)

#### Source A — Word RC (.docx) — min 2 keyword matches

| Module | Key signals |
|---|---|
| PS | CJ01, CJ20N, CN21, CJI3, "Project System", "WBS", "Network Activity", "Project Definition" |
| PM/EAM | IW31, IL01, IP01, IW38, "Plant Maintenance", "Maintenance Order", "Functional Location" |
| MM | ME21N, MIGO, ME51N, MB51, "Materials Management", "Purchase Order", "Goods Receipt" |
| SD | VA01, VF01, VL01N, "Sales Order", "Billing", "Delivery", "Sales & Distribution" |
| FI | FB01, F110, F-02, "Financial Accounting", "General Ledger", "Accounts Payable" |
| CO | KO01, KB11N, KSB1, "Controlling", "Cost Center", "Internal Order" |
| WM/EWM | LT01, LQ01, "Warehouse Management", "Transfer Order", "Extended Warehouse" |
| QM | QA01, QM01, QE01, "Quality Management", "Inspection Lot", "Quality Notification" |
| PP | MD01, CO01, MF60, "Production Planning", "Production Order", "MRP" |
| HCM | PA30, PA40, PT61, "Human Capital", "Payroll", "Personnel" |
| LE | VT01N, "Logistics Execution", "Shipment", "Transportation" |
| PLM | CV01N, "Product Lifecycle", "Document Management", "Engineering Change" |
| CS | IW51, IW52, SM30, "Customer Service", "Service Order", "Service Notification" |

#### Source B — Excel files (PRIMARY — columns `LoB/Technology` and `Business Area`)

```python
import pandas as pd
MODULE_LOB_MAP = {
    "PS":  ["PS", "Project System", "EPPM", "Enterprise Portfolio", "Project Management"],
    "PM":  ["PM", "Plant Maintenance", "EAM", "Enterprise Asset Management", "Asset Management"],
    "MM":  ["MM", "Materials Management", "Procurement", "Purchasing", "Inventory Management"],
    "SD":  ["SD", "Sales", "Sales & Distribution", "Customer Management", "Order Management"],
    "FI":  ["FI", "Financial Accounting", "Finance", "Accounting", "FI-GL", "FI-AP", "FI-AR"],
    "CO":  ["CO", "Controlling", "Management Accounting", "Cost Management"],
    "WM":  ["WM", "EWM", "Warehouse Management", "Extended Warehouse"],
    "QM":  ["QM", "Quality Management", "Quality"],
    "PP":  ["PP", "Production Planning", "Manufacturing", "Production", "MRP"],
    "HCM": ["HCM", "HR", "Human Resources", "Human Capital", "Payroll", "Personnel"],
    "LE":  ["LE", "Logistics Execution", "Shipping", "Transportation Management"],
    "PLM": ["PLM", "Product Lifecycle", "DMS", "Document Management", "Engineering"],
    "CS":  ["CS", "Customer Service", "Service Management", "After-Sales", "Field Service"],
}
excel_modules = set()
for xlsx in Path(RC_FOLDER).glob("*.xlsx"):
    try:
        df = pd.read_excel(xlsx, sheet_name=0, dtype=str)
        for col in ["LoB/Technology", "Business Area"]:
            if col in df.columns:
                for val in df[col].dropna().unique():
                    for mod, patterns in MODULE_LOB_MAP.items():
                        if any(p.lower() in str(val).lower() for p in patterns):
                            excel_modules.add(mod)
    except: continue
```

Combine both. Excel takes priority. Present clean 2-column table. Wait for user selection.

---

### Step 1 — Explore RC Folder

Identify: Word RC `.docx`, Excel files, EWA `.DOC`.

### Step 1B — System Version Analysis (MANDATORY)

Extract version. Classify conversion scenario.

### Step 1C — EWA Analysis (AUTOMATIC if file exists)

Use `ewa_lib.py`.

### Step 2 — Extract Word RC

Read `.docx`. Collect SAP Note numbers.

### Step 3 — Cross with Excel Files (HYBRID)

Filter by module + `LoB/Technology` + `Business Area`. Collect notes. Knowledge Fallback.

### Step 3C — Compatibility Scope Validation (MANDATORY)

Extract from Tables 22-23 + Excel. Report in Management Summary.

### Step 3D — Fiori Apps Enrichment (MANDATORY if roles found)

Use `fiori_library_url(app_id)` for every app.

### Step 4 — Classify Findings

- ID: `MOD-NN` | Type: Issue / Standalone Action / Compatibility Scope | Priority: High/Medium/Low
- Verify each SAP Note: `web_search` → `me.sap.com/notes/<N>`

### Step 5 — Generate .docx (English)

Save to `OUTPUT_DIR / "RC Analysis {MOD} {CLIENT_NAME}.docx"`
- Follow Master_context.md Sections 1-6 (English labels)
- `add_hyperlink()` for all notes and app IDs

### Step 6 — Generate .html (English + Copy Buttons)

Save to `OUTPUT_DIR / "RC Analysis {MOD} {CLIENT_NAME}.html"`

**Tabs:** RC Analysis | EWA Findings (#F0AB00) | Fiori Library (#27ae60)
**SAP '72' font, #0070F2 brand color, self-contained**

#### Copy Buttons (MANDATORY on every analyzed item)

**HTML per finding:**
```html
<div class="finding-block" id="finding-ps-01">
  <div class="finding-header">
    <span class="finding-id">PS-01</span>
    <span class="finding-type issue">Issue</span>
    <span class="priority high">High</span>
    <button class="copy-btn" onclick="copyFinding('finding-ps-01', this)">📋 Copy</button>
  </div>
  <div class="finding-body">
    <p><strong>What is changing:</strong> ...</p>
    <p><strong>Business Impact:</strong> ...</p>
    <p><strong>Actions:</strong> ...</p>
    <p><strong>SAP Note:</strong> <a href="...">SAP Note XXXXXXX</a></p>
  </div>
</div>
```

**Copy All per section:**
```html
<div class="section-header">
  <h2>Finding Detail</h2>
  <button class="copy-all-btn" onclick="copySection('findings-section', this)">📋 Copy All</button>
</div>
<div id="findings-section"> ... </div>
```

**JavaScript:**
```javascript
function copyFinding(blockId, btn) {
  const text = document.getElementById(blockId).querySelector('.finding-body').innerText;
  writeToClipboard(text, btn, '\ud83d\udccb Copy', '\u2705 Copied!');
}
function copySection(sectionId, btn) {
  writeToClipboard(document.getElementById(sectionId).innerText, btn, '\ud83d\udccb Copy All', '\u2705 All Copied!');
}
function writeToClipboard(text, btn, def, done) {
  const restore = () => btn.textContent = def;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => { btn.textContent = done; setTimeout(restore, 2000); }).catch(() => fallback(text, btn, done, restore));
  } else { fallback(text, btn, done, restore); }
}
function fallback(text, btn, done, restore) {
  const ta = document.createElement('textarea');
  ta.value = text; ta.style.cssText = 'position:fixed;opacity:0;';
  document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
  btn.textContent = done; setTimeout(restore, 2000);
}
```

**CSS:**
```css
.copy-btn, .copy-all-btn {
  background:#f0f7ff; border:1px solid #0070F2; border-radius:6px;
  color:#0070F2; cursor:pointer; font-size:0.8rem; font-weight:600;
  padding:4px 10px; transition:background .15s,color .15s; white-space:nowrap;
}
.copy-btn:hover,.copy-all-btn:hover { background:#0070F2; color:#fff; }
.copy-all-btn { font-size:0.85rem; padding:6px 14px; margin-left:auto; }
.finding-header { display:flex; align-items:center; gap:8px; margin-bottom:8px; }
```

**Copy buttons on:** each finding • each EWA block • each Fiori App card • Copy All on Finding Detail / Action Summary / Fiori Apps sections.

Follow Master_context.md STEP 6/6B/6C. English labels.

---

### Step 7 — Closing Message (MANDATORY — after both files saved)

```python
from pathlib import Path
OUTPUT_DIR = Path.cwd()
docx_uri = (OUTPUT_DIR / f"RC Analysis {MOD} {CLIENT_NAME}.docx").as_uri()
html_uri = (OUTPUT_DIR / f"RC Analysis {MOD} {CLIENT_NAME}.html").as_uri()
```

---

> ## ✅ Analysis Complete!
>
> Your reports are saved and ready to open:
> 📂 **`<OUTPUT_DIR>`**
>
> | File | Link |
> |---|---|
> | 📄 Word Report | [RC Analysis <MOD> <CLIENT_NAME>.docx](<DOCX_URI>) |
> | 🌐 Interactive Report | [RC Analysis <MOD> <CLIENT_NAME>.html](<HTML_URI>) |
>
> ---
>
> **What would you like to do next?**
>
> | Option | What to say |
> |---|---|
> | 🔄 Analyze another module from this same RC | `RC analysis <MODULE>` *(e.g. "RC analysis PM")* |
> | 🏢 Start a new client | `new RC` |
> | ⏰ Come back later | Just say `analyze readiness check` or `RC analysis` in a new conversation |
>
> See you next time! 😊

---

## Execution Mode

**Autonomous (auto-yes).** Pause only for: no ZIP / corrupted ZIP / no modules detected / unreadable file.

**Output:** Joule conversation working directory (`Path.cwd()`)

---

## Key Rules

- Welcome intro: VERBATIM, no prior context
- Closing message: always show with output path + clickable file links
- Output: `Path.cwd()` — Joule conversation working directory
- Module detection: Word RC + Excel `LoB/Technology` / `Business Area` (Excel = priority)
- HTML: copy button on EVERY finding, EWA block, Fiori App card + Copy All per section
- Module table: module code + full name only
- All report content: English
- SAP Notes → `me.sap.com/notes/<N>` verified
- Fiori Apps → `?appId=<APP_ID>` verified
- Links in BOTH .docx and .html
- Max 200-250 words per finding
- Action verbs: Analyze / Design / Test / Migrate / Train / Document / Verify / Decide / Evaluate / Replace