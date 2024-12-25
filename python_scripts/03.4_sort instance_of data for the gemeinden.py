import csv, re
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

def extract_instance_of_ids():
    '''
    Zählt, wie häufig jede Wikidata-ID in der Tabelle vorkommt.
    Gibt ein Dictionary mit den IDs und ihren jeweiligen Häufigkeiten zurück.
    '''
    wikidata_ids_count = defaultdict(int)
    
    with open("wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv", mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1]:
                ids = re.findall(r'Q\d+', row[1])
                for id in ids:
                    wikidata_ids_count[id] += 1

    return dict(wikidata_ids_count)


def check_if_id_was_already_done():
    '''
    Queries the wikidata id via the wikidata API.
    '''
        
    wikidata_ids_list = extract_instance_of_ids().keys()
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


def improve_instance_of_categories_csv():
    instance_of_ids_dict = extract_instance_of_ids()
    input_file = "wikidata_output/instance_of_categories.csv"
    updated_rows = []

    with open(input_file, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for i in reader:
            if i[1] == "NULL":
                sparql_query = f'''
                SELECT DISTINCT ?name
                WHERE {{
                    OPTIONAL {{ wd:{i[0]} rdfs:label ?name. FILTER(LANG(?name) = "en") }}
                }}
                '''
                sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
                sparql.setQuery(sparql_query)
                sparql.setReturnFormat(JSON)
                results = sparql.query().convert()
                english_name = "NULL"

                for entry in results['results']['bindings']:
                    if 'name' in entry:
                        english_name = entry['name']['value']
                        break
                i[1] = english_name
            i.append(instance_of_ids_dict[i[0]])
            updated_rows.append(i)
    updated_rows = sorted(updated_rows, key=lambda x: x[2], reverse=True)

    with open(input_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

if __name__ == "__main__":
    #extract_instance_of_ids()
    #check_if_id_was_already_done()
    #fetch_instance_of_name()
    improve_instance_of_categories_csv()