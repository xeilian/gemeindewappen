import csv, time, sqlite3, re, pandas as pd
from wikidata_extractor import wikidata_extractor


# 1. fetch the ids of all landkreise / gemeindefreie städte
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


def fetch_kreisfreie_städte_ids():
    database_path = "gemeindewappen.db"
    query = """
    SELECT wikidata_id, name, bundesland
    FROM kreisfreie_städte
    WHERE type="kreisfreie_stadt"
    """
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        kreisfreie_stadt_ids = {row[0]: [row[1], row[2]] for row in results}
    except sqlite3.Error as e:
        print("Fehler beim Zugriff auf die Datenbank:", e)
    finally:
        conn.close()
    return kreisfreie_stadt_ids


# 2. extract all the data from all the gemeinden, kreisstädte and other entities within the landkreis/kreisefreie stadt
def extract_gemeinde_data():
    #landkreis_ids = fetch_landkreis_ids()
    kreisfreie_stadt_ids = fetch_kreisfreie_städte_ids()
    output_file = 'wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv'
    failed_ids = []
    counter = 5

    for i in list(kreisfreie_stadt_ids.keys())[counter-1:]: #landkreis_ids.keys())[counter-1:]:  
        #temp_data = wikidata_extractor('l', i)
        temp_data = wikidata_extractor('g', "")
        fieldnames = ['wikidata_id', 'instance_of', 'admin_unit', 'area', 'capital', 'coordinates', 'population', 'subdivision',
                    'flag_info', 'flag_image', 'coat_of_arms_info', 'coat_of_arms_image', 'map_image', 'insignia',
                    'postal_code', 'first_written_record', 'inception', 'abolition', 'partner_cities', 'gnd', 'geonames_id',
                    'openstreetmap_rel_id', 'openstreetmap_node_id', 'district_key', 'regional_key',
                    'label_de', 'label_en', 'label_fr', 'desc_de', 'desc_en', 'desc_fr', 'sitelink_de',
                    'sitelink_en', 'sitelink_fr', 'bundesland', 'landkreis', 'type']
        try:
            with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
                writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
                outputfile.seek(0, 2) 
                if outputfile.tell() == 0:
                    writer.writeheader()
                row = {}
                for entry in temp_data:
                    entry['bundesland'] = kreisfreie_stadt_ids[i][1] #landkreis_ids[i][1]
                    entry['landkreis'] = kreisfreie_stadt_ids[i][0]  #landkreis_ids[i][0]
                    entry['type'] = None
                    for key, values in entry.items():
                        if isinstance(values, dict):
                            row[key] = str(values)
                        elif isinstance(values, list):
                            row[key] = f'{", ".join(map(str, values))}'
                        else:
                            row[key] = f'{str(values)}'
                    writer.writerow(row)
            #print(f"Landkreis {counter}/294: {landkreis_ids[i][0]} ({i}) successfully processed!")
            #print(f"Kreisfreie Stadt {counter}/106: {kreisfreie_stadt_ids[i][0]} ({i}) successfully processed!")
            counter += 1
            time.sleep(0)
        except Exception as e:
            print(f"Error when accessing the data for {kreisfreie_stadt_ids[i][0]} ({i}): {e}")
            failed_ids.append(i)
            with open('wikidata_output/failed_ids.csv', 'a', newline='') as csvfile:
                writer_failed = csv.writer(csvfile)
                writer_failed.writerow([i])










if __name__ == "__main__":
    extract_gemeinde_data()
    #upload_to_sql()
