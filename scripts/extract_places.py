import os, requests


PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = [
"id","displayName","formattedAddress","internationalPhoneNumber","websiteUri"
]


def search_places(query, region_code="US"):
key = os.environ["GOOGLE_PLACES_API_KEY"]
r = requests.post(
PLACES_URL,
headers={"X-Goog-Api-Key": key, "X-Goog-FieldMask": ",".join(FIELDS)},
json={"textQuery": query, "regionCode": region_code}
)
r.raise_for_status()
return r.json().get("places", [])
