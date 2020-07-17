from SPARQLWrapper import SPARQLWrapper, JSON

from wikidata_queries.wikidata_query_creator import prepare_wikidata_query

import pprint


async def query_wikidata(descriptor_type: str,
                         wikidata_uri: str) -> dict:

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql",
                           agent='omnis_wikidata_service 0.1 via sparqlwrapper 1.8.4')

    query = get_query_by_descriptor_type(descriptor_type, wikidata_uri)

    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)
    results = results['results']['bindings']
    # todo should join results in one dict if more than one instanceOf (result)
    return results[0]


def get_query_by_descriptor_type(descriptor_type: str,
                                 wikidata_uri: str) -> str:

    return prepare_wikidata_query(descriptor_type, wikidata_uri)
