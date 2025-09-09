import os
from extract_places import search_places
from scrape_website_contacts import fetch, parse_contacts, find_contact_page
from google_sheets_io import upsert_tab


SPREADSHEET_ID = os.environ["GOOGLE_SHEETS_SPREADSHEET_ID"]




def ingest(search_term, tab_name):
places = search_places(search_term)
rows = []
for p in places:
name = p.get("displayName",{}).get("text","")
addr = p.get("formattedAddress","")
phone = p.get("internationalPhoneNumber","")
site = p.get("websiteUri","")
emails, phones, whatsapp = [], [], []
if site:
html = fetch(site)
emails, phones2, whatsapp = parse_contacts(html)
phones = list(set([phone] + phones2))
if not emails:
contact_url = find_contact_page(html, site)
if contact_url:
html2 = fetch(contact_url)
e2, p2, w2 = parse_contacts(html2)
emails = e2 or emails
phones = list(set(phones + p2))
whatsapp = w2 or whatsapp
if not emails:
emails = [""]
for em in emails:
rows.append({
"Name": name, "Address": addr, "Phone": "; ".join(phones),
"Website": site, "Email": em, "WhatsApp": "; ".join(whatsapp),
"Status":"new","Notes":""
})
upsert_tab(SPREADSHEET_ID, tab_name, rows)


if __name__ == "__main__":
import sys
term = sys.argv[1]
tab = sys.argv[2] if len(sys.argv)>2 else term
ingest(term, tab)
