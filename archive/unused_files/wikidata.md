

https://query.wikidata.org/


# Test 1

```
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
    LIMIT 100000
  }
}
```

### Test 2

```
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
      UNION
      {
        ?item p:P31 ?statement3.
        ?statement3 (ps:P31/(wdt:P279*)) wd:Q5084.
      }
      UNION
      {
        ?item p:P31 ?statement4.
        ?statement4 (ps:P31/(wdt:P279*)) wd:Q532.
      }
      UNION
      {
        ?item p:P31 ?statement5.
        ?statement5 (ps:P31/(wdt:P279*)) wd:Q11183787.
      }
      UNION
      {
        ?item p:P31 ?statement6.
        ?statement6 (ps:P31/(wdt:P279*)) wd:Q1549591.
      }
      UNION
      {
        ?item p:P31 ?statement7.
        ?statement7 (ps:P31/(wdt:P279*)) wd:Q486972.
      }
      UNION
      {
        ?item p:P31 ?statement8.
        ?statement8 (ps:P31/(wdt:P279*)) wd:Q4632675.
      }
      UNION
      {
        ?item p:P31 ?statement9.
        ?statement9 (ps:P31/(wdt:P279*)) wd:Q262166.
      }
      UNION
      {
        ?item p:P31 ?statement10.
        ?statement10 (ps:P31/(wdt:P279*)) wd:Q15284.
      }
      UNION
      {
        ?item p:P31 ?statement11.
        ?statement11 (ps:P31/(wdt:P279*)) wd:Q19730508.
      }
      ?item p:P131 ?statement12.
      ?statement12 (ps:P131/(wdt:P131*)) wd:Q183.
    }
    LIMIT 1000000
  }
}
```
### Test 3

```
SELECT DISTINCT ?item ?itemLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P31 ?statement.
      ?statement (ps:P31/(wdt:P279*)) ?value.
      VALUES ?value { 
        wd:Q116457956 wd:Q42744322 wd:Q253019 wd:Q5084 wd:Q532 
        wd:Q11183787 wd:Q1549591 wd:Q486972 wd:Q4632675 wd:Q262166 
        wd:Q15284 wd:Q19730508
      }
      ?item p:P131 ?statement12.
      ?statement12 (ps:P131/(wdt:P131*)) wd:Q183.
    }
    LIMIT 1000000
  }
}
```

* Baden-Württemberg: Q985 (CHECK)
* Bayern: Q980 (NF)
* Bremen: Q24879
* Hamburg: Q1055
* Berlin: Q64


## Wichtige Kategorien
* P31 (evtl. gibt es mehere, gibt es start- und enddatum? wenn ja, bitte mitnehmen)
* P36
* P131 (evtl. gibt es da mehrere antworten)
* P625
* P1082 (alle historischen daten samt jahr)
* P150 (alle antworten bitte)
* P2046
* P94 (nur den Link zum Wappen)
* P395
* P227
* P1566
* P402
* P11693

```
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
```
