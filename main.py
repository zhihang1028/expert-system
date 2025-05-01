# Rule-Based Expert System using Certainty Factor

# Define rules with Certainty Factors
rules = {
    'Cold': [
        ('cough', 0.6),
        ('sneezing', 0.8),
        ('runny nose', 0.9),
        ('sore throat', 0.5)
    ],
    'Flu': [
        ('fever', 0.9),
        ('body ache', 0.8),
        ('fatigue', 0.7),
        ('headache', 0.6),
        ('cough', 0.5)
    ],
    'Allergy': [
        ('sneezing', 0.8),
        ('runny nose', 0.7),
        ('itchy eyes', 0.9)
    ]
}

# Collect user symptoms
print("Enter your symptoms one by one. Type 'done' when finished.")
user_symptoms = []
while True:
    symptom = input("Symptom: ").strip().lower()
    if symptom == 'done':
        break
    user_symptoms.append(symptom)

# Calculate Certainty Factor for each diagnosis
def calculate_cf(disease, symptoms):
    total_cf = 0
    for symptom, rule_cf in rules[disease]:
        if symptom in symptoms:
            total_cf += rule_cf * (1 - total_cf)  # CF combination formula
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
