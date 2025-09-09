import os, pandas as pd, gspread
from google_sheets_io import open_sheet
from generate_email_copy import make_copy
from send_with_ses import send_email


SPREADSHEET_ID = os.environ["GOOGLE_SHEETS_SPREADSHEET_ID"]




def run_tab(tab_name, sample_products):
sh = open_sheet(SPREADSHEET_ID)
ws = sh.worksheet(tab_name)
df = pd.DataFrame(ws.get_all_records())
df = df[df["Email"].str.contains("@", na=False)]
copy = make_copy(tab_name, sample_products)
subj, html = copy["subject"], copy["html_body"]


statuses = []
for i, row in df.iterrows():
status = str(row.get("Status",""))
if status.lower() in ("sent","unsub","bounced","complaint"):
statuses.append(status)
continue
email = row["Email"].strip()
if not email:
statuses.append(status)
continue
try:
send_email(email, subj, html)
statuses.append("sent")
except Exception as e:
statuses.append(f"error:{str(e)[:40]}")


df["Status"] = statuses
ws.clear()
ws.append_row(df.columns.tolist())
for r in df.itertuples(index=False):
ws.append_row(list(r))


if __name__ == "__main__":
import sys
tab = sys.argv[1]
run_tab(tab_name=tab, sample_products=[
{"title":"Rough Emerald Parcels","img":"https://www.folkmarketgems.com/path/emerald.jpg","url":"https://www.folkmarketgems.com/collections/emeralds"},
{"title":"Loose Stones (Faceted)","img":"https://www.folkmarketgems.com/path/loose.jpg","url":"https://www.folkmarketgems.com/collections/loose-gemstones"}
])
