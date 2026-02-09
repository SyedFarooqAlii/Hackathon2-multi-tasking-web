import psycopg2
from urllib.parse import urlparse

# Database connection string
conn_str = "postgresql://neondb_owner:npg_OSDVAB02kaRn@ep-noisy-band-ah7c3io8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    # Connect to the database
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()

    print("Connected to Neon database successfully!")

    # List all tables in the public schema
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)

    tables = cur.fetchall()
    print(f"\nTables found in the database: {len(tables)}")

    for table in tables:
        table_name = table[0]
        print(f"- {table_name}")

        # Count rows in each table
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cur.fetchone()[0]
        print(f"  -> Rows: {row_count}")

        # If table has rows, show first few records
        if row_count > 0:
            cur.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cur.fetchall()
            print(f"  -> Sample data:")
            for row in rows:
                print(f"     {row}")

    # Close connections
    cur.close()
    conn.close()

except Exception as e:
    print(f"Error connecting to database: {e}")