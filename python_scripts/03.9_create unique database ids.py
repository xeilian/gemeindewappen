import sqlite3

def create_unique_database_ids():
    database_path = "gemeindewappen.db"

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE entities ADD COLUMN database_id TEXT;")

    cursor.execute("""
        SELECT wikidata_id
        FROM entities
        WHERE type != 'ehem_landkreis'
        ORDER BY bundesland
    """)
    results = cursor.fetchall()
    
    for index, (wikidata_id,) in enumerate(results, start=1):
        database_id = f"DE-{str(index).zfill(5)}"
        cursor.execute("""
            UPDATE entities
            SET database_id = ?
            WHERE wikidata_id = ?;
        """, (database_id, wikidata_id))
    
    conn.commit()
    conn.close()


create_unique_database_ids()