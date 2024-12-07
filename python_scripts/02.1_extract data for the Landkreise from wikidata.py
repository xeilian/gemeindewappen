import csv, time
from wikidata_extractor import wikidata_extractor

input_file = "wikidata_output/landkreise_deutschland_raw.csv"
output_file = "landkreise_deutschland_with_data.csv"

with open(input_file, mode="r", encoding="utf-8", newline="") as inputfile:
    reader = csv.reader(inputfile)
    for i, row in enumerate(reader):
        if len(row) < 3:
            print(f"Warnung: Ungültige Zeile {i + 1} übersprungen: {row}")
            continue
        wikidata_id = row[2]
        print(f"Verarbeite Wikidata-ID: {wikidata_id}")
        try:
            data = wikidata_extractor(wikidata_id)
            if data:
                with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
                    writer = csv.DictWriter(outputfile, fieldnames=data.keys())
                    outputfile.seek(0, 2) 
                    if outputfile.tell() == 0:
                        writer.writeheader()
                    row = {}
                    for key, values in data.items():
                        row[key] = f'{', '.join(values)}'
                    writer.writerow(row)
                    time.sleep(0)
                    print(f"Ergebnisse in {output_file} gespeichert.")
            else:
                print(f"Keine Daten für Wikidata-ID: {wikidata_id}")
        except Exception as e:
            print(f"Fehler beim Abrufen der Daten für {wikidata_id}: {e}")
