from flask import Flask, jsonify, send_from_directory, render_template
import pandas as pd
import os
from analysis import (
    load_dataset, clean_macronutrients, calculate_average_macros,
    get_top_protein_recipes, add_nutrient_ratios,
    get_highest_protein_diet, get_common_cuisines, run_full_analysis
)

app = Flask(__name__)
OUTPUT_DIR = 'output'
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # serves your HTML dashboard

@app.route('/api/avg_macros')
def avg_macros_api():
    df = load_dataset("res/All_Diets.csv")
    df = clean_macronutrients(df)
    avg_macros = calculate_average_macros(df)
    return avg_macros.reset_index().to_json(orient='records')

@app.route('/api/top_protein')
def top_protein_api():
    df = load_dataset("res/All_Diets.csv")
    df = clean_macronutrients(df)
    top_protein = get_top_protein_recipes(df)
    return top_protein[['Diet_type', 'Recipe_name', 'Protein(g)', 'Cuisine_type']].to_json(orient='records')

@app.route('/api/common_cuisines')
def common_cuisines_api():
    df = load_dataset("res/All_Diets.csv")
    df = clean_macronutrients(df)
    cuisines = get_common_cuisines(df)
    return cuisines.reset_index().to_json(orient='records')

@app.route('/api/summary')
def summary_api():
    results = run_full_analysis("res/All_Diets.csv")
    return {
        "highest_protein_diet": results["highest_protein_diet"],
        "average_macros": results["average_macros"].to_dict(orient='records'),
        "common_cuisines": results["common_cuisines"].to_dict(orient='records')
    }

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(OUTPUT_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
