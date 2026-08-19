import os
import pandas as pd
from pyspark.sql import DataFrame
from sqlalchemy import create_engine, text

def save_to_csv(df: DataFrame, original_filename: str, output_dir: str):
    new_filename = f"transformed_{original_filename}"
    output_path = os.path.join(output_dir, new_filename)
    
    pandas_df = pd.DataFrame(df.collect(), columns=df.columns)
    pandas_df.to_csv(output_path, index=False)
    print(f"-> Transformeret CSV gemt i: {output_path}")

def save_to_mysql(df: DataFrame, db_config: dict, table_name: str):
    base_uri = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}"
    engine = create_engine(base_uri)
    
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}"))
        conn.commit()
        
    db_uri = f"{base_uri}/{db_config['database']}"
    db_engine = create_engine(db_uri)
    
    pandas_df = pd.DataFrame(df.collect(), columns=df.columns)
    pandas_df.to_sql(name=table_name, con=db_engine, if_exists='replace', index=False)
    print(f"-> Data gemt i MySQL-tabellen '{table_name}'")