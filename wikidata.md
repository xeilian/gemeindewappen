

https://query.wikidata.org/


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
