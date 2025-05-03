# Rule-Based Expert System using Certainty Factor

## Overview
This project is a Job Suggestion Expert System built using Python and the `customtkinter` library. The system suggests suitable job roles based on user-defined skills and their confidence levels. It uses a set of predefined rules and conditions to evaluate the best job matches (currently only for engineering jobs).

<div style="text-align: center;">
    <img src="images/screenshot.png" alt="Job Suggestion System Screenshot" width="300"/>
</div>

## Usage
- **Select Skills**: Check the boxes next to the skills.
- **Set Confidence Levels**: Use the sliders or input fields to set the confidence level for each selected skill (from 0 to 1).
- **Suggest Job**: Click the "Suggest Job" button to get the most suitable job based on the input.
- **View Detailed Results**: Click on the "Show More" link to see detailed results for all the job suggestions.
- **Clear Selections**: Use the "Clear" button to reset the selections

## Code Explanation
- The system defines a set of rules for various job roles, each associated with specific skills and their corresponding certainty factors. These rules are stored in a dictionary called `rules`. Additionally, conditions for certain jobs (like "Mechatronics Engineer") are defined to specify required skills that must be met ('and/or' statements).
- The system uses certainty factors to evaluate how well a user's skills match the requirements for each job. The `combine_cf` function calculates the combined certainty factor for a job based on the user's skills and their confidence levels. It applies a formula to adjust the certainty factors based on the rules defined for each job.
- The `calculate_cf` function determines the certainty factor for each job based on user input. It checks for any specific conditions (like "and" and "or" requirements) and calculates the certainty factors accordingly. If conditions are met, the certainty factors are combined using the `combine_cf` function.
- The application uses the `customtkinter` library to create a user-friendly graphical interface. Users can select their skills, adjust confidence levels using sliders, and receive job suggestions based on their input. The interface includes buttons for suggesting jobs, clearing selections, and accessing help information.
- When a user requests job suggestions, the system displays the most suitable job along with its certainty factor. Users can also view detailed results for all job suggestions, which include the certainty factors for each job.
- The application includes error handling to ensure that users provide valid input. If no skills are selected, an error message is displayed in a new window, prompting the user to make a selection.

## Acknowledgments
- Thanks to the creators of customtkinter for providing a great library for building custom GUI applications in Python.
- Special thanks to ChatGPT for the documentation, explanations, and code writing.
