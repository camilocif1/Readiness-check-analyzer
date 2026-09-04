"""ewa_lib.py — Reusable library to extract findings from an EWA .DOC (WordML XML).
Invoked from the RC report master generator."""
import re
from pathlib import Path

# ============================================================================
# 1) Generic WordML XML (.DOC) extractor — returns plain text
# ============================================================================
def extract_ewa_text(ewa_path: Path) -> str:
    """Reads an EWA .DOC (WordML XML) and returns concatenated paragraphs as plain text."""
    with open(ewa_path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    paras = re.findall(r'<w:p[\s>].*?</w:p>', raw, flags=re.DOTALL)
    out = []
    for p in paras:
        parts = re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, flags=re.DOTALL)
        if parts:
            text = "".join(parts)
            text = (text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                        .replace("&quot;", '"').replace("&apos;", "'").replace("&#xA;", " "))
            if text.strip():
                out.append(text.strip())
    return "\n".join(out)

# ============================================================================
# 2) Generic system-wide findings (apply to all modules)
# ============================================================================
def extract_system_findings(txt: str) -> dict:
    """Extracts system-wide findings from the EWA (red report rating)."""
    findings = {
        "rating_overall": "",
        "alerts_red": [],
        "performance": {},
        "kpis": [],
        "abap_dumps_count": None,
        "update_errors_count": None,
        "hana_memory_critical": False,
        "security_alerts": [],
    }
    m = re.search(r'Alerts Decisive For Red Report\s*(.+?)(?:Alert Overview|Check Overview)',
                  txt, re.DOTALL)
    if m:
        for ln in m.group(1).split("\n"):
            ln = ln.strip()
            if ln and len(ln) > 5 and "Alerts" not in ln:
                findings["alerts_red"].append(ln)

    m = re.search(r'Alert Overview\s*(.+?)(?:Hide and Snooze)', txt, re.DOTALL)
    if m:
        for ln in m.group(1).split("\n"):
            ln = ln.strip()
            if ln and len(ln) > 10 and not ln.startswith(("Hide", "Note:", "How to")):
                findings["alerts_red"].append(ln)

    perf_block = re.search(r'Performance Indicators for [A-Z0-9]+\s*(.+?)Landscape', txt, re.DOTALL)
    if perf_block:
        lines = [l.strip() for l in perf_block.group(1).split("\n") if l.strip()]
        i = 0
        while i < len(lines) - 2:
            if lines[i] in ("System Performance", "Hardware Capacity",
                            "Database Performance", "Database Space Management"):
                area = lines[i]; indicator = lines[i+1]; val = lines[i+2]
                findings["kpis"].append({"area": area, "indicator": indicator, "value": val})
                i += 3
            else:
                i += 1

    m = re.search(r'(\d+)\s+ABAP dumps have been recorded', txt)
    if m:
        findings["abap_dumps_count"] = int(m.group(1))

    m = re.search(r'We have detected\s+(\d+)\s+update errors', txt)
    if m:
        findings["update_errors_count"] = int(m.group(1))

    if "memory usage of tables exceeds 50%" in txt or "Memory consumption of Indexserver" in txt:
        findings["hana_memory_critical"] = True

    findings["side_effects"] = []
    for area in ["SAP Finance", "SAP Logistics General", "SAP Cross-Application Components"]:
        block = re.search(
            rf'Missing Side Effect Solving Notes for {re.escape(area)}\s*(.+?)(?:Implemented|Missing|Important SAP Notes)',
            txt, re.DOTALL)
        if block:
            notes = re.findall(r'(\d{7})\s+(\d{7})\s+(.+?)(?:Can be implemented|Not downloaded)',
                                block.group(1), re.DOTALL)
            for cause, solve, desc in notes:
                findings["side_effects"].append({
                    "area": area, "causing": cause.strip(),
                    "solving": solve.strip(),
                    "description": desc.strip()[:150],
                })
    return findings

# ============================================================================
# 3) Module-filtered findings
# ============================================================================
MODULE_SIGNALS = {
    "PS": {
        "tcodes": ["CJ20N", "CJI3", "CJI3N", "CJ40", "CJ41", "CJ02", "CN21", "CN22",
                   "CJ20", "CJ88", "CJ02N", "CN41", "CN43", "CJB1", "CJ7G",
                   "CJ08", "CJB2", "CN23", "CN52N", "CN53N", "CJEH"],
        "fiori_app_prefixes": ["i2d.eppm", "ps.fpm", "F1976", "F2638", "F2818"],
        "z_keywords": ["PROJ", "WBS", "PS_"],
        "areas": ["PS-"],
    },
    "PM": {
        "tcodes": ["IW21", "IW22", "IW23", "IW28", "IW29", "IW31", "IW32", "IW33",
                   "IW37N", "IW38", "IW39", "IW40", "IW47", "IW48", "IW49", "IW58",
                   "IW59", "IW65", "IW66", "IW67", "IW68", "IL01", "IL02", "IL03",
                   "IH01", "IH08", "IH09", "IP10", "IP30", "IP42", "IB51", "IB52",
                   "IB53", "MAINT", "ZIW", "OICOM"],
        "fiori_app_prefixes": ["i2d.eam", "EAM_", "F2168", "F2170", "F2176"],
        "z_keywords": ["EAM", "MAINT", "OICOM", "_PM_"],
        "areas": ["PM-", "EAM"],
    },
    "PLM": {
        "tcodes": ["CC01", "CC02", "CC04", "CC05", "CV01N", "CV02N", "CV03N",
                   "CV04N", "CL01", "CL02", "CL03", "CT04", "DMS", "CS01", "CS02",
                   "CS03", "CS11", "CS12", "CS13", "CA01", "CA02", "CA03",
                   "/PLMB/", "PPM"],
        "fiori_app_prefixes": ["plm.", "i2d.plm", "DMS_"],
        "z_keywords": ["PLM", "RECIPE", "SPEC_"],
        "areas": ["PLM"],
    },
    "EPPM": {
        "tcodes": ["CJ20N", "CJI3", "CJI3N", "CN21", "CN22", "/RPM/", "RPM_"],
        "fiori_app_prefixes": ["i2d.eppm", "rpm.", "ppm.", "F2638"],
        "z_keywords": ["PORTFOLIO", "RPM_", "PROJ"],
        "areas": ["PS-", "EPPM"],
    },
}

def build_ewa_block_for_module(ewa_text: str, mod_key: str, mod_name: str) -> dict:
    """Builds a structured EWA block for a specific module."""
    signals = MODULE_SIGNALS.get(mod_key, {})
    tcodes = signals.get("tcodes", [])
    keywords = signals.get("z_keywords", []) + signals.get("areas", [])

    system_findings = extract_system_findings(ewa_text)

    module_lines = []
    for line in ewa_text.split("\n"):
        line_up = line.upper()
        if any(t in line_up for t in tcodes) or any(k.upper() in line_up for k in keywords):
            if len(line.strip()) > 10:
                module_lines.append(line.strip())

    return {
        "module": mod_name,
        "system_wide": system_findings,
        "module_specific": module_lines[:30],
        "recommendations": [
            l for l in module_lines
            if any(w in l.lower() for w in ["recommend", "should", "must", "required", "note"])
        ][:10]
    }
