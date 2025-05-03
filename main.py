# Rule-Based Expert System using Certainty Factor

# Define rules with Certainty Factors
rules = {
    'Cold': [
        ('cough', 0.6), # if cough, then cold {cf 0.6}
        ('sore throat', 0.5),
        ('runny nose', 0.9)
    ],
    'Flu': [
        ('fever', 0.9),
        ('body ache', 0.8),
        ('fatigue', 0.7),
        ('cough', 0.5)
    ],
    'Allergy': [
        ('sneezing', 0.8),
        ('runny nose', 0.7),
        ('itchy eyes', 0.9)
    ],
    'Measles': [
        ('fever', 0.9),
        ('cough', 0.7),
        ('rash', 0.85)
    ],
    'Tuberculosis': [
        ('persistent cough', 0.9),
        ('fever', 0.6),
        ('weight loss', 0.8),
        ('night sweats', 0.7)
    ],
    'Strep Throat': [
        ('sore throat', 0.9),
        ('fever', 0.8),
        ('swollen lymph nodes', 0.7)
    ],
    'Gastroenteritis': [
        ('nausea', 0.8),
        ('vomiting', 0.7),
        ('diarrhea', 0.9),
        ('fever', 0.6)
    ],
    'Rheumatoid Arthritis': [
        ('joint pain', 0.8),
        ('fatigue', 0.6),
        ('sore throat', 0.5)
    ],
    'Migraine': [
        ('severe headache', 0.9),
        ('nausea', 0.8),
        ('sensitivity to light', 0.7),
        ('fatigue', 0.6)
    ],
    'Viral Infection': [
        ('fever', 0.8),
        ('cough', 0.7),
        ('fatigue', 0.6)
    ]
}

# Collect user symptoms and their confidence levels
print("Enter your symptoms and their confidence levels (e.g., 'cough, 0.9'). Type 'done' when finished.")
user_symptoms = []
while True:
    user_input = input("Symptom and CF: ").strip().lower()
    if user_input == 'done':
        break
    symptom, cf = user_input.split(',')
    user_symptoms.append((symptom.strip(), float(cf.strip())))  # Store as tuple (symptom, user CF)

# Calculate Certainty Factor for each diagnosis
def calculate_cf(disease, user_symptoms):
    total_cf = 0
    for symptom, user_cf in user_symptoms:
        for rule_symptom, rule_cf in rules[disease]:
            if symptom == rule_symptom:
                # Multiply user-provided CF with internal CF
                adjusted_cf = user_cf * rule_cf
                total_cf += adjusted_cf * (1 - total_cf)  # CF combination formula
    return round(total_cf, 3)

# Diagnose
results = {}
for disease in rules:
    cf = calculate_cf(disease, user_symptoms)
    results[disease] = cf

# Sort and display
sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
print("\nDiagnosis Results:")
for disease, cf in sorted_results:
    print(f"{disease}: CF = {cf}")

# Suggest likely diagnosis
likely = sorted_results[0]
if likely[1] > 0:
    print(f"\nMost likely condition: {likely[0]} with confidence {likely[1]}")
else:
    print("\nNo likely condition found based on input.")
