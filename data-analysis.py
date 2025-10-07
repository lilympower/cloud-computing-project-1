import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Improved logging function
def log_step(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

log_step("Starting script")

# Load the dataset. Change the file path to the location of All_diets.csv on your machine
df = pd.read_csv("path to csv")
log_step("Dataset loaded")

# Handle missing data (fill missing values with mean)
df[['Protein(g)', 'Carbs(g)', 'Fat(g)']] = df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].fillna(df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean())
log_step("Handled missing values in macronutrient columns")

# Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
log_step("Calculated average macronutrient content per diet type")

# Find the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
log_step("Identified top 5 protein-rich recipes per diet type")

# Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']
log_step("Added Protein-to-Carbs and Carbs-to-Fat ratio columns")

# Identify the diet type with the highest average protein content
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
log_step(f"Diet type with the highest average protein content: {highest_protein_diet}")

# Identify the most common cuisines for each diet type
common_cuisines = df.groupby('Diet_type')['Cuisine_type'].agg(
    lambda x: x.mode().iloc[0] if not x.mode().empty else 'Unknown'
)
log_step("Identified most common cuisine per diet type")

# Visualizations

log_step("Visualizing average Protein by diet type")
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title('Average Protein by Diet Type')
plt.ylabel('Average Protein (g)')
plt.xlabel('Diet Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

log_step("Visualizing average Carbs by diet type")
sns.barplot(x=avg_macros.index, y=avg_macros['Carbs(g)'])
plt.title('Average Carbs by Diet Type')
plt.ylabel('Average Carbs (g)')
plt.xlabel('Diet Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

log_step("Visualizing average Fat by diet type")
sns.barplot(x=avg_macros.index, y=avg_macros['Fat(g)'])
plt.title('Average Fat by Diet Type')
plt.ylabel('Average Fat (g)')
plt.xlabel('Diet Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

log_step("Visualizing heatmap of average macronutrients by diet type")
sns.heatmap(avg_macros, annot=True, cmap='YlGnBu', fmt='.1f')
plt.title('Heatmap of Average Macronutrients by Diet Type')
plt.ylabel('Diet Type')
plt.xlabel('Macronutrient')
plt.tight_layout()
plt.show()

log_step("Visualizing top 5 protein-rich recipes per diet type as scatter plot")
sns.scatterplot(data=top_protein, x='Diet_type', y='Protein(g)', hue='Cuisine_type')
plt.title('Top 5 Protein-Rich Recipes per Diet Type')
plt.ylabel('Protein (g)')
plt.xlabel('Diet Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

log_step("Printing results")

print("\nAverage Macronutrient content per diet type:\n", avg_macros)
print("\nTop 5 protein-rich recipes per diet type:\n", top_protein[['Diet_type', 'Recipe_name', 'Protein(g)', 'Cuisine_type']])
print("\nDiet type with highest average protein content:", highest_protein_diet)
print("\nMost common cuisine per diet type:\n", common_cuisines)

log_step("Script finished")

