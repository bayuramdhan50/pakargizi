import pandas as pd
import random

class NutritionExpert:
    def __init__(self, age, gender, kategori=None, food_df=None):
        self.age = age
        self.gender = self._normalize_gender(gender)
        self.kategori = kategori

        df = pd.read_csv('kebutuhan_gizi_usia_gender.csv')
        try:
            row = df[(df['Gender'].str.lower() == self.gender) & (self.age <= df['Usia (max)'])].iloc[0]
        except IndexError:
            raise Exception("Data kebutuhan gizi tidak ditemukan untuk usia dan gender ini.")

        self.kalori = int(row['Kalori'])
        self.protein = int(row['Protein'])
        self.lemak = int(row['Lemak'])
        self.karbohidrat = int(row['Karbohidrat'])  # Changed from carbs to karbohidrat
        self.serat = int(row['Serat'])  # Changed from fiber to serat

        if food_df is not None:
            self.food_data = food_df.copy()
        else:
            self.food_data = pd.read_csv('daftar_makanan_gizi.csv')

        self.food_data.columns = [col.strip().lower() for col in self.food_data.columns]
        self.food_data = self.food_data.rename(columns={
            'makanan': 'nama',
            'kalori': 'kalori',
            'protein': 'protein',
            'lemak': 'lemak',
            'karbohidrat': 'karbohidrat',
            'serat': 'serat',
            'kategori': 'kategori'
        })
        
        # Initialize nutrition facts with Indonesian terminology
        self.facts = {
            'usia': self.age,
            'gender': self.gender,
            'kebutuhan_kalori': self.kalori,
            'kebutuhan_protein': self.protein,
            'kebutuhan_lemak': self.lemak,
            'kebutuhan_karbohidrat': self.karbohidrat,
            'kebutuhan_serat': self.serat
        }
        
    def _normalize_gender(self, gender):
        if gender.lower() in ['pria', 'laki-laki', 'male']:
            return 'male'
        elif gender.lower() in ['wanita', 'perempuan', 'female']:
            return 'female'
        else:
            raise ValueError("Gender tidak valid. Gunakan 'pria' atau 'wanita'.")

    def analyze_bmi(self, bmi):
        """Analyze BMI and provide recommendations using forward chaining"""
        rules = {
            'underweight': (0, 18.5, 'Berat badan kurang', [
                'Tingkatkan asupan kalori harian',
                'Konsumsi makanan tinggi protein',
                'Makan dengan porsi lebih sering',
                'Konsultasikan dengan dokter untuk program penambahan berat badan'
            ]),
            'normal': (18.5, 24.9, 'Berat badan normal', [
                'Pertahankan pola makan sehat',
                'Konsumsi makanan seimbang',
                'Jaga aktivitas fisik rutin'
            ]),
            'overweight': (25, 29.9, 'Berat badan berlebih', [
                'Kurangi asupan kalori harian',
                'Tingkatkan aktivitas fisik',
                'Batasi makanan tinggi lemak dan gula',
                'Konsumsi lebih banyak sayur dan buah'
            ]),
            'obese': (30, float('inf'), 'Obesitas', [
                'Konsultasikan dengan dokter untuk program penurunan berat badan',
                'Kurangi porsi makan secara bertahap',
                'Hindari makanan tinggi kalori dan lemak',
                'Lakukan olahraga teratur sesuai kemampuan'
            ])
        }

        for status, (min_bmi, max_bmi, label, recommendations) in rules.items():
            if min_bmi <= bmi < max_bmi:
                return {
                    'status': label,
                    'rekomendasi': recommendations
                }
        
        # Default case if BMI doesn't fall into any range (shouldn't happen with proper validation)
        return {
            'status': 'Berat badan tidak valid',
            'rekomendasi': ['Pastikan data berat dan tinggi badan sudah benar']
        }

    def compare_nutrition(self, selected_foods_nutrition):
        """Membandingkan asupan gizi dari makanan yang dipilih dengan kebutuhan harian menggunakan forward chaining"""
        comparisons = {}
        nutrients = {
            'kalori': ('Kalori', 'kkal'),
            'protein': ('Protein', 'gram'),
            'lemak': ('Lemak', 'gram'),
            'karbohidrat': ('Karbohidrat', 'gram'),
            'serat': ('Serat', 'gram')
        }
        
        # Forward chaining rules for nutrition comparison
        for nutrient, (label, unit) in nutrients.items():
            current = selected_foods_nutrition.get(nutrient, 0)
            target = getattr(self, nutrient)  # Now using consistent attribute names
            percentage = (current / target * 100) if target > 0 else 0
            
            # Initialize status and recommendations
            status = 'cukup'
            rekomendasi = []
            
            # Rule 1: Defisit nutrisi (kurang dari 80% kebutuhan)
            if percentage < 80:
                status = 'kurang'
                deficit = target - current
                rekomendasi.append(f'Anda masih kurang {label.lower()} sebesar {deficit:.1f} {unit}')
                
                # Sub-rules for specific nutrients
                if nutrient == 'kalori':
                    if percentage < 60:
                        rekomendasi.extend([
                            'Segera tingkatkan asupan kalori Anda',
                            'Perbanyak frekuensi makan dalam porsi sedang',
                            'Pilih makanan padat energi'
                        ])
                    else:
                        rekomendasi.extend([
                            'Tingkatkan porsi makan secara bertahap',
                            'Tambahkan makanan selingan bergizi'
                        ])
                
                elif nutrient == 'protein':
                    if percentage < 60:
                        rekomendasi.extend([
                            'Prioritaskan konsumsi protein hewani seperti:',
                            '- Daging tanpa lemak',
                            '- Ikan',
                            '- Telur',
                            'Atau protein nabati seperti tempe dan tahu'
                        ])
                    else:
                        rekomendasi.extend([
                            'Tambahkan asupan protein dari:',
                            '- Kacang-kacangan',
                            '- Produk susu',
                            '- Daging tanpa lemak'
                        ])
                
                elif nutrient == 'lemak':
                    rekomendasi.extend([
                        'Tambahkan sumber lemak sehat seperti:',
                        '- Minyak zaitun',
                        '- Alpukat',
                        '- Kacang-kacangan'
                    ])
                
                elif nutrient == 'karbohidrat':
                    if percentage < 60:
                        rekomendasi.extend([
                            'Segera tingkatkan asupan karbohidrat dari:',
                            '- Nasi',
                            '- Roti gandum',
                            '- Kentang',
                            '- Umbi-umbian'
                        ])
                    else:
                        rekomendasi.extend([
                            'Tambahkan porsi karbohidrat kompleks',
                            'Pilih makanan berserat tinggi'
                        ])
            
            # Rule 2: Kelebihan nutrisi (lebih dari 120% kebutuhan)
            elif percentage > 120:
                status = 'berlebih'
                excess = current - target
                rekomendasi.append(f'Anda kelebihan {label.lower()} sebesar {excess:.1f} {unit}')
                
                if nutrient == 'kalori':
                    if percentage > 150:
                        rekomendasi.extend([
                            'Segera kurangi asupan kalori secara signifikan',
                            'Konsultasikan dengan ahli gizi',
                            'Tingkatkan aktivitas fisik'
                        ])
                    else:
                        rekomendasi.extend([
                            'Kurangi porsi makan secara bertahap',
                            'Pilih makanan rendah kalori'
                        ])
                
                elif nutrient == 'lemak':
                    if percentage > 150:
                        rekomendasi.extend([
                            'Segera kurangi konsumsi makanan berlemak',
                            'Hindari gorengan dan fast food',
                            'Pilih metode memasak yang lebih sehat',
                            'Konsultasikan dengan ahli gizi'
                        ])
                    else:
                        rekomendasi.extend([
                            'Kurangi konsumsi makanan berlemak',
                            'Pilih metode memasak yang lebih sehat'
                        ])
                
                elif nutrient == 'karbohidrat':
                    rekomendasi.extend([
                        'Kurangi porsi makanan sumber karbohidrat',
                        'Ganti dengan sayuran',
                        'Pilih karbohidrat kompleks'
                    ])
            
            # Rule 3: Asupan normal (antara 80-120% kebutuhan)
            else:
                rekomendasi.append(f'Asupan {label.lower()} sudah sesuai dengan kebutuhan')
                if percentage >= 90 and percentage <= 110:
                    rekomendasi.append('Pertahankan pola makan saat ini')

            comparisons[nutrient] = {
                'nilai_saat_ini': current,
                'nilai_kebutuhan': target,
                'persentase': round(percentage, 1),
                'status': status,
                'rekomendasi': rekomendasi,
                'unit': unit
            }
            
        return comparisons

    def analyze_nutrition_status(self):
        """Implement forward chaining untuk analisis status gizi"""
        status = {}
        recommendations = []
        
        # Rule 1: Analisis Kalori
        daily_calories = self.facts['kebutuhan_kalori']
        if self.age <= 5:
            kalori_min = daily_calories * 0.9
            kalori_max = daily_calories * 1.1
            status['kalori'] = {
                'status': 'normal' if kalori_min <= self.kalori <= kalori_max else 'tidak normal',
                'rekomendasi': [
                    'Pertahankan asupan kalori' if kalori_min <= self.kalori <= kalori_max 
                    else 'Konsultasikan dengan dokter untuk penyesuaian asupan kalori'
                ]
            }
        
        # Rule 2: Analisis Protein
        protein_min = self.facts['kebutuhan_protein'] * 0.8
        if self.protein < protein_min:
            status['protein'] = {
                'status': 'kurang',
                'rekomendasi': [
                    'Tingkatkan asupan protein dengan mengkonsumsi:',
                    '- Daging tanpa lemak',
                    '- Ikan',
                    '- Telur',
                    '- Kacang-kacangan'
                ]
            }
        else:
            status['protein'] = {
                'status': 'cukup',
                'rekomendasi': ['Pertahankan asupan protein saat ini']
            }
        
        # Rule 3: Analisis Lemak
        lemak_max = self.facts['kebutuhan_lemak'] * 1.2
        if self.lemak > lemak_max:
            status['lemak'] = {
                'status': 'berlebih',
                'rekomendasi': [
                    'Kurangi konsumsi makanan berlemak',
                    'Hindari gorengan',
                    'Pilih metode memasak yang lebih sehat seperti kukus atau panggang',
                    'Batasi konsumsi makanan cepat saji'
                ]
            }
        else:
            status['lemak'] = {
                'status': 'normal',
                'rekomendasi': ['Pertahankan asupan lemak saat ini']
            }
        
        # Rule 4: Analisis Karbohidrat
        karbo_min = self.facts['kebutuhan_karbohidrat'] * 0.9
        karbo_max = self.facts['kebutuhan_karbohidrat'] * 1.1
        if self.karbohidrat < karbo_min:
            status['karbohidrat'] = {
                'status': 'kurang',
                'rekomendasi': [
                    'Tingkatkan asupan karbohidrat dari:',
                    '- Nasi',
                    '- Roti gandum',
                    '- Kentang',
                    '- Umbi-umbian'
                ]
            }
        elif self.karbohidrat > karbo_max:
            status['karbohidrat'] = {
                'status': 'berlebih',
                'rekomendasi': [
                    'Kurangi porsi makanan sumber karbohidrat',
                    'Ganti dengan sayuran',
                    'Pilih karbohidrat kompleks'
                ]
            }
        else:
            status['karbohidrat'] = {
                'status': 'normal',
                'rekomendasi': ['Pertahankan asupan karbohidrat saat ini']
            }

        return status

    def get_food_recommendations(self, nutrition_status):
        """Generate food recommendations based on nutrition status"""
        recommendations = []
        df = self.food_data

        if nutrition_status['protein']['status'] == 'kurang':
            protein_foods = df[df['protein'] >= 5].sample(n=min(3, len(df)))
            recommendations.extend([
                f"- {row['nama']} (protein: {row['protein']}g)"
                for _, row in protein_foods.iterrows()
            ])

        if nutrition_status['lemak']['status'] == 'berlebih':
            low_fat_foods = df[df['lemak'] <= 3].sample(n=min(3, len(df)))
            recommendations.extend([
                f"- {row['nama']} (lemak: {row['lemak']}g)"
                for _, row in low_fat_foods.iterrows()
            ])

        if nutrition_status['karbohidrat']['status'] != 'normal':
            if nutrition_status['karbohidrat']['status'] == 'kurang':
                carb_foods = df[df['karbohidrat'] >= 20].sample(n=min(3, len(df)))
            else:
                carb_foods = df[df['karbohidrat'] <= 15].sample(n=min(3, len(df)))
            recommendations.extend([
                f"- {row['nama']} (karbohidrat: {row['karbohidrat']}g)"
                for _, row in carb_foods.iterrows()
            ])

        return recommendations

    def daily_menu_list(self, total_items=7):
        """Generate daily menu recommendations using forward chaining"""
        # Analyze current nutrition status
        nutrition_status = self.analyze_nutrition_status()
        
        # Get food recommendations based on status
        food_recommendations = self.get_food_recommendations(nutrition_status)
        
        # Filter foods based on category if specified
        df = self.food_data
        if self.kategori:
            df = df[df['kategori'].str.lower() == self.kategori.lower()]
        
        # Select foods based on nutritional needs
        if nutrition_status['protein']['status'] == 'kurang':
            protein_foods = df[df['protein'] >= 5].sample(n=min(3, len(df)))
            remaining = total_items - len(protein_foods)
            other_foods = df[~df.index.isin(protein_foods.index)].sample(n=remaining)
            selected = pd.concat([protein_foods, other_foods])
        else:
            selected = df.sample(n=total_items)
        
        selected = selected.reset_index(drop=True)
        
        result = {
            'menu': selected.to_dict('records'),
            'status_gizi': nutrition_status,
            'rekomendasi_khusus': food_recommendations
        }
        
        return result
