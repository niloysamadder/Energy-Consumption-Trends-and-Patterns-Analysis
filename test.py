import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

def connect_snowflake():
    """
    Establishes a connection to Snowflake.
    :return: Snowflake connection object, cursor object
    """
    try:
        conn = snowflake.connector.connect(
            user="NILOYSAMADDER",
            password="Niloy110068/",
            account="vgbiase-qx65374",
            warehouse="COMPUTE_WH",
            database="energy_consumption_db",
            schema="consumption_schema"
        )
        cur = conn.cursor()
        print("✅ Connected to Snowflake!")
        return conn, cur
    except Exception as e:
        print(f"❌ Error connecting to Snowflake: {e}")
        return None, None

# Test connection
if __name__ == "__main__":
    conn, cur = connect_snowflake()
    if conn and cur:
        print("✅ Snowflake connection successful!")
    else:
        print("❌ Snowflake connection failed!")

