import csv, re

def sort_specific_categories_out():
    with open('wikidata_output/gemeinden_deutschland.csv', mode='r', encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)
        verwaltungsgemeinden = []

        for row in rows:
            ids = re.findall(r'Q\d+', row[1])
            if "Q23006" in ids:
                verwaltungsgemeinden.append(row)
                rows.remove(row)
        
        with open('wikidata_output/gemeinden_deutschland.csv', mode='w', encoding='utf-8', newline='') as file1:
            writer1 = csv.writer(file1)
            for i in rows:
                writer1.writerow(i)

        with open('wikidata_output/verwaltungsgemeinden_deutschland.csv', mode='a', encoding='utf-8', newline='') as file2:
            writer2 = csv.writer(file2)
            for i in verwaltungsgemeinden:
                writer2.writerow(i)

if __name__ == "__main__":
    sort_specific_categories_out()

# 1. verwaltungsgemeinden (Q15725618, Q41762994, Q1561418, Q14455864, Q447523, Q1500932, Q1317260, Q23006)
