import csv, time
from wikidata_extractor_v1 import wikidata_extractor

input_file = ["wikidata_output/dummy_data.csv", 2]#/landkreise_deutschland_raw.csv",2]   # [input_file, row number of wikidata_id]
output_file = "wikidata_output/landkreise_deutschland_with_data.csv"

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
            data = wikidata_extractor(wikidata_id)
            data['bundesland'] = row[0]
            if data:
                with open(output_file, mode="a", encoding="utf-8", newline="") as outputfile:
                    writer = csv.DictWriter(outputfile, fieldnames=data.keys())
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
                    time.sleep(0)
                    print(f"Results successfully saved in {output_file}.")
            else:
                print(f"No data for wikidata id: {wikidata_id}")
        except Exception as e:
            print(f"Error when accessing the data for {wikidata_id}: {e}")
            failed_ids.append(wikidata_id)
            with open('wikidata_output/failed_ids.csv', 'a', newline='') as csvfile:
                writer_failed = csv.writer(csvfile)
                writer_failed.writerow([wikidata_id])
    
print("Failed IDs: ", failed_ids)
