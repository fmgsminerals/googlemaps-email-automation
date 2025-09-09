import gspread, pandas as pd
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def open_sheet(spreadsheet_id):
creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
if creds_json:
import json, io
creds_dict = json.loads(creds_json)
creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
gc = gspread.authorize(creds)
return gc.open_by_key(spreadsheet_id)


import os


def upsert_tab(spreadsheet_id, tab_name, rows):
sh = open_sheet(spreadsheet_id)
try:
ws = sh.worksheet(tab_name)
except gspread.WorksheetNotFound:
ws = sh.add_worksheet(title=tab_name, rows="100", cols="10")
ws.append_row(["Name","Address","Phone","Website","Email","WhatsApp","Status","Notes"])
df_old = pd.DataFrame(ws.get_all_records())
df_new = pd.DataFrame(rows)
if df_old.empty:
df = df_new
else:
df = pd.concat([df_old, df_new], ignore_index=True)
if "Email" in df.columns and "Website" in df.columns:
df = df.drop_duplicates(subset=["Email","Website"], keep="first")
ws.clear()
ws.append_row(df.columns.tolist())
for r in df.itertuples(index=False):
ws.append_row(list(r))
