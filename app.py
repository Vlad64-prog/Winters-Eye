from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database initialization
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Create facts table without user-related columns
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                topic TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/add_sample_facts')
def add_sample_facts():
    sample_facts = [
        ("Space is completely silent.", "Space Exploration"),
        ("A shrimp's heart is in its head.", "Ocean Life"),
        ("The Great Wall of China is not visible from space.", "Space Exploration"),
        ("Bananas are berries, but strawberries are not.", "Food Facts"),
        ("Octopuses have three hearts.", "Ocean Life"),
        ("The octopus has three hearts: one pumps blood to the body, while the other two pump blood to the gills.", "Ocean Life"),
        ("Sharks have been around longer than trees. They've existed for over 400 million years.", "Ocean Life"),
        ("The Great Pyramid of Giza was the tallest man-made structure in the world for over 3,800 years.", "Ancient Egypt"),
        ("Ancient Egyptians believed in over 2,000 gods and goddesses.", "Ancient Egypt"),
        ("The ancient Egyptians invented the 365-day calendar, which was based on the solar year.", "Ancient Egypt"),
        ("Cleopatra VII, the last Pharaoh of Egypt, was actually Greek, not Egyptian.", "Ancient Egypt"),
        ("Space is completely silent because sound waves need a medium like air to travel through, and space is a vacuum.", "Space Exploration"),
        ("There are more living creatures in the ocean than on land.", "Ocean Life"),
        ("Over 80% of the ocean is unexplored, making it one of the most mysterious places on Earth.", "Ocean Life")
    ]
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO facts (content, topic) VALUES (?, ?)', sample_facts)
        conn.commit()
    return "Sample facts added successfully!"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    topics = ['Space Exploration', 'Ocean Life', 'Ancient Egypt']  # Replace with your topic list
    return render_template('dashboard.html', topics=topics)

@app.route('/get_fact/<topic>')
def get_fact(topic):
    print(f"Fetching fact for topic: {topic}")  # Debug print
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT content FROM facts WHERE topic = ?', (topic,))
            facts = cursor.fetchall()

        if facts:
            random_fact = random.choice(facts)
            print(f"Found fact: {random_fact[0]}")  # Debug print
            return random_fact[0]  # Returning the fact content as plain text
        else:
            print("No facts found for this topic")  # Debug print
            return "No facts available for this topic."
    except Exception as e:
        print(f"Error: {e}")  # Print the exception if any occurs
        return "An error occurred while fetching the fact."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
