import customtkinter as ctk

# define rules (easy to add new in the future)
rules = {
    'Mechatronics Engineer': [
        ('robotics', 0.9),
        ('hands-on work', 0.85),
        ('control systems', 0.8),
        ('electronics', 0.85),
        ('outdoors', -0.5)
    ],
    'Civil Engineer': [
        ('project management', 0.8),
        ('outdoors', 0.7),
        ('analytical skills', 0.6),
        ('teamwork', -0.4)
    ],
    'Software Engineer': [
        ('programming', 0.9),
        ('problem solving', 0.8),
        ('teamwork', 0.6),
        ('long-term projects', -0.3)
    ],
    'Mechanical Engineer': [
        ('thermodynamics', 0.8),
        ('hands-on work', 0.8),
        ('math skills', 0.6),
        ('office work', -0.4)
    ],
    'Electrical Engineer': [
        ('circuit design', 0.9),
        ('power systems', 0.8),
        ('electronics', 0.7),
        ('complex systems', -0.5)
    ],
    'Chemical Engineer': [
        ('chemistry', 0.9),
        ('lab work', 0.8),
        ('analytical skills', 0.7),
        #('hazardous materials', -0.4)
    ]
}


# define conditions and/or (also easier to add new in the future)
conditions = {
    'Mechatronics Engineer': {
        'and': ['hands-on work', 'electronics'],
        'or': ['control systems', 'robotics']
    },
}

def combine_cf(job, user_skills):
    total_cf = 0
    for skill, user_cf in user_skills:
        for rule_trait, rule_cf in rules[job]:
            if skill == rule_trait:
                adjusted_cf = user_cf * rule_cf # multiply user cf with internal cf

                # applying the certainty factor formula for all three cases
                if total_cf >= 0 and adjusted_cf >= 0:
                    total_cf += adjusted_cf * (1 - total_cf)
                elif total_cf < 0 and adjusted_cf < 0:
                    total_cf += adjusted_cf * (1 + total_cf)
                elif total_cf < 0 or adjusted_cf < 0:
                    total_cf = (total_cf + adjusted_cf) / (1 - min(abs(total_cf), abs(adjusted_cf)))
                    
    return total_cf

def calculate_cf(job, user_skills):
    total_cf = 0
    if job in conditions:   # if the job is inside the condition dictionary (and/or)
        job_conditions = conditions[job]
        skills_cond = user_skills.copy()    # so that it wont alter the original list

        if 'and' in job_conditions:
            and_cf = calculate_and_cf(skills_cond, job_conditions['and'])   # compare and get the min value
            skills_cond.append(and_cf)  # add the min cf value (and) into the list

            for trait in conditions[job]['and']:    # remove both cf values (and) from the list
                for i in range(len(skills_cond)):
                    if skills_cond[i][0] == trait:
                        skills_cond.pop(i)
                        break

        if 'or' in job_conditions:
            or_cf = calculate_or_cf(skills_cond, job_conditions['or'])  # now for max value (or)
            skills_cond.append(or_cf)

            for trait in conditions[job]['or']:
                for i in range(len(skills_cond)):
                    if skills_cond[i][0] == trait:
                        skills_cond.pop(i)
                        break

            total_cf = combine_cf(job, skills_cond) # combine all the cf values inside the skill list (for condition jobs only)

    else:  
        total_cf = combine_cf(job, user_skills) # for jobs that are not in condition dict

    return round(total_cf, 3)

def calculate_and_cf(user_skills, required_skills):
    skill_cfs = {skill: user_cf for skill, user_cf in user_skills if skill in required_skills}  # create dict for cf and skills
    if len(skill_cfs) == len(required_skills):  # check if all skills available (as in the and condition)
        min_skill = min(skill_cfs, key=skill_cfs.get)  # compare and get min cf
        return (min_skill, skill_cfs[min_skill])
    return ("", 0)

def calculate_or_cf(user_skills, optional_skills):
    skill_cfs = {skill: user_cf for skill, user_cf in user_skills if skill in optional_skills}

    if not skill_cfs:
        return ("", 0)  # if no skills match (or)

    if len(skill_cfs) == 1:
        skill, cf = next(iter(skill_cfs.items()))  # if only 1 skill match then directly return the cf of the skill
        return (skill, cf)
        
    max_skill = max(skill_cfs, key=skill_cfs.get)  # if multiple skill then compare and take max value
    return (max_skill, skill_cfs[max_skill])

