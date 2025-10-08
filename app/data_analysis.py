import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Logging function
def log_step(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

# Load the dataset
def load_dataset(filepath):
    log_step("Loading dataset")
    return pd.read_csv(filepath)

# Handle missing data (fill missing values with mean)
def clean_macronutrients(df):
    log_step("Handling missing values in macronutrient columns")
    df[['Protein(g)', 'Carbs(g)', 'Fat(g)']] = df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].fillna(
        df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
    )
    return df

# Calculate the average macronutrient content for each diet type
def calculate_average_macros(df):
    log_step("Calculating average macronutrient content per diet type")
    return df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Find the top 5 protein-rich recipes for each diet type
def get_top_protein_recipes(df, top_n=5):
    log_step(f"Identifying top {top_n} protein-rich recipes per diet type")
    return df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(top_n)

# Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
def add_nutrient_ratios(df):
    log_step("Adding Protein-to-Carbs and Carbs-to-Fat ratio columns")
    df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
    df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']
    return df

# Identify the diet type with the highest average protein content
def get_highest_protein_diet(avg_macros):
    log_step("Finding diet type with the highest average protein content")
    return avg_macros['Protein(g)'].idxmax()

# Identify the most common cuisines for each diet type
def get_common_cuisines(df):
    log_step("Identifying most common cuisine per diet type")
    return df.groupby('Diet_type')['Cuisine_type'].agg(
        lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
    )

# Visualizations
def visualize_avg_macronutrient_bar(avg_macros, nutrient):
    log_step(f"Visualizing average {nutrient} by diet type")
    plt.figure()
    sns.barplot(x=avg_macros.index, y=avg_macros[nutrient])
    plt.title(f'Average {nutrient} by Diet Type')
    plt.ylabel(f'Average {nutrient}')
    plt.xlabel('Diet Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = os.path.join(OUTPUT_DIR, f'{nutrient}_by_diet.png')
    plt.savefig(filename)
    plt.close()
    log_step(f"Saved plot: {filename}")

def visualize_heatmap(avg_macros):
    log_step("Visualizing heatmap of average macronutrients by diet type")
    plt.figure()
    sns.heatmap(avg_macros, annot=True, cmap='rocket_r', fmt='.1f')
    plt.title('Heatmap of Average Macronutrients by Diet Type')
    plt.ylabel('Diet Type')
    plt.xlabel('Macronutrient')
    plt.tight_layout()
    filename = os.path.join(OUTPUT_DIR, 'heatmap.png')
    plt.savefig(filename)
    plt.close()
    log_step(f"Saved plot: {filename}")

def visualize_top_protein_scatter(top_protein):
    log_step("Visualizing top protein-rich recipes per diet type as scatter plot")
    plt.figure()
    sns.scatterplot(data=top_protein, x='Diet_type', y='Protein(g)', hue='Cuisine_type')
    plt.title('Top 5 Protein-Rich Recipes per Diet Type')
    plt.ylabel('Protein (g)')
    plt.xlabel('Diet Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = os.path.join(OUTPUT_DIR, 'top_protein.png')
    plt.savefig(filename)
    plt.close()
    log_step(f"Saved plot: {filename}")


def main():
    log_step("Starting script")

    # Load the dataset. Change the path to wherever the csv is located on your system.
    df = load_dataset("res/All_Diets.csv")

    # Handle missing data
    df = clean_macronutrients(df)

    # Calculate average macronutrient content
    avg_macros = calculate_average_macros(df)

    # Find the top 5 protein-rich recipes for each diet type
    top_protein = get_top_protein_recipes(df)

    # Add new metrics
    df = add_nutrient_ratios(df)

    # Identify the highest protein diet
    highest_protein_diet = get_highest_protein_diet(avg_macros)

    # Identify most common cuisine per diet
    common_cuisines = get_common_cuisines(df)

    # Visualizations
    visualize_avg_macronutrient_bar(avg_macros, 'Protein(g)')
    visualize_avg_macronutrient_bar(avg_macros, 'Carbs(g)')
    visualize_avg_macronutrient_bar(avg_macros, 'Fat(g)')
    visualize_heatmap(avg_macros)
    visualize_top_protein_scatter(top_protein)

    # Output results
    log_step("Printing results")
    print("\nAverage Macronutrient content per diet type:\n", avg_macros)
    print("\nTop 5 protein-rich recipes per diet type:\n", top_protein[['Diet_type', 'Recipe_name', 'Protein(g)', 'Cuisine_type']])
    print("\nDiet type with highest average protein content:", highest_protein_diet)
    print("\nMost common cuisine per diet type:\n", common_cuisines)

    log_step("Script finished")

if __name__ == "__main__":
    main()
