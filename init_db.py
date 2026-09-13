import sqlite3

def init_db():
    connection = sqlite3.connect('tracker.db')
    cursor = connection.cursor()

    with open('schema.sql', 'r') as f:
        cursor.executescript(f.read())

    cursor.execute("SELECT COUNT(*) FROM problems")
    if cursor.fetchone()[0] == 0:
        sample_problems = [
    (
        'Arrays & Hashing', 
        'Two Sum', 
        'Easy', 
        'https://takeuforward.org/data-structure/two-sum-check-if-a-pair-with-given-sum-exists-in-array', 
        'https://leetcode.com/problems/two-sum/'
    ),
    (
        'Arrays & Hashing', 
        'Best Time to Buy and Sell Stock', 
        'Easy', 
        'https://takeuforward.org/data-structure/stock-buy-and-sell', 
        'https://leetcode.com/problems/best-time-to-buy-and-sell-stock/'
    ),
    (
        'Linked List', 
        'Reverse Linked List', 
        'Easy', 
        'https://takeuforward.org/data-structure/reverse-a-linked-list', 
        'https://leetcode.com/problems/reverse-linked-list/'
    )
]
    cursor.executemany("""
            INSERT INTO problems (topic, title, difficulty, theory_url, practice_url)
            VALUES (?, ?, ?, ?, ?)
        """, sample_problems)


    connection.commit()
    print("Database seeded with sample problems!")

    connection.close()
    print("Database initialization complete.")


if __name__ == '__main__':
    init_db()

