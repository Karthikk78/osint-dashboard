import ssl
import socket
from datetime import datetime

def get_ssl_info(domain):

    try:

        context = ssl.create_default_context()

        with socket.create_connection((domain, 443)) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=domain
            ) as ssock:

                cert = ssock.getpeercert()

        issuer = dict(
            x[0]
            for x in cert["issuer"]
        )

        subject = dict(
            x[0]
            for x in cert["subject"]
        )

        valid_from = cert["notBefore"]
        valid_until = cert["notAfter"]

        expiry_date = datetime.strptime(
            valid_until,
            "%b %d %H:%M:%S %Y %Z"
        )

        days_remaining = (
            expiry_date - datetime.now()
        ).days

        return {

            "issuer":
                issuer.get(
                    "organizationName",
                    "Unknown"
                ),

            "subject":
                subject.get(
                    "commonName",
                    "Unknown"
                ),

            "valid_from":
                valid_from,

            "valid_until":
                valid_until,

            "days_remaining":
                days_remaining
        }

    except Exception as e:

        return {
            "error": str(e)
        }