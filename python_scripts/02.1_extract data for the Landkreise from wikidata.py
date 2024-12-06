import csv
from wikidata_extractor import wikidata_extractor

with open('wikidata_output/dummy_data.csv', mode="r", encoding="utf-8", newline="") as inputfile:
    reader = csv.reader(inputfile)

    output_file = "landkreise_deutschland_with_data.csv"
    all_data = []

    for i, row in enumerate(reader):
        if len(row) < 3:
            print(f"Warnung: Ungültige Zeile {i + 1} übersprungen: {row}")
            continue
        
        wikidata_id = row[2]
        print(f"Verarbeite Wikidata-ID: {wikidata_id}")
        
        try:
            data = wikidata_extractor(wikidata_id)
            if data:
                data_rows = [
                    {key: data[key][j] if j < len(data[key]) else "NULL" for key in data}
                    for j in range(len(next(iter(data.values()))))
                ]
                all_data.extend(data_rows) 
            else:
                print(f"Keine Daten für Wikidata-ID: {wikidata_id}")
        except Exception as e:
            print(f"Fehler beim Abrufen der Daten für {wikidata_id}: {e}")

    if all_data:
        fieldnames = list(all_data[0].keys())
        with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_data)
        print(f"Ergebnisse in {output_file} gespeichert.")
    else:
        print("Keine Daten zum Schreiben.")
