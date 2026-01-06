"""
SQLite Database Basics in Python

This module demonstrates fundamental database operations using SQLite,
which comes built-in with Python. Covers CRUD operations, queries,
transactions, and best practices.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager
import json


@contextmanager
def get_db_connection(db_path: str = "example.db"):
    """Context manager for database connections."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()


def create_tables():
    """Create example database tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')

        # Create posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                user_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')

        # Create post_categories junction table (many-to-many)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_categories (
                post_id INTEGER,
                category_id INTEGER,
                PRIMARY KEY (post_id, category_id),
                FOREIGN KEY (post_id) REFERENCES posts (id),
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')

        conn.commit()
        print("✓ Database tables created successfully")


def insert_sample_data():
    """Insert sample data into the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Insert users
        users_data = [
            ("alice_smith", "alice@example.com", 28),
            ("bob_johnson", "bob@example.com", 34),
            ("charlie_brown", "charlie@example.com", 22),
            ("diana_prince", "diana@example.com", 31),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO users (username, email, age) VALUES (?, ?, ?)",
            users_data
        )

        # Insert categories
        categories_data = [
            ("Technology", "Posts about technology and programming"),
            ("Science", "Scientific discoveries and research"),
            ("Travel", "Travel experiences and tips"),
            ("Food", "Recipes and culinary adventures"),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)",
            categories_data
        )

        # Insert posts
        posts_data = [
            ("Python Best Practices", "Learn about writing clean Python code...", 1),
            ("Machine Learning Basics", "Introduction to ML concepts and algorithms...", 2),
            ("Exploring Japan", "My journey through Japan's beautiful landscapes...", 3),
            ("Homemade Pizza Recipe", "The perfect pizza dough and toppings guide...", 4),
            ("Web Development Trends", "Latest trends in web development for 2024...", 1),
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO posts (title, content, user_id) VALUES (?, ?, ?)",
            posts_data
        )

        # Insert post-category relationships
        post_categories_data = [
            (1, 1),  # Python post -> Technology
            (2, 1),  # ML post -> Technology
            (2, 2),  # ML post -> Science
            (3, 3),  # Travel post -> Travel
            (4, 4),  # Food post -> Food
            (5, 1),  # Web dev post -> Technology
        ]

        cursor.executemany(
            "INSERT OR IGNORE INTO post_categories (post_id, category_id) VALUES (?, ?)",
            post_categories_data
        )

        conn.commit()
        print("✓ Sample data inserted successfully")


def basic_queries():
    """Demonstrate basic database queries."""
    print("\n=== Basic Queries ===")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Select all users
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        print(f"Total users: {len(users)}")
        for user in users:
            print(f"  {user['username']} ({user['email']}) - Age: {user['age']}")

        # Count posts by user
        cursor.execute("""
            SELECT users.username, COUNT(posts.id) as post_count
            FROM users
            LEFT JOIN posts ON users.id = posts.user_id
            GROUP BY users.id, users.username
            ORDER BY post_count DESC
        """)

        print("\nPosts by user:")
        for row in cursor.fetchall():
            print(f"  {row['username']}: {row['post_count']} posts")

        # Find posts with their categories
        cursor.execute("""
            SELECT posts.title, users.username, GROUP_CONCAT(categories.name) as categories
            FROM posts
            JOIN users ON posts.user_id = users.id
            LEFT JOIN post_categories ON posts.id = post_categories.post_id
            LEFT JOIN categories ON post_categories.category_id = categories.id
            GROUP BY posts.id, posts.title, users.username
        """)

        print("\nPosts with categories:")
        for row in cursor.fetchall():
            categories = row['categories'] if row['categories'] else "No categories"
            print(f"  '{row['title']}' by {row['username']} - Categories: {categories}")


def parameterized_queries():
    """Demonstrate parameterized queries for security."""
    print("\n=== Parameterized Queries ===")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Safe parameterized query
        username = "alice_smith"
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            print(f"Found user: {user['username']} - {user['email']}")
        else:
            print("User not found")

        # Multiple parameters
        min_age = 25
        is_active = True
        cursor.execute(
            "SELECT username, age FROM users WHERE age >= ? AND is_active = ?",
            (min_age, is_active)
        )

        print(f"\nUsers aged {min_age}+:")
        for row in cursor.fetchall():
            print(f"  {row['username']}: {row['age']} years old")


