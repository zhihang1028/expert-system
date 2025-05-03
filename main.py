import customtkinter as ctk

# Define the rules with certainty factors for various traits related to jobs
rules = {
    'Mechanical Engineer': [
        ('mechanical skills', 0.9),
        ('problem solving', 0.8),
        ('creativity', 0.7),
        ('attention to detail', 0.6)
    ],
    'Software Engineer': [
        ('programming', 0.9),
        ('problem solving', 0.9),
        ('creativity', 0.8),
        ('collaboration', 0.7)
    ],
    'Electrical Engineer': [
        ('circuit design', 0.9),
        ('analytical thinking', 0.8),
        ('problem solving', 0.8),
        ('teamwork', 0.7)
    ],
    'Civil Engineer': [
        ('project management', 0.8),
        ('problem solving', 0.8),
        ('creativity', 0.7),
        ('communication', 0.6)
    ],
    'Chemical Engineer': [
        ('chemical analysis', 0.9),
        ('problem solving', 0.8),
        ('teamwork', 0.7),
        ('attention to detail', 0.6)
    ],
    'Mechatronics Engineer': [
        ('programming', 0.9),
        ('mechanical skills', 0.9),
        ('problem solving', 0.8),
        ('creativity', 0.7),
        ('circuit design', 0.8)
    ],
    'Environmental Engineer': [
        ('environmental science', 0.9),
        ('problem solving', 0.8),
        ('analytical thinking', 0.7),
        ('communication', 0.6)
    ]
}

# Define conditions for each job
conditions = {
    'Mechatronics Engineer': {
        'and': ['mechanical skills', 'programming'],
        'or': ['creativity', 'teamwork']
    },
}

def combine_cf(job, user_skills):
    total_cf = 0
    for skill, user_cf in user_skills:
        for rule_trait, rule_cf in rules[job]:
            if skill == rule_trait:
                adjusted_cf = user_cf * rule_cf
                total_cf += adjusted_cf * (1 - total_cf)  # applying the certainty factor combination formula
    return total_cf

# Function to calculate the certainty factor for each job
def calculate_cf(job, user_skills):
    total_cf = 0
    if job in conditions:
        job_conditions = conditions[job]

        # Handle "and" conditions
        if 'and' in job_conditions:
            and_cf = calculate_and_cf(user_skills, job_conditions['and'])
            user_skills.append(and_cf)  # add the minimum cf value (and)

            for trait in conditions[job]['and']:    # remove both cf values (and)
                for i in range(len(user_skills)):
                    if user_skills[i][0] == trait:
                        user_skills.pop(i)
                        break

            total_cf = combine_cf(job, user_skills)

        # Handle "or" conditions
        if 'or' in job_conditions:
            or_cf = calculate_or_cf(user_skills, job_conditions['or'])
            user_skills.append(or_cf)

            for trait in conditions[job]['or']:
                for i in range(len(user_skills)):
                    if user_skills[i][0] == trait:
                        user_skills.pop(i)
                        break

            total_cf = combine_cf(job, user_skills)

    else:
        # Normal calculation for other jobs
        total_cf = combine_cf(job, user_skills)

    return round(total_cf, 3)

def calculate_and_cf(user_skills, required_skills):
    # Create a dictionary of skills and their confidence factors
    skill_cfs = {skill: user_cf for skill, user_cf in user_skills if skill in required_skills}
    if len(skill_cfs) == len(required_skills):  # All required skills are present
        # Find the skill with the minimum confidence factor
        min_skill = min(skill_cfs, key=skill_cfs.get)  # Get the skill with the minimum CF
        return (min_skill, skill_cfs[min_skill])  # Return the skill and its CF as a tuple
    return ("", 0)  # Return a tuple indicating incomplete skills

def calculate_or_cf(user_skills, optional_skills):
    # Create a dictionary of skills and their confidence factors
    skill_cfs = {skill: user_cf for skill, user_cf in user_skills if skill in optional_skills}
    if len(skill_cfs) == len(optional_skills):  # All required skills are present
        # Find the skill with the maximum confidence factor
        max_skill = max(skill_cfs, key=skill_cfs.get)  # Get the skill with the maximum CF
        return (max_skill, skill_cfs[max_skill])  # Return the skill and its CF as a tuple
    return ("", 0)  # Return a tuple indicating incomplete skills

# Variable to track detailed results
detailed_results_shown = False
detailed_results_text = ""

