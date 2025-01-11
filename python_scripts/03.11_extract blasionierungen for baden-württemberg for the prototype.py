import csv, requests
from bs4 import BeautifulSoup

def get_blasionierungen_from_leo():
    with open('../csv_files/archive/leo_bw_blasionierungen_bw.csv', 'r', encoding='utf-8', newline='') as input:
        reader = csv.reader(input)
        rows = [row for row in reader]
        rows_finished = []
        counter = 1

        for row in rows:
            page = requests.get(row[3])
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                gnd = soup.find('div', id='collapse-ids').table.tbody.tr.td.ul.li.a.text
            except:
                gnd = None
            try:
                blasionierung = soup.find('div', id='collapse-5').p.text
            except:
                blasionierung = None
            row_finished = [row[2], row[3], blasionierung, gnd]
            rows_finished.append(row_finished)
            with open('../csv_files/coat_of_arms_blasionierungen_bw.csv', 'a', encoding='utf-8', newline='') as output:
                writer = csv.writer(output)
                writer.writerow(row_finished)
            print(f"{counter}/{len(rows)}")
            counter += 1
        
    return rows_finished


if __name__ == '__main__':
    get_blasionierungen_from_leo()
