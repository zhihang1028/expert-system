import customtkinter as ctk

# Define rules with Certainty Factors
rules = {
    'Cold': [
        ('cough', 0.8),
        ('sore throat', 0.7),
        ('sneezing', 0.9),
        ('body ache', 0.1),
        ('runny nose', 0.8)
    ],
    'Flu': [
        ('fever', 0.9),
        ('body ache', 0.8),
        ('fatigue', 0.7),
        ('cough', 0.8),
        ('sneezing', 0.4),
        ('headache', 0.8),
        ('runny nose', 0.5)
    ],
    'Allergy': [
        ('sneezing', 0.8),
        ('runny nose', 0.7),
        ('itchy eyes', 0.9),
        ('rash', 0.8),
        ('persistent cough', 0.3),
        ('nausea', 0.2)
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
    'COVID-19': [
        ('fever', 0.8),
        ('body ache', 0.5),
        ('fatigue', 0.5),
        ('cough', 0.8),
        ('shortness of breath', 0.6),
        ('headache', 0.5),
        ('runny nose', 0.5),
        ('loss of taste', 0.6),
    ]
}

# Calculate Certainty Factor for each diagnosis
def calculate_cf(disease, user_symptoms):
    total_cf = 0
    for symptom, user_cf in user_symptoms:
        for rule_symptom, rule_cf in rules[disease]:
            if symptom == rule_symptom:
                adjusted_cf = user_cf * rule_cf
                total_cf += adjusted_cf * (1 - total_cf)  # CF combination formula
    return round(total_cf, 3)

# Detailed results tracking
detailed_results_shown = False
detailed_results_text = ""

# Diagnose button
def diagnose():
    global detailed_results_text  # Make this variable global
    user_symptoms = []
    for symptom, var in symptom_vars.items():
        if var.get() == 1:
            cf = float(symptom_sliders[symptom].get())  # Get value from the slider
            user_symptoms.append((symptom, cf))

    if not user_symptoms:
        show_error_message("Please select at least one symptom.")
        return

    results = {disease: calculate_cf(disease, user_symptoms) for disease in rules}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # Get the most likely condition
    likely = sorted_results[0]
    result_text = f"Most likely condition: {likely[0]} with confidence {likely[1]}\n"

    # Prepare detailed results text
    detailed_results_text = "\n"
    for disease, cf in sorted_results:
        detailed_results_text += f"{disease}: CF = {cf}\n"

    # Show only the most likely condition initially
    result_label.configure(text=result_text)
    result_label.pack(pady=0)
    clickable_text.configure(text="Show More")  # Set initial text for clickable label
    clickable_text.pack(pady=5)  # Show the clickable text

def show_error_message(message):
    error_window = ctk.CTk()
    error_window.title("Warning")
    error_window.geometry("300x150")

    # Create a label to display the error message
    error_label = ctk.CTkLabel(error_window, text=message, font=("Arial", 12), justify="center")
    error_label.pack(pady=20)

    # Create a close button
    close_button = ctk.CTkButton(error_window, text="Close", command=error_window.destroy)
    close_button.pack(pady=5)

    error_window.mainloop()

# Clear selections
def clear_selection():
    for var in symptom_vars.values():
        var.set(0)
    # Shift focus away from the entry field
    button_frame.focus_set()
    for entry in symptom_entries.values():
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.configure(placeholder_text="CF (e.g. 0.50)")
        entry.configure(state='disabled')
    for symptom, slider in symptom_sliders.items():
        slider.set(0.5)
        slider.configure(state="disabled")
    result_label.configure(text="")
    clickable_text.configure(text="")

# Clickable text for showing more results
def show_detailed_results(event=None):
    detailed_window = ctk.CTk()     # Window Pop out
    detailed_window.title("Detailed Diagnosis Results")
    detailed_window.geometry("300x350")

    ctk.CTkLabel(detailed_window, text="Diagnosis Results:", font=("Arial", 12)).pack(anchor='center', padx=10, pady=(20, 0))

    # Create background frame
    frame = ctk.CTkFrame(detailed_window)
    frame.pack(padx=10, pady=0)

    # Create label
    detailed_label = ctk.CTkLabel(frame, text=detailed_results_text, justify="left")
    detailed_label.pack(padx=10, pady=0, fill="both", expand=True)

    # Close button
    close_button = ctk.CTkButton(detailed_window, text="Close", command=detailed_window.destroy)
    close_button.pack(pady=15)

    detailed_window.mainloop()

# Help button function
def show_help():
    help_window = ctk.CTk()  # Create a new window
    help_window.title("Help")
    help_window.geometry("400x200")

    help_text = "\nThis is a medical diagnosis expert system.\n\n" \
                "1. Select your symptoms from the list.\n" \
                "2. Adjust the confidence levels using the sliders\n" \
                "   from 0 (Definitely No) to 1 (Definitely Yes).\n" \
                "3. Click 'Diagnose' to get the most likely condition.\n" \
                "4. Use 'Clear' to reset your selections."

    help_label = ctk.CTkLabel(help_window, text=help_text, justify="left")
    help_label.pack(padx=10, pady=10)

    close_button = ctk.CTkButton(help_window, text="Close", command=help_window.destroy)
    close_button.pack(pady=10)

    help_window.mainloop()  # Start the event loop for the help window


# Create the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("EEM348 Rule-Based Expert System")
window.geometry("400x600")

# Title Label
title_label = ctk.CTkLabel(window, text="Medical Diagnosis Expert System", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Instruction
ctk.CTkLabel(window, text="Select your symptoms and enter confidence levels:", font=("Arial", 14)).pack(anchor='w', padx=10, pady=(20, 0))

# Scrollable frame for symptoms
scrollable_frame = ctk.CTkScrollableFrame(window)
scrollable_frame.pack(pady=10, fill="both", expand=True)

# Symptom checkboxes and slider fields for confidence factors
symptom_vars = {}
symptom_sliders = {}
symptom_entries = {}
symptom_list = [
    'fever', 'cough', 'sneezing', 'runny nose', 
    'headache', 'sore throat', 'body ache', 
    'fatigue', 'loss of taste', 'itchy eyes', 'nausea', 'vomiting', 
    'diarrhea', 'joint pain', 'rash', 'shortness of breathe',
    'persistent cough', 
    'weight loss', 'night sweats', 'swollen lymph nodes', 
    'sensitivity to light', 'severe headache'
]

# Function to enable/disable slider based on checkbox state
def toggle_slider(symptom, var):
    slider = symptom_sliders.get(symptom)  # Get the slider for the symptom
    entry = symptom_entries.get(symptom)  # Get the entry for the symptom
    if slider:  # Check if the slider exists
        if var.get() == 1:  # Checkbox is checked
            slider.configure(state='normal')  # Enable the slider
            entry.configure(state='normal')  # Enable the entry
            entry.configure(text_color="white")  # Reset text color to normal
        else:  # Checkbox is unchecked
            slider.configure(state='disabled')  # Disable the slider
            entry.configure(text_color="darkgray")  # Change text color to light gray
            entry.configure(state='disabled')  # Disable the entry field
            #entry.delete(0, 'end')  # Clear the entry field

for symptom in symptom_list:
    var = ctk.IntVar()
    cb = ctk.CTkCheckBox(scrollable_frame, text=symptom.capitalize(), variable=var,
                          command=lambda symptom=symptom, var=var: toggle_slider(symptom, var))
    cb.pack(anchor='w', padx=20, pady=5)
    symptom_vars[symptom] = var

    # Slider for confidence factor
    slider = ctk.CTkSlider(scrollable_frame, from_=0, to=1, number_of_steps=100, state='disabled')  # Start disabled
    slider.pack(anchor='w', padx=20, pady=5)
    symptom_sliders[symptom] = slider  # Store the slider in the dictionary

    # Entry for manual input of confidence factor
    entry = ctk.CTkEntry(scrollable_frame, placeholder_text="CF (e.g. 0.50)")
    entry.pack(anchor='w', padx=20, pady=5)
    entry.configure(state='disabled')
    symptom_entries[symptom] = entry

    # Update the slider when the entry is changed
    def update_slider_from_entry(event, symptom=symptom, entry=entry, slider=slider, var=var):
        if var.get() == 1:  # Checkbox is checked
            try:
                value = float(entry.get())
                if 0 <= value <= 1:
                    slider.set(value)
                elif value > 1:
                    entry.delete(0, 'end')
                    entry.insert(0, "1")
                    slider.set(1)
                else:
                    entry.delete(0, 'end')
                    entry.insert(0, "0")
                    slider.set(0)
            except ValueError:
                button_frame.focus_set()
                entry.delete(0, 'end')
                entry.configure(placeholder_text="CF (e.g. 0.50)")
        else:  # Checkbox is not checked
            button_frame.focus_set()
            entry.delete(0, 'end')  # Clear the entry
            entry.configure(placeholder_text="CF (e.g. 0.50)")  # Set placeholder text

    # Bind the entry to the update function
    entry.bind("<Return>", update_slider_from_entry)

    # Update the entry when the slider is moved
    def update_entry(symptom=symptom, slider=slider, entry=entry, var=var):
        if var.get() == 1:  # Only update if the checkbox is checked
            entry.delete(0, 'end')
            entry.insert(0, f"{slider.get():.2f}")
        else:
            entry.delete(0, 'end')  # Clear the entry if the checkbox is not checked
            entry.configure(placeholder_text="CF (e.g. 0.50)")  # Set placeholder text
    
    # Bind the slider to the update function
    slider.bind("<ButtonRelease-1>", lambda event, symptom=symptom, slider=slider, entry=entry, var=var: update_entry(symptom, slider, entry, var))

# Diagnose and Clear buttons
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=20)

# Use grid for better control
ctk.CTkButton(button_frame, text="Diagnose", command=diagnose).grid(row=0, column=0, padx=(5, 2.5), pady=5)
ctk.CTkButton(button_frame, text="Clear", command=clear_selection).grid(row=0, column=1, padx=(2.5, 2.5))
ctk.CTkButton(button_frame, text="?", command=show_help, width=30).grid(row=0, column=2, padx=(2.5, 5))

# Clickable text for showing more results
clickable_text = ctk.CTkLabel(window, text="", text_color="white", cursor="hand2", font=("Arial", 12, "underline"))
clickable_text.bind("<Button-1>", show_detailed_results)  # Bind left mouse button click

# Result label
result_label = ctk.CTkLabel(window, text="", font=("Arial", 12), justify="left")
result_label.pack(padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
