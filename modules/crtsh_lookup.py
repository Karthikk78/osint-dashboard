import requests

def get_subdomains(domain):

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    print("Requesting:", url)

    response = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=60
    )

    print("Status Code:", response.status_code)

    data = response.json()

    print("Entries Found:", len(data))

    return data