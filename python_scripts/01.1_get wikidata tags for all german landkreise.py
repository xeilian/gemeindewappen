import csv
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Liste der Wikidata-IDs der Bundesländer
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

bundesland_wikidata_ids = wikidata_bundeslaender.keys()

def extract_alle_landkreise(bundesland_wikidata_id):
    sparql_query = f"""
    SELECT DISTINCT ?item ?itemLabel WHERE {{
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }}
    {{
        SELECT DISTINCT ?item WHERE {{
        ?item p:P31 ?statement0.
        ?statement0 (ps:P31/(wdt:P279*)) wd:Q106658.
        ?item p:P131 ?statement1.
        ?statement1 (ps:P131/(wdt:P131*)) wd:{bundesland_wikidata_id}.
        }}
        LIMIT 100
    }}
    }}
    """
    
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        with open(f"{bundesland_wikidata_id}_landkreise.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Label"])
            
            for result in results["results"]["bindings"]:
                item = result['item']['value']
                label = result['itemLabel']['value']
                writer.writerow([item, label])
    except:
        print(f"Error: {bundesland_wikidata_id} failed!")
