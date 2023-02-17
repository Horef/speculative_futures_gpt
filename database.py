table_name = ""

def create_db(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE table IF NOT EXISTS {table_name}
    (id integer primary key auto_increment,
    name text not null,
    text text not null,
    timestamp datetime default current timestamp)
    """)
    conn.commit()
    

def insert_db(conn, name, text):
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO {table_name} (name, text)
    VALUES ({name}, {text})
    """)
    conn.commit()

def query_db(conn):
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT * FROM {table_name}
    """)
    return cursor.fetchall()