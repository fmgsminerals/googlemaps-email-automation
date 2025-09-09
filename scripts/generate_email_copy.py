import os, json
from openai import OpenAI


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


SYSTEM = """
You are an email copywriter for a B2B gemstone wholesaler (Folkmarket Gems).
Write concise, helpful emails with a clear CTA and compliance footer.
Return JSON with fields: subject, preheader, html_body.
"""


def make_copy(segment_name, sample_products):
prompt = f"""
Segment: {segment_name}
Products: {json.dumps(sample_products[:3], ensure_ascii=False)}
Goals: introduce Folkmarket Gems, include 1-2 product images (as URLs), link to category,
short bullets, and 1 CTA button. Keep it 120-160 words.
"""
resp = client.chat.completions.create(
model="gpt-4o-mini",
messages=[{"role":"system","content":SYSTEM},{"role":"user","content":prompt}],
response_format={"type":"json_object"}
)
return json.loads(resp.choices[0].message.content)
