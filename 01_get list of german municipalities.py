import csv, time, tqdm
import csv, time, tqdm
from SPARQLWrapper import SPARQLWrapper, JSON


wikidata_bundeslaender = {
    "Q985": "Baden-Württemberg",
    "Q980": "Bayern",
    "Q1209": "Bremen",
    "Q1055": "Hamburg",
    "Q64": "Berlin",
    "Q1196": "Mecklenburg-Vorpommern",
    "Q1202": "Sachsen",
    "Q1206": "Sachsen-Anhalt",
    "Q1205": "Thüringen",
    "Q1194": "Schleswig-Holstein",
    "Q1201": "Saarland",
    "Q1200": "Rheinland-Pfalz",
    "Q1208": "Brandenburg",
    "Q1198": "Nordrhein-Westfalen",
    "Q1199": "Hessen",
    "Q1197": "Niedersachsen",
}


def extract_alle_landkreise(bundesland_wikidata_id):
    sparql_query = f"""
    SELECT DISTINCT ?item ?itemLabel WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
        ?item p:P31 ?statement0.
        ?statement0 (ps:P31/(wdt:P279*)) wd:Q106658.
        ?item p:P131 ?statement1.
        ?statement1 (ps:P131/(wdt:P131*)) wd:{bundesland_wikidata_id}.
    }}
    LIMIT 100
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    
    print(f"[Landkreise] SPARQL-Query für {wikidata_bundeslaender[bundesland_wikidata_id]} gesendet!")

    try:
        results = sparql.query().convert()
        with open(f"gemeinden_deutschland\landkreise_deutschland.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Wikidata-Link", "Name"])
            
            landkreis_ids = []
            for result in results["results"]["bindings"]:
                item = result['item']['value']
                label = result['itemLabel']['value']
                writer.writerow([wikidata_bundeslaender[bundesland_wikidata_id], item, label])
                landkreis_ids.append(item)
        print(f"Die Landkreise für {wikidata_bundeslaender[bundesland_wikidata_id]} wurden verarbeitet!")
        return landkreis_ids
    except Exception as e:
        print(f"Fehler beim Abrufen oder Speichern von Landkreisdaten für {wikidata_bundeslaender[bundesland_wikidata_id]}: {e}")
        return None


def extract_alle_gemeinden(landkreis_wikidata_id, bundesland_wikidata_id):
    sparql_query = f"""
    SELECT DISTINCT ?item ?itemLabel WHERE {{
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
        ?item p:P31 ?statement0.
        ?statement0 (ps:P31/(wdt:P279*)) wd:Q262166.
        ?item p:P131 ?statement1.
        ?statement1 (ps:P131/(wdt:P131*)) wd:{landkreis_wikidata_id}.
    }}
    LIMIT 100
    """
    
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    print(f"[Gemeinden] SPARQL-Query für {wikidata_bundeslaender[bundesland_wikidata_id]} gesendet!")

    try:
        results = sparql.query().convert()
        with open(f"gemeinden_deutschland\{wikidata_bundeslaender[bundesland_wikidata_id].lower().replace(" ", "_").replace("ü","ue")}_gemeinden.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Wikidata-Link", "Name"])
            
            for result in results["results"]["bindings"]:
                item = result['item']['value']
                label = result['itemLabel']['value']
                writer.writerow([item, label])
        print(f"Die Gemeinden für {wikidata_bundeslaender[bundesland_wikidata_id]} wurde verarbeitet!")
    except Exception as e:
        print(f"Fehler beim Abrufen oder Speichern von Daten für {wikidata_bundeslaender[bundesland_wikidata_id]}: {e}")


if __name__ == "__main__":
    for i in wikidata_bundeslaender.keys():
        extract_alle_gemeinden(i)
        for i in tqdm.tqdm(range(50)):
            time.sleep(1)

if __name__ == "__main__":
    for i in wikidata_bundeslaender.keys():
        list_landkreise = extract_alle_landkreise(i)
        for j in list_landkreise:
            extract_alle_gemeinden(j, i)