import sqlite3
import pandas as pd
import re

def extract_year(date_str):
    if isinstance(date_str, str):
        match = re.match(r".*\((\d{4})-\d{2}-\d{2}.*", date_str)
        return match.group(1) if match else None
    return None

csv_file = "wikidata_output/landkreise_deutschland_with_data.csv"
df = pd.read_csv(csv_file)

for column in df.columns:
    if df[column].dtype == 'object':
        df[column] = df[column].fillna('')

conn = sqlite3.connect('gemeindewappen.db')
cur = conn.cursor()


# sql: tabellen erstellen
cur.execute('''
CREATE TABLE IF NOT EXISTS population (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wikidata_id TEXT,
    year INTEGER,
    population_value INTEGER
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS area (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wikidata_id TEXT,
    year INTEGER,
    area_value REAL
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS wappen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wikidata_id TEXT,
    name TEXT,
    coat_of_arms_info TEXT,
    coat_of_arms_image TEXT
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS normdaten (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wikidata_id TEXT,
    name TEXT,
    gnd TEXT,
    geonames_id TEXT,
    openstreetmap_rel_id TEXT,
    openstreetmap_node_id TEXT,
    label_de TEXT,
    label_en TEXT,
    label_fr TEXT,
    desc_de TEXT,
    desc_en TEXT,
    desc_fr TEXT,
    sitelink_de TEXT,
    sitelink_en TEXT,
    sitelink_fr TEXT
);
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS landkreise (
    wikidata_id TEXT PRIMARY KEY,
    name TEXT,
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
    inception TEXT,
    abolition TEXT,
    partner_cities TEXT,
    normdaten_id INTEGER,
    FOREIGN KEY(normdaten_id) REFERENCES normdaten(id)
);
''')

# sql: daten einfügen
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
        INSERT INTO normdaten (wikidata_id, name, gnd, geonames_id, openstreetmap_rel_id, openstreetmap_node_id,
                               label_de, label_en, label_fr, desc_de, desc_en, desc_fr, sitelink_de, sitelink_en, sitelink_fr)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (wikidata_id, label_de, row['gnd'], row['geonames_id'], row['openstreetmap_rel_id'], row['openstreetmap_node_id'],
              row['label_de'], row['label_en'], row['label_fr'], row['desc_de'], row['desc_en'], row['desc_fr'],
              row['sitelink_de'], row['sitelink_en'], row['sitelink_fr']))
        normdaten_id = cur.lastrowid

        # landkreise
        cur.execute('''
        INSERT INTO landkreise (wikidata_id, name, instance_of, admin_unit, coordinates, population_ids, area_ids, capital,
                                flag_info, flag_image, map_image, insignia, postal_code, inception, abolition, partner_cities,
                                normdaten_id, bundesland)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (wikidata_id, label_de, instance_of, admin_unit, coordinates, ','.join(map(str, population_ids)), ','.join(map(str, area_ids)),
              row['capital'], row['flag_info'], row['flag_image'], row['map_image'], row['insignia'], row['postal_code'], row['inception'],
              row['abolition'], row['partner_cities'], normdaten_id, bundesland))
    except Exception as e:
        print(f"Error in line {index}: {e}")

conn.commit()
conn.close()

print("The data was processed successfully and inserted into the database!")
