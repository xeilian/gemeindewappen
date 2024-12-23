import csv, time, sqlite3, re, pandas as pd
from wikidata_extractor import wikidata_extractor
from collections import defaultdict

input_file = ["wikidata_output/kreisfreie_städte_raw.csv", 1]   # [input_file, row number of wikidata_id]
output_file = "wikidata_output/kreisfreie_städte_with_data.csv"

# extract the data
def extract_kreisfreie_städte():
    with open(input_file[0], mode="r", encoding="utf-8", newline="") as inputfile:
        reader = csv.reader(inputfile)
        for i, row in enumerate(reader):
            if len(row) < 3:
                print(f"Warning: Invalid line {i + 1} skipped: {row}")
                continue
            wikidata_id = row[input_file[1]]
            failed_ids = []
            print(f"Processing Wikidata-ID: {wikidata_id}")
            try:
                data = wikidata_extractor('s', wikidata_id)
                data['bundesland'] = row[3]
                data['type'] = 'kreisfreie_stadt'
                fieldnames = ['wikidata_id', 'instance_of', 'admin_unit', 'area', 'capital', 'coordinates', 'population', 'subdivision',
                               'flag_info', 'flag_image', 'coat_of_arms_info', 'coat_of_arms_image', 'map_image', 'insignia',
                               'postal_code', 'first_written_record', 'inception', 'abolition', 'partner_cities', 'gnd', 'geonames_id',
                               'openstreetmap_rel_id', 'openstreetmap_node_id', 'district_key', 'regional_key',
                               'label_de', 'label_en', 'label_fr', 'desc_de', 'desc_en', 'desc_fr', 'sitelink_de',
                               'sitelink_en', 'sitelink_fr', 'bundesland', 'type']
                with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
                    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
                    outputfile.seek(0, 2) 
                    if outputfile.tell() == 0:
                        writer.writeheader()
                    row = {}
                    for key, values in data.items():
                        if isinstance(values, dict):
                            row[key] = str(values)
                        elif isinstance(values, list):
                            row[key] = f'{", ".join(map(str, values))}'
                        else:
                            row[key] = f'{str(values)}'
                    writer.writerow(row)
                print(f"The new csv file was successfully created: {output_file}")
            except Exception as e:
                print(f"Error when accessing the data for {wikidata_id}: {e}")
                failed_ids.append(wikidata_id)
                with open('wikidata_output/failed_ids.csv', 'a', newline='') as csvfile:
                    writer_failed = csv.writer(csvfile)
                    writer_failed.writerow([wikidata_id])
        time.sleep(1)
    print("Failed IDs: ", failed_ids)


def extract_year(date_str):
    if isinstance(date_str, str):
        match = re.match(r".*\((\d{4})-\d{2}-\d{2}.*", date_str)
        return match.group(1) if match else None
    return None


