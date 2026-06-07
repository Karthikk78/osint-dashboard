import requests

def get_technologies(domain):

    try:

        url = f"https://{domain}"

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        headers = response.headers

        tech = {}

        tech["server"] = headers.get(
            "Server",
            "Unknown"
        )

        tech["powered_by"] = headers.get(
            "X-Powered-By",
            "Not Exposed"
        )

        tech["cdn"] = "Unknown"

        if "cloudflare" in str(headers).lower():
            tech["cdn"] = "Cloudflare"

        elif "akamai" in str(headers).lower():
            tech["cdn"] = "Akamai"

        elif "fastly" in str(headers).lower():
            tech["cdn"] = "Fastly"

        tech["hsts"] = (
            "Enabled"
            if "Strict-Transport-Security" in headers
            else "Disabled"
        )

        return tech

    except Exception as e:

        return {
            "error": str(e)
        }