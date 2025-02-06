import os
import pandas as pd
import kaggle
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL

def extract_data_from_kaggle(output_dir):
    """Extract dataset from Kaggle API and save it to the specified directory."""
    try:
        kaggle.api.authenticate()
        dataset = "mrsimple07/energy-consumption-prediction"
        kaggle.api.dataset_download_files(dataset, path=output_dir, unzip=True)
        print(f"Dataset downloaded successfully to {output_dir}")
    except Exception as e:
        print(f"Error in extracting data: {e}")

def transform_data(input_path, output_path):
    """Transform dataset: handle missing values, encoding, feature engineering."""
    try:
        df = pd.read_csv(input_path)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        df["Hour"] = df["Timestamp"].dt.hour
        df["Weekend"] = df["DayOfWeek"].isin(["Saturday", "Sunday"]).astype(int)
        df["HVACUsage"] = df["HVACUsage"].map({"On": 1, "Off": 0})
        df["LightingUsage"] = df["LightingUsage"].map({"On": 1, "Off": 0})
        df["Holiday"] = df["Holiday"].map({"Yes": 1, "No": 0})
        df.drop(columns=["DayOfWeek"], inplace=True)
        df.to_csv(output_path, index=False)
        print(f"Data transformation successful. Saved to {output_path}")
        return df
    except Exception as e:
        print(f"Error in data transformation: {e}")
        return None


def connect_snowflake():
    """Establishes a connection to Snowflake."""
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


def setup_snowflake_database_and_table(cur):
    """Creates the database, schema, and table if they do not exist."""
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS energy_consumption_db;")
        cur.execute("CREATE SCHEMA IF NOT EXISTS energy_consumption_db.consumption_schema;")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS energy_consumption_db.consumption_schema.energy_consumption (
                Timestamp TIMESTAMP,
                Temperature FLOAT,
                Humidity FLOAT,
                SquareFootage FLOAT,
                Occupancy INT,
                HVACUsage INT,
                LightingUsage INT,
                RenewableEnergy FLOAT,
                Holiday INT,
                Hour INT,
                Weekend INT,
                EnergyConsumption FLOAT
            );
        """)
        print("✅ Database, schema, and table ensured in Snowflake.")
    except Exception as e:
        print(f"❌ Error setting up Snowflake database and table: {e}")

def load_data_to_snowflake(conn, cur, df):
    """Loads the transformed data into Snowflake while preventing duplicates."""
    try:
        # Ensure table exists before loading data
        setup_snowflake_database_and_table(cur)
        
        # **Delete existing data before inserting new records**
        cur.execute("DELETE FROM energy_consumption_db.consumption_schema.energy_consumption;")
        print("🗑️ Existing data deleted before inserting new records.")

        # Ensure column names are uppercase before inserting
        df.columns = df.columns.str.upper()
        
        # Load data using write_pandas
        success, nchunks, nrows, _ = write_pandas(conn, df, "ENERGY_CONSUMPTION", schema="CONSUMPTION_SCHEMA")
        
        if success:
            print(f"✅ Data Loaded Successfully! Rows Inserted: {nrows}")
        else:
            raise Exception("❌ Data load failed. Check schema and table structure.")
    except Exception as e:
        print(f"❌ Error loading data to Snowflake: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



def run_tests():
    """Runs unit and integrity tests on the ETL pipeline."""
    try:
        print("🔍 Running Unit and Integrity Tests...")
        
        # Check if transformed file exists
        assert os.path.exists("F:/Portfolio Projects/Energy Consumption Prediction/data/Energy_consumption_transformed.csv"), "❌ Transformed file missing!"
        print("✅ Transformed file exists.")
        
        # Check if Snowflake table contains data
        conn, cur = connect_snowflake()
        if conn and cur:
            cur.execute("SELECT COUNT(*) FROM energy_consumption_db.consumption_schema.energy_consumption;")
            count = cur.fetchone()[0]
            assert count > 0, "❌ No data found in Snowflake table!"
            print(f"✅ Data integrity test passed! Rows in Snowflake: {count}")
            cur.close()
            conn.close()
    except Exception as e:
        print(f"❌ Test failed: {e}")

# **Execute the ETL Pipeline**
if __name__ == "__main__":
    # Define directory paths
    base_dir = "F:/Portfolio Projects/Energy Consumption Prediction"
    data_dir = os.path.join(base_dir, "data")
    transformed_file = os.path.join(data_dir, "Energy_consumption_transformed.csv")
    
    os.makedirs(data_dir, exist_ok=True)  # Ensure directory exists
    
    # Step 1: Extract data from Kaggle
    extract_data_from_kaggle(data_dir)
    
    # Step 2: Transform the dataset
    raw_file_path = os.path.join(data_dir, "Energy_consumption.csv")
    transformed_df = transform_data(raw_file_path, transformed_file)
    
    if transformed_df is not None:
        # Step 3: Connect to Snowflake and load data
        conn, cur = connect_snowflake()
        if conn and cur:
            load_data_to_snowflake(conn, cur, transformed_df)
            run_tests()
        else:
            print("❌ Snowflake connection failed. Skipping data load.")
    else:
        print("❌ Transformation failed. Skipping data load.")
