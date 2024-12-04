from SPARQLWrapper import SPARQLWrapper, JSON

sparql_query = """
SELECT DISTINCT ?instanceOf ?capital ?adminUnit ?coordinates ?population ?subdivision 
                ?area ?coatOfArms ?insignia ?gnd ?geonamesID ?openStreetMapID ?municode
                ?startDate ?endDate WHERE {
  
  # Instanz von (P31)
  OPTIONAL { wd:Q3232 wdt:P31 ?instanceOf. }
  
  # Hauptstadt (P36)
  OPTIONAL { wd:Q3232 wdt:P36 ?capital. }
  
  # Verwaltungseinheit (P131)
  OPTIONAL { wd:Q3232 wdt:P131 ?adminUnit. }
  
  # Koordinaten (P625)
  OPTIONAL { wd:Q3232 wdt:P625 ?coordinates. }
  
  # Bevölkerung (P1082) mit Datum (P585) für historische Populationen
  OPTIONAL {
    wd:Q3232 p:P1082 ?populationStatement.
    ?populationStatement ps:P1082 ?population.
    OPTIONAL { ?populationStatement pq:P585 ?startDate. }
    OPTIONAL { ?populationStatement pq:P582 ?endDate. }
  }
  
  # Untereinheiten (P150)
  OPTIONAL { wd:Q3232 wdt:P150 ?subdivision. }
  
  # Fläche (P2046)
  OPTIONAL { wd:Q3232 wdt:P2046 ?area. }
  
  # Wappen (P94)
  OPTIONAL { wd:Q3232 wdt:P94 ?coatOfArms. }
  
  # Insignien (P395)
  OPTIONAL { wd:Q3232 wdt:P395 ?insignia. }
  
  # GND (P227)
  OPTIONAL { wd:Q3232 wdt:P227 ?gnd. }
  
  # Geonames-ID (P1566)
  OPTIONAL { wd:Q3232 wdt:P1566 ?geonamesID. }
  
  # OpenStreetMap-ID (P402)
  OPTIONAL { wd:Q3232 wdt:P402 ?openStreetMapID. }
  
  # Muni-Code (P11693)
  OPTIONAL { wd:Q3232 wdt:P11693 ?municode. }
}
ORDER BY ?instanceOf ?startDate ?capital
"""

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)

results = sparql.query().convert()
print(results)

for entry in results['results']['bindings']:
    instance_of = entry['instanceOf']['value']
    admin_unit = entry['adminUnit']['value']
    coordinates = entry['coordinates']['value']
    population = entry['population']['value']
    area = entry['area']['value']
    coat_of_arms = entry['coatOfArms']['value']
    insignia = entry['insignia']['value']
    gnd = entry['gnd']['value']
    geonames_id = entry['geonamesID']['value']
    openstreetmap_id = entry['openStreetMapID']['value']
    municode = entry['municode']['value']
    start_date = entry['startDate']['value']

    print(f"Instance Of: {instance_of}")
    print(f"Admin Unit: {admin_unit}")
    print(f"Coordinates: {coordinates}")
    print(f"Population: {population}")
    print(f"Area: {area}")
    print(f"Coat of Arms: {coat_of_arms}")
    print(f"Insignia: {insignia}")
    print(f"GND: {gnd}")
    print(f"Geonames ID: {geonames_id}")
    print(f"OpenStreetMap ID: {openstreetmap_id}")
    print(f"Municode: {municode}")
    print(f"Start Date: {start_date}")
    print('-' * 50)  # Trennlinie für Klarheit    