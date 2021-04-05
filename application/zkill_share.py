import json
import requests
from urllib.parse import urlparse


ZKILL_DOMAIN = "zkillboard.com"
ESI_ZKILL_BASE_PATH = 'https://esi.evetech.net/latest/killmails/%s/%s/'
APPRAISAL_URL = "https://evepraisal.com/appraisal/structured.json"

# appraisal stuff
# curl -XPOST "n" --data '{"market_name": "jita", "items": [{"type_id": 20413, "quantity": 40}, {"type_id": 25599, "quantity": 116}]}'


"""
The path is like /kill/12345678/
"""


def get_kill_id_from_path(path):
    x = path.split("/")
    if x[1] != "kill":
        return None
    else:
        return x[2]


def get_kill_id_and_hash_from_url(url):
    o = urlparse(url)
    if o.netloc != ZKILL_DOMAIN:
        return None, None

    kill_id = get_kill_id_from_path(o.path)
    kill_details_url = build_zkill_api_url(kill_id)
    r = requests.get(kill_details_url)
    result = r.json()
    return kill_id, result[0]['zkb']['hash']


def get_dropped_items_with_volumes(kill_id, esi_hash):
    esi_api = build_esi_url(kill_id, esi_hash)
    r = requests.get(esi_api)
    result = r.json()
    items_dropped = []
    for items in result["victim"]["items"]:
        if "quantity_dropped" in items:
            items_dropped.append(
                {"type_id": items["item_type_id"], "quantity": items["quantity_dropped"]})
    # print(items_dropped)
    return items_dropped


def build_zkill_api_url(kill_id):
    url = "https://%s/api/killID/%d/" % (ZKILL_DOMAIN, int(kill_id))
    return url


def build_esi_url(kill_id, esi_hash):
    esi_url = ESI_ZKILL_BASE_PATH % (kill_id, esi_hash)
    # print(esi_url)
    return esi_url


def fetch_appraisal(items):

    payload = {"market_name": "jita", "items": items}
    r = requests.post(APPRAISAL_URL, data=json.dumps(payload))
    result = r.json()
    # print(result)
    return result


def get_buy_sell_from_appraisal(url):
    kill_id, kill_hash = get_kill_id_and_hash_from_url(url)
    items = get_dropped_items_with_volumes(kill_id, kill_hash)
    # print(items)
    if items:
        appraisal = fetch_appraisal(items)
        return appraisal["appraisal"]["totals"]["buy"], appraisal["appraisal"]["totals"]["sell"]

    else:
        return 0,0
