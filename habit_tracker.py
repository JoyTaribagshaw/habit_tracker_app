"""
Core habit tracking module containing the MyHabits class.
Handles habit creation, completion tracking, and streak calculations.
"""
import logging
from datetime import datetime, timedelta
from models import Habit, Task, Difficulty, HabitStatus, TaskStatus

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MyHabits:
    """
    Main class for managing habits and tracking completions.
    
    Attributes:
        cursor: Database cursor for executing queries
        connection: Database connection for committing changes
    """
    def __init__(self, db_cursor, db_connection):
        self.cursor = db_cursor
        self.connection = db_connection

    def add_habit(self, habit_name, habit_period):
        """
        Add a new habit to the database.
        
        Args:
            habit_name (str): Name of the habit
            habit_period (int): 1 for daily, 2 for weekly
            
        Raises:
            ValueError: If habit_name is empty or habit_period is invalid
        """
        # Input validation
        if not habit_name or not str(habit_name).strip():
            raise ValueError("Habit name cannot be empty")
            
        if habit_period not in [1, 2]:
            raise ValueError("Invalid periodicity. Use 1 for daily, 2 for weekly.")
            
        habit_period = "daily" if habit_period == 1 else "weekly"

        new_habit = Habit(habit_name, habit_period)
        self.cursor.execute("""
            INSERT INTO Habits (habit_name, habit_period, creation_date, last_completed, streak, habit_status)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (new_habit.name, new_habit.period, new_habit.creation_date, None, 0, new_habit.status))
        self.connection.commit()
        new_habit.id = self.cursor.lastrowid
        print(f"Habit '{new_habit.name}' added with ID {new_habit.id}.")

    def edit_habit(self, habit_id, new_name=None, new_period=None):
        """
        Edit an existing habit's name and/or periodicity.
        Preserves all streak data and completion history.
        
        Args:
            habit_id (int): ID of the habit to edit
            new_name (str, optional): New name for the habit
            new_period (int, optional): New periodicity (1 for daily, 2 for weekly)
        """
        # Fetch current habit data
        self.cursor.execute("SELECT habit_name, habit_period FROM Habits WHERE id = ?", (habit_id,))
        result = self.cursor.fetchone()
        
        if not result:
            print("Habit not found.")
            return
        
        current_name, current_period = result
        updates = []
        params = []
        
        # Validate and prepare name update
        if new_name is not None:
            if not new_name or not str(new_name).strip():
                raise ValueError("Habit name cannot be empty")
            updates.append("habit_name = ?")
            params.append(new_name.strip())
        
        # Validate and prepare period update
        if new_period is not None:
            if new_period not in [1, 2]:
                raise ValueError("Invalid periodicity. Use 1 for daily, 2 for weekly.")
            period_str = "daily" if new_period == 1 else "weekly"
            updates.append("habit_period = ?")
            params.append(period_str)
        
        if not updates:
            print("No changes specified.")
            return
        
        # Update the habit
        params.append(habit_id)
        query = f"UPDATE Habits SET {', '.join(updates)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.connection.commit()
        
        print(f"Habit updated successfully!")
        print(f"  Previous: {current_name} ({current_period})")
        print(f"  Current: {new_name or current_name} ({params[-2] if new_period else current_period})")

    def deactivate_habit(self, habit_id):
        self.cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (habit_id,))
        result = self.cursor.fetchone()
        if result:
            self.cursor.execute("UPDATE Habits SET habit_status = 'inactive' WHERE id = ?", (habit_id,))
            self.connection.commit()
            print(f"Habit '{result[0]}' has been deactivated.")
        else:
            print("Habit not found.")

    def list_all_active_habits(self):
        self.cursor.execute("""
            SELECT id, habit_name, habit_period, creation_date, 
                   COALESCE(streak, 0) as streak 
            FROM Habits 
            WHERE habit_status = 'active'
        """)
        habits = self.cursor.fetchall()
        if habits:
            print("\nActive Habits:")
            print("-" * 50)
            print(f"{'ID':<4} {'Habit Name':<20} {'Period':<8} {'Created':<12} {'Streak':<6}")
            print("-" * 50)
            for h in habits:
                # Format the creation date to show only the date part
                created_date = h[3].split()[0] if h[3] else 'N/A'
                print(f"{h[0]:<4} {h[1]:<20} {h[2]:<8} {created_date:<12} {h[4]}")
            print("-" * 50)
        else:
            print("No active habits found.")

    def list_habits_by_periodicity(self, habit_period):
        period = "daily" if habit_period == 1 else "weekly"
        self.cursor.execute("""
            SELECT id, habit_name, creation_date, COALESCE(streak, 0) as streak 
            FROM Habits 
            WHERE habit_status = 'active' AND habit_period = ?
        """, (period,))
        habits = self.cursor.fetchall()
        if habits:
            print(f"\nActive {period.capitalize()} Habits:")
            print("-" * 50)
            print(f"{'ID':<4} {'Habit Name':<20} {'Created':<12} {'Streak':<6}")
            print("-" * 50)
            for h in habits:
                created_date = h[2].split()[0] if h[2] else 'N/A'
                print(f"{h[0]:<4} {h[1]:<20} {created_date:<12} {h[3]}")
            print("-" * 50)
        else:
            print(f"No active {period} habits found.")

    def mark_task_completed(self, habit_id):
        """
        Mark a habit as completed for the current period.
        Respects habit periodicity (daily/weekly) and updates streak accordingly.
        
        Args:
            habit_id (int): ID of the habit to mark as completed
        """
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM Habits WHERE id = ?", (habit_id,))
        habit_data = self.cursor.fetchone()

        if not habit_data:
            print("Habit not found.")
            return

        habit_name = habit_data[1]
        habit_period = habit_data[3]  # Index 3 for habit_period
        # Index 6 for streak (0-based)
        current_streak = int(habit_data[6]) if habit_data[6] is not None else 0
        # Index 8 for habit_status (0-based)
        habit_status = habit_data[8]

        if habit_status != 'active':
            print("This habit is inactive and cannot be marked completed.")
            return

        # Check if already completed for this period
        if habit_period == 'daily':
            self.cursor.execute("SELECT * FROM Tasks WHERE habit_id = ? AND task_log_date = ?", (habit_id, today))
            if self.cursor.fetchone():
                print("Already marked as completed for today.")
                return

        elif habit_period == 'weekly':
            week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime("%Y-%m-%d")
            week_end = (datetime.now() + timedelta(days=(6 - datetime.now().weekday()))).strftime("%Y-%m-%d")
            self.cursor.execute("""
                SELECT * FROM Tasks WHERE habit_id = ? AND task_log_date BETWEEN ? AND ?
            """, (habit_id, week_start, week_end))
            if self.cursor.fetchone():
                print("Already marked as completed this week.")
                return

        new_task = Task(habit_id=habit_id, completion_date=today)
        # Ensure periodicity is in correct format
        periodicity = 'daily' if habit_period == 1 or habit_period == 'daily' else 'weekly'
        # Ensure current_streak is an integer
        current_streak = int(current_streak) if current_streak is not None else 0
        
        self.cursor.execute("""
            INSERT INTO Tasks (habit_id, task_name, task_log_date, periodicity, streak, task_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (new_task.habit_id, habit_name, new_task.completion_date, periodicity, current_streak + 1, "completed"))

        self.cursor.execute("""
            UPDATE Habits SET last_completed = ?, streak = ? WHERE id = ?
        """, (today, current_streak + 1, habit_id))

        self.connection.commit()
        print(f"Habit '{habit_name}' marked completed. Streak: {current_streak + 1}")

    def get_completed_tasks(self, log_date=None):
        log_date = log_date or datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT * FROM Tasks WHERE task_log_date = ?", (log_date,))
        tasks = self.cursor.fetchall()
        if tasks:
            print(f"Tasks completed on {log_date}:")
            for t in tasks:
                self.cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (t[1],))
                habit_name = self.cursor.fetchone()[0]
                print(f"- {habit_name} (ID: {t[0]}, Status: {t[6]}, Streak: {t[5]})")
        else:
            print(f"No tasks completed on {log_date}.")

    def list_all_tasks(self):
        self.cursor.execute("SELECT * FROM Tasks")
        tasks = self.cursor.fetchall()
        if tasks:
            print("All Tasks:")
            for t in tasks:
                self.cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (t[1],))
                habit_name = self.cursor.fetchone()[0]
                print(f"- {habit_name} (Task ID: {t[0]}, Date: {t[4]}, Periodicity: {t[3]}, Streak: {t[5]}, Status: {t[6]})")
        else:
            print("No tasks found.")
