import requests

def get_whois(domain):

    try:

        url = f"https://rdap.org/domain/{domain}"

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        data = response.json()

        result = {
            "domain": data.get("ldhName", "N/A"),
            "registrar": "N/A",
            "creation_date": "N/A",
            "expiration_date": "N/A"
        }

        if "entities" in data:

            for entity in data["entities"]:

                roles = entity.get("roles", [])

                if "registrar" in roles:

                    vcard = entity.get("vcardArray", [])

                    if len(vcard) > 1:

                        for item in vcard[1]:

                            if item[0] == "fn":

                                result["registrar"] = item[3]

        if "events" in data:

            for event in data["events"]:

                if event.get("eventAction") == "registration":

                    result["creation_date"] = event.get(
                        "eventDate",
                        "N/A"
                    )

                elif event.get("eventAction") == "expiration":

                    result["expiration_date"] = event.get(
                        "eventDate",
                        "N/A"
                    )

        return result

    except Exception as e:

        return {
            "error": str(e)
        }