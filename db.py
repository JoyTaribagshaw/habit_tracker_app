import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_FILE = "my_habits.db"

def create_connection(db_file=DB_FILE):
    """Create a database connection to the SQLite database."""
    if db_file == ':memory:':
        logger.warning("You are using an in-memory database. Data will NOT persist after the app exits!")
        print("WARNING: You are using an in-memory database. Data will NOT persist after the app exits!")
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA foreign_keys = ON;")
        logger.info(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error connecting to database: {e}")
        return None

def create_tables(cursor):
    """
    Create the database tables with enhanced schema.
    Includes categories, difficulty levels, and additional tracking fields.
    """
    # Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            color_code TEXT DEFAULT '#3498db'
        );
    """)

    # Habits Table: Enhanced with additional fields
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            description TEXT,
            habit_period TEXT NOT NULL CHECK(habit_period IN ('daily', 'weekly')),
            creation_date TEXT NOT NULL,
            last_completed TEXT,
            streak INTEGER NOT NULL DEFAULT 0,
            best_streak INTEGER NOT NULL DEFAULT 0,
            habit_status TEXT NOT NULL CHECK(habit_status IN ('active', 'inactive')),
            difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
            category_id INTEGER,
            target_days INTEGER DEFAULT 7,
            reminder_time TEXT,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (category_id) REFERENCES Categories(id),
            UNIQUE(habit_name)
        );
    """)

    # Tasks Table: Enhanced with additional fields
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            task_name TEXT NOT NULL,
            periodicity TEXT NOT NULL CHECK(periodicity IN ('daily', 'weekly')),
            task_log_date TEXT NOT NULL,
            streak INTEGER NOT NULL DEFAULT 0,
            task_status TEXT NOT NULL CHECK(task_status IN ('completed', 'skipped', 'missed')),
            mood INTEGER CHECK(mood BETWEEN 1 AND 5),
            notes TEXT,
            completion_time INTEGER,
            FOREIGN KEY (habit_id) REFERENCES Habits(id) ON DELETE CASCADE,
            UNIQUE(habit_id, task_log_date)
        );
    """)

    # Achievements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT,
            points INTEGER DEFAULT 0,
            condition_type TEXT,
            condition_value INTEGER,
            is_secret BOOLEAN DEFAULT 0
        );
    """)

    # User_Achievements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS User_Achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            achievement_id INTEGER NOT NULL,
            earned_date TEXT NOT NULL,
            FOREIGN KEY (achievement_id) REFERENCES Achievements(id)
        );
    """)

    # Insert default categories if not exists
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name, description, color_code) VALUES (1, 'Health', 'Physical health and wellness', '#e74c3c')")
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name, description, color_code) VALUES (2, 'Productivity', 'Work and productivity habits', '#2ecc71')")
    cursor.execute("INSERT OR IGNORE INTO Categories (id, name, description, color_code) VALUES (3, 'Learning', 'Education and personal growth', '#f1c40f')")

    # Insert default achievements if not exists
    cursor.execute("INSERT OR IGNORE INTO Achievements (id, name, description, icon, points, condition_type, condition_value, is_secret) VALUES (1, 'First Habit', 'Create your first habit', '🌱', 10, 'create_habit', 1, 0)")
    cursor.execute("INSERT OR IGNORE INTO Achievements (id, name, description, icon, points, condition_type, condition_value, is_secret) VALUES (2, 'One Week Streak', 'Complete a habit for 7 days in a row', '🔥', 20, 'streak', 7, 0)")
    cursor.execute("INSERT OR IGNORE INTO Achievements (id, name, description, icon, points, condition_type, condition_value, is_secret) VALUES (3, 'Consistency', 'Complete any habit 30 times', '🏅', 30, 'completion', 30, 0)")
