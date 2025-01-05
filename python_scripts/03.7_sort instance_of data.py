import csv, re
from collections import defaultdict

def extract_instance_of_ids():
    '''
    Zählt, wie häufig jede Wikidata-ID in der Tabelle vorkommt.
    Gibt ein Dictionary mit den IDs und ihren jeweiligen Häufigkeiten zurück.
    '''
    wikidata_ids_count = defaultdict(int)
    
    with open("wikidata_output/gemeinden_deutschland.csv", mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1]:
                ids = re.findall(r'Q\d+', row[1])
                for id in ids:
                    wikidata_ids_count[id] += 1
    
    return dict(wikidata_ids_count)

def write_to_csv_with_names(id_counts, categories_file, output_file):
    '''
    Schreibt die IDs, Namen und Häufigkeiten in eine neue CSV-Datei.
    '''
    id_name_mapping = {}
    with open(categories_file, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            id_name_mapping[row[0]] = row[1]
    
    with open(output_file, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Häufigkeit"])
        for id_, count in id_counts.items():
            name = id_name_mapping.get(id_, "Unbekannt")
            writer.writerow([id_, name, count])

if __name__ == "__main__":
    id_counts = extract_instance_of_ids()
    write_to_csv_with_names(
        id_counts,
        "wikidata_output/instance_of_categories_gesamt.csv",
        "wikidata_output/instance_of_categories_gemeinden.csv"
    )
