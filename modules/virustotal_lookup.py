import os
import requests

API_KEY = os.environ.get("VT_API_KEY")

def get_virustotal(domain):

    try:

        if not API_KEY:

            print(
                "VirusTotal API key not found"
            )

            return {}

        url = (
            f"https://www.virustotal.com/api/v3/"
            f"domains/{domain}"
        )

        headers = {

            "x-apikey": API_KEY

        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:

            print(
                "VT ERROR:",
                response.status_code
            )

            return {}

        data = response.json()

        stats = data[
            "data"
        ][
            "attributes"
        ][
            "last_analysis_stats"
        ]

        return {

            "malicious": stats.get(
                "malicious",
                0
            ),

            "suspicious": stats.get(
                "suspicious",
                0
            ),

            "harmless": stats.get(
                "harmless",
                0
            ),

            "undetected": stats.get(
                "undetected",
                0
            )

        }

    except Exception as e:

        print(
            "VT ERROR:",
            e
        )

        return {}