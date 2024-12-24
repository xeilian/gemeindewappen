import csv, time, sqlite3, re, pandas as pd
from wikidata_extractor import wikidata_extractor

input_file = ["wikidata_output/gemeinden_siedlungen_deutschland_raw.csv",0] # [input_file, row number of wikidata_id]
output_file = "wikidata_output/gemeinden_siedlungen_deutschland_with_data.csv"
failed_ids = []

def extract_kreisfreie_städte():
    with open(input_file[0], mode="r", encoding="utf-8", newline="") as inputfile:
        reader = csv.reader(inputfile)
        for i, row in enumerate(reader):
            if len(row) < 3:
                print(f"Warning: Invalid line {i + 1} skipped: {row}")
                continue
            wikidata_id = row[input_file[1]]
            failed_ids = []
            #print(f"Processing Wikidata-ID: {wikidata_id}")
            try:
                data = wikidata_extractor('s', wikidata_id)
                data[0]['bundesland'] = row[2]
                data[0]['landkreis'] = row[1]
                data[0]['type'] = None
                fieldnames = ['wikidata_id', 'instance_of', 'admin_unit', 'area', 'capital', 'coordinates', 'population', 'subdivision',
                               'flag_info', 'flag_image', 'coat_of_arms_info', 'coat_of_arms_image', 'map_image', 'insignia',
                               'postal_code', 'first_written_record', 'inception', 'abolition', 'partner_cities', 'gnd', 'geonames_id',
                               'openstreetmap_rel_id', 'openstreetmap_node_id', 'district_key', 'regional_key',
                               'label_de', 'label_en', 'label_fr', 'desc_de', 'desc_en', 'desc_fr', 'sitelink_de',
                               'sitelink_en', 'sitelink_fr', 'bundesland', 'landkreis', 'type']
                with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
                    writer = csv.DictWriter(outputfile, fieldnames=fieldnames)
                    outputfile.seek(0, 2) 
                    if outputfile.tell() == 0:
                        writer.writeheader()
                    for i in data:
                        row = {}
                        for key, values in i.items():
                            if isinstance(values, dict):
                                row[key] = str(values)
                            elif isinstance(values, list):
                                row[key] = f'{", ".join(map(str, values))}'
                            else:
                                row[key] = f'{str(values)}'
                        writer.writerow(row)
            except Exception as e:
                print(f"Error when accessing the data for {wikidata_id}: {e}")
                failed_ids.append(wikidata_id)
                with open('wikidata_output/failed_ids.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    writer_failed = csv.writer(csvfile)
                    writer_failed.writerow([wikidata_id, row[1], row[2]])

extract_kreisfreie_städte()