# track detailed result
detailed_results_shown = False
detailed_results_text = ""

# after clicking suggest job button
def suggest_job():
    global detailed_results_text  # global variable
    user_traits = []
    for trait, var in trait_vars.items():
        if var.get() == 1:
            cf = float(trait_sliders[trait].get())  # take value from slider
            user_traits.append((trait, cf))

    if not user_traits:
        show_error_message("Please select at least one preference/skill.")
        return

    results = {job: calculate_cf(job, user_traits) for job in rules}
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    # check for highest cf (suitable job)
    likely = sorted_results[0]
    if likely[1] <= 0.2:    # cf lower than (or equal) 0.2
        show_error_message(f"CF value too low to suggest job (CF={likely[1]}).\nPlease brush up your skills and try again.")
    else:
        result_text = f"Most suitable job:\n{likely[0]} with confidence {likely[1]}\n"

        # loop through all jobs with cf
        detailed_results_text = "\n"
        for job, cf in sorted_results:
            detailed_results_text += f"{job}: CF = {cf}\n"

        # only display most suitable job
        result_label.configure(text=result_text)
        result_label.pack(pady=0)
        clickable_text.configure(text="Show More")
        clickable_text.pack(pady=(0, 10))  # display the clickable text
    
def show_error_message(message):    # pop out error window
    error_window = ctk.CTk()
    error_window.title("Warning")
    error_window.geometry("340x140")

    error_label = ctk.CTkLabel(error_window, text=message, font=("Arial", 12), justify="center")
    error_label.pack(pady=20)

    close_button = ctk.CTkButton(error_window, text="Close", command=error_window.destroy)
    close_button.pack(pady=5)

    error_window.mainloop()

# when pressing clear button
def clear_selection():
    for var in trait_vars.values(): # reset checkbox
        var.set(0)
    
    button_frame.focus_set()    # shift focus away from entry before reseting (prevent bug)

    for entry in trait_entries.values():    # reset entry
        entry.configure(state='normal')
        entry.delete(0, 'end')
        entry.configure(placeholder_text="CF (e.g. 0.50)")
        entry.configure(state='disabled')

    for trait, slider in trait_sliders.items(): # reset slider
        slider.set(0)
        slider.configure(state="disabled")

    result_label.configure(text="") # clear result section text
    clickable_text.configure(text="")

# after clicking show more
def show_detailed_results(event=None):
    detailed_window = ctk.CTk()
    detailed_window.title("Detailed Job Suggestion Results")
    detailed_window.geometry("300x350")

    ctk.CTkLabel(detailed_window, text="Job Suggestion Results:", font=("Arial", 12)).pack(anchor='center', padx=10, pady=(20, 0))

    frame = ctk.CTkFrame(detailed_window)   # add gray frame
    frame.pack(padx=10, pady=0)

    detailed_label = ctk.CTkLabel(frame, text=detailed_results_text, justify="left")    # display all job cf values
    detailed_label.pack(padx=10, pady=0, fill="both", expand=True)

    close_button = ctk.CTkButton(detailed_window, text="Close", command=detailed_window.destroy)
    close_button.pack(pady=15)

    detailed_window.mainloop()

