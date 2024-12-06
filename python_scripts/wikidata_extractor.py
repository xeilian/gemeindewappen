def wikidata_extractor(wikidata_id):
    from SPARQLWrapper import SPARQLWrapper, JSON
    sparql_query = f"""
    SELECT DISTINCT 
        ?instanceOfData ?adminUnitData ?areaData ?capital ?coordinates ?populationData 
        ?subdivision ?coatOfArms ?insignia ?gnd ?geonamesID ?openStreetMapRelationID 
        ?openStreetMapNodeID ?label_de ?label_en ?label_fr ?desc_de ?desc_en ?desc_fr 
        ?sitelink_de ?sitelink_en ?sitelink_fr
    WHERE {{
        # Labels in different languages
        OPTIONAL {{ wd:{wikidata_id} rdfs:label ?label_de. FILTER(LANG(?label_de) = "de") }}
        OPTIONAL {{ wd:{wikidata_id} rdfs:label ?label_en. FILTER(LANG(?label_en) = "en") }}
        OPTIONAL {{ wd:{wikidata_id} rdfs:label ?label_fr. FILTER(LANG(?label_fr) = "fr") }}

        # Descriptions in different languages
        OPTIONAL {{ wd:{wikidata_id} schema:description ?desc_de. FILTER(LANG(?desc_de) = "de") }}
        OPTIONAL {{ wd:{wikidata_id} schema:description ?desc_en. FILTER(LANG(?desc_en) = "en") }}
        OPTIONAL {{ wd:{wikidata_id} schema:description ?desc_fr. FILTER(LANG(?desc_fr) = "fr") }}

        # Sitelinks for German, English, and French Wikipedia
        OPTIONAL {{
            ?sitelink_de schema:about wd:{wikidata_id};
                        schema:isPartOf <https://de.wikipedia.org/>. 
        }}
        OPTIONAL {{
            ?sitelink_en schema:about wd:{wikidata_id};
                        schema:isPartOf <https://en.wikipedia.org/>. 
        }}
        OPTIONAL {{
            ?sitelink_fr schema:about wd:{wikidata_id};
                        schema:isPartOf <https://fr.wikipedia.org/>. 
        }}

        # Instance Of (P31)
        OPTIONAL {{
            wd:{wikidata_id} p:P31 ?instanceOfStatement.
            ?instanceOfStatement ps:P31 ?instanceOf.
            OPTIONAL {{ ?instanceOfStatement pq:P580 ?instanceOfStartDate. }}  # Start date
            OPTIONAL {{ ?instanceOfStatement pq:P582 ?instanceOfEndDate. }}    # End date
        }}
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

        # Admin Unit (P131)
        OPTIONAL {{
            wd:{wikidata_id} p:P131 ?adminUnitStatement.
            ?adminUnitStatement ps:P131 ?adminUnit.
            OPTIONAL {{ ?adminUnitStatement pq:P580 ?adminUnitStartDate. }}  # Start date
            OPTIONAL {{ ?adminUnitStatement pq:P582 ?adminUnitEndDate. }}    # End date
        }}
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

        # Area (P2046)
        OPTIONAL {{
            wd:{wikidata_id} p:P2046 ?areaStatement.
            ?areaStatement ps:P2046 ?area.
            OPTIONAL {{ ?areaStatement pq:P585 ?areaStartDate. }}  # Area date
        }}
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

        # Capital (P36)
        OPTIONAL {{ wd:{wikidata_id} wdt:P36 ?capital. }}

        # Coordinates (P625)
        OPTIONAL {{ wd:{wikidata_id} wdt:P625 ?coordinates. }}
        
        # Population (P1082) with Date (P585)
        OPTIONAL {{
            wd:{wikidata_id} p:P1082 ?populationStatement.
            ?populationStatement ps:P1082 ?population.
            OPTIONAL {{ ?populationStatement pq:P585 ?popDate. }}
        }}
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

        # Subdivisions (P150)
        OPTIONAL {{ wd:{wikidata_id} wdt:P150 ?subdivision. }}
        
        # Coat of Arms (P94)
        OPTIONAL {{ wd:{wikidata_id} wdt:P94 ?coatOfArms. }}
        
        # Insignia (P395)
        OPTIONAL {{ wd:{wikidata_id} wdt:P395 ?insignia. }}
        
        # GND ID (P227)
        OPTIONAL {{ wd:{wikidata_id} wdt:P227 ?gnd. }}
        
        # Geonames ID (P1566)
        OPTIONAL {{ wd:{wikidata_id} wdt:P1566 ?geonamesID. }}
        
        # OpenStreetMap Relation ID (P402)
        OPTIONAL {{ wd:{wikidata_id} wdt:P402 ?openStreetMapRelationID. }}
        
        # OpenStreetMap Node ID (P11693)
        OPTIONAL {{ wd:{wikidata_id} wdt:P11693 ?openStreetMapNodeID. }}
    }}
    ORDER BY ?instanceOfData ?adminUnitData ?areaData
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)

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
        "label_de": [],
        "label_en": [],
        "label_fr": [],
        "desc_de": [],
        "desc_en": [],
        "desc_fr": [],
        "sitelink_de": [],
        "sitelink_en": [],
        "sitelink_fr": [],
    }

    for entry in results['results']['bindings']:
        instance_of = entry.get('instanceOfData', {}).get('value', "NULL")
        admin_unit = entry.get('adminUnitData', {}).get('value', "NULL")
        coordinates = entry.get('coordinates', {}).get('value', "NULL")
        population = entry.get('populationData', {}).get('value', "NULL")
        area = entry.get('areaData', {}).get('value', "NULL")
        coat_of_arms = entry.get('coatOfArms', {}).get('value', "NULL")
        insignia = entry.get('insignia', {}).get('value', "NULL")
        gnd = entry.get('gnd', {}).get('value', "NULL")
        geonames_id = entry.get('geonamesID', {}).get('value', "NULL")
        openstreetmap_rel_id = entry.get('openStreetMapRelationID', {}).get('value', "NULL")
        openstreetmap_node_id = entry.get('openStreetMapNodeID', {}).get('value', "NULL")
        label_de = entry.get('label_de', {}).get('value', "NULL")
        label_en = entry.get('label_en', {}).get('value', "NULL")
        label_fr = entry.get('label_fr', {}).get('value', "NULL")
        desc_de = entry.get('desc_de', {}).get('value', "NULL")
        desc_en = entry.get('desc_en', {}).get('value', "NULL")
        desc_fr = entry.get('desc_fr', {}).get('value', "NULL")
        sitelink_de = entry.get('sitelink_de', {}).get('value', "NULL")
        sitelink_en = entry.get('sitelink_en', {}).get('value', "NULL")
        sitelink_fr = entry.get('sitelink_fr', {}).get('value', "NULL")

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
            "label_de": label_de,
            "label_en": label_en,
            "label_fr": label_fr,
            "desc_de": desc_de,
            "desc_en": desc_en,
            "desc_fr": desc_fr,
            "sitelink_de": sitelink_de,
            "sitelink_en": sitelink_en,
            "sitelink_fr": sitelink_fr,
        }

        for key, value in dict_temp.items():
            if value not in data[key]:
                data[key].append(value)

    return data