import sqlite3, requests

def download_coat_of_arms_files():
    database_path = "gemeindewappen.db"
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = """
    SELECT wappen.coat_of_arms_image, entities.database_id
    FROM wappen, entities
    WHERE entities.wikidata_id == wappen.wikidata_id AND wappen.coat_of_arms_image != "" AND entities.type != 'ehem_landkreis'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    counter = 1

    for i in results:
        image = i[0]
        if len(image.split(", ")) > 1:
            split_file = image.split(", ")
            t = 1
            for file in split_file:
                r = requests.get(file, allow_redirects=True)
                with open(f'coat_of_arms_svg/{i[1]}.{file.split('.')[-1]}_{t}', 'wb') as file:
                    file.write(r.content)
                t = t + 1
        else:
            r = requests.get(i[0], allow_redirects=True)
            with open(f'coat_of_arms_svg/{i[1]}.{image.split('.')[-1]}', 'wb') as file:
                file.write(r.content)
        
        counter += 1
        if counter % 100 == 0:
            print(f"({round((counter/len(results)), 2)}%: {counter}/{len(results)}")


download_coat_of_arms_files()