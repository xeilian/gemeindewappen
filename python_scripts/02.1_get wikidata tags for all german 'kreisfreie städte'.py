import csv
from SPARQLWrapper import SPARQLWrapper, JSON

def kreisfreie_städte_ids():
    sparql_query = """
    SELECT DISTINCT ?item ?itemLabel WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
    {
        SELECT DISTINCT ?item WHERE {
        ?item p:P31 ?statement0.
        ?statement0 (ps:P31/(wdt:P279*)) wd:Q22865. #Q2285: kreisfreie Stadt in Deutschland
        }
    }
    }
    """
    
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    try:
        results = sparql.query().convert()

        with open(f"wikidata_output/kreisfreie_städte_raw.csv", mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Label"])
            
            for result in results["results"]["bindings"]:
                item = result['item']['value']
                label = result['itemLabel']['value']
                writer.writerow([item, label])
    except:
        print("Error: failed extraction!")

kreisfreie_städte_ids()

# Disclaimer:
# The finished 'kreisfreie_städte_raw.csv' was matched with the wikipedia-article (https://de.wikipedia.org/wiki/Liste_der_kreisfreien_St%C3%A4dte_in_Deutschland).
# So only the 106 'kreisfreien Städte' are included in the csv file.
# The file has four columns: wikidata-link, wikidata-id, name, bundesland.