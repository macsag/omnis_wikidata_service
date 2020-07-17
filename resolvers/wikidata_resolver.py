import requests


async def resolve_nlp_descriptor_id(nlp_descriptor_id: str) -> dict:

    r = requests.get(f'http://khw.data.bn.org.pl/api/authorities/{nlp_descriptor_id}')
    return r.json()
