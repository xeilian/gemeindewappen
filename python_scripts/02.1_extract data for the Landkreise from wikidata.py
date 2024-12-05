import csv
from wikidata_extractor import wikidata_extractor

with open('wikidata_output/dummy_data.csv', mode="r", encoding="utf-8", newline="") as inputfile:
    reader = csv.reader(inputfile)

    for i in reader:
        wikidata_id = i[2]
        data = wikidata_extractor(wikidata_id)
        categories = data.keys()
        with open("landkreise_deutschland_with_data.csv", mode="a", encoding="utf-8", newline="") as outputfile:
            writer = csv.DictWriter(outputfile, fieldnames=categories)
            writer.writeheader()
            writer.writerows(data)