# Function to handle the job suggestion process
def suggest_job():
    global detailed_results_text  # declare this variable as global
    user_traits = []
    for trait, var in trait_vars.items():
        if var.get() == 1:
            cf = float(trait_sliders[trait].get())  # retrieve the value from the slider
            user_traits.append((trait, cf))

    if not user_traits:
        show_error_message("Please select at least one skill.")
        return

    results = {job: calculate_cf(job, user_traits) for job in rules}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # Identify the most likely job
    likely = sorted_results[0]
    result_text = f"Most suitable job: {likely[0]} with confidence {likely[1]}\n"

    # Prepare the detailed results text
    detailed_results_text = "\n"
    for job, cf in sorted_results:
        detailed_results_text += f"{job}: CF = {cf}\n"

    # Display only the most likely job initially
    result_label.configure(text=result_text)
    result_label.pack(pady=0)
    clickable_text.configure(text="Show More")  # set initial text for the clickable
    clickable_text.pack(pady=5)  # display the clickable text

# Function to show an error message in a new window
def show_error_message(message):
    error_window = ctk.CTk()
    error_window.title("Warning")
    error_window.geometry("300x150")

    # Create a label to display the error message
    error_label = ctk.CTkLabel(error_window, text=message, font=("Arial", 12), justify="center")
    error_label.pack(pady=20)

    # Create a button to close the error window
    close_button = ctk.CTkButton(error_window, text="Close", command=error_window.destroy)
    close_button.pack(pady=5)

    error_window.mainloop()

# Function to clear all selections
def clear_selection():
    for var in trait_vars.values():
        var.set(0)
    # Shift focus away from the entry field
    button_frame.focus_set()
    for entry in trait_entries.values():
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.configure(placeholder_text="CF (e.g. 0.50)")
        entry.configure(state='disabled')
    for trait, slider in trait_sliders.items():
        slider.set(0.5)
        slider.configure(state="disabled")
    result_label.configure(text="")
    clickable_text.configure(text="")

# Function to show detailed results when clicked
def show_detailed_results(event=None):
    detailed_window = ctk.CTk()  # Create a new window for detailed results
    detailed_window.title("Detailed Job Suggestion Results")
    detailed_window.geometry("300x350")

    ctk.CTkLabel(detailed_window, text="Job Suggestion Results:", font=("Arial", 12)).pack(anchor='center', padx=10, pady=(20, 0))

    # Create a frame for the background
    frame = ctk.CTkFrame(detailed_window)
    frame.pack(padx=10, pady=0)

    # Create a label to display detailed results
    detailed_label = ctk.CTkLabel(frame, text=detailed_results_text, justify="left")
    detailed_label.pack(padx=10, pady=0, fill="both", expand=True)

    # Button to close the detailed results window
    close_button = ctk.CTkButton(detailed_window, text="Close", command=detailed_window.destroy)
    close_button.pack(pady=15)

    detailed_window.mainloop()

# Function to show help information with multiple pages
def show_help():
    help_window = ctk.CTk()  # Create a new window for help
    help_window.title("Help")
    help_window.geometry("400x300")

    # List of help pages
    help_pages = [
        "This is a job suggestion expert system.\n\n"
        "1. Select your skills from the list.\n"
        "2. Adjust the confidence levels using the sliders\n"
        "   from 0 (Definitely No) to 1 (Definitely Yes).\n"
        "3. Click 'Suggest Job' to get the most suitable job.\n"
        "4. Use 'Clear' to reset your selections.",
        
        "Tips for using the system:\n\n"
        "1. Make sure to select at least one skill.\n"
        "2. You can enter confidence factors manually or use the sliders.\n"
        "3. The system will suggest jobs based on your input.\n"
        "4. Once searching job, click 'Show More' to see detailed results.",
        
        "For further assistance:\n\n"
        "1. Contact support at support@example.com.\n"
        "2. Visit our website for more resources.\n"
        "3. Follow us on social media for updates."
    ]

    current_page = 0  # Track the current page index

    # Function to update the help content
    def update_help_content():
        help_label.configure(text=help_pages[current_page])
        prev_button.configure(state="normal" if current_page > 0 else "disabled")
        next_button.configure(state="normal" if current_page < len(help_pages) - 1 else "disabled")

    # Create a label to display help content
    help_label = ctk.CTkLabel(help_window, text="", justify="left")
    help_label.pack(padx=10, pady=10)

    # Create Previous and Next buttons
    prev_button = ctk.CTkButton(help_window, text="Previous", command=lambda: change_page(-1))
    prev_button.pack(side="left", padx=(10, 5), pady=10)

    next_button = ctk.CTkButton(help_window, text="Next", command=lambda: change_page(1))
    next_button.pack(side="right", padx=(5, 10), pady=10)

    # Function to change the page
    def change_page(direction):
        nonlocal current_page
        current_page += direction
        update_help_content()

    # Initialize the help content
    update_help_content()

    # Button to close the help window
    close_button = ctk.CTkButton(help_window, text="Close", command=help_window.destroy)
    close_button.pack(pady=10)

    help_window.mainloop()  # Start the event loop for the help window

