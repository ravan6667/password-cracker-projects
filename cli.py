#!/usr/bin/env python3
"""Small CLI wrapper for password_checker.PasswordChecker.

Usage:
  - Interactive: `python cli.py` (prompts for passwords)
  - Single check: `python cli.py --password 'MyPass123!'`
"""
from __future__ import annotations
import argparse
import json
from password_checker import PasswordChecker


def run_interactive(checker: PasswordChecker) -> None:
    print("Password Strength Checker (type 'quit' to exit)")
    while True:
        pw = input("Enter a password: ")
        if not pw:
            continue
        if pw.lower() == "quit":
            break
        result = checker.check_password_strength(pw)
        print(json.dumps(result, indent=2))


def run_one(checker: PasswordChecker, password: str) -> None:
    result = checker.check_password_strength(password)
    print(json.dumps(result, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Password strength checker CLI")
    parser.add_argument("--password", "-p", help="Password to check (if omitted, runs interactive)")
    args = parser.parse_args()

    checker = PasswordChecker()
    if args.password:
        run_one(checker, args.password)
    else:
        run_interactive(checker)


if __name__ == "__main__":
    main()
