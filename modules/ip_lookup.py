import requests


def get_ip_info(ip):

    try:

        response = requests.get(
            f"http://ip-api.com/json/{ip}",
            timeout=10
        )

        data = response.json()

        return {

            "ip": ip,

            "country":
                data.get(
                    "country",
                    "Unknown"
                ),

            "region":
                data.get(
                    "regionName",
                    "Unknown"
                ),

            "city":
                data.get(
                    "city",
                    "Unknown"
                ),

            "isp":
                data.get(
                    "isp",
                    "Unknown"
                ),

            "asn":
                data.get(
                    "as",
                    "Unknown"
                ),

            "timezone":
                data.get(
                    "timezone",
                    "Unknown"
                )
        }

    except Exception as e:

        return {
            "error": str(e)
        }