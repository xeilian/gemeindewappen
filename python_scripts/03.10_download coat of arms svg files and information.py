import sqlite3, requests, time, shutil

# def download_coat_of_arms_files():
#     database_path = "gemeindewappen.db"
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()
#     query = """
#     SELECT wappen.coat_of_arms_image, entities.database_id
#     FROM wappen, entities
#     WHERE entities.wikidata_id == wappen.wikidata_id AND wappen.coat_of_arms_image != "" AND entities.type != 'ehem_landkreis' AND entities.bundesland == 'Baden-Württemberg'
#     """
#     cursor.execute(query)
#     results = cursor.fetchall()
#     counter = 1
#     errors = []

#     for i in results:
#         image = i[0].replace('http://commons.wikimedia.org/wiki/Special:FilePath/', 'https://upload.wikimedia.org/wikipedia/commons/c/c6/')
#         if len(image.split(", ")) > 1:
#             split_file = image.split(", ")
#             t = 1
#             for file in split_file:
#                 r = requests.get(file, allow_redirects=True, stream=True)
#                 if r.status_code == 200 or "Error" in r.content:
#                     errors.append({i[1]: i[0]})
#                     print("Unsuccessful :/")
#                 else: 
#                     with open(f'coat_of_arms_files/{i[1]}._{t}{file.split('.')[-1]}', 'wb') as file:
#                         # file.write(r.content)
#                         shutil.copyfileobj(r.raw, file)
#                         print(f"Successful! {round(((counter/len(results))*100), 2)}%: {counter}/{len(results)}")
#                 t = t + 1
#         else:
#             r = requests.get(i[0], allow_redirects=True, stream=True)
#             if r.status_code == 200:
#                 with open(f'coat_of_arms_files/{i[1]}.{image.split('.')[-1]}', 'wb') as file:
#                     # file.write(r.content)
#                     shutil.copyfileobj(r.raw, file)
#                     print(f"Successful! {round(((counter/len(results))*100), 2)}%: {counter}/{len(results)}")
#             else:
#                 errors.append({i[1]: i[0]})            
#                 print("Unsuccessful :/")

#         time.sleep(0)
#         counter += 1
#     print("Errors: ", errors)


import sqlite3
import urllib.request
import shutil
import os

def download_coat_of_arms_files():
    database_path = "gemeindewappen.db"
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    query = """
    SELECT wappen.coat_of_arms_image, entities.database_id
    FROM wappen, entities
    WHERE entities.wikidata_id == wappen.wikidata_id AND wappen.coat_of_arms_image != "" AND entities.type != 'ehem_landkreis' AND entities.bundesland == 'Baden-Württemberg'
    """
    cursor.execute(query)
    results = cursor.fetchall()
    os.makedirs('coat_of_arms_files', exist_ok=True)
    counter = 1
    errors = []

    for i in results:
        # Transformiere die URL
        image = i[0]#.replace('http://commons.wikimedia.org/wiki/Special:FilePath/', 'https://upload.wikimedia.org/wikipedia/commons/c/c6/')
        urls = image.split(", ")

        for idx, url in enumerate(urls, start=1):
            ext = url.split('.')[-1]
            path = f'coat_of_arms_files/{i[1]}_{idx}.{ext}'

            try:
                with urllib.request.urlopen(url) as response:
                    if response.status == 200:
                        with open(path, 'wb') as file:
                            shutil.copyfileobj(response, file)
                            print(f"Successful! {round(((counter/len(results))*100), 2)}%: {counter}/{len(results)}")
                    else:
                        errors.append({i[1]: url})
                        print("Unsuccessful :/")
            except Exception as e:
                errors.append({i[1]: url})
                print(f"Error downloading {url}: {e}")
        time.sleep(10)
        counter += 1

    print("Errors: ", errors)




download_coat_of_arms_files()