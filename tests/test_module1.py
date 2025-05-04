from jobsuggestion import calculate_cf, rules

# define test input
test_skills = [
    ('programming', 1.0), 
    ('problem solving', 0.9), 
    ('teamwork', 0.8), 
    ('hands-on work', 0.7)
]

expected_cfs = {
    'Mechatronics Engineer': 0,
    'Civil Engineer': -0.32,
    'Software Engineer': 0.985,
    'Mechanical Engineer': 0.56,
    'Electrical Engineer': 0,
    'Chemical Engineer': 0
}

# run test
print("Testing final CF values for each job...")
for job in rules:
    calculated_cf = calculate_cf(job, test_skills)
    expected_cf = expected_cfs.get(job, 0)
    passed = abs(calculated_cf - expected_cf) < 0.001  # allow minor rounding error
    print(f"{job}: Expected = {expected_cf}, Calculated = {calculated_cf} -> {'PASS' if passed else 'FAIL'}")
