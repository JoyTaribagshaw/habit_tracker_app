import pytest
from datetime import datetime
import logging
from models import Habit, Task, Difficulty, HabitStatus, TaskStatus
from db import create_connection, create_tables
from habit_tracker import MyHabits

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def test_db():
    conn = create_connection(":memory:")
    cursor = conn.cursor()
    create_tables(cursor)
    conn.commit()
    yield conn
    conn.close()

@pytest.fixture
def my_habits(test_db):
    return MyHabits(test_db.cursor(), test_db)

def test_add_habit(my_habits, test_db):
    my_habits.add_habit("Test Reading", 1)
    cur = test_db.cursor()
    cur.execute("SELECT * FROM Habits WHERE habit_name = ?", ("Test Reading",))
    assert cur.fetchone() is not None

def test_deactivate_habit(my_habits, test_db):
    cur = test_db.cursor()
    cur.execute("SELECT id FROM Habits WHERE habit_name = ?", ("Test Reading",))
    habit_id = cur.fetchone()[0]
    my_habits.deactivate_habit(habit_id)
    cur.execute("SELECT habit_status FROM Habits WHERE id = ?", (habit_id,))
    assert cur.fetchone()[0] == "inactive"

def test_mark_task_completed(my_habits, test_db):
    my_habits.add_habit("Test Exercise", 1)
    cur = test_db.cursor()
    cur.execute("SELECT id FROM Habits WHERE habit_name = ?", ("Test Exercise",))
    habit_id = cur.fetchone()[0]
    my_habits.mark_task_completed(habit_id)
    cur.execute("SELECT * FROM Tasks WHERE habit_id = ?", (habit_id,))
    assert cur.fetchone() is not None

# --- Analytics Tests ---
from analytics import get_most_missed_habits, get_habit_completion_correlation, suggest_habits_to_focus

def seed_analytics_data(cursor):
    # Add habits
    cursor.execute("INSERT INTO Habits (habit_name, habit_period, creation_date, habit_status, streak) VALUES (?, ?, ?, ?, ?)", ("A", "daily", "2025-08-01", "active", 1))
    cursor.execute("INSERT INTO Habits (habit_name, habit_period, creation_date, habit_status, streak) VALUES (?, ?, ?, ?, ?)", ("B", "daily", "2025-08-01", "active", 2))
    cursor.execute("INSERT INTO Habits (habit_name, habit_period, creation_date, habit_status, streak) VALUES (?, ?, ?, ?, ?)", ("C", "daily", "2025-08-01", "active", 0))
    # Get IDs
    cursor.execute("SELECT id FROM Habits WHERE habit_name = 'A'"); id_a = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM Habits WHERE habit_name = 'B'"); id_b = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM Habits WHERE habit_name = 'C'"); id_c = cursor.fetchone()[0]
    # Add tasks
    # A missed twice, B missed once, C missed three times
    cursor.executemany("INSERT INTO Tasks (habit_id, task_name, periodicity, task_log_date, streak, task_status) VALUES (?, ?, ?, ?, ?, ?)", [
        (id_a, "A", "daily", "2025-08-02", 1, "missed"),
        (id_a, "A", "daily", "2025-08-03", 1, "missed"),
        (id_b, "B", "daily", "2025-08-02", 1, "missed"),
        (id_c, "C", "daily", "2025-08-02", 1, "missed"),
        (id_c, "C", "daily", "2025-08-03", 1, "missed"),
        (id_c, "C", "daily", "2025-08-04", 1, "missed"),
        # Completions for correlation
        (id_a, "A", "daily", "2025-08-05", 1, "completed"),
        (id_b, "B", "daily", "2025-08-05", 1, "completed"),
        (id_a, "A", "daily", "2025-08-06", 1, "completed"),
        (id_c, "C", "daily", "2025-08-06", 1, "completed"),
    ])


def test_get_most_missed_habits(test_db):
    cur = test_db.cursor()
    seed_analytics_data(cur)
    result = get_most_missed_habits(cur, top_n=2)
    assert result[0][1] == "C"  # Most missed
    assert result[1][1] == "A" or result[1][1] == "B"

def test_get_habit_completion_correlation(test_db):
    cur = test_db.cursor()
    # Data already seeded in previous test
    result = get_habit_completion_correlation(cur)
    assert isinstance(result, dict)
    assert any(isinstance(k, tuple) and isinstance(v, float) for k, v in result.items())

def test_suggest_habits_to_focus(test_db):
    cur = test_db.cursor()
    # Data already seeded in previous test
    suggestions = suggest_habits_to_focus(cur)
    assert "C" in suggestions  # Lowest streak
