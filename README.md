# 🧭 Habit Tracker CLI Application

A modular command-line application to track daily and weekly habits using Python and SQLite. Designed to help users build consistency, measure progress, and generate insightful analytics from their habit routines.
---

## 📌 Features

- 📅 Track **daily** and **weekly** habits
- ✅ Mark tasks as completed with streak tracking
- 📊 View analytics: longest streak, missed habits, struggling habits
- 🔄 Simulate real user data with a 30-day seeding script
- 🧪 Tested with `pytest` to ensure reliability
- 🧱 Built using clean Object-Oriented Design

---

## 📂 Project Structure

```
chibuike_habit_tracker/
├── habit_tracker.py           # Core habit/task logic (OOP)
└── docs/
    ├── habit_tracker_abstract.docx
    └── habit_tracker_presentation.pptx
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
git clone https://github.com/ChibykeOS/chibuike_onah_habit_tracker_app.git
cd chibuike_onah_habit_tracker_app
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

- Longest current streak per habit
- List of missed habits
- Habits that are struggling over time
- Active daily and weekly habit summaries

---

## ✅ Testing

Run tests using:

```bash
pytest
```

---



## 🔗 Project Repository

**GitHub Link:**  
[https://github.com/ChibykeOS/chibuike_onah_habit_tracker_app](https://github.com/ChibykeOS/chibuike_onah_habit_tracker_app)

---

 
