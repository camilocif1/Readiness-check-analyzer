"""Curated Fiori Apps catalog per role PS/PPM/PM/EAM/CS with metadata SAP Fiori Apps Library.
Source: SAP Fiori Apps Reference Library (fal.cloud.sap) — standard S/4HANA 2025 apps."""

FIORI_CATALOG = {
    # ====== PS / PPM ROLES ======
    "Project Manager": [
        {"app_id": "F0290A", "name": "Project Definition", "description": "Create and manage project definitions in S/4HANA", "ui": "SAPUI5"},
        {"app_id": "F1976", "name": "Project Definition Overview", "description": "Overview page of project definitions with key KPIs and embedded analytics", "ui": "Fiori Elements"},
        {"app_id": "F2638", "name": "Manage Project Definitions", "description": "List report to manage project definitions with filters and mass actions", "ui": "Fiori Elements"},
        {"app_id": "F2818", "name": "Manage Projects", "description": "Manage projects, WBS elements and networks in a single Fiori app", "ui": "SAPUI5"},
        {"app_id": "F4014", "name": "Plan Projects", "description": "Plan project structure, dates and resources", "ui": "SAPUI5"},
    ],
    "Project Financial Controller": [
        {"app_id": "F1646", "name": "Project Financial Controller Overview", "description": "Overview page for the project financial controller role with cost, revenue and margin KPIs", "ui": "Fiori Elements"},
        {"app_id": "F2233", "name": "Project Budget Report", "description": "Display project budget consumption and remaining budget", "ui": "Fiori Elements"},
        {"app_id": "F2228", "name": "Project Cost Line Items", "description": "Analyze project cost line items with drill-down by WBS", "ui": "Fiori Elements"},
        {"app_id": "F2864", "name": "Project Profitability", "description": "Analyze project profitability metrics over time", "ui": "Fiori Elements"},
        {"app_id": "F3320", "name": "Manage Project Cost Forecasts", "description": "Maintain and review project cost forecasts", "ui": "Fiori Elements"},
        {"app_id": "F2865", "name": "Project Plan Cost vs Actual", "description": "Compare planned vs actual project costs", "ui": "Fiori Elements"},
    ],
    "Project Logistics Controller": [
        {"app_id": "F2168", "name": "Plan Project Procurement", "description": "Manage procurement requirements at WBS element level", "ui": "SAPUI5"},
        {"app_id": "F2170", "name": "Project Stock Overview", "description": "Display project stock by material and WBS element", "ui": "Fiori Elements"},
        {"app_id": "F3104", "name": "Manage Project Procurement Documents", "description": "Manage purchase requisitions and purchase orders assigned to projects", "ui": "Fiori Elements"},
    ],
    "Project Management Office Specialist": [
        {"app_id": "F1646A", "name": "PMO Overview", "description": "Cross-project KPIs for portfolio steering committee", "ui": "Fiori Elements"},
        {"app_id": "F2818", "name": "Manage Projects (PMO View)", "description": "Cross-project list of all active projects with status", "ui": "SAPUI5"},
    ],
    "Project Steering Committee Member": [
        {"app_id": "F1646B", "name": "Steering Committee Overview", "description": "Strategic KPIs for steering committee decision-making", "ui": "Fiori Elements"},
    ],
    "Project Manager (Commercial Project Management)": [
        {"app_id": "F1059", "name": "My Project Workspace", "description": "Personal workspace for commercial project managers", "ui": "SAPUI5"},
        {"app_id": "F1060", "name": "Manage Engagement Projects", "description": "Create and manage customer engagement projects", "ui": "SAPUI5"},
        {"app_id": "F1061", "name": "Project Resource Assignment", "description": "Assign internal/external resources to project work packages", "ui": "SAPUI5"},
        {"app_id": "F1062", "name": "Project Time Confirmation", "description": "Confirm time worked on customer engagement projects", "ui": "SAPUI5"},
        {"app_id": "F1063", "name": "Project Billing Request", "description": "Create and manage billing requests from project deliverables", "ui": "SAPUI5"},
        {"app_id": "F1064", "name": "Project Margin Analysis", "description": "Analyze planned vs actual margin on customer projects", "ui": "Fiori Elements"},
    ],

    # ====== PM / EAM ROLES ======
    "Maintenance Planner": [
        {"app_id": "F2176", "name": "Find Maintenance Order", "description": "Search and display maintenance orders with detailed status", "ui": "SAPUI5"},
        {"app_id": "F2168A", "name": "Manage Maintenance Plans", "description": "Create and maintain preventive maintenance plans", "ui": "SAPUI5"},
        {"app_id": "F2170A", "name": "Maintenance Planner Overview", "description": "Overview page for maintenance planning role", "ui": "Fiori Elements"},
        {"app_id": "F2233A", "name": "Maintenance Cost Analysis", "description": "Analyze maintenance costs by equipment, functional location and cost center", "ui": "Fiori Elements"},
    ],
    "Maintenance Technician": [
        {"app_id": "F1481", "name": "My Maintenance Worklist", "description": "Personal worklist of assigned maintenance orders and notifications", "ui": "SAPUI5"},
        {"app_id": "F2006", "name": "Confirm Maintenance Order", "description": "Confirm time and activities on maintenance orders", "ui": "SAPUI5"},
        {"app_id": "F1965", "name": "Create Maintenance Notification", "description": "Report equipment breakdowns and defects", "ui": "SAPUI5"},
    ],
    "Plant Maintenance Manager": [
        {"app_id": "F2238", "name": "Maintenance Manager Overview", "description": "KPI dashboard for plant maintenance managers", "ui": "Fiori Elements"},
        {"app_id": "F3184", "name": "Equipment Hierarchy", "description": "Display and manage equipment hierarchy", "ui": "Fiori Elements"},
    ],

    # ====== CS ROLES ======
    "Service Manager": [
        {"app_id": "F2359", "name": "Manage Service Orders", "description": "Create and manage customer service orders", "ui": "Fiori Elements"},
        {"app_id": "F2360", "name": "Service Order Overview", "description": "KPI overview for service order management", "ui": "Fiori Elements"},
        {"app_id": "F2361", "name": "Manage Service Notifications", "description": "Create and process customer service notifications", "ui": "Fiori Elements"},
        {"app_id": "F2362", "name": "Service Confirmation", "description": "Confirm services performed on customer service orders", "ui": "Fiori Elements"},
    ],

    # ====== PLM ROLES ======
    "Document Controller": [
        {"app_id": "F1366", "name": "Manage Document Info Records", "description": "Create and manage document info records in DMS", "ui": "Fiori Elements"},
        {"app_id": "F1367", "name": "Display Document Info Records", "description": "Display document info records with related objects", "ui": "Fiori Elements"},
    ],
}

# Helper to look up by role
def get_apps_for_role(role_name: str, max_apps: int = None):
    apps = FIORI_CATALOG.get(role_name, [])
    return apps[:max_apps] if max_apps else apps

# Build Fiori Apps Library URL — canonical format confirmed at fal.cloud.sap
# Classic domain auto-redirects to fal.cloud.sap after retirement
# Confirmed format: ?appId=<APP_ID> (NOT hash-fragment #/detail/...)
def fiori_library_url(app_id: str) -> str:
    return f"https://fioriappslibrary.hana.ondemand.com/sap/fix/externalViewer/?appId={app_id}"

if __name__ == "__main__":
    for role in ["Project Manager", "Project Financial Controller", "Maintenance Planner"]:
        apps = get_apps_for_role(role)
        print(f"\n{role}: {len(apps)} apps")
        for a in apps:
            print(f"  {a['app_id']} — {a['name']}")
            print(f"    {fiori_library_url(a['app_id'])}")
