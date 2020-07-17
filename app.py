from fastapi import FastAPI

import uvicorn

from resolvers.wikidata_resolver import resolve_nlp_descriptor_id
from wikidata_client.wikidata_client import query_wikidata

app = FastAPI()


@app.get("/wikidata_items/{nlp_descriptor_id}")
async def get_item(nlp_descriptor_id: str):
    khw_data_response = await resolve_nlp_descriptor_id(nlp_descriptor_id)
    resolved_ids = khw_data_response.get(nlp_descriptor_id)
    wikidata_uri = resolved_ids.get('wikidata_uri')

    if wikidata_uri:
        wikidata_sparql_parsed_response = await query_wikidata('geographical_descriptor', wikidata_uri)
    else:
        wikidata_sparql_parsed_response = None
    return {'wikidata_resolved_id': wikidata_uri,
            'wikidata_properties': wikidata_sparql_parsed_response}

uvicorn.run(app, host='127.0.0.1', port=8000)
