# 🚀 Habit Tracker CLI Application

A modular yet user-friendly command-line application designed to help you cultivate positive habits and break negative ones. Built with Python and SQLite, this tool offers a seamless way to track your daily and weekly routines while providing actionable insights into your progress and consistency patterns.

## 📌 Key Features

- 📅 Track **daily** and **weekly** habits with periodicity support
- ✏️ **Edit habits** (name and periodicity) while preserving streak data
- ✅ Mark habits as completed with automatic streak calculation
- 🔄 Deactivate/reactivate habits without losing data
- 📊 View comprehensive analytics including longest streaks and habit correlations
- 🧩 Modular architecture with separate components for UI, logic, and data
- 🧪 Rigorously tested with `pytest` for reliability (13 passing tests)

**By Joy Tari Bagshaw**  
*Helping you build better habits, one day at a time*
---

## ✨ Why This Habit Tracker?

### 🔄 Smart Habit Management
- 🔄 **Flexible Tracking**: Supports both daily and weekly habit tracking
- 📈 **Streak Tracking**: Automatic streak calculation to keep you motivated
- 📅 **Habit History**: View your completion history and patterns

### 📊 Data-Driven Insights
- 📊 **Analytics Dashboard**: Get insights into your habit performance
- 🔍 **Habit Correlation**: Discover relationships between different habits
- 📉 **Missed Habits**: Identify which habits need more attention

### 💻 Technical Highlights
- 🏗️ **Clean Architecture**: Well-organized OOP design
- 💾 **Local Storage**: SQLite database for data persistence
- 🧪 **Test Coverage**: Comprehensive unit tests for core functionality
- 🚀 **CLI Interface**: Simple, keyboard-driven interface

---

## 📂 Project Structure

```
habit_tracking_app/
├── habit_tracker.py           # Core habit/task logic (OOP)
├── main.py                    # Main application entry point
├── db.py                      # Database connection and setup
├── models.py                  # Data models
├── analytics.py               # Analytics functions
└── tests/                     # Test files
    └── test_habit_tracker.py
```

---

## 🛠️ Technologies Used

- **Python 3.10**
- **SQLite** for embedded persistent storage
- **pytest** for testing
- **VS Code** as IDE
- **Git + GitHub** for version control

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/JoyTaribagshaw/habit_tracker_app.git
cd habit_tracker_app
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
venv\\Scripts\\activate       # on Windows
source venv/bin/activate      # on macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed the Database with Sample Data (Optional)

```bash
python seed_data.py
```

### 5. Run the App

```bash
python main.py
```

---

## 📊 Analytics Available

- **Longest Streak**: View the longest current streak per habit
- **Most Missed Habits**: Identify habits with the most missed completions
- **Habit Correlation**: Discover which habits are often completed together
- **Struggling Habits**: See which habits have low completion rates
- **Focus Suggestions**: Get recommendations on which habits to prioritize
- **Active Habit Summaries**: View all daily and weekly habits at a glance

---

## 🎯 Menu Options

1. Add a New Habit
2. Edit a Habit (name and/or periodicity)
3. Deactivate a Habit
4. List All Active Habits
5. List Habits by Periodicity
6. Mark Habit as Completed
7. Show Completed Tasks for Today
8. List All Tasks
9. Show Analytics Summary
10. Get Longest Streak for Habit
0. Exit

---

## ✅ Testing

The project includes comprehensive unit tests covering:
- Habit creation, editing, and deletion
- Streak calculations respecting periodicity
- Analytics module functionality
- Edge cases (double completion, invalid inputs, etc.)

Run tests using:

```bash
pytest -v
```

**Test Results**: 13 tests passing ✅

---

## 📄 License

This project is part of an academic portfolio for the IU International University of Applied Sciences.

---

## 🔗 Project Repository

**GitHub Link:**  
[https://github.com/JoyTaribagshaw/habit_tracker_app](https://github.com/JoyTaribagshaw/habit_tracker_app)

---

## 👤 Author

**Joy Tari Bagshaw**  
IU International University of Applied Sciences  
Portfolio Project - Habit Tracking Application


