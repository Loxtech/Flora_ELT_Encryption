import os
import pandas as pd
from sqlalchemy import create_engine

# Importer dine opdelte moduler
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
    
    # =========================================================================
    # REFLEKSION OM VALG AF EXTRACT-METODE (Requests):
    #
    # Jeg har valgt Python-biblioteket 'requests' frem for 'wget' og 'subprocess/cURL':
    # 
    # 1. Sikkerhed (Command Injection):
    #    Requests arbejder direkte på Pythons netværkslag og opretter socket-
    #    forbindelser. Den tilgår aldrig operativsystemets shell, hvilket udelukker 
    #    risikoen for command injection 100%. 
    #    'subprocess/cURL' kan derimod udgøre en sikkerhedsrisiko, hvis input indeholder 
    #    skadelige tegn og eksekveres via shell.
    #
    # 2. HTTPS & Datatransport:
    #    Requests verificerer automatisk SSL/TLS-certifikater under transporten over HTTPS.
    #
    # 3. Robusthed & Streaming:
    #    Ved at anvende `stream=True` og `iter_content(chunk_size=1024)` overføres 
    #    data i kontrollerede datablokke (chunks). Dette sikrer, at koden kan håndtere 
    #    store datamængder og ustabile netværk uden at overbelaste hukommelsen (RAM).
    #
    # 4. Cross-platform:
    #    Requests virker ensartet på tværs af Linux, Windows og macOS uden afhængighed 
    #    af eksterne systembinærer som cURL.
    # =========================================================================

    print("--- 1. EXTRACT ---")
    extracted_filepath = extract.extract_data(DATA_URL, INPUT_DIR, HEADER_LINE)
    filename = os.path.basename(DATA_URL)
    print(f"Fil hentet og gemt i: {extracted_filepath}")

    print("\n--- 2. TRANSFORM ---")
    # PySpark indlæser data og filtrerer på Iris-setosa
    transformed_pyspark_df = transform.transform_data(extracted_filepath)

    print("\n--- 3. LOAD ---")
    # Gemmer transformeret data som ny CSV med 'transformed_' præfiks
    load.save_to_csv(transformed_pyspark_df, filename, OUTPUT_DIR)
    
    # Gemmer/overskriver i MySQL databasen
    load.save_to_mysql(transformed_pyspark_df, DB_CONFIG, table_name="iris_setosa")

    print("\n--- 4. VISUALISERING ---")
    # Opret forbindelses-URI til den oprettede MySQL database
    db_uri = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    engine = create_engine(db_uri)
    
    # Hent transformeret data ud af databasen til en Pandas DataFrame
    df_from_db = pd.read_sql("SELECT * FROM iris_setosa", con=engine)
    
    # Kør de tre visningsmetoder fra visualiseringsmodulet
    visualize.plot_scatter(df_from_db)
    visualize.plot_histogram(df_from_db)
    visualize.plot_boxplots(df_from_db)

if __name__ == "__main__":
    main()