from pathlib import Path

import yaml


def prepare_wikidata_query(descriptor_type: str,
                           wikidata_uri: str) -> str:

    query = f'SELECT {get_select_by_descr_type(descriptor_type)} WHERE {{ ' \
            f'{get_where_by_descr_type(descriptor_type, wikidata_uri)} ' \
            f'SERVICE wikibase:label {{ bd:serviceParam wikibase:language "pl,en" }} }}'
    return query


def get_select_by_descr_type(descriptor_type: str) -> str:
    path_to_configuration = Path.cwd() / 'wikidata_queries' / 'queries_configuration' / 'descr_configuration.yaml'
    configuration = get_queries_configuration(str(path_to_configuration))
    configuration_by_type = configuration.get(descriptor_type)

    select_list = []
    for item in configuration_by_type:
        select_list.append(item['select'])
        if item['label']:
            select_list.append(f'{item["select"]}Label')
    select_str_to_return = ' '.join(sel for sel in select_list)
    return select_str_to_return


def get_where_by_descr_type(descriptor_type: str, wikidata_uri: str) -> str:
    path_to_configuration = Path.cwd() / 'wikidata_queries' / 'queries_configuration' / 'descr_configuration.yaml'
    configuration = get_queries_configuration(str(path_to_configuration))
    configuration_by_type = configuration.get(descriptor_type)

    where_list = []
    for item in configuration_by_type:
        where_list.append(f'OPTIONAL {{ <{wikidata_uri}> {item["property_id"]} {item["select"]}. }}')
    where_str_to_return = ' '.join(where for where in where_list)
    return where_str_to_return


def get_queries_configuration(path_to_config_files: str) -> dict:
    with open(path_to_config_files, 'r', encoding='utf-8') as fp:
        configuration = yaml.load(fp, Loader=yaml.FullLoader)
        return configuration
