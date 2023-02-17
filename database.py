table_name = ""

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE table IF NOT EXISTS {table_name}
    (id integer primary key autoincrement,
    name text not null,
    text text not null,
    timestamp datetime default current_timestamp)
    """)
    conn.commit()
    

def insert_db(conn, name, text):
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO {table_name} (name, text)
    VALUES ('{name}', '{text}')
    """)
    conn.commit()

def query_db(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM {table_name}
    """)
    return cursor.fetchall()

def clear_table(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    DELETE FROM {table_name}
    """)
    conn.commit()