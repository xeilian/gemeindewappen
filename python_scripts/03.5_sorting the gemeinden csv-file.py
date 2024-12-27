import csv, re, sqlite3
from SPARQLWrapper import SPARQLWrapper, JSON


def ortsteile_ids(landkreis_id):
    sparql_query = f"""
    SELECT DISTINCT ?item WHERE {{
    ?item p:P31 ?statement0.
    ?statement0 (ps:P31/(wdt:P279*)) wd:Q253019.
    ?item p:P131 ?statement1.
    ?statement1 (ps:P131/(wdt:P131)) wd:{landkreis_id}.
    }}
    """
    
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    
    results = sparql.query().convert()
    ortsteile_list = [result['item']['value'].replace("http://www.wikidata.org/entity/", "") for result in results["results"]["bindings"]]
    return ortsteile_list


def new_column():
    with open('file.csv', 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    new_column_index = 2
    new_column_name = "NeueSpalte"
    rows[0].insert(new_column_index, new_column_name)
    for row in rows[1:]:
        row.insert(new_column_index, "")
    with open('file.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def sort_into_the_new_csv_files():
    with open('wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv', encoding="utf-8", mode="r", newline="") as inputfile:
        input_reader = csv.reader(inputfile)
        for i in input_reader:
            ids = re.findall(r'Q\d+', i[1])
            coa_image = re.findall(r'http://commons.wikimedia.org/', i[11])

            if i[24] is not "":
                with open('wikidata_output/gemeinden_deutschland.csv', encoding="utf-8", mode="a", newline="") as gemeindefile:
                    gemeinde_writer = csv.writer(gemeindefile)
                    gemeinde_writer.writerow(i)
            elif (
                any(item in ids for item in ['Q116457956', 'Q42744322', 'Q253019', 'Q1138414', 'Q532', 'Q5084', 'Q486972', 'Q262166', 'Q123705', 'Q10354598']) 
                and i[24] == "") or "http://commons.wikimedia.org/" in coa_image:
                with open('wikidata_output/siedlungen_ortsteile_deutschland.csv', encoding="utf-8", mode="a", newline="") as ortsteilefile:
                    ortsteile_writer = csv.writer(ortsteilefile)
                    ortsteile_writer.writerow(i)
            else:
                with open('wikidata_output/rest_deutschland.csv', encoding="utf-8", mode="a", newline="") as ortsteilefile:
                    ortsteile_writer = csv.writer(ortsteilefile)
                    ortsteile_writer.writerow(i)
    
