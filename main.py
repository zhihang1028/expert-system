import customtkinter as ctk
from tkinter import messagebox

# Define rules with Certainty Factors
rules = {
    'Cold': [   # Assign CF value of 1.0 for all diseases.
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
    selected_symptoms = [symptom for symptom, var in symptom_vars.items() if var.get() == 1]

    if not selected_symptoms:
        messagebox.showwarning("No symptoms", "Please select at least one symptom.")
        return

    results = {disease: calculate_cf(disease, selected_symptoms) for disease in rules}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    result_text = "Diagnosis Results:\n"
    for disease, cf in sorted_results:
        result_text += f"{disease}: CF = {cf}\n"

    likely = sorted_results[0]
    if likely[1] > 0:
        result_text += f"\nMost likely condition: {likely[0]} with confidence {likely[1]}"
    else:
        result_text += "\nNo likely condition found based on input."

    result_label.configure(text=result_text)

# Clear selections
def clear_selection():
    for var in symptom_vars.values():
        var.set(0)
    result_label.configure(text="")

# Create the main window
ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue", etc.

window = ctk.CTk()
window.title("Medical Diagnosis Expert System")
window.geometry("400x600")

# Title Label
title_label = ctk.CTkLabel(window, text="Medical Diagnosis Expert System", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Symptom selection frame
symptom_frame = ctk.CTkFrame(window)
symptom_frame.pack(pady=10)

ctk.CTkLabel(symptom_frame, text="Select your symptoms:", font=("Arial", 14)).pack(anchor='w', padx=10)

# Symptom checkboxes
symptom_vars = {}
symptom_list = [
    'fever', 'cough', 'sneezing', 'runny nose', 
    'headache', 'body ache', 'sore throat', 
    'fatigue', 'itchy eyes'
]

for symptom in symptom_list:
    var = ctk.IntVar()
    cb = ctk.CTkCheckBox(symptom_frame, text=symptom.capitalize(), variable=var)
    cb.pack(anchor='w', padx=20, pady=5)
    symptom_vars[symptom] = var

# Diagnose and Clear buttons
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=20)

ctk.CTkButton(button_frame, text="Diagnose", command=diagnose).pack(side='left', padx=10, pady=5)
ctk.CTkButton(button_frame, text="Clear", command=clear_selection).pack(side='right', padx=10)

# Result label
result_label = ctk.CTkLabel(window, text="", font=("Arial", 12), justify="left")
result_label.pack(padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
