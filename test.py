from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_all_municipalities():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
        SELECT DISTINCT ?item ?itemLabel WHERE {
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
        {
            SELECT DISTINCT ?item WHERE {
            {
                ?item p:P31 ?statement0.
                ?statement0 (ps:P31/(wdt:P279*)) wd:Q116457956.
            }
            UNION
            {
                ?item p:P31 ?statement1.
                ?statement1 (ps:P31/(wdt:P279*)) wd:Q42744322.
            }
            UNION
            {
                ?item p:P31 ?statement2.
                ?statement2 (ps:P31/(wdt:P279*)) wd:Q253019.
            }
            }
            LIMIT 100
        }
        }
        """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    results_df = pd.json_normalize(results['results']['bindings'])
    selected_df = results_df[['itemLabel.value']] # 'item.value', 
    selected_df.to_csv("output.csv", index=False)


def extract_information():
    pass


if __name__ == "__main__":
    get_all_municipalities()
