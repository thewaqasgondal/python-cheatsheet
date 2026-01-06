"""
Regular Expressions Examples in Python

This module demonstrates comprehensive usage of Python's 're' module for
pattern matching, text processing, and data validation.
"""

import re
from typing import List, Optional, Match, Pattern
import json


def basic_pattern_matching():
    """Demonstrate basic regex pattern matching."""
    print("=== Basic Pattern Matching ===")

    text = "Hello, my email is user@example.com and my phone is 123-456-7890."

    # Simple pattern matching
    patterns = [
        (r"email", "Find 'email'"),
        (r"\d{3}-\d{3}-\d{4}", "Find phone number pattern"),
        (r"\w+@\w+\.\w+", "Find email pattern"),
        (r"[A-Z][a-z]+", "Find capitalized words"),
    ]

    for pattern, description in patterns:
        matches = re.findall(pattern, text)
        print(f"{description}: {matches}")

    print()


def compiling_patterns():
    """Demonstrate compiling regex patterns for better performance."""
    print("=== Compiling Patterns ===")

    # Compile patterns for reuse
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
    url_pattern = re.compile(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)')

    test_text = """
    Contact us at support@company.com or call (555) 123-4567.
    Visit our website at https://www.example.com/page?param=value#section
    Or email john.doe+tag@gmail.com for more info.
    """

    print("Text to analyze:")
    print(test_text.strip())
    print()

    emails = email_pattern.findall(test_text)
    phones = phone_pattern.findall(test_text)
    urls = url_pattern.findall(test_text)

    print(f"Emails found: {emails}")
    print(f"Phones found: {phones}")
    print(f"URLs found: {urls}")

    print()


def search_vs_match_vs_findall():
    """Demonstrate different regex methods."""
    print("=== Search vs Match vs Findall ===")

    text = "The year is 2024, and Python 3.9 was released in 2020."

    # re.match() - Only matches at the beginning
    match_result = re.match(r'\d{4}', text)
    print(f"re.match(r'\\d{{4}}', text): {match_result.group() if match_result else None}")

    # re.search() - Finds first occurrence anywhere
    search_result = re.search(r'\d{4}', text)
    print(f"re.search(r'\\d{{4}}', text): {search_result.group() if search_result else None}")

    # re.findall() - Finds all occurrences
    findall_result = re.findall(r'\d{4}', text)
    print(f"re.findall(r'\\d{{4}}', text): {findall_result}")

    # re.finditer() - Returns iterator of match objects
    finditer_results = [match.group() for match in re.finditer(r'\d{4}', text)]
    print(f"re.finditer(r'\\d{{4}}', text): {finditer_results}")

    print()


def groups_and_capturing():
    """Demonstrate capturing groups in regex."""
    print("=== Groups and Capturing ===")

    # Extracting date components
    date_text = "Meeting on 2024-01-15 and another on 2023-12-25."

    # Capture groups for year, month, day
    date_pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    matches = date_pattern.findall(date_text)

    print(f"Date extraction: {matches}")

    # Named groups
    named_date_pattern = re.compile(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})')
    for match in named_date_pattern.finditer(date_text):
        print(f"Named groups: Year={match.group('year')}, Month={match.group('month')}, Day={match.group('day')}")

    # Extracting name and domain from email
    email_text = "Contact john.doe@example.com or jane.smith@company.org"
    email_pattern = re.compile(r'(\w+(?:\.\w+)*)@(\w+(?:\.\w+)*)')

    for match in email_pattern.finditer(email_text):
        username, domain = match.groups()
        print(f"Email: {username}@{domain}")

    print()


def substitution_and_replacement():
    """Demonstrate regex substitution."""
    print("=== Substitution and Replacement ===")

    text = "Contact us at phone: 123-456-7890 or email: user@example.com"

    # Simple replacement
    censored = re.sub(r'\d{3}-\d{3}-\d{4}', 'XXX-XXX-XXXX', text)
    print(f"Censored phone: {censored}")

    # Replacement with function
    def mask_email(match: Match[str]) -> str:
        email = match.group(0)
        username, domain = email.split('@')
        masked_username = username[0] + '*' * (len(username) - 2) + username[-1] if len(username) > 2 else username
        return f"{masked_username}@{domain}"

    masked_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', mask_email, text)
    print(f"Masked email: {masked_text}")

    # Replace multiple spaces with single space
    messy_text = "This    text   has    irregular   spacing."
    cleaned = re.sub(r'\s+', ' ', messy_text)
    print(f"Cleaned spacing: {cleaned}")

    print()


