import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from security import get_or_create_key, decrypt_val

def generate_visualizations(db_url: str, table_name: str, output_dir: str):
    key = get_or_create_key()
    engine = create_engine(db_url)

    # 1. Hent krypteret data fra MySQL
    encrypted_df = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)

    # 2. Dekrypter alle kolonner
    decrypted_df = encrypted_df.copy()
    for col in decrypted_df.columns:
        decrypted_df[col] = decrypted_df[col].apply(lambda x: decrypt_val(x, key))

    # 3. Konverter målingskolonnerne fra streng tilbage til float
    numeric_cols = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for col in numeric_cols:
        if col in decrypted_df.columns:
            decrypted_df[col] = pd.to_numeric(decrypted_df[col])

    # 4. Generer grafer ud fra de dekrypterede data
    sns.set_theme(style="whitegrid")

    # Diagram 1: Scatterplot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=decrypted_df, x='sepal_length', y='petal_length', color='green')
    plt.title('Sepal Length vs Petal Length (Iris Setosa)')
    plt.savefig(f"{output_dir}/scatter_plot.png")
    plt.close()

    # Diagram 2: Histogram
    plt.figure(figsize=(8, 6))
    sns.histplot(decrypted_df['petal_width'], kde=True, color='teal')
    plt.title('Distribution of Petal Width')
    plt.savefig(f"{output_dir}/histogram.png")
    plt.close()

    # Diagram 3: Boxplots
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=decrypted_df[numeric_cols], color='white')
    plt.title('Boxplot of Iris Setosa Features')
    plt.savefig(f"{output_dir}/boxplots.png")
    plt.close()

    print(f"[VISUALIZE] Grafer genereret ud fra dekrypteret data i {output_dir}")