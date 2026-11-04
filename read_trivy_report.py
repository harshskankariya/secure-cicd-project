import json
from collections import Counter

# Load Trivy report
with open("trivy-report.json", "r") as file:
    report = json.load(file)

results = report.get("Results", [])

total = 0
severity_count = Counter()

print("\n========== TRIVY SECURITY REPORT ==========\n")

print("Docker Image:", report.get("ArtifactName"))
print("Trivy Version:", report.get("Trivy", {}).get("Version"))

for result in results:

    vulnerabilities = result.get("Vulnerabilities") or []

    for vuln in vulnerabilities:

        total += 1

        severity = vuln.get("Severity", "UNKNOWN").upper()
        severity_count[severity] += 1

print("\n========== VULNERABILITY SUMMARY ==========\n")

print("Total Vulnerabilities:", total)

for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]:
    print(f"{severity}: {severity_count[severity]}")

print("\n========== HIGH AND CRITICAL ISSUES ==========\n")

for result in results:

    vulnerabilities = result.get("Vulnerabilities") or []

    for vuln in vulnerabilities:

        severity = vuln.get("Severity", "").upper()

        if severity in ["HIGH", "CRITICAL"]:

            print("------------------------------------")
            print("CVE ID:", vuln.get("VulnerabilityID"))
            print("Package:", vuln.get("PkgName"))
            print("Installed Version:", vuln.get("InstalledVersion"))
            print("Fixed Version:", vuln.get("FixedVersion"))
            print("Severity:", severity)
            print("Description:", vuln.get("Title"))
            print("Reference:", vuln.get("PrimaryURL"))

print("\n========== SCAN COMPLETED ==========")