def transactions_example():
    """Demonstrate database transactions."""
    print("\n=== Database Transactions ===")

    with get_db_connection() as conn:
        try:
            # Start transaction
            conn.execute("BEGIN TRANSACTION")

            cursor = conn.cursor()

            # Insert a new user
            cursor.execute(
                "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
                ("transaction_user", "transaction@example.com", 26)
            )

            # Get the new user's ID
            user_id = cursor.lastrowid

            # Insert a post for this user
            cursor.execute(
                "INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)",
                ("Transaction Test Post", "This post was created in a transaction", user_id)
            )

            # Simulate an error (uncomment to test rollback)
            # raise Exception("Simulated error - transaction should rollback")

            # Commit transaction
            conn.commit()
            print("✓ Transaction committed successfully")

        except Exception as e:
            # Rollback on error
            conn.rollback()
            print(f"✗ Transaction rolled back due to error: {e}")


def update_and_delete():
    """Demonstrate UPDATE and DELETE operations."""
    print("\n=== Update and Delete Operations ===")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Update user age
        cursor.execute(
            "UPDATE users SET age = age + 1 WHERE username = ?",
            ("alice_smith",)
        )
        print(f"✓ Updated {cursor.rowcount} user(s)")

        # Delete inactive users (none in our sample, but shows the pattern)
        cursor.execute("DELETE FROM users WHERE is_active = 0")
        print(f"✓ Deleted {cursor.rowcount} inactive user(s)")

        # Soft delete by updating is_active flag
        cursor.execute(
            "UPDATE users SET is_active = 0 WHERE username = ?",
            ("transaction_user",)
        )
        print(f"✓ Soft deleted {cursor.rowcount} user(s)")

        conn.commit()


def advanced_queries():
    """Demonstrate advanced SQL queries."""
    print("\n=== Advanced Queries ===")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Complex join with aggregation
        cursor.execute("""
            SELECT
                categories.name as category,
                COUNT(posts.id) as post_count,
                AVG(users.age) as avg_author_age
            FROM categories
            LEFT JOIN post_categories ON categories.id = post_categories.category_id
            LEFT JOIN posts ON post_categories.post_id = posts.id
            LEFT JOIN users ON posts.user_id = users.id
            GROUP BY categories.id, categories.name
            ORDER BY post_count DESC
        """)

        print("Category statistics:")
        for row in cursor.fetchall():
            avg_age = row['avg_author_age']
            if avg_age:
                print(f"  {row['category']}: {row['post_count']} posts, avg author age: {avg_age:.1f}")
            else:
                print(f"  {row['category']}: {row['post_count']} posts, no authors")

        # Subquery example
        cursor.execute("""
            SELECT username, email
            FROM users
            WHERE id IN (
                SELECT DISTINCT user_id
                FROM posts
                WHERE user_id IS NOT NULL
            )
        """)

        print("\nUsers who have written posts:")
        for row in cursor.fetchall():
            print(f"  {row['username']} ({row['email']})")


def export_to_json():
    """Demonstrate exporting database data to JSON."""
    print("\n=== Export to JSON ===")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Export users with their posts
        cursor.execute("""
            SELECT
                users.username,
                users.email,
                users.age,
                json_group_array(
                    json_object(
                        'id', posts.id,
                        'title', posts.title,
                        'created_at', posts.created_at
                    )
                ) as posts
            FROM users
            LEFT JOIN posts ON users.id = posts.user_id
            GROUP BY users.id, users.username, users.email, users.age
        """)

        users_data = []
        for row in cursor.fetchall():
            user_dict = dict(row)
            # Parse the JSON string back to Python objects
            user_dict['posts'] = json.loads(user_dict['posts']) if user_dict['posts'] != '[null]' else []
            users_data.append(user_dict)

        # Save to JSON file
        with open('users_export.json', 'w') as f:
            json.dump(users_data, f, indent=2, default=str)

        print("✓ Database exported to users_export.json")
        print(f"Exported {len(users_data)} users")


def cleanup_database():
    """Clean up the example database."""
    if os.path.exists("example.db"):
        os.remove("example.db")
        print("✓ Database file cleaned up")

    if os.path.exists("users_export.json"):
        os.remove("users_export.json")
        print("✓ Export file cleaned up")


def main():
    """Run all database examples."""
    print("SQLite Database Examples")
    print("=" * 40)

    try:
        # Clean up any existing database
        cleanup_database()

        # Create and populate database
        create_tables()
        insert_sample_data()

        # Demonstrate various operations
        basic_queries()
        parameterized_queries()
        transactions_example()
        update_and_delete()
        advanced_queries()
        export_to_json()

        print("\n✓ All database examples completed successfully!")

    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        # Clean up
        cleanup_database()


if __name__ == "__main__":
    main()