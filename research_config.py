
RESEARCH_FIELDS = [
    "authentication_methods",
    "credential_access",
    "api_breadth",
    "mcp_available",
    "buildability_verdict",
    "main_blocker",
    "evidence_urls"
]

BUILDABILITY_OPTIONS = [
    "Buildable",
    "Partially Buildable",
    "Blocked",
    "Needs Verification"
]

CREDENTIAL_OPTIONS = [
    "Self-serve",
    "Approval Required",
    "Contact Sales",
    "Not Available",
    "Needs Verification"
]

MCP_OPTIONS = [
    "Available",
    "Not Available",
    "Third-party Available",
    "Needs Verification"
]

print("Research configuration loaded!")
print("Research fields:", len(RESEARCH_FIELDS))
