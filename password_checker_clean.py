import re
import string

class PasswordChecker:
    # A class to check the strength of passwords based on various criteria:
    # - Length
    # - Complexity
    # - Types of characters used
    
    def __init__(self):
        self.lowercase = set(string.ascii_lowercase)
        self.uppercase = set(string.ascii_uppercase)
        self.digits = set(string.digits)
        self.special_chars = set(string.punctuation)
    
    def check_password_strength(self, password):
        # Check the strength of a password and return a score and feedback
        # Args:
        #     password (str): The password to check
        # Returns:
        #     dict: A dictionary containing score, strength level, and feedback
        score = 0
        feedback = []
        
        # Check length
        length = len(password)
        if length < 6:
            feedback.append("Password is too short. Use at least 8 characters.")
        elif length >= 8:
            score += 1
        if length >= 12:
            score += 1
        
        # Check for character variety
        password_chars = set(password)
        
        # Lowercase letters
        if password_chars & self.lowercase:
            score += 1
        else:
            feedback.append("Add lowercase letters.")
        
        # Uppercase letters
        if password_chars & self.uppercase:
            score += 1
        else:
            feedback.append("Add uppercase letters.")
        
        # Digits
        if password_chars & self.digits:
            score += 1
        else:
            feedback.append("Add numbers.")
        
        # Special characters
        if password_chars & self.special_chars:
            score += 1
        else:
            feedback.append("Add special characters (!@#\$%^&*(),./;: etc.).")
        
        # Check for common patterns
        if self._has_common_patterns(password):
            score -= 1
            feedback.append("Avoid common patterns like '123456', 'qwerty', etc.")
        
        # Determine strength level
        if score <= 2:
            strength = "Very Weak"
        elif score <= 3:
            strength = "Weak"
        elif score <= 4:
            strength = "Fair"
        elif score <= 5:
            strength = "Good"
        else:
            strength = "Strong"
        
        return {
            "score": score,
            "max_score": 6,
            "strength": strength,
            "feedback": feedback
        }
    
    def _has_common_patterns(self, password):
        # Check if password contains common weak patterns
        # Args:
        #     password (str): The password to check
        # Returns:
        #     bool: True if common patterns are found, False otherwise
        common_patterns = [
            r'123456',
            r'password',
            r'qwerty',
            r'abc',
            r'000',
            r'111',
            r'222',
            r'333',
            r'444',
            r'555',
            r'666',
            r'777',
            r'888',
            r'999',
            r'0000',
            r'1111',
            r'2222',
            r'3333',
            r'4444',
            r'5555',
            r'6666',
            r'7777',
            r'8888',
            r'9999',
        ]
        
        password_lower = password.lower()
        for pattern in common_patterns:
            if pattern in password_lower:
                return True
        
        return False


def main():
    checker = PasswordChecker()
    
    print("Password Strength Checker")
    print("=========================")
    
    while True:
        password = input("\n Enter a password to check (or 'quit' to exit): ")
        
        if password.lower() == 'quit':
            break
        
        result = checker.check_password_strength(password)
        
        print(f"\n Password Strength: {result['strength']}")
        print(f"Score: {result['score']}/{result['max_score']}")
        
        if result['feedback']:
            print("Suggestions to improve:")
            for suggestion in result['feedback']:
                print(f"  - {suggestion}")


if __name__ == "__main__":
    main()