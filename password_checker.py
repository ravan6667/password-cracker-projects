import re
import string
import math
from typing import Dict, List, Optional


class PasswordChecker:
    """Robust password checker suitable for small production deployments.

    Provides:
    - Shannon entropy estimate
    - Sequence and repeat detection
    - Common pattern blacklist check
    - Configurable policy (min length, required types)
    - JSON-friendly result dict (score, entropy, feedback)
    """

    COMMON_PATTERNS = [
        "123456",
        "password",
        "qwerty",
        "letmein",
        "admin",
        "welcome",
        "iloveyou",
        "12345",
        "11111",
        "abc123",
    ]

    def __init__(
        self,
        min_length: int = 8,
        strong_length: int = 12,
        require_mixed_case: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
        banned_passwords: Optional[List[str]] = None,
    ) -> None:
        self.min_length = min_length
        self.strong_length = strong_length
        self.require_mixed_case = require_mixed_case
        self.require_digits = require_digits
        self.require_special = require_special
        self.banned_passwords = set(p.lower() for p in (banned_passwords or []))
        self.lowercase = set(string.ascii_lowercase)
        self.uppercase = set(string.ascii_uppercase)
        self.digits = set(string.digits)
        self.special_chars = set(string.punctuation)

    def check_password_strength(self, password: str) -> Dict:
        if password is None:
            raise ValueError("password must be a string")

        feedback: List[str] = []
        score = 0

        length = len(password)
        entropy = self._shannon_entropy(password)

        # Length scoring
        if length >= self.min_length:
            score += 2
        else:
            feedback.append(f"Make your password at least {self.min_length} characters long.")

        if length >= self.strong_length:
            score += 1

        # Character variety
        has_lower = any(c in self.lowercase for c in password)
        has_upper = any(c in self.uppercase for c in password)
        has_digit = any(c in self.digits for c in password)
        has_special = any(c in self.special_chars for c in password)

        if has_lower and (not self.require_mixed_case or has_upper):
            score += 1
        else:
            feedback.append("Include both lowercase and uppercase characters.")

        if (not self.require_digits) or has_digit:
            score += 1
        else:
            feedback.append("Include some digits.")

        if (not self.require_special) or has_special:
            score += 1
        else:
            feedback.append("Include special characters (e.g. !@#$%).")

        # Entropy-based scoring
        if entropy >= 50:
            score += 3
        elif entropy >= 40:
            score += 2
        elif entropy >= 28:
            score += 1

        # Negative checks
        if self._has_common_patterns(password):
            feedback.append("Avoid common words or sequences (e.g. '123456', 'password').")
            score = max(0, score - 2)

        if self._has_repeated_chars(password):
            feedback.append("Avoid repeated characters or simple repeats (e.g. 'aaaa' or 'ababab').")
            score = max(0, score - 1)

        if password.lower() in self.banned_passwords:
            feedback.append("This password is banned/blacklisted.")
            score = 0

        # Map score to label
        max_score = 10
        if score <= 2:
            strength = "Very Weak"
        elif score <= 4:
            strength = "Weak"
        elif score <= 6:
            strength = "Fair"
        elif score <= 8:
            strength = "Good"
        else:
            strength = "Strong"

        guesses = 2 ** entropy if entropy < 160 else float("inf")
        guesses_per_second = 1e9
        crack_time_seconds = guesses / guesses_per_second if guesses != float("inf") else float("inf")

        return {
            "score": int(score),
            "max_score": max_score,
            "strength": strength,
            "feedback": feedback,
            "entropy_bits": round(entropy, 2),
            "estimated_crack_time_seconds": crack_time_seconds,
        }

    def _shannon_entropy(self, s: str) -> float:
        if not s:
            return 0.0
        freq = {}
        for ch in s:
            freq[ch] = freq.get(ch, 0) + 1
        entropy = 0.0
        length = len(s)
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy * length

    def _has_common_patterns(self, password: str) -> bool:
        pw = password.lower()
        for pat in self.COMMON_PATTERNS:
            if pat in pw:
                return True
        keyboard_rows = [
            "qwertyuiop",
            "asdfghjkl",
            "zxcvbnm",
            "1234567890",
        ]
        for row in keyboard_rows:
            for i in range(len(row) - 3):
                if row[i : i + 4] in pw:
                    return True
        return False

    def _has_repeated_chars(self, password: str) -> bool:
        if re.search(r"(.)\1{3,}", password):
            return True
        for l in range(1, 5):
            if len(password) >= l * 3:
                block = password[0:l]
                if block * (len(password) // l) == password:
                    return True
        return False


def main() -> None:
    checker = PasswordChecker()
    print("Password Strength Checker")
    print("=========================")
    while True:
        password = input("\nEnter a password to check (or 'quit' to exit): ")
        if password.lower() == "quit":
            break
        result = checker.check_password_strength(password)
        print(f"\nPassword Strength: {result['strength']}")
        print(f"Score: {result['score']}/{result['max_score']}")
        if result["feedback"]:
            print("Suggestions to improve:")
            for suggestion in result["feedback"]:
                print(f"  - {suggestion}")


if __name__ == "__main__":
    main()