def validation_examples():
    """Demonstrate using regex for data validation."""
    print("=== Data Validation ===")

    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def validate_phone(phone: str) -> bool:
        """Validate US phone number formats."""
        pattern = r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$'
        return bool(re.match(pattern, phone))

    def validate_credit_card(card_number: str) -> bool:
        """Basic credit card number validation (format only)."""
        # Remove spaces and dashes
        cleaned = re.sub(r'[\s-]', '', card_number)
        # Check if it's 13-19 digits
        return bool(re.match(r'^\d{13,19}$', cleaned))

    # Test validation
    test_emails = ["user@example.com", "invalid-email", "user@.com", "user@domain.co.uk"]
    test_phones = ["123-456-7890", "(123) 456-7890", "123.456.7890", "invalid"]
    test_cards = ["4111-1111-1111-1111", "4111111111111111", "123", "abcd"]

    print("Email validation:")
    for email in test_emails:
        print(f"  {email}: {'✓' if validate_email(email) else '✗'}")

    print("\nPhone validation:")
    for phone in test_phones:
        print(f"  {phone}: {'✓' if validate_phone(phone) else '✗'}")

    print("\nCredit card format validation:")
    for card in test_cards:
        print(f"  {card}: {'✓' if validate_credit_card(card) else '✗'}")

    print()


def advanced_patterns():
    """Demonstrate advanced regex patterns."""
    print("=== Advanced Patterns ===")

    # Lookahead and lookbehind
    text = "The quick brown fox jumps over the lazy dog."

    # Positive lookahead - find 'fox' only if followed by 'jumps'
    fox_ahead = re.findall(r'fox(?=\sjumps)', text)
    print(f"Positive lookahead: {fox_ahead}")

    # Negative lookahead - find 'fox' not followed by 'runs'
    fox_not_runs = re.findall(r'fox(?!sruns)', text)
    print(f"Negative lookahead: {fox_not_runs}")

    # Positive lookbehind - find 'brown' only if preceded by 'quick'
    brown_behind = re.findall(r'(?<=quick\s)brown', text)
    print(f"Positive lookbehind: {brown_behind}")

    # Non-capturing groups
    colors = "red, green, blue, yellow"
    # Extract colors without capturing the comma and space
    color_list = re.findall(r'(?:^|,\s)(\w+)', colors)
    print(f"Non-capturing groups: {color_list}")

    # Atomic groups and possessive quantifiers
    # (More advanced - prevents backtracking for performance)

    print()


def log_parsing_example():
    """Demonstrate parsing log files with regex."""
    print("=== Log Parsing Example ===")

    # Sample log entries
    logs = [
        "2024-01-15 10:30:45 INFO User login: alice",
        "2024-01-15 10:31:12 ERROR Database connection failed",
        "2024-01-15 10:32:01 WARNING High memory usage: 85%",
        "2024-01-15 10:32:30 INFO User logout: bob",
    ]

    # Pattern to parse log entries
    log_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})\s(\w+)\s(.+)')

    parsed_logs = []
    for log in logs:
        match = log_pattern.match(log)
        if match:
            date, time, level, message = match.groups()
            parsed_logs.append({
                'date': date,
                'time': time,
                'level': level,
                'message': message
            })

    print("Parsed log entries:")
    for log in parsed_logs:
        print(f"  {log['date']} {log['time']} [{log['level']}] {log['message']}")

    # Count log levels
    levels = [log['level'] for log in parsed_logs]
    level_counts = {level: levels.count(level) for level in set(levels)}
    print(f"\nLog level counts: {level_counts}")

    print()


def html_tag_extraction():
    """Demonstrate extracting data from HTML-like text."""
    print("=== HTML Tag Extraction ===")

    html = """
    <div class="user">
        <h2>John Doe</h2>
        <p>Email: john@example.com</p>
        <span>Age: 30</span>
    </div>
    <div class="user">
        <h2>Jane Smith</h2>
        <p>Email: jane@company.org</p>
        <span>Age: 25</span>
    </div>
    """

    # Extract names
    names = re.findall(r'<h2>([^<]+)</h2>', html)
    print(f"Names: {names}")

    # Extract emails
    emails = re.findall(r'Email:\s*([^<\n]+)', html)
    print(f"Emails: {emails}")

    # Extract ages
    ages = re.findall(r'Age:\s*(\d+)', html)
    print(f"Ages: {ages}")

    # Extract all user data
    user_pattern = re.compile(r'<div class="user">(.*?)</div>', re.DOTALL)
    users = user_pattern.findall(html)

    print("\nExtracted user data:")
    for i, user_html in enumerate(users, 1):
        user_name = re.search(r'<h2>([^<]+)</h2>', user_html)
        user_email = re.search(r'Email:\s*([^<\n]+)', user_html)
        user_age = re.search(r'Age:\s*(\d+)', user_html)

        print(f"User {i}:")
        print(f"  Name: {user_name.group(1) if user_name else 'N/A'}")
        print(f"  Email: {user_email.group(1) if user_email else 'N/A'}")
        print(f"  Age: {user_age.group(1) if user_age else 'N/A'}")

    print()


def main():
    """Run all regex demonstrations."""
    print("Python Regular Expressions Examples")
    print("=" * 40)
    print()

    basic_pattern_matching()
    compiling_patterns()
    search_vs_match_vs_findall()
    groups_and_capturing()
    substitution_and_replacement()
    validation_examples()
    advanced_patterns()
    log_parsing_example()
    html_tag_extraction()


if __name__ == "__main__":
    main()