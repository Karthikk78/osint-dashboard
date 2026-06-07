from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)



def generate_report(
    filename,
    domain,
    whois_data,
    dns_data,
    ssl_data,
    risk_score,
    risk_level
):

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "OSINT Dashboard Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,12)
    )

    content.append(
        Paragraph(
            f"Target: {domain}",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            f"Risk Score: {risk_score}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {risk_level}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            "WHOIS Information",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            str(whois_data),
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            "DNS Information",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            str(dns_data),
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1,10)
    )

    content.append(
        Paragraph(
            "SSL Information",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            str(ssl_data),
            styles["Normal"]
        )
    )

    pdf.build(content)