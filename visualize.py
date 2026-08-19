import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_scatter(df: pd.DataFrame, output_dir: str = "Output_dir"):
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x='sepal_length', y='petal_length', color='darkgreen')
    plt.title('Scatterplot: Sepal Length vs Petal Length (Iris-setosa)')
    plt.xlabel('Sepal Length (cm)')
    plt.ylabel('Petal Length (cm)')
    plt.grid(True)
    
    filepath = os.path.join(output_dir, "scatter_plot.png")
    plt.savefig(filepath)
    plt.close()
    print(f"-> Graf gemt: {filepath}")

def plot_histogram(df: pd.DataFrame, output_dir: str = "Output_dir"):
    plt.figure(figsize=(8, 6))
    sns.histplot(df['petal_width'], bins=10, kde=True, color='teal')
    plt.title('Histogram over Petal Width')
    plt.xlabel('Petal Width (cm)')
    plt.ylabel('Antal (Frequency)')
    plt.grid(True)
    
    filepath = os.path.join(output_dir, "histogram.png")
    plt.savefig(filepath)
    plt.close()
    print(f"-> Graf gemt: {filepath}")

def plot_boxplots(df: pd.DataFrame, output_dir: str = "Output_dir"):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('Boxplots for Iris-setosa Målinger', fontsize=14)
    
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for ax, feature in zip(axes.flatten(), features):
        sns.boxplot(y=df[feature], ax=ax, color='skyblue')
        ax.set_title(f'Boxplot af {feature}')
        ax.set_ylabel('Størrelse (cm)')
        ax.grid(True)
        
    plt.tight_layout()
    filepath = os.path.join(output_dir, "boxplots.png")
    plt.savefig(filepath)
    plt.close()
    print(f"-> Graf gemt: {filepath}")