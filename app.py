from flask import Flask, render_template, request, jsonify
from nutrition_expert import NutritionExpert

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Get user data
        data = request.get_json()
        age = int(data['age'])
        gender = data['gender']
        
        # Get food consumption data
        foods = data['foods']
        
        # Create expert system instance
        expert = NutritionExpert(age, gender)
        
        # Calculate total nutrition
        total_calories = sum(food['calories'] for food in foods)
        total_protein = sum(food['protein'] for food in foods)
        total_fat = sum(food['fat'] for food in foods)
        total_carbs = sum(food['carbs'] for food in foods)
        
        # Get daily requirements
        daily_calories = expert.get_calorie_requirement()
        daily_protein = expert.get_protein_requirement()
        daily_fat = expert.get_fat_requirement()
        daily_carbs = expert.get_carb_requirement()
        
        # Calculate percentages
        calorie_percentage = (total_calories / daily_calories) * 100
        protein_percentage = (total_protein / daily_protein) * 100
        fat_percentage = (total_fat / daily_fat) * 100
        carbs_percentage = (total_carbs / daily_carbs) * 100
        
        # Forward chaining to determine nutrition status
        result = expert.evaluate_nutrition(
            calorie_percentage,
            protein_percentage,
            fat_percentage,
            carbs_percentage
        )
        
        return jsonify({
            'status': 'success',
            'result': result,
            'details': {
                'calories': {'total': total_calories, 'required': daily_calories, 'percentage': calorie_percentage},
                'protein': {'total': total_protein, 'required': daily_protein, 'percentage': protein_percentage},
                'fat': {'total': total_fat, 'required': daily_fat, 'percentage': fat_percentage},
                'carbs': {'total': total_carbs, 'required': daily_carbs, 'percentage': carbs_percentage}
            }
        })
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)