# after clicking ? button
def show_help():
    help_window = ctk.CTk()
    help_window.title("Help")
    help_window.geometry("410x300")

    # help pages list
    help_pages = [
        "Welcome to the Job Suggestion Expert System!\n\n"
        "This system helps you find suitable job recommendations based on your preferences/skills and confidence levels.\n\n"
        "Follow these steps to get started:\n"
        "1. Select your preferences from the provided list.\n"
        "2. Adjust the confidence levels using the sliders.\n"
        "3. Click 'Suggest Job' to receive the most appropriate job suggestions.\n"
        "4. Use the 'Clear' button to reset your selections and start over.",
        
        "Tips for Using the System:\n\n"
        "1. Ensure you select at least one preference to receive job suggestions.\n"
        "2. You can manually enter certainty factors or adjust them using the sliders.\n"
        "3. The system generates job suggestions based on your selected skills and confidence levels.\n"
        "4. After receiving suggestions, click 'Show More' to view detailed CF values for each job.",
        
        "Understanding Certainty Factors (CF):\n\n"
        "Inputs\n"
        "1. Positive CF values indicate strong preferences or that you have acquired the skill.\n"
        "2. Negative CF values indicate disagreement or that you have not acquired the skill.\n"
        "3. A CF of 0 (or sometimes between -0.2 and 0.2) means uncertainty.\n\n"
        "Results\n"
        "1. Positive CF values in your results indicate a strong belief match for the job, suggesting you are well-suited for it.\n"
        "2. Negative CF values in your results indicate a mismatch, suggesting that the job may not be suitable for you.\n",
        
        "Job Descriptions:\n\n"
        "Mechatronics Engineer: Combines mechanical, electronic, and software engineering to design and create smart machines.\n\n"
        "Civil Engineer: Plans, designs, and oversees construction projects, focusing on infrastructure and public works.\n\n"
        "Software Engineer: Develops software applications, requiring strong programming and problem-solving skills.\n\n"
        "Mechanical Engineer: Works on the design and manufacturing of mechanical systems, utilizing principles of physics and materials science.\n\n"
        "Electrical Engineer: Designs and develops electrical systems and components, including power generation and distribution.\n\n"
        "Chemical Engineer: Applies principles of chemistry and engineering to develop processes for producing chemicals and materials."
        ]

    current_page = 0  # track page index

    def update_help_content():
        help_text.delete(1.0, ctk.END)  # clear text
        help_text.insert(ctk.END, help_pages[current_page])  # insert new text
        prev_button.configure(state="normal" if current_page > 0 else "disabled")
        next_button.configure(state="normal" if current_page < len(help_pages) - 1 else "disabled")
    
    # scrollable text box
    help_text = ctk.CTkTextbox(help_window, wrap="word", width=380, height=200)
    help_text.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")  # use sticky to fill space

    prev_button = ctk.CTkButton(help_window, text="<", width=30, command=lambda: change_page(-1))
    prev_button.grid(row=1, column=1, padx=(100, 2.5), pady=5, sticky="e")  # slign to right (east)

    close_button = ctk.CTkButton(help_window, text="Close", command=help_window.destroy)
    close_button.grid(row=1, column=2, padx=(2.5, 2.5), pady=5)

    next_button = ctk.CTkButton(help_window, text=">", width=30, command=lambda: change_page(1))
    next_button.grid(row=1, column=3, padx=(2.5, 100), pady=5, sticky="w")  # align to left (west)

    # change page
    def change_page(direction):
        nonlocal current_page
        current_page += direction
        update_help_content()

    # initialise help content
    update_help_content()
    
    help_window.mainloop()

# create main application window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("EEM348 Job Suggestion Expert System") # window title
window.geometry("400x600")

# main text
title_label = ctk.CTkLabel(window, text="Job Suggestion Expert System", font=("Arial", 16, "bold"))
title_label.pack(pady=20)

ctk.CTkLabel(window, text="Select your preferences/skills and enter confidence levels:", font=("Arial", 14)).pack(anchor='w', padx=10, pady=(20, 0))

# scrollable frame for preferences/skills selection
scrollable_frame = ctk.CTkScrollableFrame(window)
scrollable_frame.pack(pady=10, fill="both", expand=True)

# dictionaries to hold values
trait_vars = {} # tickbox
trait_sliders = {}  # slider
trait_entries = {}  # entry
trait_list = [  # preferences/skills
    'robotics', 'hands-on work', 'control systems', 'electronics',
    'project management', 'outdoors', 'analytical skills',
    'teamwork', 'programming', 'problem solving', 'long-term projects',
    'thermodynamics', 'math skills', 'office work', 'circuit design', 'power systems',
    'complex systems', 'chemistry', 'lab work'
]

