from habit_tracker import MyHabits
from analytics import display_analytics_summary, get_longest_streak_for_habit
from database import create_connection, create_tables

def get_valid_integer(prompt, valid_range=None):
    while True:
        try:
            value = int(input(prompt))
            if valid_range and value not in valid_range:
                raise ValueError(f"Please enter one of: {valid_range}")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")

def display_menu():
    print("\n📋 Habit Tracker CLI Menu:")
    print("1️⃣  Add a New Habit")
    print("2️⃣  Deactivate a Habit")
    print("3️⃣  List All Active Habits")
    print("4️⃣  List Habits by Periodicity")
    print("5️⃣  Mark Habit as Completed")
    print("6️⃣  Show Completed Tasks for Today")
    print("7️⃣  List All Tasks")
    print("8️⃣  Show Analytics Summary")
    print("9️⃣  Get Longest Streak for Habit")
    print("0️⃣  Exit")

def main():
    db_file = input("Enter database file name (default: my_habits.db): ").strip() or "my_habits.db"
    connection = create_connection(db_file)
    cursor = connection.cursor()
    from db import create_tables
    create_tables(cursor)
    connection.commit()
    my_habits = MyHabits(cursor, connection)
    print(f"Connected to database: {db_file}")

    while True:
        display_menu()
        choice = get_valid_integer("Select an option (0-9): ", range(10))

        if choice == 1:
            name = get_non_empty_input("Enter Habit Name: ")
            period = get_valid_integer("Enter Periodicity (1 = Daily, 2 = Weekly): ", [1, 2])
            my_habits.add_habit(name, period)

        elif choice == 2:
            habit_id = get_valid_integer("Enter Habit ID to deactivate: ")
            my_habits.deactivate_habit(habit_id)

        elif choice == 3:
            my_habits.list_all_active_habits()

        elif choice == 4:
            period = get_valid_integer("Enter Periodicity (1 = Daily, 2 = Weekly): ", [1, 2])
            my_habits.list_habits_by_periodicity(period)

        elif choice == 5:
            habit_id = get_valid_integer("Enter Habit ID to mark completed: ")
            my_habits.mark_task_completed(habit_id)

        elif choice == 6:
            my_habits.get_completed_tasks()

        elif choice == 7:
            my_habits.list_all_tasks()

        elif choice == 8:
            display_analytics_summary()

        elif choice == 9:
            name = get_non_empty_input("Enter Habit Name: ")
            get_longest_streak_for_habit(name)

        elif choice == 0:
            print("👋 Exiting. Goodbye!")
            break

    if 'connection' in locals():
        connection.commit()
        connection.close()

if __name__ == "__main__":
    main()
