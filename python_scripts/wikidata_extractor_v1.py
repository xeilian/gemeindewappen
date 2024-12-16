def wikidata_extractor(wikidata_id):
    from SPARQLWrapper import SPARQLWrapper, JSON
    sparql_query = f"""
    SELECT DISTINCT 
        ?instanceOfData ?adminUnitData ?areaData ?capital ?coordinates ?populationData 
        ?subdivision ?flagInfo ?flagImage ?coatOfArmsInfo ?coatOfArmsImage ?mapImage ?insignia ?postalCode ?inception ?abolition ?partnerCities 
        ?gnd ?geonamesID ?openStreetMapRelationID ?openStreetMapNodeID ?label_de ?label_en ?label_fr 
        ?desc_de ?desc_en ?desc_fr ?sitelink_de ?sitelink_en ?sitelink_fr
    WHERE {{
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

        # Flag information (P163)
        OPTIONAL {{ wd:{wikidata_id} wdt:P163 ?flagInfo. }}

        # Flag image (P41)
        OPTIONAL {{ wd:{wikidata_id} wdt:P41 ?flagImage. }}
        
        # Coat of Arms Info (P14659)
        OPTIONAL {{ wd:{wikidata_id} wdt:P14659 ?coatOfArmsInfo. }}

        # Coat of Arms Image (P94)
        OPTIONAL {{ wd:{wikidata_id} wdt:P94 ?coatOfArmsImage. }}
        
        # Map Image (P242)
        OPTIONAL {{ wd:{wikidata_id} wdt:P242 ?mapImage. }}
        
        # Insignia (P395)
        OPTIONAL {{ wd:{wikidata_id} wdt:P395 ?insignia. }}

        # Postal Code (P281)
        OPTIONAL {{ wd:{wikidata_id} wdt:P281 ?postalCode. }}

        # Inception (P571)
        OPTIONAL {{ wd:{wikidata_id} wdt:P571 ?inception. }}

        # Abolition (P576)
        OPTIONAL {{ wd:{wikidata_id} wdt:P576 ?abolition. }}
        
        # Partner Cities (P190)
        OPTIONAL {{ wd:{wikidata_id} wdt:P190 ?partnerCities. }}

        # GND ID (P227)
        OPTIONAL {{ wd:{wikidata_id} wdt:P227 ?gnd. }}
        
        # Geonames ID (P1566)
        OPTIONAL {{ wd:{wikidata_id} wdt:P1566 ?geonamesID. }}
        
        # OpenStreetMap Relation ID (P402)
        OPTIONAL {{ wd:{wikidata_id} wdt:P402 ?openStreetMapRelationID. }}
        
        # OpenStreetMap Node ID (P11693)
        OPTIONAL {{ wd:{wikidata_id} wdt:P11693 ?openStreetMapNodeID. }}

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
    }}
    ORDER BY ?instanceOfData ?adminUnitData ?areaData
    """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = {
        "wikidata_id": [],
        "instance_of": [],
        "admin_unit": [],
        "coordinates": [],
        "population": [],
        "subdivisions": [],
        "area": [],
        "capital": [],
        "flag_info": [],
        "flag_image": [],
        "coat_of_arms_info": [],
        "coat_of_arms_image": [],
        "map_image": [],
        "insignia": [],
        "postal_code": [],
        "inception": [],
        "abolition": [],
        "partner_cities": [],
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
        "sitelink_fr": []
    }

    for entry in results['results']['bindings']:
        instance_of = entry['instanceOfData']['value'] if 'instanceOfData' in entry else "NULL"
        admin_unit = entry['adminUnitData']['value'] if 'adminUnitData' in entry else "NULL"
        coordinates = entry['coordinates']['value'] if 'coordinates' in entry else "NULL"
        population = entry['populationData']['value'] if 'populationData' in entry else "NULL"
        subdivisions = entry['subdivision']['value'] if 'subdivision' in entry else "NULL"
        area = entry['areaData']['value'] if 'areaData' in entry else "NULL"
        capital = entry['capital']['value'] if 'capital' in entry else "NULL"
        flag_info = entry['flagInfo']['value'] if 'flagInfo' in entry else "NULL"
        flag_image = entry['flagImage']['value'] if 'flagImage' in entry else "NULL"
        coat_of_arms_info = entry['coatOfArmsInfo']['value'] if 'coatOfArmsInfo' in entry else "NULL"
        coat_of_arms_image = entry['coatOfArmsImage']['value'] if 'coatOfArmsImage' in entry else "NULL"
        map_image = entry['mapImage']['value'] if 'mapImage' in entry else "NULL"
        insignia = entry['insignia']['value'] if 'insignia' in entry else "NULL"
        postal_code = entry['postalCode']['value'] if 'postalCode' in entry else "NULL"
        inception = entry['inception']['value'] if 'inception' in entry else "NULL"
        abolition = entry['abolition']['value'] if 'abolition' in entry else "NULL"
        partner_cities = entry['partnerCities']['value'] if 'partnerCities' in entry else "NULL"
        gnd = entry['gnd']['value'] if 'gnd' in entry else "NULL"
        geonames_id = entry['geonamesID']['value'] if 'geonamesID' in entry else "NULL"
        openstreetmap_rel_id = entry['openStreetMapRelationID']['value'] if 'openStreetMapRelationID' in entry else "NULL"
        openstreetmap_node_id = entry['openStreetMapNodeID']['value'] if 'openStreetMapNodeID' in entry else "NULL"
        label_de = entry['label_de']['value'] if 'label_de' in entry else "NULL"
        label_en = entry['label_en']['value'] if 'label_en' in entry else "NULL"
        label_fr = entry['label_fr']['value'] if 'label_fr' in entry else "NULL"
        desc_de = entry['desc_de']['value'] if 'desc_de' in entry else "NULL"
        desc_en = entry['desc_en']['value'] if 'desc_en' in entry else "NULL"
        desc_fr = entry['desc_fr']['value'] if 'desc_fr' in entry else "NULL"
        sitelink_de = entry['sitelink_de']['value'] if 'sitelink_de' in entry else "NULL"
        sitelink_en = entry['sitelink_en']['value'] if 'sitelink_en' in entry else "NULL"
        sitelink_fr = entry['sitelink_fr']['value'] if 'sitelink_fr' in entry else "NULL"

        dict_temp = {
            "wikidata_id": wikidata_id,
            "instance_of": instance_of,
            "admin_unit": admin_unit,
            "coordinates": coordinates,
            "population": population,
            "subdivisions": subdivisions,
            "area": area,
            "capital": capital,
            "flag_info": flag_info,
            "flag_image": flag_image,
            "coat_of_arms_info": coat_of_arms_info,
            "coat_of_arms_image": coat_of_arms_image,        
            "map_image": map_image,
            "insignia": insignia,
            "postal_code": postal_code,
            "inception": inception,
            "abolition": abolition,
            "partner_cities": partner_cities,
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