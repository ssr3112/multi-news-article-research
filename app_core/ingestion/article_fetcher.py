

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url


def create_session():
    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    })

    return session


def extract_with_bs4(html: str):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled Article"
    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
    article_text = " ".join(paragraphs).strip()

    if len(article_text) < 100:
        return None

    return {
        "title": title,
        "text": article_text
    }


def extract_with_newspaper(url: str, html: str = None):
    try:
        from newspaper import Article

        article = Article(url)

        if html:
            article.download(input_html=html)
        else:
            article.download()

        article.parse()

        text = article.text.strip() if article.text else ""
        title = article.title.strip() if article.title else "Untitled Article"

        if len(text) < 100:
            return None

        return {
            "title": title,
            "text": text
        }

    except Exception as e:
        print(f"Newspaper3k extraction failed: {e}")
        return None


def extract_with_trafilatura(html: str, url: str):
    try:
        import trafilatura

        text = trafilatura.extract(html, url=url)

        if not text or len(text.strip()) < 100:
            return None

        return {
            "title": "Untitled Article",
            "text": text.strip()
        }

    except Exception as e:
        print(f"Trafilatura extraction failed: {e}")
        return None


def fetch_article_text(url):
    url = normalize_url(url)
    session = create_session()

    html = None

    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()
        html = response.text

        result = extract_with_bs4(html)
        if result:
            return {
                "title": result["title"],
                "url": url,
                "text": result["text"]
            }

        result = extract_with_newspaper(url, html)
        if result:
            return {
                "title": result["title"],
                "url": url,
                "text": result["text"]
            }

        result = extract_with_trafilatura(html, url)
        if result:
            return {
                "title": result["title"],
                "url": url,
                "text": result["text"]
            }

    except Exception as e:
        print(f"Requests fetch failed: {e}")

    try:
        result = extract_with_newspaper(url)
        if result:
            return {
                "title": result["title"],
                "url": url,
                "text": result["text"]
            }
    except Exception as e:
        print(f"Final fallback failed: {e}")

    print("Could not extract article text.")
    return None