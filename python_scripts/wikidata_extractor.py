def wikidata_extractor(wikidata_id):
    from SPARQLWrapper import SPARQLWrapper, JSON
    '''
    This function extracts the values of a number of different categories from place data sets in wikidata.
    The input is the wikidata id from a larger administrative entity (like a region or Landkreis).
    The output is a large list of all records that are associated with one of the categories and are a smaller location entity within the definied larger entity.
    In an afterstep it sorts the data and returns it as a sorted dictionary.
    This function is a improved second version of the initial wikidata_extractor. 
    '''

    sparql_query = f"""
    SELECT DISTINCT ?id
        ?instanceOfData ?adminUnitData ?areaData ?capital ?coordinates ?populationData 
        ?subdivision ?flagInfo ?flagImage ?coatOfArmsInfo ?coatOfArmsImage ?mapImage ?insignia ?postalCode ?inception ?abolition ?partnerCities 
        ?gnd ?geonamesID ?openStreetMapRelationID ?openStreetMapNodeID ?label_de ?label_en ?label_fr 
        ?desc_de ?desc_en ?desc_fr ?sitelink_de ?sitelink_en ?sitelink_fr
    WHERE {{{{
      ?id wdt:P131 wd:{wikidata_id}.
        # Instance Of (P31)
        OPTIONAL {{
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

        # Admin Unit (P131)
        UNION {{
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

        # Coordinates (P625)
        UNION {{ ?id wdt:P625 ?coordinates. }}
        
        # Population (P1082) with Date (P585)
        UNION {{
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

        # Subdivisions (P150)
        UNION {{ ?id wdt:P150 ?subdivision. }}

        # Area (P2046)
        UNION {{
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

        # Capital (P36)
        UNION {{ ?id wdt:P36 ?capital. }}

        # Flag information (P163)
        UNION {{ ?id wdt:P163 ?flagInfo. }}

        # Flag image (P41)
        UNION {{ ?id wdt:P41 ?flagImage. }}
        
        # Coat of Arms Info (P14659)
        UNION {{ ?id wdt:P14659 ?coatOfArmsInfo. }}

        # Coat of Arms Image (P94)
        UNION {{ ?id wdt:P94 ?coatOfArmsImage. }}
        
        # Map Image (P242)
        UNION {{ ?id wdt:P242 ?mapImage. }}
        
        # Insignia (P395)
        UNION {{ ?id wdt:P395 ?insignia. }}

        # Postal Code (P281)
        UNION {{ ?id wdt:P281 ?postalCode. }}

        # Inception (P571)
        UNION {{ ?id wdt:P571 ?inception. }}

        # Abolition (P576)
        UNION {{ ?id wdt:P576 ?abolition. }}
        
        # Partner Cities (P190)
        UNION {{ ?id wdt:P190 ?partnerCities. }}

        # GND ID (P227)
        UNION {{ ?id wdt:P227 ?gnd. }}
        
        # Geonames ID (P1566)
        UNION {{ ?id wdt:P1566 ?geonamesID. }}
        
        # OpenStreetMap Relation ID (P402)
        UNION {{ ?id wdt:P402 ?openStreetMapRelationID. }}
        
        # OpenStreetMap Node ID (P11693)
        UNION {{ ?id wdt:P11693 ?openStreetMapNodeID. }}

        # Labels in different languages
        UNION {{ ?id rdfs:label ?label_de. FILTER(LANG(?label_de) = "de") }}
        UNION {{ ?id rdfs:label ?label_en. FILTER(LANG(?label_en) = "en") }}
        UNION {{ ?id rdfs:label ?label_fr. FILTER(LANG(?label_fr) = "fr") }}

        # Descriptions in different languages
        UNION {{ ?id schema:description ?desc_de. FILTER(LANG(?desc_de) = "de") }}
        UNION {{ ?id schema:description ?desc_en. FILTER(LANG(?desc_en) = "en") }}
        UNION {{ ?id schema:description ?desc_fr. FILTER(LANG(?desc_fr) = "fr") }}

        # Sitelinks for German, English, and French Wikipedia
        UNION {{
            ?sitelink_de schema:about ?id;
                        schema:isPartOf <https://de.wikipedia.org/>. 
        }}
        UNION {{
            ?sitelink_en schema:about ?id;
                        schema:isPartOf <https://en.wikipedia.org/>. 
        }}
        UNION {{
            ?sitelink_fr schema:about ?id;
                        schema:isPartOf <https://fr.wikipedia.org/>. 
        }}}}
    }}
    ORDER BY ?instanceOfData ?adminUnitData ?areaData
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()


    return print(sparql_query)
    

wikidata_extractor("Q8177")