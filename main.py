import tkinter as tk
from tkinter import messagebox

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

# Calculate Certainty Factor for each diagnosis
def calculate_cf(disease, symptoms):
    total_cf = 0
    for symptom, rule_cf in rules[disease]:
        if symptom in symptoms:
            total_cf += rule_cf * (1 - total_cf)  # CF combination formula
    return round(total_cf, 3)

# When "Diagnose" button is clicked
def diagnose():
    selected_symptoms = []
    for symptom, var in symptom_vars.items():
        if var.get() == 1:
            selected_symptoms.append(symptom)

    if not selected_symptoms:
        messagebox.showwarning("No symptoms", "Please select at least one symptom.")
        return

    results = {}
    for disease in rules:
        cf = calculate_cf(disease, selected_symptoms)
        results[disease] = cf

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    result_text = "Diagnosis Results:\n"
    for disease, cf in sorted_results:
        result_text += f"{disease}: CF = {cf}\n"

    likely = sorted_results[0]
    if likely[1] > 0:
        result_text += f"\nMost likely condition: {likely[0]} with confidence {likely[1]}"
    else:
        result_text += "\nNo likely condition found based on input."

    result_label.config(text=result_text)

#__________________________________GUI Part__________________________________#

window = tk.Tk()
window.title("EEM348 Rule-Based Expert System")
window.geometry("400x600")
window.configure(bg="lightblue")

tk.Label(window, text="Select your symptoms:", bg="lightblue", font=("Arial", 14)).pack(pady=10)

# Symptom checkboxes
symptom_vars = {}
symptom_list = [
    'fever', 'cough', 'sneezing', 'runny nose', 
    'headache', 'body ache', 'sore throat', 
    'fatigue', 'itchy eyes'
]

for symptom in symptom_list:
    var = tk.IntVar()
    cb = tk.Checkbutton(window, text=symptom.capitalize(), variable=var, bg="lightblue", font=("Arial", 12))
    cb.pack(anchor='w', padx=20)
    symptom_vars[symptom] = var

# Diagnose button
tk.Button(window, text="Diagnose", command=diagnose, font=("Arial", 14), bg="navy", fg="white").pack(pady=20)

# Result label
result_label = tk.Label(window, text="", bg="lightblue", font=("Arial", 12), justify="left")
result_label.pack(padx=10, pady=10)

window.mainloop()
