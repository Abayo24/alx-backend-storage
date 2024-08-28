import requests
import redis

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL, caches it,
    and tracks the access count.
    """

    r.incr(f"count:{url}")

    cached_page = r.get(f"cache:{url}")

    if cached_page:
        return cached_page.decode('utf-8')

    response = requests.get(url)
    page_content = response.text

    r.setex(f"cache:{url}", 10, page_content)

    return page_content
