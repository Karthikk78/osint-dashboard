import shodan

API_KEY = "qrck6GjE8n7POfpFNEhd4iblPhLbU6W9"

def get_shodan_info(ip):

    try:

        api = shodan.Shodan(API_KEY)

        result = api.host(ip)

        return {
            "organization":
                result.get("org", "Unknown"),

            "country":
                result.get("country_name", "Unknown"),

            "os":
                result.get("os", "Unknown"),

            "ports":
                result.get("ports", []),

            "hostnames":
                result.get("hostnames", [])
        }

    except Exception as e:

        return {
            "error": str(e)
        }