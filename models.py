from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class HabitStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class TaskStatus(Enum):
    COMPLETED = "completed"
    SKIPPED = "skipped"
    MISSED = "missed"

class Habit:
    def __init__(self,
                 name: str,
                 period: str,
                 description: str = "",
                 difficulty: str = "medium",
                 category_id: Optional[int] = None,
                 target_days: int = 7,
                 reminder_time: str = "09:00",
                 creation_date: Optional[str] = None,
                 status: str = "active",
                 habit_id: Optional[int] = None,
                 streak: int = 0,
                 best_streak: int = 0,
                 points: int = 0):
        self.id = habit_id
        self.name = name
        self.description = description
        self.period = period.lower()
        self.difficulty = difficulty.lower()
        self.category_id = category_id
        self.target_days = min(max(1, target_days), 7)
        self.reminder_time = reminder_time
        self.creation_date = creation_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status.lower()
        self.streak = streak
        self.best_streak = best_streak
        self.points = points
        self._validate()

    def _validate(self) -> None:
        if self.period not in ['daily', 'weekly']:
            logger.error(f"Invalid period: {self.period}")
            raise ValueError("Period must be 'daily' or 'weekly'")
        if self.difficulty not in [d.value for d in Difficulty]:
            logger.error(f"Invalid difficulty: {self.difficulty}")
            raise ValueError(f"Difficulty must be one of: {[d.value for d in Difficulty]}")
        if self.status not in [s.value for s in HabitStatus]:
            logger.error(f"Invalid status: {self.status}")
            raise ValueError(f"Status must be one of: {[s.value for s in HabitStatus]}")

    def calculate_points(self, completion_time: Optional[int] = None) -> int:
        base_points = {
            'easy': 5,
            'medium': 10,
            'hard': 15
        }.get(self.difficulty, 5)
        time_bonus = 2 if completion_time and completion_time < 5 else 0
        streak_bonus = min(self.streak // 7, 5)
        return base_points + time_bonus + streak_bonus

    def update_streak(self, completed: bool = True) -> None:
        if completed:
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            self.points += self.calculate_points()
        else:
            self.streak = 0

    def get_streak_emoji(self) -> str:
        if self.streak == 0:
            return "🔴"
        elif self.streak < 3:
            return "🟡"
        elif self.streak < 7:
            return "🟢"
        elif self.streak < 14:
            return "🔵"
        else:
            return "🟣"

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'period': self.period,
            'difficulty': self.difficulty,
            'category_id': self.category_id,
            'target_days': self.target_days,
            'reminder_time': self.reminder_time,
            'creation_date': self.creation_date,
            'status': self.status,
            'streak': self.streak,
            'best_streak': self.best_streak,
            'points': self.points
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Habit':
        return cls(
            name=data['name'],
            period=data['period'],
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 'medium'),
            category_id=data.get('category_id'),
            target_days=data.get('target_days', 7),
            reminder_time=data.get('reminder_time', '09:00'),
            creation_date=data.get('creation_date'),
            status=data.get('status', 'active'),
            habit_id=data.get('id'),
            streak=data.get('streak', 0),
            best_streak=data.get('best_streak', 0),
            points=data.get('points', 0)
        )

    def __str__(self) -> str:
        status_icon = "✅" if self.status == "active" else "⏸️" if self.status == "inactive" else "🗄️"
        period_icon = "📅" if self.period == "daily" else "📆"
        difficulty_emoji = {
            'easy': '😊',
            'medium': '😐',
            'hard': '😰'
        }.get(self.difficulty, '❓')
        return (
            f"{status_icon} {self.name} {period_icon}\n"
            f"   {self.description or 'No description'}\n"
            f"   📊 Streak: {self.streak} days {self.get_streak_emoji()}\n"
            f"   🏆 Best: {self.best_streak} days | {difficulty_emoji} {self.difficulty.capitalize()}\n"
            f"   ⭐ Points: {self.points} | 🎯 Target: {self.target_days} days/week"
        )

class Task:
    def __init__(self,
                 habit_id: int,
                 completion_date: Optional[str] = None,
                 status: str = "completed",
                 notes: str = "",
                 mood: Optional[int] = None,
                 completion_time: Optional[int] = None,
                 points_earned: int = 0,
                 task_id: Optional[int] = None):
        self.id = task_id
        self.habit_id = habit_id
        self.completion_date = completion_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status.lower()
        self.notes = notes
        self.mood = mood
        self.completion_time = completion_time
        self.points_earned = points_earned

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'habit_id': self.habit_id,
            'completion_date': self.completion_date,
            'status': self.status,
            'notes': self.notes,
            'mood': self.mood,
            'completion_time': self.completion_time,
            'points_earned': self.points_earned
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        return cls(
            habit_id=data['habit_id'],
            completion_date=data.get('completion_date'),
            status=data.get('status', 'completed'),
            notes=data.get('notes', ''),
            mood=data.get('mood'),
            completion_time=data.get('completion_time'),
            points_earned=data.get('points_earned', 0),
            task_id=data.get('id')
        )

    def __str__(self) -> str:
        status_emoji = {
            'completed': '✅',
            'skipped': '⏭️',
            'missed': '❌'
        }.get(self.status, '❓')
        mood_str = f" | Mood: {self.mood}" if self.mood else ""
        return (
            f"{status_emoji} Task for Habit ID {self.habit_id} on {self.completion_date}{mood_str} | Points: {self.points_earned}"
        )