# enable or disable the slider based on the tickbox state
def toggle_slider(trait, var):
    slider = trait_sliders.get(trait)  # get slider value
    entry = trait_entries.get(trait)  # get entry value
    if slider:  # if slider exists
        if var.get() == 1:  # if tickbox checked by user
            slider.configure(state='normal')  # enable slider (unlock)
            entry.configure(state='normal')  # enable entry
            entry.configure(text_color="white")  # reset text colour
        else:  # if tickbox unchecked by user (still preserve the value without clearing it)
            slider.configure(state='disabled')  # disable slider (lock)
            entry.configure(text_color="darkgray") # set text colour (grayout)
            entry.configure(state='disabled')  # disable entry

# loop through all the preferences to create tickbox, slider, and entry
for trait in trait_list:
    var = ctk.IntVar()  # tickbox
    cb = ctk.CTkCheckBox(scrollable_frame, text=trait.capitalize(), variable=var,
                          command=lambda trait=trait, var=var: toggle_slider(trait, var))
    cb.pack(anchor='w', padx=20, pady=5)
    trait_vars[trait] = var

    # create slider
    slider = ctk.CTkSlider(scrollable_frame, from_=-1, to=1, number_of_steps=100, state='disabled')  # lock slider by default
    slider.pack(anchor='w', padx=20, pady=5)
    trait_sliders[trait] = slider  # store slider in dictionary

    # create entry
    entry = ctk.CTkEntry(scrollable_frame, placeholder_text="CF (e.g. 0.50)")   # set placeholder text before locking entry
    entry.pack(anchor='w', padx=20, pady=5)
    entry.configure(state='disabled')   # lock entry by default
    trait_entries[trait] = entry # store to dict

    # update slider according to entry
    def update_slider_from_entry(event, trait=trait, entry=entry, slider=slider, var=var):
        if var.get() == 1:  # if tickbox checked
            try:
                value = float(entry.get())
                if -1 <= value <= 1:    # make sure entry value in bound
                    slider.set(value)
                elif value > 1: # if user enter value larger than 1 then autoset back to 1
                    entry.delete(0, 'end')
                    entry.insert(0, "1")
                    slider.set(1)
                else:   # if user enter value smaller than -1 then autoset back to -1
                    entry.delete(0, 'end')
                    entry.insert(0, "-1")
                    slider.set(-1)
            except ValueError:  # handle other error
                button_frame.focus_set()    # move away focus before clearing entry
                entry.delete(0, 'end')
                entry.configure(placeholder_text="CF (e.g. 0.50)")  # reset placeholder text
        else:  # if tickbox not checked
            button_frame.focus_set()    # move away the focus from entry
            entry.delete(0, 'end')  #  clear entry
            entry.configure(placeholder_text="CF (e.g. 0.50)")

    # bind entry to slider after pressing enter
    entry.bind("<Return>", update_slider_from_entry)

    # update entry with slider
    def update_entry(trait=trait, slider=slider, entry=entry, var=var):
        if var.get() == 1:  # only update if tickbox is checked
            entry.delete(0, 'end')
            entry.insert(0, f"{slider.get():.2f}")
        else:
            entry.delete(0, 'end')  # clear entry
            entry.configure(placeholder_text="CF (e.g. 0.50)")  # reset placeholder text
    
    # bind slider entry (after clicking/dragging the slider)
    slider.bind("<ButtonRelease-1>", lambda event, trait=trait, slider=slider, entry=entry, var=var: update_entry(trait, slider, entry, var))

# button setup
button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=20)

ctk.CTkButton(button_frame, text="Suggest Job", command=suggest_job).grid(row=0, column=0, padx=(5, 2.5), pady=5)
ctk.CTkButton(button_frame, text="Clear", command=clear_selection).grid(row=0, column=1, padx=(2.5, 2.5))
ctk.CTkButton(button_frame, text="?", command=show_help, width=30).grid(row=0, column=2, padx=(2.5, 5))

# show more clickable text
clickable_text = ctk.CTkLabel(window, text="", text_color="white", cursor="hand2", font=("Arial", 12, "underline"))
clickable_text.bind("<Button-1>", show_detailed_results)  # Bind left mouse button click to the function

result_label = ctk.CTkLabel(window, text="", font=("Arial", 12), justify="left")
result_label.pack(padx=10, pady=10)

# start gui loop
window.mainloop()
