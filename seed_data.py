import logging
from models import Habit, Task, Difficulty, HabitStatus, TaskStatus
from db import create_connection
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Establish DB connection
connection = create_connection()
cursor = connection.cursor()

# Fixed 30-day data range ending on June 16, 2025
end_date = datetime.strptime("2025-06-16", "%Y-%m-%d").date()
start_date = end_date - timedelta(days=29)

# Habits
daily_habits = ["Drink Water", "Exercise", "Journal"]
weekly_habits = ["Call Family", "Clean Room"]

# Insert habits if they don't exist
for name in daily_habits:
    cursor.execute("""
        INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM Habits WHERE LOWER(habit_name) = LOWER(?) AND habit_period = ?
        )
    """, (name, "daily", start_date.strftime("%Y-%m-%d"), None, 0, "active", name, "daily"))

for name in weekly_habits:
    cursor.execute("""
        INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status)
        SELECT ?, ?, ?, ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM Habits WHERE LOWER(habit_name) = LOWER(?) AND habit_period = ?
        )
    """, (name, "weekly", start_date.strftime("%Y-%m-%d"), None, 0, "active", name, "weekly"))

# Fetch habit IDs
cursor.execute("SELECT id, habit_name, habit_period FROM Habits")
habit_records = cursor.fetchall()
habit_map = {name: hid for hid, name, period in habit_records}

# Insert task completions for 30 days
for i in range(30):
    current_day = start_date + timedelta(days=i)
    date_str = current_day.strftime("%Y-%m-%d")

    for habit_name in daily_habits:
        if random.random() < 0.85:  # ~85% chance of completion
            cursor.execute("""
                INSERT INTO Tasks (habit_id, task_name, periodicity, task_log_date, streak, task_status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (habit_map[habit_name], habit_name, "daily", date_str, 0, "completed"))

# Insert weekly tasks (one per week)
total_days = 30
for i in range(0, total_days, 7):
    day_of_week = start_date + timedelta(days=i + 1)  # use Tuesday of each week
    date_str = day_of_week.strftime("%Y-%m-%d")

    for habit_name in weekly_habits:
        if random.random() < 0.9:  # ~90% chance
            cursor.execute("""
                INSERT INTO Tasks (habit_id, task_name, periodicity, task_log_date, streak, task_status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (habit_map[habit_name], habit_name, "weekly", date_str, 0, "completed"))

connection.commit()
connection.close()
print("✅ Sample data inserted.")
