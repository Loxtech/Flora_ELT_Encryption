import os
import pandas as pd
from sqlalchemy import create_engine
import security

def _encrypt_dataframe(pyspark_df) -> pd.DataFrame:
    """Hjælpefunktion der konverterer PySpark DF til Pandas og krypterer alle felter."""
    # Hent rækker med .collect() i stedet for .toPandas() for at undgå Py4J-fejl
    data = [row.asDict() for row in pyspark_df.collect()]
    pdf = pd.DataFrame(data)
    
    key = security.get_or_create_key()
    
    encrypted_pdf = pdf.copy()
    for col in encrypted_pdf.columns:
        encrypted_pdf[col] = encrypted_pdf[col].apply(lambda x: security.encrypt_val(x, key))
        
    return encrypted_pdf

def save_to_csv(pyspark_df, filename: str, output_dir: str):
    """Krypterer data og gemmer som CSV-fil."""
    encrypted_pdf = _encrypt_dataframe(pyspark_df)
    
    output_filepath = os.path.join(output_dir, f"transformed_{filename}")
    encrypted_pdf.to_csv(output_filepath, index=False)
    print(f"[LOAD] Krypteret data gemt i CSV: {output_filepath}")

def save_to_mysql(pyspark_df, db_config: dict, table_name: str = "iris_setosa_encrypted"):
    """Krypterer data og gemmer i MySQL-databasen."""
    encrypted_pdf = _encrypt_dataframe(pyspark_df)
    
    db_uri = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(db_uri)
    
    encrypted_pdf.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print(f"[LOAD] Krypteret data gemt i MySQL tabellen: '{table_name}'")