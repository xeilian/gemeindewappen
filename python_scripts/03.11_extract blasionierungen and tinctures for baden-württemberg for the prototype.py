import csv, requests, sqlite3
from bs4 import BeautifulSoup

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

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

def upload_blasionierungen_leobwid_and_tinctures_into_sql():
    with open('../csv_files/coat_of_arms_blasionierungen_bw.csv', 'r', encoding='utf-8', newline='') as input:
        reader = csv.reader(input)
        conn = sqlite3.connect('../gemeindewappen.db')
        cursor = conn.cursor()
        errors = []
        not_errors = []
        
        # new columns        
        query1 = '''
        ALTER TABLE wappen
        ADD COLUMN blasionierung VARCHAR(255)
        '''
        cursor.execute(query1)

        columns = ['schwarz', 'gelb', 'weiß', 'grün', 'blau', 'rot']
        for i in columns:
            query2 = f'''
            ALTER TABLE wappen
            ADD COLUMN {i} VARCHAR(1);
            '''
            cursor.execute(query2)
        
        query3 = '''
            ALTER TABLE normdaten
            ADD COLUMN leobw_link VARCHAR(255);
        '''
        cursor.execute(query3)

        for i in reader:
            query4 = f"""
            SELECT wikidata_id
            FROM normdaten
            WHERE gnd == '{i[3]}';
            """
            cursor.execute(query4)
            try:
                wikidata_id = cursor.fetchall()[0][0]
                i.append(wikidata_id)
                not_errors.append(i)
            except:
                errors.append(i)
        for i in not_errors:
            query5 = f"""
            UPDATE wappen
            SET blasionierung == '{i[2]}'
            WHERE wikidata_id == '{i[4]}';
            """
            query6 = f"""
            UPDATE normdaten
            SET leobw_link == '{i[1]}'
            WHERE wikidata_id == '{i[4]}';
            """
            cursor.execute(query5).execute(query6)

            # tinctures
            tinctures = get_tinctures(i[2])
            print(tinctures)
            query7 = f"""
            UPDATE wappen
            SET schwarz = '{tinctures[0]}', gelb = '{tinctures[1]}', weiß = '{tinctures[2]}', grün = '{tinctures[3]}', blau = '{tinctures[4]}', rot = '{tinctures[5]}'
            WHERE wikidata_id = '{i[4]}';
            """
            cursor.execute(query7)

    
    for error in errors:
        with open('../csv_files/entities_missing_in_db.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(error)
    
    conn.commit()
    conn.close()


def get_tinctures(blasionierung):
    tinctures_in_blasionierung = ['schwarz', 'gelb', 'gold', 'weiß', 'weiss', 'grün', 'blau', 'silber', 'rot']
    tinctures_dict = {}

    for i in tinctures_in_blasionierung:
        tinctures_dict[i] = f'{i}' in blasionierung.lower()

    if tinctures_dict['gelb'] == True or tinctures_dict['gold'] == True:
        tinctures_dict['gelb'] = True

    if tinctures_dict['weiss'] == True or tinctures_dict['weiß'] == True or tinctures_dict['silber'] == True:
        tinctures_dict['weiß'] = True
    
    tinctures_result = []
    tinctures_var = ['schwarz', 'gelb', 'weiß', 'grün', 'blau', 'rot']

    for tincture in tinctures_var:
        if tinctures_dict[tincture] == True:
            tinctures_result.append("x")
        else:
            tinctures_result.append("")
    
    return tinctures_result




if __name__ == '__main__':
    #get_blasionierungen_from_leo()
    upload_blasionierungen_leobwid_and_tinctures_into_sql()