# Create the main application window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Job Suggestion Expert System")
window.geometry("400x600")

# Title label for the application
title_label = ctk.CTkLabel(window, text="Job Suggestion Expert System", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

# Instruction label for user guidance
ctk.CTkLabel(window, text="Select your skills and enter confidence levels:", font=("Arial", 14)).pack(anchor='w', padx=10, pady=(20, 0))

# Create a scrollable frame for trait selection
scrollable_frame = ctk.CTkScrollableFrame(window)
scrollable_frame.pack(pady=10, fill="both", expand=True)

# Dictionaries to hold trait variables, sliders, and entries
trait_vars = {}
trait_sliders = {}
trait_entries = {}
trait_list = [
    'mechanical skills', 'programming', 'circuit design', 
    'project management', 'chemical analysis', 
    'environmental science', 
    'problem solving', 'creativity', 'teamwork', 
    'communication', 'analytical thinking', 'attention to detail'
]

# Function to enable or disable the slider based on the checkbox state
def toggle_slider(trait, var):
    slider = trait_sliders.get(trait)  # Retrieve the slider for the trait
    entry = trait_entries.get(trait)  # Retrieve the entry for the trait
    if slider:  # Check if the slider exists
        if var.get() == 1:  # If the checkbox is checked
            slider.configure(state='normal')  # Enable the slider
            entry.configure(state='normal')  # Enable the entry
            entry.configure(text_color="white")  # Reset text color to normal
        else:  # If the checkbox is unchecked
            slider.configure(state='disabled')  # Disable the slider
            entry.configure(text_color="darkgray") 
            entry.configure(state='disabled')  # Disable the entry field

# Loop through the trait list to create checkboxes, sliders, and entries
for trait in trait_list:
    var = ctk.IntVar()
    cb = ctk.CTkCheckBox(scrollable_frame, text=trait.capitalize(), variable=var,
                          command=lambda trait=trait, var=var: toggle_slider(trait, var))
    cb.pack(anchor='w', padx=20, pady=5)
    trait_vars[trait] = var

    # Create a slider for the confidence factor
    slider = ctk.CTkSlider(scrollable_frame, from_=0, to=1, number_of_steps=100, state='disabled')  # Start disabled
    slider.pack(anchor='w', padx=20, pady=5)
    trait_sliders[trait] = slider  # Store the slider in the dictionary

    # Create an entry for manual input of the confidence factor
    entry = ctk.CTkEntry(scrollable_frame, placeholder_text="CF (e.g. 0.50)")
    entry.pack(anchor='w', padx=20, pady=5)
    entry.configure(state='disabled')
    trait_entries[trait] = entry

    # Update the slider when the entry is changed
    def update_slider_from_entry(event, trait=trait, entry=entry, slider=slider, var=var):
        if var.get() == 1:  # If the checkbox is checked
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
        else:  # If the checkbox is not checked
            button_frame.focus_set()
            entry.delete(0, 'end')  # Clear the entry
            entry.configure(placeholder_text="CF (e.g. 0.50)")  # Set placeholder text

    # Bind the entry to the update function
    entry.bind("<Return>", update_slider_from_entry)

    # Update the entry when the slider is moved
    def update_entry(trait=trait, slider=slider, entry=entry, var=var):
        if var.get() == 1:  # Only update if the checkbox is checked
            entry.delete(0, 'end')
            entry.insert(0, f"{slider.get():.2f}")
        else:
            entry.delete(0, 'end')  # Clear the entry if the checkbox is not checked
            entry.configure(placeholder_text="CF (e.g. 0.50)")  # Set placeholder text
    
    # Bind the slider to the update function
    slider.bind("<ButtonRelease-1>", lambda event, trait=trait, slider=slider, entry=entry, var=var: update_entry(trait, slider, entry, var))

# Create buttons for suggesting jobs and clearing selections
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=20)

# Use grid layout for better control of button placement
ctk.CTkButton(button_frame, text="Suggest Job", command=suggest_job).grid(row=0, column=0, padx=(5, 2.5), pady=5)
ctk.CTkButton(button_frame, text="Clear", command=clear_selection).grid(row=0, column=1, padx=(2.5, 2.5))
ctk.CTkButton(button_frame, text="?", command=show_help, width=30).grid(row=0, column=2, padx=(2.5, 5))

# Create a clickable label for showing more detailed results
clickable_text = ctk.CTkLabel(window, text="", text_color="white", cursor="hand2", font=("Arial", 12, "underline"))
clickable_text.bind("<Button-1>", show_detailed_results)  # Bind left mouse button click to the function

# Label to display the result of the job suggestion
result_label = ctk.CTkLabel(window, text="", font=("Arial", 12), justify="left")
result_label.pack(padx=10, pady=10)

# Start the GUI event loop
window.mainloop()
