def calculate_risk_score(
    ssl_data,
    security_headers
):

    score = 0

    # SSL

    if not ssl_data.get("error"):

        score += 20

        if ssl_data.get(
            "days_remaining",
            0
        ) > 30:

            score += 20

    # Security Headers

    for status in security_headers.values():

        if status == "Present":

            score += 10

    if score > 100:
        score = 100

    return score