from flask import Flask, request, jsonify, render_template
from nutrition_expert import NutritionExpert
import pandas as pd
import numpy as np
from functools import wraps
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_numpy_types(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, pd.Series):
        return obj.to_list()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(item) for item in obj]
    return obj

def validate_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_json()
            if not data:
                return jsonify(status="error", message="Data JSON tidak ditemukan"), 400
            
            required_fields = {
                'umur': ('int', lambda x: 0 <= x <= 150),
                'gender': ('str', lambda x: x.lower() in ['pria', 'wanita', 'laki-laki', 'perempuan']),
                'berat': ('float', lambda x: 20 <= x <= 300),  # Minimum weight 20kg
                'tinggi': ('float', lambda x: 100 <= x <= 250)  # Height between 100-250cm
            }
            
            for field, (field_type, validator) in required_fields.items():
                value = data.get(field)
                if value is None and field not in ['berat', 'tinggi']:  # Optional fields
                    return jsonify(status="error", message=f"Field '{field}' harus diisi"), 400
                
                if value is not None:
                    try:
                        if field_type == 'int':
                            value = int(value)
                        elif field_type == 'float':
                            value = float(value)
                        if not validator(value):
                            return jsonify(status="error", message=f"Nilai '{field}' tidak valid"), 400
                    except ValueError:
                        return jsonify(status="error", message=f"Format '{field}' tidak valid"), 400
                
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kategori')
def kategori():
    try:
        df = pd.read_csv('daftar_makanan_gizi.csv')
        if 'Makanan' in df.columns:
            makanan_list = sorted(df['Makanan'].dropna().unique().tolist())
            return jsonify(status="success", kategori=makanan_list)
        return jsonify(status="error", message="Format data makanan tidak sesuai"), 500
    except Exception as e:
        logger.error(f"Error in kategori: {str(e)}")
        return jsonify(status="error", message="Gagal membaca data makanan"), 500

@app.route('/calculate', methods=['POST'])
@validate_input
def calculate():
    try:
        data = request.get_json()
        umur = int(data.get('umur'))
        gender = data.get('gender')
        makanan_dengan_porsi = data.get('makanan', [])
        berat = float(data.get('berat', 0))
        tinggi = float(data.get('tinggi', 0))

        # Initialize expert system
        expert = NutritionExpert(umur, gender)
        
        # Analyze selected foods with portions
        df = pd.read_csv('daftar_makanan_gizi.csv')
        
        total_nutrition = {
            'kalori': 0, 'protein': 0, 'lemak': 0, 'karbohidrat': 0, 'serat': 0
        }
        
        selected_foods_list = []
        
        for item in makanan_dengan_porsi:
            food_name = item['nama']
            portion = float(item['porsi'])
            
            food_data = df[df['Makanan'] == food_name].iloc[0].copy()
            # Multiply nutritional values by portion
            for nutrient in ['Kalori', 'Protein', 'Lemak', 'Karbohidrat', 'Serat']:
                if nutrient in food_data:
                    food_data[nutrient] *= portion
                    total_nutrition[nutrient.lower()] += food_data[nutrient]
            
            food_data['Porsi'] = portion
            selected_foods_list.append(food_data.to_dict())

        # Compare nutrition with daily requirements
        nutrition_comparison = expert.compare_nutrition(total_nutrition)
        
        # Calculate BMI if weight and height are provided
        bmi_data = None
        if berat >= 20 and tinggi >= 100:  # Validate minimum values
            # Convert height from cm to meters and calculate BMI
            tinggi_m = tinggi / 100.0
            bmi = berat / (tinggi_m * tinggi_m)
            
            # Validate BMI result
            if 10 <= bmi <= 100:  # Reasonable BMI range
                bmi_status = expert.analyze_bmi(bmi)
                bmi_data = {
                    'nilai': round(bmi, 1),  # Round to 1 decimal place
                    'status': bmi_status['status'],
                    'rekomendasi': bmi_status['rekomendasi']
                }
            else:
                bmi_data = {
                    'nilai': round(bmi, 1),
                    'status': 'Nilai BMI tidak valid',
                    'rekomendasi': ['Pastikan data berat dan tinggi badan sudah benar']
                }

        response_data = {
            'kebutuhan': {
                'kalori': int(expert.kalori),
                'protein': int(expert.protein),
                'lemak': int(expert.lemak),
                'karbohidrat': int(expert.karbohidrat),
                'serat': int(expert.serat)
            },
            'asupan_saat_ini': total_nutrition,
            'perbandingan_gizi': nutrition_comparison,
            'makanan_dipilih': selected_foods_list
        }
        
        if bmi_data:
            response_data['bmi'] = bmi_data

        return jsonify(status="success", data=response_data)

    except Exception as e:
        logger.error(f"Error in calculate: {str(e)}")
        return jsonify(status="error", message=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
