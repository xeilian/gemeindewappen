import csv, sqlite3, time
from SPARQLWrapper import SPARQLWrapper, JSON
#from wikidata_extractor import wikidata_extractor

def ortsteile_ids(landkreis_id):
    sparql_query = f"""
    SELECT DISTINCT ?item WHERE {{
    ?item p:P31 ?statement0.
    ?statement0 (ps:P31/(wdt:P279*)) wd:Q253019.
    ?item p:P131 ?statement1.
    ?statement1 (ps:P131/(wdt:P131)) wd:{landkreis_id}.
    }}
    """
    
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    ortsteile_list = [result['item']['value'].replace("http://www.wikidata.org/entity/", "") for result in results["results"]["bindings"]]
    return ortsteile_list



def fetch_landkreis_ids():
    database_path = "gemeindewappen.db"
    query = """
    SELECT wikidata_id, name, bundesland
    FROM landkreise
    WHERE type="landkreis"
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        landkreis_ids = {row[0]: [row[1], row[2]] for row in results}
    except sqlite3.Error as e:
        print("Fehler beim Zugriff auf die Datenbank:", e)
    finally:
        conn.close()
    return landkreis_ids


def ortsteile_ids_to_csv():
    landkreis_ids = fetch_landkreis_ids()
    output_file = 'wikidata_output/gemeinden_siedlungen_deutschland_raw.csv'
    failed_ids = []
    
    for counter, i in enumerate(landkreis_ids.keys(), start=1):
        print(f"Fetching data from Landkreis {counter}/294, {landkreis_ids[i][0]} ({i})...")
        try:
            ortsteile_list = ortsteile_ids(i)
            for entry in ortsteile_list:
                with open(output_file, mode="a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow([entry, landkreis_ids[i][0], landkreis_ids[i][1]])
            print(f"Landkreis {counter}/294: {landkreis_ids[i][0]} ({i}) successfully processed!")
        except Exception as e:
            print(f"Error when accessing the data for {landkreis_ids[i][0]} ({i}): {e}")
            failed_ids.append(i)
            with open('wikidata_output/failed_ids.csv', 'a', newline='') as csvfile:
                writer_failed = csv.writer(csvfile)
                writer_failed.writerow([i])


if __name__ == "__main__":
    ortsteile_ids_to_csv()




