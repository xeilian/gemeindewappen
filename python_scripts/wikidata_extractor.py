def wikidata_extractor(mode, wikidata_id):
    '''
    This function extracts the values of a number of different categories from place data sets in wikidata.

    The input is twofold:
        * First, it is important to specify the mode of extraction. There are three types of modes:
            - 's', extraction of the given entity itself: the output should contain extracted information of only the one admitted entity (wikidata_id).
            - 'l', extraction of all entities inside of given entity: the output should contain extracted information of all entities that lie inside of a larger administrative entity (like a region or Landkreis).
            - 'p', extraction of all entities that are of a given type: e.g. extract all data from entities that have the property 'urban municipalities'
        * Secondly, of course, the wikidata_id of the entity you'd like to extract, or in the case of mode 'p' the property.
    
    The output is a large list of all records that are associated with one of the categories and are a smaller location entity within the definied larger entity. 
    In an afterstep it sorts the data and returns it as a sorted dictionary.
    This function is a improved second version of the initial wikidata_extractor. 
    '''

    # imports
    from SPARQLWrapper import SPARQLWrapper, JSON
    from collections import defaultdict

    # check: Is the mode correctly stated (s or l?)?
    if mode == 's':
        mode_in_query = f"BIND(wd:{wikidata_id} AS ?id)"
    elif mode == 'l':
        mode_in_query = f"?id wdt:P131 wd:{wikidata_id}."
    elif mode == 'p':
        mode_in_query = f"?id wdt:P31 wd:{wikidata_id}."
    else:
        return print("Error: Wrong query. Mode input should either be 's' for self-extraction, 'l' for extraction of all entities inside of bigger entity or 'g' for extraction of all entities that have a given property.")

    sparql_query = f"""
    SELECT DISTINCT ?id
          ?instanceOfData ?adminUnitData ?areaData ?capital ?coordinates ?populationData 
          ?subdivision ?flagInfo ?flagImage ?coatOfArmsInfo ?coatOfArmsImage ?mapImage ?insignia ?postalCode ?inception ?abolition ?partnerCities 
          ?gnd ?geonamesID ?openStreetMapRelationID ?openStreetMapNodeID ?label_de ?label_en ?label_fr 
          ?desc_de ?desc_en ?desc_fr ?sitelink_de ?sitelink_en ?sitelink_fr
    WHERE {{
      {mode_in_query}
      {{
        ?id p:P31 ?instanceOfStatement.
        ?instanceOfStatement ps:P31 ?instanceOf.
        OPTIONAL {{ ?instanceOfStatement pq:P580 ?instanceOfStartDate. }}  # Start date
        OPTIONAL {{ ?instanceOfStatement pq:P582 ?instanceOfEndDate. }}    # End date
        BIND (
          IF(BOUND(?instanceOf),
            CONCAT(STR(?instanceOf),
                    IF(BOUND(?instanceOfStartDate),
                      CONCAT(" (", STR(?instanceOfStartDate),
                              IF(BOUND(?instanceOfEndDate), " - ", ""),
                              IF(BOUND(?instanceOfEndDate), STR(?instanceOfEndDate), ""), ")"),
                      "")
                  ),
            ""
            ) AS ?instanceOfData
        )
      }}
      UNION
      {{
        ?id p:P131 ?adminUnitStatement.
        ?adminUnitStatement ps:P131 ?adminUnit.
        OPTIONAL {{ ?adminUnitStatement pq:P580 ?adminUnitStartDate. }}  # Start date
        OPTIONAL {{ ?adminUnitStatement pq:P582 ?adminUnitEndDate. }}    # End date
        BIND (
          IF(BOUND(?adminUnit),
            CONCAT(STR(?adminUnit),
                    IF(BOUND(?adminUnitStartDate),
                      CONCAT(" (", STR(?adminUnitStartDate),
                              IF(BOUND(?adminUnitEndDate), " - ", ""),
                              IF(BOUND(?adminUnitEndDate), STR(?adminUnitEndDate), ""), ")"),
                      "")
                  ),
            ""
            ) AS ?adminUnitData
        )
      }}
      UNION
      {{ ?id wdt:P625 ?coordinates. }}
      UNION
      {{
        ?id p:P1082 ?populationStatement.
        ?populationStatement ps:P1082 ?population.
        OPTIONAL {{ ?populationStatement pq:P585 ?popDate. }}
        BIND (
          IF(BOUND(?population),
            CONCAT(STR(?population),
                    IF(BOUND(?popDate),
                      CONCAT(" (", STR(?popDate), ")"),
                      "")
                  ),
            ""
            ) AS ?populationData
        )
      }}
      UNION
      {{ ?id wdt:P150 ?subdivision. }}
      UNION
      {{
        ?id p:P2046 ?areaStatement.
        ?areaStatement ps:P2046 ?area.
        OPTIONAL {{ ?areaStatement pq:P585 ?areaStartDate. }}  # Area date
        BIND (
          IF(BOUND(?area),
            CONCAT(STR(?area),
                    IF(BOUND(?areaStartDate),
                      CONCAT(" (", STR(?areaStartDate), ")"),
                      "")
                  ),
            ""
            ) AS ?areaData
        )
      }}
      UNION
      {{ ?id wdt:P36 ?capital. }}
      UNION
      {{ ?id wdt:P163 ?flagInfo. }}
      UNION
      {{ ?id wdt:P41 ?flagImage. }}
      UNION
      {{ ?id wdt:P14659 ?coatOfArmsInfo. }}
      UNION
      {{ ?id wdt:P94 ?coatOfArmsImage. }}
      UNION
      {{ ?id wdt:P242 ?mapImage. }}
      UNION
      {{ ?id wdt:P395 ?insignia. }}
      UNION
      {{ ?id wdt:P281 ?postalCode. }}
      UNION
      {{ ?id wdt:P571 ?inception. }}
      UNION
      {{ ?id wdt:P576 ?abolition. }}
      UNION
      {{ ?id wdt:P190 ?partnerCities. }}
      UNION
      {{ ?id wdt:P227 ?gnd. }}
      UNION
      {{ ?id wdt:P1566 ?geonamesID. }}
      UNION
      {{ ?id wdt:P402 ?openStreetMapRelationID. }}
      UNION
      {{ ?id wdt:P11693 ?openStreetMapNodeID. }}
      UNION
      {{ ?id rdfs:label ?label_de. FILTER(LANG(?label_de) = "de") }}
      UNION
      {{ ?id rdfs:label ?label_en. FILTER(LANG(?label_en) = "en") }}
      UNION
      {{ ?id rdfs:label ?label_fr. FILTER(LANG(?label_fr) = "fr") }}
      UNION
      {{ ?id schema:description ?desc_de. FILTER(LANG(?desc_de) = "de") }}
      UNION
      {{ ?id schema:description ?desc_en. FILTER(LANG(?desc_en) = "en") }}
      UNION
      {{ ?id schema:description ?desc_fr. FILTER(LANG(?desc_fr) = "fr") }}
      UNION
      {{
        ?sitelink_de schema:about ?id;
                    schema:isPartOf <https://de.wikipedia.org/>. 
      }}
      UNION
      {{
        ?sitelink_en schema:about ?id;
                    schema:isPartOf <https://en.wikipedia.org/>. 
      }}
      UNION
      {{
        ?sitelink_fr schema:about ?id;
                    schema:isPartOf <https://fr.wikipedia.org/>. 
      }}
    }}
    ORDER BY ?instanceOfData ?adminUnitData ?areaData
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Caching the output?
    #output_file = "wikidata_extractor_temp_save.txt"
    #with open(output_file, "w", encoding="utf-8") as file:
    #    file.write(str(results))

    # Sorting the data and transforming it into a usuable dictionary
    categories = {'wikidataID': 'wikidata_id',
                  'instanceOfData': 'instance_of',
                  'adminUnitData': 'admin_unit',
                  'areaData': 'area',
                  'capital': 'capital',
                  'coordinates': 'coordinates',
                  'populationData': 'population',
                  'subdivision': 'subdivision',
                  'flagInfo': 'flag_info',
                  'flagImage': 'flag_image',
                  'coatOfArmsInfo': 'coat_of_arms_info',
                  'coatOfArmsImage': 'coat_of_arms_image',
                  'mapImage': 'map_image', 
                  'insignia': 'insignia',
                  'postalCode': 'postal_code',
                  'inception': 'inception',
                  'abolition': 'abolition',
                  'partnerCities': 'partner_cities',
                  'gnd': 'gnd',
                  'geonamesID': 'geonames_id',
                  'openStreetMapRelationID': 'openstreetmap_rel_id',
                  'openStreetMapNodeID': 'openstreetmap_node_id',
                  'label_de': 'label_de',
                  'label_en': 'label_en',
                  'label_fr': 'label_fr',
                  'desc_de': 'desc_de',
                  'desc_en': 'desc_en',
                  'desc_fr': 'desc_fr',
                  'sitelink_de': 'sitelink_de',
                  'sitelink_en': 'sitelink_en',
                  'sitelink_fr': 'sitelink_fr'
                  }

    sorted_data = defaultdict(lambda: {cat: [] for cat in categories.values()})

    for entry in results['results']['bindings']:
        id_value = entry['id']['value']
        for key, value in entry.items():
            if key != 'id' and key in categories:
                snake_case_key = categories[key]
                sorted_data[id_value][snake_case_key].append(value['value'].replace("http://www.wikidata.org/entity/", ""))

    for id_value, attributes in sorted_data.items():
        for key, values in attributes.items():
            if len(values) == 1:
                attributes[key] = values[0]
            elif len(values) == 0:
                attributes[key] = None
    sorted_data = dict(sorted_data[id_value])
    sorted_data['wikidata_id'] = id_value.replace("http://www.wikidata.org/entity/", "")
    return sorted_data

# for one-time inputs
# mode = input("Mode? ")
# wikidata_id = input("ID? ")
# print(wikidata_extractor(mode, wikidata_id))
