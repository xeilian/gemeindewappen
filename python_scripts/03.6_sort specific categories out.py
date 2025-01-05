import csv, re

def sort_specific_categories_out():
    with open('wikidata_output/gemeinden_deutschland.csv', mode='r', encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)
        temp_list = []

        for row in rows:
            ids = re.findall(r'Q\d+', row[1])
            if "Q2520755" in ids:
                # row[37] = "kreisstadt"
                temp_list.append(row)
                rows.remove(row)
        
        with open('wikidata_output/gemeinden_deutschland.csv', mode='w', encoding='utf-8', newline='') as file1:
            writer1 = csv.writer(file1)
            for i in rows:
                writer1.writerow(i)

        with open('wikidata_output/verwaltungsgemeinden_deutschland.csv', mode='a', encoding='utf-8', newline='') as file2:
            writer2 = csv.writer(file2)
            for i in temp_list:
                writer2.writerow(i)

if __name__ == "__main__":
    sort_specific_categories_out()

# verwaltungsgemeinden (Q15725618, Q41762994, Q1561418, Q14455864, Q447523, Q1500932, Q1317260, Q23006, Q2513995, Q478847, Q2513989, Q399445, Q2520755)
# siedlungen_ortsteile_deutschland (Q821435)
# gemeindefreies_gebiet (Q15974311)
