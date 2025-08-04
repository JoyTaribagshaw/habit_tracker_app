from datetime import datetime, timedelta
from models import Habit, Task, Difficulty, HabitStatus, TaskStatus
from db import create_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Establish DB connection
connection = create_connection()
cursor = connection.cursor()

def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")

def week_diff(start_date, end_date):
    sy, sw, _ = start_date.isocalendar()
    ey, ew, _ = end_date.isocalendar()
    return (ey - sy) * 52 + (ew - sw) + 1

def get_all_active_habits():
    query = "SELECT habit_name, creation_date, habit_period FROM Habits WHERE habit_status = 'active'"
    return cursor.execute(query).fetchall()

def get_longest_streak():
    query = "SELECT habit_name, MAX(streak) FROM Habits WHERE habit_status = 'active'"
    result = cursor.execute(query).fetchone()
    return {"habit_name": result[0], "streak": result[1]} if result else None

def get_longest_streak_for_habit(habit_name):
    query = "SELECT streak FROM Habits WHERE habit_name = ? AND habit_status = 'active'"
    result = cursor.execute(query, (habit_name,)).fetchone()
    if result:
        print(f"Longest streak for '{habit_name}': {result[0]} days")
        return result[0]
    else:
        print(f"No active habit found with the name: {habit_name}")
        return 0

def get_missed_counts(habit_name, habit_period, creation_date):
    now = datetime.now()
    creation = datetime.strptime(creation_date, "%Y-%m-%d")
    start_date = max(now - timedelta(days=30), creation)

    if habit_period == 'daily':
        tracked_units = (now - start_date).days + 1
        query = """
            SELECT COUNT(DISTINCT task_log_date) 
            FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?
        """
    elif habit_period == 'weekly':
        tracked_units = week_diff(start_date, now)
        query = """
            SELECT COUNT(DISTINCT strftime('%Y-%W', task_log_date)) 
            FROM Tasks WHERE task_name = ? AND task_log_date BETWEEN ? AND ?
        """
    else:
        raise ValueError("Invalid habit period")

    completed_units = cursor.execute(
        query,
        (habit_name, start_date.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"))
    ).fetchone()[0]

    return tracked_units, completed_units

def get_struggled_habits():
    struggled = []
    for habit_name, creation_date, period in get_all_active_habits():
        creation = datetime.strptime(creation_date, "%Y-%m-%d")
        interval = min((datetime.now() - creation).days if period == 'daily' else week_diff(creation, datetime.now()), 30 if period == 'daily' else 4)
        tracked, completed = get_missed_counts(habit_name, period, creation_date)

        if completed < interval:
            missed = tracked - completed
            struggled.append(f"'{habit_name}' ({period}) missed {missed} of {interval} expected completions last month.")
    return struggled

def get_missed_habits():
    missed_list = []
    for habit_name, creation_date, period in get_all_active_habits():
        tracked, completed = get_missed_counts(habit_name, period, creation_date)
        if completed < tracked:
            missed_list.append(f"'{habit_name}' missed {tracked - completed} completions since creation.")
    return missed_list

def display_data(header, items):
    print(f"\n=== {header} ===")
    if not items:
        print("No data available.")
    for item in items:
        print(f"- {item}")

def display_analytics_summary():
    longest = get_longest_streak()
    if longest:
        print(f"Longest streak: {longest['streak']} for habit '{longest['habit_name']}'")
    else:
        print("No data on longest streak.")

    daily = [h[0] for h in get_all_active_habits() if h[2] == 'daily']
    weekly = [h[0] for h in get_all_active_habits() if h[2] == 'weekly']
    struggled = get_struggled_habits()
    missed = get_missed_habits()

    display_data("Active Daily Habits", daily)
    display_data("Active Weekly Habits", weekly)
    display_data("Habits with Low Completion (Last Month)", struggled)
    display_data("Missed Habits Since Creation", missed)

def get_completed_tasks_for_date(log_date):
    query = "SELECT * FROM Tasks WHERE task_log_date = ?"
    return cursor.execute(query, (log_date,)).fetchall()

def list_all_tasks():
    return cursor.execute("SELECT * FROM Tasks").fetchall()

def list_all_active_habits():
    return cursor.execute("SELECT * FROM Habits WHERE habit_status = 'active'").fetchall()

# --- Advanced Analytics Enhancements ---
from collections import Counter, defaultdict
from typing import List, Dict, Tuple

def get_most_missed_habits(cursor, top_n: int = 3) -> List[Tuple[int, str, int]]:
    """Return top N most missed habits (by count)."""
    cursor.execute("""
        SELECT Habits.id, Habits.habit_name, COUNT(*) as missed_count
        FROM Tasks
        JOIN Habits ON Tasks.habit_id = Habits.id
        WHERE Tasks.task_status = 'missed'
        GROUP BY Habits.id, Habits.habit_name
        ORDER BY missed_count DESC
        LIMIT ?
    """, (top_n,))
    result = cursor.fetchall()
    logger.info(f"Most missed habits: {result}")
    return result

def get_habit_completion_correlation(cursor) -> Dict[Tuple[str, str], float]:
    """Estimate correlation between pairs of habits based on same-day completions."""
    cursor.execute("SELECT habit_id, task_log_date FROM Tasks WHERE task_status = 'completed'")
    completions = cursor.fetchall()
    date_habits = defaultdict(set)
    for habit_id, date in completions:
        date_habits[date].add(habit_id)
    pair_counts = Counter()
    habit_counts = Counter()
    for habits in date_habits.values():
        for h in habits:
            habit_counts[h] += 1
        for h1 in habits:
            for h2 in habits:
                if h1 < h2:
                    pair_counts[(h1, h2)] += 1
    correlations = {}
    for (h1, h2), count in pair_counts.items():
        total = habit_counts[h1] + habit_counts[h2] - count
        correlations[(h1, h2)] = round(count / total, 2) if total else 0.0
    logger.info(f"Habit correlations: {correlations}")
    return correlations

def suggest_habits_to_focus(cursor, user_id: int = None) -> List[str]:
    """Suggest habits to focus on: most missed or lowest streak."""
    cursor.execute("SELECT habit_name, streak FROM Habits WHERE habit_status = 'active'")
    habits = cursor.fetchall()
    if not habits:
        return []
    habits_sorted = sorted(habits, key=lambda x: x[1])
    suggestions = [h[0] for h in habits_sorted[:3]]
    logger.info(f"Suggested habits to focus: {suggestions}")
    return suggestions

if __name__ == "__main__":
    display_analytics_summary()
