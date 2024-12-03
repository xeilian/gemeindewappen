import sqlite3, csv

database = sqlite3.connect("gemeindewappen.db")
cursor = database.cursor()


# creating the table landkreise
create_table = """
CREATE TABLE landkreise (
    bundesland VARCHAR(100),
    wikidata_id VARCHAR(100) PRIMARY KEY,
    wikidata_link VARCHAR(100),
    name VARCHAR(100)
);
"""
cursor.execute(create_table)

# insert the data from the csv file
with open("wikidata_output/landkreise_deutschland.csv", newline="", encoding="utf-8") as file:
    csv_reader = csv.reader(file)
    for i in csv_reader:
        bundesland = i[0]
        wikidata_link = i[1]
        wikidata_id = i[2]
        cursor.execute("""
        INSERT OR IGNORE INTO landkreise (bundesland, wikidata_link, wikidata_id)
        VALUES(?, ?, ?);
        """, (bundesland, wikidata_link, wikidata_id))

database.commit()
database.close()
