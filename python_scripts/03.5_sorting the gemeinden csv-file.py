import csv, re, sqlite3
from SPARQLWrapper import SPARQLWrapper, JSON


def fetch_landkreis_ids():
    database_path = "gemeindewappen.db"
    query = """
    SELECT wikidata_id, name, bundesland
    FROM landkreise
    WHERE type="landkreis"
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        landkreis_ids = {row[0]: [row[1], row[2]] for row in results}
    except sqlite3.Error as e:
        print("Fehler beim Zugriff auf die Datenbank:", e)
    finally:
        conn.close()
    return landkreis_ids


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


def fetch_municipality_keys():
    landkreis_ids = fetch_landkreis_ids()
    csv_file_path = 'wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv'

    for i in landkreis_ids.keys():
        pass

    sparql_query = f'''
    SELECT DISTINCT ?id ?municipalityKey  
    WHERE {{
      ?id wdt:P131 wd:{i}.
      {{ ?id wdt:P439 ?municipalityKey. }}
    }}
    '''

    # Ergebnisse iterieren
    for entry in results['results']['bindings']:
        id_value = entry['id']['value'].replace("http://www.wikidata.org/entity/", "")
        municipality_key = entry['municipalityKey']['value']

        # Temporäre Datei zum Überschreiben erstellen
        temp_file_path = 'wikidata_output/temp.csv'

        with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file, \
            open(temp_file_path, mode="w", newline="", encoding="utf-8") as temp_file:
            
            reader = csv.reader(file)
            writer = csv.writer(temp_file)
            
            # Datei zeilenweise lesen
            for row in reader:
                # Prüfen, ob die ID in der ersten Spalte übereinstimmt
                if row[0] == id_value:
                    # Sicherstellen, dass genügend Spalten vorhanden sind
                    if len(row) > 24:
                        row[24] = municipality_key
                    else:
                        # Fehlende Spalten auffüllen
                        row.extend([""] * (24 - len(row)))
                        row.append(municipality_key)
                # Zeile in die temporäre Datei schreiben
                writer.writerow(row)

        # Originaldatei durch die aktualisierte Datei ersetzen
        import os
        os.replace(temp_file_path, csv_file_path)

        print(f"ID {id_value} erfolgreich mit Wert bei Index 24 aktualisiert.")




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


if __name__ == "__main__":
    #fetch_landkreis_ids()
    #new_column()
    #fetch_municipality_keys()
    #sort_into_the_new_csv_files()
    pass