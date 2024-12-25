import csv, re
from SPARQLWrapper import SPARQLWrapper, JSON


def extract_instance_of_ids():
    '''
    Extracts Wikidata-IDs from the table. The output is a list of IDs.
    '''
    wikidata_ids_set = set()
    with open("wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv", mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1]:
                ids = re.findall(r'Q\d+', row[1])
                wikidata_ids_set.update(ids)
    wikidata_ids_list = list(wikidata_ids_set)
    return wikidata_ids_list


def check_if_id_was_already_done():
    '''
    Queries the wikidata id via the wikidata API.
    '''
        
    wikidata_ids_list = extract_instance_of_ids()
    wikidata_ids_already_done = []
    wikidata_ids_to_do = []
    with open("wikidata_output/instance_of_categories.csv", mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for i in reader:
            wikidata_ids_already_done.append(i[0])
        for i in wikidata_ids_list:
            if i not in wikidata_ids_already_done:
                wikidata_ids_to_do.append(i)
            else:
                continue
    return wikidata_ids_to_do


def fetch_instance_of_name():
    wikidata_ids_to_do = check_if_id_was_already_done()
    for wikidata_id in wikidata_ids_to_do:
        sparql_query = f'''
        SELECT DISTINCT ?name
        WHERE {{
            OPTIONAL {{ wd:{wikidata_id} rdfs:label ?name. FILTER(LANG(?name) = "de") }}
        }}
        '''

        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        sparql.setQuery(sparql_query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for entry in results['results']['bindings']:
            name = entry['name']['value'] if 'name' in entry else "NULL"

        with open('wikidata_output/instance_of_categories.csv', mode="a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([wikidata_id, name])


if __name__ == "__main__":
    print(len(extract_instance_of_ids()))
    fetch_instance_of_name()