def upload_kreisfreie_städte_into_sql():
    conn = sqlite3.connect('gemeindewappen.db')
    cur = conn.cursor()
    csv_file = "wikidata_output/kreisfreie_städte_with_data.csv"
    df = pd.read_csv(csv_file)

    for column in df.columns:
        if df[column].dtype == 'object':
            df[column] = df[column].fillna('')


    # sql: create tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS kreisfreie_städte (
        wikidata_id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        instance_of TEXT,
        admin_unit TEXT,
        bundesland TEXT,
        coordinates TEXT,
        population_ids TEXT,
        area_ids TEXT,
        capital TEXT,
        flag_info TEXT,
        flag_image TEXT,
        map_image TEXT,
        insignia TEXT,
        postal_code TEXT,
        first_written_record TEXT,
        inception TEXT,
        abolition TEXT,
        partner_cities TEXT,
        normdaten_id INTEGER,
        FOREIGN KEY(normdaten_id) REFERENCES normdaten(id),
        FOREIGN KEY(type) REFERENCES types(name) MATCH SIMPLE
    );
    ''')

    # sql: insert the data
    wikidata_ids = []
    for index, row in df.iterrows():
        try:
            wikidata_id = row['wikidata_id']
            if wikidata_id in wikidata_ids:
                continue
            else:
                wikidata_ids.append(wikidata_id)
            instance_of = row['instance_of']
            admin_unit = row['admin_unit']
            coordinates = row['coordinates']
            population_data = row['population']
            area_data = row['area']
            coat_of_arms_info = row['coat_of_arms_info']
            coat_of_arms_image = row['coat_of_arms_image']
            label_de = row['label_de']
            bundesland = row['bundesland']
            entity_type = row['type']

            # populationsdaten
            population_ids = []
            if isinstance(population_data, str) and population_data:
                population_values = population_data.split(', ')
                for val in population_values:
                    year = extract_year(val)
                    try:
                        population_value = int(re.match(r"(\d+)", val).group(1))
                        cur.execute("INSERT INTO population (wikidata_id, year, population_value) VALUES (?, ?, ?)",
                                    (wikidata_id, year, population_value))
                        population_ids.append(cur.lastrowid)
                    except (ValueError, AttributeError):
                        print(f"Error in population data: {val}")

            # areadaten
            area_ids = []
            if area_data:
                if not isinstance(area_data, str):
                    area_data = str(area_data)
                area_values = area_data.split(', ')
                for val in area_values:
                    year = extract_year(val) 
                    if not year:
                        year = None
                    try:
                        area_value = float(re.match(r"(\d+(\.\d+)?)", val).group(1))
                    except (ValueError, AttributeError):
                        area_value = None

                    if area_value is not None:
                        cur.execute("INSERT INTO area (wikidata_id, year, area_value) VALUES (?, ?, ?)",
                                    (wikidata_id, year, area_value))
                        area_id = cur.lastrowid
                        area_ids.append(area_id)
            else:
                area_id = None


            # wappendaten
            if coat_of_arms_info or coat_of_arms_image:
                cur.execute("INSERT INTO wappen (wikidata_id, name, coat_of_arms_info, coat_of_arms_image) VALUES (?, ?, ?, ?)",
                            (wikidata_id, label_de, coat_of_arms_info, coat_of_arms_image))

            # normdaten
            cur.execute('''
            INSERT INTO normdaten (wikidata_id, name, gnd, geonames_id, openstreetmap_rel_id, openstreetmap_node_id, district_key, regional_key,
                                   label_de, label_en, label_fr, desc_de, desc_en, desc_fr, sitelink_de, sitelink_en, sitelink_fr)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (wikidata_id, label_de, row['gnd'], row['geonames_id'], row['openstreetmap_rel_id'], row['openstreetmap_node_id'], row['district_key'], row['regional_key'],
                  row['label_de'], row['label_en'], row['label_fr'], row['desc_de'], row['desc_en'], row['desc_fr'],
                  row['sitelink_de'], row['sitelink_en'], row['sitelink_fr']))
            normdaten_id = cur.lastrowid

            # kreisfreie_städte
            cur.execute('''
            INSERT INTO kreisfreie_städte (wikidata_id, name, type, instance_of, admin_unit, coordinates, population_ids, area_ids, capital,
                                    flag_info, flag_image, map_image, insignia, postal_code, first_written_record, inception, abolition, partner_cities,
                                    normdaten_id, bundesland)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (wikidata_id, label_de, entity_type, instance_of, admin_unit, coordinates, ','.join(map(str, population_ids)), ','.join(map(str, area_ids)),
                  row['capital'], row['flag_info'], row['flag_image'], row['map_image'], row['insignia'], row['postal_code'], row['first_written_record'], row['inception'],
                  row['abolition'], row['partner_cities'], normdaten_id, bundesland))
        except Exception as e:
            print(f"Error in line {index}: {e}")

    conn.commit()
    conn.close()

    print("The data was processed successfully and inserted into the database!")


if __name__ == "__main__":
    extract_kreisfreie_städte()
    upload_kreisfreie_städte_into_sql()
