import time
import requests

BASE_URL = "https://api.kickbase.com/v4"

def get_json_with_token(url, token, max_retries=6):
    """Fetch JSON data from a given URL using token for authorization.
    Retries with a pause on rate limits (429) and temporary server errors."""

    headers = {"Authorization": f"Bearer {token}"}

    for attempt in range(max_retries):
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code in (429, 500, 502, 503, 504):
            retry_after = resp.headers.get("Retry-After")
            if retry_after and retry_after.isdigit():
                wait = int(retry_after)
            else:
                wait = min(2 ** attempt * 2, 60)
            time.sleep(wait)
            continue

        resp.raise_for_status()
        return resp.json()

    resp.raise_for_status()
    return resp.json()
