"""
Retrieve ESA HAPI data using authentication.
"""

import requests
import json


def get_esa_hapi_connection():
    """
    Create an ESA OAuth2 client-credentials connection header.

    Returns
    -------
    dict or None
        ``{"Authorization": "Bearer <token>"}`` when successful, else ``None``.
    """
    issuer = "https://sso.s2p.esa.int/realms/swe/.well-known/openid-configuration"
    scope = "openid swe_hapiserver"
    # The following values are temporary.
    # Users should obtain and use their own "client_id" and "client_secret" as described in the readme file.
    client_id = "ed039925634925f75da9075ff297fd0c"
    client_secret = "dpX1Gzy8sp7DNfIqQpxz8r6se7m2Ae8C"

    try:
        metadata_response = requests.get(issuer, timeout=30)
        metadata_response.raise_for_status()
        metadata = metadata_response.json()
        token_url = metadata["token_endpoint"]

        token_response = requests.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "scope": scope,
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30,
        )
        token_response.raise_for_status()
        token = token_response.json()["access_token"]

        return {"Authorization": f"Bearer {token}"}
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        print(f"Error creating ESA connection: {e}")
        return None


def get_esa_hapi_data(url):
    """
    Fetch ESA HAPI data from a fully qualified URL.

    Parameters
    ----------
    url : str
        Target ESA HAPI URL (for example ``/hapi/catalog`` or ``/hapi/data``).

    Returns
    -------
    str or None
        Response body as text when successful, else ``None``.
    """
    try:
        headers = get_esa_hapi_connection()
        if not headers:
            return None
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error getting data from {url}: {e}")
        return None


def check_esa_hapi_connection():
    """
    Check ESA HAPI connectivity using the capabilities endpoint.

    Returns
    -------
    bool
        ``True`` when ``/hapi/capabilities`` reports status ``OK`` (or code 1200),
        otherwise ``False``.
    """
    capabilities_url = "https://swe.ssa.esa.int/hapi/capabilities/"
    try:
        capabilities_text = get_esa_hapi_data(capabilities_url)
        if not capabilities_text:
            return False
        capabilities = json.loads(capabilities_text)
        status = capabilities.get("status", {})

        return status.get("message") == "OK" or status.get("code") == 1200
    except ValueError:
        return False


if __name__ == "__main__":
    # Check connection to ESA server
    res = check_esa_hapi_connection()
    print(res)
