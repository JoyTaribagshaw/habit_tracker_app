# 🛣️ Habit Tracker - Development Roadmap

This document outlines the major milestones and deliverables for building and improving the CLI-based habit tracking system.

---

## ✅ Phase 1: Conception (Complete)
- [x] Define objective and feature scope
- [x] Choose SQLite as database
- [x] Outline architecture and class responsibilities
- [x] Receive and incorporate professor feedback

---

## 🚧 Phase 2: Core Development
### 🧱 Backend Modules
- [x] `database.py`: schema, constraints, and FK enforcement
- [x] `habit_tracker.py`: OOP structure (`Habit`, `Task`, `MyHabits`)
- [x] `analytics.py`: insights on performance, missed habits, longest streak
- [x] `main.py`: CLI wrapper with validation helpers

### 📦 Seed/Test Data
- [x] `seed_data.py`: initial dataset for testing
- [x] `test_habit_tracker.py`: Pytest coverage for key flows

---

## 🚀 Phase 3: Enhancements
### 🧪 Testing & Coverage
- [ ] Expand unit tests for edge cases
- [ ] Add integration tests (cross-module)

### 🖥️ CLI Improvements
- [ ] Add `argparse`-based commands
- [ ] Support habit search/edit/delete by name

### 📊 Analytics Expansion
- [ ] Habit heatmaps (by week/day)
- [ ] Weekly/monthly summary report
- [ ] CSV export for completions

---

## 🌐 Phase 4: Future Extensions
- [ ] Web interface (Flask or Django)
- [ ] Notifications/reminders via email
- [ ] User authentication and multiple user support
- [ ] Cloud sync (e.g., Firebase or Supabase)

---

## 📅 Timeline Estimate
| Week | Task |
|------|------|
| 1 | Setup DB, Habit class, seed/test data |
| 2 | CLI + analytics module |
| 3 | Testing, validation, custom analytics |
| 4 | CLI refactor, enhancements, polish |

---

## 🧠 Final Notes
The project is structured for growth. All logic is modular and testable, setting the foundation for CLI, web, and possibly mobile platforms.
