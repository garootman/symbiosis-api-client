import httpx

URL = "https://api.github.com/repos/symbiosis-finance/js-sdk/commits?path=src/crosschain/config/mainnet.ts&sha=main"
TARGET_COMMIT = "4a9a96064a8178f43e4b729f96763450041698e0"


def check_latest_commit(
    client: httpx.Client | None = None,
    url: str | None = None,
    commit: str | None = None,
) -> bool:
    """Checks that latest commit in mainnet.ts is the same as the one in the repo."""
    if url is None:
        url = URL
    if commit is None:
        commit = TARGET_COMMIT
    if client is None:
        client = httpx.Client()
    response = client.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Expected a list of commits")
    if not data:
        raise ValueError("No commits found")

    latest_sha = data[0]["sha"]
    return latest_sha == commit
