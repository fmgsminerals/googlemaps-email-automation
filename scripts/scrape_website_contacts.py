import re, requests
from bs4 import BeautifulSoup


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
WHATSAPP_RE = re.compile(r"(?:\+?\d[\d\s\-()]{7,}\d).*(?:whats ?app|wa\.me|api\.whatsapp)", re.I)


HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; FolkmarketBot/1.0)"}


def fetch(url, timeout=15):
try:
return requests.get(url, timeout=timeout, headers=HEADERS).text
except Exception:
return ""


def find_contact_page(home_html, base_url):
soup = BeautifulSoup(home_html, "html.parser")
for a in soup.select("a[href]"):
text = (a.get_text() or "").lower()
href = a["href"]
if any(k in text for k in ["contact","support","about"]) or "contact" in href.lower():
return href if href.startswith("http") else base_url.rstrip("/") + "/" + href.lstrip("/")
return None


def parse_contacts(html):
emails = set(EMAIL_RE.findall(html))
whatsapp_hits, phones = set(), set()
for m in WHATSAPP_RE.finditer(html):
whatsapp_hits.add(m.group(0))
phones = set(re.findall(r"(?:\+?\d[\d\s\-()]{7,}\d)", html))
return list(emails), list(phones), list(whatsapp_hits)
