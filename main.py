import os

# Importer opdelte moduler
import extract
import transform
import load
import visualize

# --- Konfiguration og stier ---
DATA_URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
HEADER_LINE = "sepal_length,sepal_width,petal_length,petal_width,species"

INPUT_DIR = "Input_dir"
OUTPUT_DIR = "Output_dir"

DB_CONFIG = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'port': 3306,
    'database': 'flora_db'
}

def main():
    # Sikr at input og output mapper eksisterer
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("--- 1. EXTRACT ---")
    extracted_filepath = extract.extract_data(DATA_URL, INPUT_DIR, HEADER_LINE)
    filename = os.path.basename(DATA_URL)
    print(f"Fil hentet og gemt i: {extracted_filepath}")

    print("\n--- 2. TRANSFORM ---")
    # PySpark indlæser data og filtrerer på Iris-setosa
    transformed_pyspark_df = transform.transform_data(extracted_filepath)

    print("\n--- 3. LOAD (ENCRYPTED) ---")
    # Gemmer krypteret data som ny CSV
    load.save_to_csv(transformed_pyspark_df, filename, OUTPUT_DIR)
    
    # Gemmer krypteret data i den nye database-tabel
    load.save_to_mysql(transformed_pyspark_df, DB_CONFIG, table_name="iris_setosa_encrypted")

    print("\n--- 4. VISUALISERING (DECRYPT) ---")
    # Opret forbindelses-URI til MySQL
    db_uri = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    
    # Kør samlet visualisering (henter fra DB, dekrypterer og gemmer graferne)
    visualize.generate_visualizations(db_uri, table_name="iris_setosa_encrypted", output_dir=OUTPUT_DIR)

if __name__ == "__main__":
    main()