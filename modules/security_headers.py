import requests

def check_security_headers(domain):

    try:

        response = requests.get(
            f"https://{domain}",
            timeout=10,
            headers={
                "User-Agent":"Mozilla/5.0"
            }
        )

        headers = response.headers

        checks = {

            "Strict-Transport-Security":
                "Present" if
                "Strict-Transport-Security"
                in headers
                else "Missing",

            "Content-Security-Policy":
                "Present" if
                "Content-Security-Policy"
                in headers
                else "Missing",

            "X-Frame-Options":
                "Present" if
                "X-Frame-Options"
                in headers
                else "Missing",

            "X-Content-Type-Options":
                "Present" if
                "X-Content-Type-Options"
                in headers
                else "Missing",

            "Referrer-Policy":
                "Present" if
                "Referrer-Policy"
                in headers
                else "Missing",

            "Permissions-Policy":
                "Present" if
                "Permissions-Policy"
                in headers
                else "Missing"
        }

        return checks

    except Exception as e:

        return {
            "error": str(e)
        }