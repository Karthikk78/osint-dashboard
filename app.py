import os
import secrets


from flask import session
from flask import Flask, render_template, request
from flask import send_file
from flask import redirect

from modules.whois_lookup import get_whois
from modules.security_headers import check_security_headers
from modules.tech_lookup import get_technologies
from modules.dns_lookup import get_dns_records
from modules.ssl_lookup import get_ssl_info
from modules.risk_score import calculate_risk_score
from database.db import get_analytics
from modules.report_generator import generate_report
from modules.ip_lookup import get_ip_info
from modules.virustotal_lookup import get_virustotal


from database.db import (
    init_db,
    save_scan,
    get_history
)

app = Flask(__name__)
app.secret_key = "osint-dashboard-secret-key"

# Create database/table on startup
init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():

    # Get domain from form
    domain = request.form.get("domain", "").strip().lower()

    # Clean URL input
    domain = domain.replace("https://", "")
    domain = domain.replace("http://", "")
    domain = domain.replace("www.", "")
    domain = domain.split("/")[0]

    # OSINT Modules
    whois_data = get_whois(domain)
    tech_data = get_technologies(domain)
    dns_data = get_dns_records(domain)
    ssl_data = get_ssl_info(domain)
    security_headers = check_security_headers(domain)
    vt_data = get_virustotal(domain)
    
    

    ip_info = {}

    if dns_data.get("A"):

        ip = dns_data["A"][0]

        ip_info = get_ip_info(ip)

    # Risk Score
    risk_score = calculate_risk_score(
        ssl_data,
        security_headers
    )

    # Risk Level
    if risk_score >= 80:
        risk_level = "LOW"

    elif risk_score >= 50:
        risk_level = "MEDIUM"

    else:
        risk_level = "HIGH"

    # Save Scan
    save_scan(
    domain,
    risk_score,
    risk_level
    )

    if "history" not in session:
        session["history"] = []

    history = session["history"]

    history.append({
    "domain": domain,
    "score": risk_score,
    "risk": risk_level
    })

    session["history"] = history
    print("SESSION SAVED:", session["history"])

    

    # Debug Logs
    print("\n========== SCAN RESULT ==========")
    print("DOMAIN:", domain)
    print("WHOIS:", whois_data)
    print("TECH:", tech_data)
    print("DNS:", dns_data)
    print("SSL:", ssl_data)
    print("HEADERS:", security_headers)
    print("RISK SCORE:", risk_score)
    print("RISK LEVEL:", risk_level)
    print("=================================\n")
    
   
    print(session["history"])

    return render_template(
        "results.html",
        domain=domain,
        whois_data=whois_data,
        tech_data=tech_data,
        dns_data=dns_data,
        ssl_data=ssl_data,
        security_headers=security_headers,
        risk_score=risk_score,
        risk_level=risk_level,
        ip_info=ip_info,
        vt_data=vt_data
       
    )

# Scan History
@app.route("/history")
def history():

    history_data = session.get(
    "history",
    []
)
    print("HISTORY DATA:", history_data)

    return render_template(
        "history.html",
        history_data=history_data
    )

@app.route("/clear-history")
def clear_history_route():

    session.pop(
        "history",
        None
    )

    return redirect("/history")

# Analytics Dashboard
@app.route("/dashboard")
def dashboard():

    history = session.get(
        "history",
        []
    )

    total_scans = len(history)

    if total_scans > 0:

        avg_score = round(

            sum(
                item["score"]
                for item in history
            ) / total_scans

        )

    else:

        avg_score = 0

    risk_counts = {

        "LOW": 0,
        "MEDIUM": 0,
        "HIGH": 0

    }

    for item in history:

        risk_counts[
            item["risk"]
        ] += 1

    analytics = {

        "total_scans": total_scans,

        "avg_score": avg_score,

        "risk_data": [

            ["LOW", risk_counts["LOW"]],

            ["MEDIUM", risk_counts["MEDIUM"]],

            ["HIGH", risk_counts["HIGH"]]

        ]

    }

    return render_template(
        "dashboard.html",
        analytics=analytics
    )

# Export PDF Report
@app.route("/export/<domain>")
def export_report(domain):
    import os

    whois_data = get_whois(domain)
    dns_data = get_dns_records(domain)
    ssl_data = get_ssl_info(domain)

    security_headers = check_security_headers(domain)

    risk_score = calculate_risk_score(
        ssl_data,
        security_headers
    )

    if risk_score >= 80:
        risk_level = "LOW"
    elif risk_score >= 50:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    os.makedirs(
    "reports",
    exist_ok=True
)

    filename = f"reports/{domain}.pdf"

    generate_report(
        filename,
        domain,
        whois_data,
        dns_data,
        ssl_data,
        risk_score,
        risk_level
    )

    return send_file(
    filename,
    as_attachment=True,
    download_name=f"{domain}_report.pdf"
)

# Comparison Page
@app.route("/compare")
def compare_page():
    return render_template("compare.html")


@app.route("/compare-result", methods=["POST"])
def compare_result():

    domain1 = request.form["domain1"]
    domain2 = request.form["domain2"]

    ssl1 = get_ssl_info(domain1)
    ssl2 = get_ssl_info(domain2)

    dns1 = get_dns_records(domain1)
    dns2 = get_dns_records(domain2)

    tech1 = get_technologies(domain1)
    tech2 = get_technologies(domain2)

    headers1 = check_security_headers(domain1)
    headers2 = check_security_headers(domain2)

    score1 = calculate_risk_score(
        ssl1,
        headers1
    )

    score2 = calculate_risk_score(
        ssl2,
        headers2
    )

    risk_level1 = (
        "LOW" if score1 >= 80
        else "MEDIUM" if score1 >= 50
        else "HIGH"
    )

    risk_level2 = (
        "LOW" if score2 >= 80
        else "MEDIUM" if score2 >= 50
        else "HIGH"
    )

    return render_template(
    "compare_result.html",

    domain1=domain1,
    domain2=domain2,
    score1=score1,
    score2=score2,
    risk_level1=risk_level1,
    risk_level2=risk_level2,
    ssl1=ssl1,
    ssl2=ssl2,
    dns1=dns1,
    dns2=dns2,
    tech1=tech1,
    tech2=tech2,
    headers1=headers1,
    headers2=headers2
)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )