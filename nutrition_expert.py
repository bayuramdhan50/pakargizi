class NutritionExpert:
    def __init__(self, age, gender):
        self.age = age
        self.gender = gender
        
    def get_calorie_requirement(self):
        # Simplified calculation - you can make this more accurate based on your requirements
        if self.gender == 'male':
            return 2500
        return 2000
    
    def get_protein_requirement(self):
        if self.gender == 'male':
            return 65
        return 50
    
    def get_fat_requirement(self):
        if self.gender == 'male':
            return 80
        return 60
    
    def get_carb_requirement(self):
        if self.gender == 'male':
            return 350
        return 300
    
    def evaluate_nutrition(self, calorie_percentage, protein_percentage, fat_percentage, carbs_percentage):
        # Forward chaining rules
        rules = {
            'sufficient': lambda: all(p >= 50 for p in [calorie_percentage, protein_percentage, fat_percentage, carbs_percentage]),
            'insufficient': lambda: any(p < 50 for p in [calorie_percentage, protein_percentage, fat_percentage, carbs_percentage])
        }
        
        # Evaluate rules
        if rules['sufficient']():
            return "Gizi Tercukupi"
        elif rules['insufficient']():
            return "Gizi Tidak Tercukupi"
        
        return "Status Gizi Tidak Dapat Ditentukan"