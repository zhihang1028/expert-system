# Rule-Based Expert System using Certainty Factor

## Overview
This project uses a rule-based expert system that diagnoses potential health conditions based on user-reported symptoms. The system uses certainty factors to evaluate the likelihood of various conditions. Thus, providing users with a diagnosis based on their input.

## Features
- Rule-based diagnosis using certainty factors.
- Input for symptoms.
- Calculates and displays the most likely condition based on user symptoms.

## How It Works
The system defines a set of rules for different diseases, each associated with specific symptoms and their corresponding certainty factors. Users can input their symptoms, and the system calculates the certainty factor for each potential diagnosis.

## Code Explanation
1. **Define Rules**: The system defines rules for various conditions (e.g., Cold, Flu, Allergy) along with their associated symptoms and certainty factors.
2. **Collect User Symptoms**: The program prompts the user to enter symptoms one by one until they type 'done'.
3. **Calculate Certainty Factor**: The `calculate_cf` function computes the certainty factor for each disease based on the user's symptoms.
4. **Diagnose**: The system evaluates all diseases and sorts them based on their certainty factors.
5. **Display Results**: The program displays the diagnosis results and suggests the most likely condition.

## Usage
- Run the program and enter your symptoms one by one.
- Type 'done' when you have finished entering symptoms.
- The system will calculate and display the most likely condition based on the input symptoms.
- Example:
```
Enter your symptoms one by one. Type 'done' when finished.
Symptom: cough
Symptom: sneezing
Symptom: done

Diagnosis Results:
Flu: CF = 0.5
Cold: CF = 0.6
Allergy: CF = 0.0

Most likely condition: Cold with confidence 0.6
```

## Acknowledgments
- The concept of certainty factors and rule-based systems from artificial intelligence literature.
- ChatGPT for assistance in project documentation and code explanations.
