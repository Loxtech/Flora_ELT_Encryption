from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col

def transform_data(csv_filepath: str) -> DataFrame:
    # Opret eller genbrug Spark Session
    spark = SparkSession.builder \
        .appName("FloraETL") \
        .master("local[*]") \
        .getOrCreate()
    
    # Indlæs CSV med automatisk type-inferens og overskrifter
    df = spark.read.csv(csv_filepath, header=True, inferSchema=True)
    
    # Filtrer observationer hvor species er Iris-setosa
    transformed_df = df.filter(col("species") == "Iris-setosa")
    
    return transformed_df