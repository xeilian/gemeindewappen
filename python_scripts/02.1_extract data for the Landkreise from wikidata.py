from SPARQLWrapper import SPARQLWrapper, JSON

sparql_query = """
SELECT DISTINCT ?instanceOfData ?adminUnitData ?areaData ?capital ?coordinates ?populationData 
                ?subdivision ?coatOfArms ?insignia ?gnd ?geonamesID ?openStreetMapRelationID 
                ?openStreetMapNodeID WHERE {

    # Instanz von (P31)
    OPTIONAL {
      wd:Q3232 p:31 ?instanceOfStatement.
      ?instanceOfStatement ps:P31 ?instanceOf.
      OPTIONAL { ?instanceOfStatement pq:P585 ?instanceOfStartDate. }
    }
    BIND (
        IF(BOUND(?instanceOf),
           CONCAT(STR(?instanceOf),
                  IF(BOUND(?instanceOfStartDate),
                     CONCAT(" (", STR(?instanceOfStartDate),
                            IF(BOUND(?instanceOfStartDate) && BOUND(?instanceOfEndDate), " - ", ""),
                            IF(BOUND(?instanceOfEndDate), STR(?instanceOfEndDate), ""), ")"),
                     "")
                  ),
           ""
        ) AS ?instanceOfData
    )

    # Verwaltungseinheit (P131)
    OPTIONAL {
      wd:Q3232 p:131 ?adminUnitStatement.
      ?adminUnitStatement ps:P131 ?adminUnit.
      OPTIONAL { ?adminUnitStatement pq:P585 ?adminUnitStartDate. }
      OPTIONAL { ?adminUnitStatement pq:P582 ?adminUnitEndDate. }
    }
    BIND (
        IF(BOUND(?adminUnit),
           CONCAT(STR(?adminUnit),
                  IF(BOUND(?adminUnitStartDate),
                     CONCAT(" (", STR(?adminUnitStartDate),
                            IF(BOUND(?adminUnitStartDate) && BOUND(?adminUnitEndDate), " - ", ""),
                            IF(BOUND(?adminUnitEndDate), STR(?adminUnitEndDate), ""), ")"),
                     "")
                  ),
           ""
        ) AS ?adminUnitData
    )

    # Fläche (P2046)
    OPTIONAL {
      wd:Q3232 p:P2046 ?areaStatement.
      ?areaStatement ps:P1082 ?area.
      OPTIONAL { ?areaStatement pq:P585 ?areaStartDate. }
    }
    BIND (
        IF(BOUND(?area),
           CONCAT(STR(?area),
                  IF(BOUND(?areaStartDate),
                     CONCAT(" (", STR(?areaStartDate),
                            IF(BOUND(?areaStartDate) && BOUND(?areaEndDate), " - ", ""),
                            IF(BOUND(?areaEndDate), STR(?areaEndDate), ""), ")"),
                     "")
                  ),
           ""
        ) AS ?areaData
    )

    # Hauptstadt (P36)
    OPTIONAL { wd:Q3232 wdt:P36 ?capital. }

    # Koordinaten (P625)
    OPTIONAL { wd:Q3232 wdt:P625 ?coordinates. }
    
    # Bevölkerung (P1082) mit Datum (P585)
    OPTIONAL {
      wd:Q3232 p:P1082 ?populationStatement.
      ?populationStatement ps:P1082 ?population.
      OPTIONAL { ?populationStatement pq:P585 ?popDate. }
    }
    BIND (IF(BOUND(?population) && BOUND(?popDate), CONCAT(STR(?population), " (", STR(?popDate), ")"), STR(?population)) AS ?populationData)

    # Untereinheiten (P150)
    OPTIONAL { wd:Q3232 wdt:P150 ?subdivision. }
    
    # Wappen (P94)
    OPTIONAL { wd:Q3232 wdt:P94 ?coatOfArms. }
    
    # Insignien (P395)
    OPTIONAL { wd:Q3232 wdt:P395 ?insignia. }
    
    # GND (P227)
    OPTIONAL { wd:Q3232 wdt:P227 ?gnd. }
    
    # Geonames-ID (P1566)
    OPTIONAL { wd:Q3232 wdt:P1566 ?geonamesID. }
    
    # OpenStreetMap-Relation-ID (P402)
    OPTIONAL { wd:Q3232 wdt:P402 ?openStreetMapRelationID. }
    
    # OpenStreetMap-Node-ID (P11693)
    OPTIONAL { wd:Q3232 wdt:P11693 ?openStreetMapNodeID. }
}
ORDER BY ?instanceOfData ?adminUnitData ?areaData
"""

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

data = {
    "instance_of": [],
    "admin_unit": [],
    "coordinates": [],
    "population": [],
    "area": [],
    "coat_of_arms": [],
    "insignia": [],
    "gnd": [],
    "geonames_id": [],
    "openstreetmap_rel_id": [],
    "openstreetmap_node_id": [],
    "start_date": []
}

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
    openstreetmap_rel_id = entry['openStreetMapRelationID']['value']
    openstreetmap_node_id = entry['openStreetMapNodeID']['value']
    start_date = entry['startDate']['value']

    dict_temp = {
    "instance_of": instance_of,
    "admin_unit": admin_unit,
    "coordinates": coordinates,
    "population": population,
    "area": area,
    "coat_of_arms": coat_of_arms,
    "insignia": insignia,
    "gnd": gnd,
    "geonames_id": geonames_id,
    "openstreetmap_rel_id": openstreetmap_rel_id,
    "openstreetmap_node_id": openstreetmap_node_id,
    "start_date": start_date
    }

    for key, value in dict_temp.items():
      if value not in data[key]:
          data[key].append(value)

    print(data)
