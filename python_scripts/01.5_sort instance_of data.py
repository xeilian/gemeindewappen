import sqlite3
import re
import requests
from SPARQLWrapper import SPARQLWrapper, JSON


def extract_wikidata_ids(table):
    '''
    Extrahiert Wikidata-IDs aus der Tabelle und gibt eine Liste von IDs zurück.
    '''
    conn = sqlite3.connect('gemeindewappen.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT instance_of FROM {table}")
    rows = cursor.fetchall()
    wikidata_ids_set = set()
    for row in rows:
        if row[0]:
            ids = re.findall(r'Q\d+', row[0])
            wikidata_ids_set.update(ids)
    wikidata_ids_list = list(wikidata_ids_set)
    conn.close()

    return wikidata_ids_list

def fetch_wikidata_name():
    '''
    Ruft den Namen der Wikidata-ID über die Wikidata API ab.
    '''

    wikidata_ids = extract_wikidata_ids("landkreise")
    types = []

    print(wikidata_ids)

    for wikidata_id in wikidata_ids:
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

        types.append([wikidata_id, name])
    
    print(types)
    return types

def upload_into_sql():
    data = fetch_wikidata_name()
    conn = sqlite3.connect('gemeindewappen.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wikidata_id TEXT,
        name TEXT)
    ''')

    for i in data:
        print([i[0], i[1]])
        cur.execute("INSERT INTO types (wikidata_id, name) VALUES (?, ?)",
                    (i[0], i[1]))
        
        
upload_into_sql()

                


