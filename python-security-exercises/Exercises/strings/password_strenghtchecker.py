def password_strength(password):
    checks = {
        'length' : len(password) >= 8,
        'uppercase' : any(c.isupper() for c in password),
        'lowercase' : any(c.islower() for c in password),
        'digit' : any(c.isdigit() for c in password),
        'special' : any(not c.isalnum() for c in password),

    }
    score = sum(checks.values()) #0-5
    feedback = "Weak" if score < 3 else "Medium" if score < 5 else "Strong"
    return f"Score: {score}/5 - {feedback}"

print(password_strength("Azkat1246@"))
