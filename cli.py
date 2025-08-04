import typer
from typing import Optional
from models import Habit, Difficulty, HabitStatus
from db import create_connection
import logging

app = typer.Typer()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.command()
def add_habit(
    name: str = typer.Argument(..., help="Name of the habit"),
    period: str = typer.Option("daily", help="Periodicity: daily or weekly"),
    description: str = typer.Option("", help="Description of the habit"),
    difficulty: str = typer.Option("medium", help="Difficulty: easy, medium, hard"),
    target_days: int = typer.Option(7, help="Target days per week (1-7)"),
    reminder_time: str = typer.Option("09:00", help="Reminder time (HH:MM)")
):
    """Add a new habit."""
    connection = create_connection()
    cursor = connection.cursor()
    try:
        habit = Habit(
            name=name,
            period=period,
            description=description,
            difficulty=difficulty,
            target_days=target_days,
            reminder_time=reminder_time
        )
        cursor.execute(
            """
            INSERT INTO Habits (
                habit_name, habit_period, description, difficulty, target_days, reminder_time, creation_date, habit_status, streak, best_streak, points
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                habit.name,
                habit.period,
                habit.description,
                habit.difficulty,
                habit.target_days,
                habit.reminder_time,
                habit.creation_date,
                habit.status,
                habit.streak,
                habit.best_streak,
                habit.points
            )
        )
        connection.commit()
        typer.echo(f"Habit '{habit.name}' added successfully!")
    except Exception as e:
        logger.error(f"Error adding habit: {e}")
        typer.echo(f"Error: {e}")
    finally:
        connection.close()

@app.command()
def list_habits(status: str = typer.Option("active", help="Status: active, inactive, archived")):
    """List habits by status."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, habit_name, habit_period, description, streak, best_streak, points FROM Habits WHERE habit_status = ?", (status,))
    habits = cursor.fetchall()
    if not habits:
        typer.echo(f"No {status} habits found.")
    else:
        for h in habits:
            typer.echo(f"ID: {h[0]}, Name: {h[1]}, Period: {h[2]}, Desc: {h[3]}, Streak: {h[4]}, Best: {h[5]}, Points: {h[6]}")
    connection.close()

@app.command()
def deactivate_habit(habit_id: int):
    """Deactivate a habit by ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (habit_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("UPDATE Habits SET habit_status = 'inactive' WHERE id = ?", (habit_id,))
        connection.commit()
        typer.echo(f"Habit '{result[0]}' has been deactivated.")
    else:
        typer.echo("Habit not found.")
    connection.close()

@app.command()
def delete_habit(habit_id: int):
    """Delete a habit by ID."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT habit_name FROM Habits WHERE id = ?", (habit_id,))
    result = cursor.fetchone()
    if result:
        cursor.execute("DELETE FROM Habits WHERE id = ?", (habit_id,))
        connection.commit()
        typer.echo(f"Habit '{result[0]}' deleted.")
    else:
        typer.echo("Habit not found.")
    connection.close()

if __name__ == "__main__":
    app()
