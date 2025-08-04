import sqlite3

DB_FILE = "habit_tracker.db"

def create_connection(db_file=DB_FILE):
    """
    Establish a connection to the SQLite database.
    Enables foreign key constraints for referential integrity.
    Accepts custom db_file for test or in-memory usage.
    """
    conn = sqlite3.connect(db_file)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enforce FK constraints
    return conn

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
            completion_time INTEGER,  # Time taken in minutes
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
    
    # Create default categories if they don't exist
    default_categories = [
        ('Health & Fitness', 'Physical activities and wellness', '#e74c3c'),
        ('Productivity', 'Work and personal productivity', '#2ecc71'),
        ('Learning', 'Educational and skill development', '#9b59b6'),
        ('Mindfulness', 'Mental health and meditation', '#3498db'),
        ('Personal', 'Personal development and habits', '#f1c40f')
    ]
    
    cursor.executemany(
        """
        INSERT OR IGNORE INTO Categories (name, description, color_code)
        VALUES (?, ?, ?)
        """,
        default_categories
    )
    
    # Create default achievements
    default_achievements = [
        ('First Step', 'Complete your first habit', '👣', 10, 'total_completions', 1, 0),
        ('Streak Starter', 'Maintain a 7-day streak', '🔥', 25, 'streak', 7, 0),
        ('Habit Master', 'Complete 30 days of any habit', '🏆', 50, 'total_days', 30, 0),
        ('Early Bird', 'Complete a habit before 8 AM', '🌅', 15, 'early_completion', 1, 1),
        ('Weekend Warrior', 'Complete a habit on both weekend days', '💪', 20, 'weekend_streak', 2, 1)
    ]
    
    cursor.executemany(
        """
        INSERT OR IGNORE INTO Achievements (name, description, icon, points, condition_type, condition_value, is_secret)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        default_achievements
    )
