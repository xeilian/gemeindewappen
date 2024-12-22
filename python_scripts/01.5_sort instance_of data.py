import sqlite3
import re
from SPARQLWrapper import SPARQLWrapper, JSON


def extract_wikidata_ids(table):
    '''
    Extracts Wikidata-IDs from the table. The output is a list of IDs.
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
    Queries the wikidata id via the wikidata API.
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
    #data = fetch_wikidata_name()
    data = [['Q106658', 'Landkreis'], ['Q5283531', 'Landkreis in Preußen'], ['Q56754679', 'Bezirksamt in Bayern'], ['Q61980413', 'Landkreis in Hessen'], ['Q85482556', 'Landkreis in Bayern'], ['Q20738945', 'Landkreis in Thüringen'], ['Q17302772', 'Landkreis in Sachsen-Anhalt'], ['Q61818979', 'Landkreis im Saarland'], ['Q106517174', 'Optionskommune'], ['Q61708063', 'Landkreis in Sachsen'], ['Q61793460', 'Landkreis in Brandenburg'], ['Q20738811', 'Kreis in Nordrhein-Westfalen'], ['Q837766', 'Gebietskörperschaft'], ['Q1780389', 'Kommunalverband besonderer Art'], ['Q15849374', 'Kreis der DDR'], ['Q85332736', 'Landkreis in Niedersachsen'], ['Q61856889', 'Kreis in Schleswig-Holstein'], ['Q85493040', 'Landkreis in Rheinland-Pfalz'], ['Q192611', 'Wahlkreis'], ['Q13221722', 'Verwaltungseinheit dritter Ebene']]
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
        cur.execute("INSERT INTO types (wikidata_id, name) VALUES (?, ?)", (i[0], i[1]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    upload_into_sql()
