from password_checker import PasswordChecker


def test_various_passwords():
    checker = PasswordChecker()

    # Basic known cases: simplest and complex
    r1 = checker.check_password_strength("weak")
    assert r1["strength"] == "Very Weak"

    r2 = checker.check_password_strength("password123")
    assert r2["strength"] == "Very Weak"

    r6 = checker.check_password_strength("ComplexP@ssw0rd2023!")
    assert r6["strength"] == "Strong"

    # Middle cases should produce a label and numeric score
    for pw in ["MyPass", "MyPass123", "MyPass123!"]:
        res = checker.check_password_strength(pw)
        assert "score" in res
        assert "entropy_bits" in res
        assert res["strength"] in ["Very Weak", "Weak", "Fair", "Good", "Strong"]
