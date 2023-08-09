import json
from datetime import datetime

# Define the ExtendedTask class
class ExtendedTask:
    def __init__(self, task_type, initiated_today, cancelled_in_a_row, last_feedback,
                 performed_this_week, completion_time, initial_completion_time,
                 previous_completion_times, correction_cues, pressure_spread, game_points,
                 weight_for_speed=1, weight_for_correction=1, weight_for_pressure=1, weight_for_points=1,
                 last_updated=None):

        # Task properties
        self.task_type = task_type
        self.initiated_today = initiated_today
        self.cancelled_in_a_row = cancelled_in_a_row
        self.last_feedback = last_feedback
        self.performed_this_week = performed_this_week
        self.completion_time = completion_time
        self.initial_completion_time = initial_completion_time
        self.previous_completion_times = previous_completion_times
        self.correction_cues = correction_cues
        self.pressure_spread = pressure_spread
        self.game_points = game_points
        self.weight_for_speed = weight_for_speed
        self.weight_for_correction = weight_for_correction
        self.weight_for_pressure = weight_for_pressure
        self.weight_for_points = weight_for_points
        # Timestamp for last updated metrics
        self.last_updated = datetime.fromisoformat(last_updated) if last_updated else datetime.min
        self.points = 0

    def calculate_competence_factor(self):
        # Avoid division by zero errors
        if not self.previous_completion_times or self.completion_time == 0:
            return 0

        avg_previous_completion = sum(self.previous_completion_times) / len(self.previous_completion_times)

        if self.task_type == 'sit-up-down':
            correction_avg = sum(self.correction_cues) / len(self.correction_cues) if self.correction_cues and any(
                self.correction_cues) else 1
            return self.weight_for_speed * (
                        avg_previous_completion / self.completion_time) - self.weight_for_correction * (
                               self.correction_cues[-1] / correction_avg)

        if self.task_type == 'balance':
            pressure_avg = sum(self.pressure_spread) / len(self.pressure_spread) if self.pressure_spread and any(
                self.pressure_spread) else 1
            return self.weight_for_speed * (
                        avg_previous_completion / self.completion_time) - self.weight_for_pressure * (
                               self.pressure_spread[-1] / pressure_avg)

        if self.task_type == 'saccades':
            return 0

        if self.task_type == 'memory':
            points_avg = sum(self.game_points) / len(self.game_points) if self.game_points and any(
                self.game_points) else 1
            return self.weight_for_speed * (avg_previous_completion / self.completion_time) - self.weight_for_points * (
                        self.game_points[-1] / points_avg)

        return 0


def calculate_points(task):
    # Initialize points
    total_points = 0

    # Assign points based on initiation frequency
    if task.initiated_today <= 2:
        total_points += 10
    elif task.initiated_today <= 5:
        total_points += 5
    else:
        total_points += 1

    # Deduct points for cancellations
    cancel_penalty = task.cancelled_in_a_row * 2
    total_points -= min(cancel_penalty, 10)

    # Add points for positive feedback
    if task.last_feedback == 'positive':
        total_points += 10

    # Add points if task hasn't been performed this week
    if not task.performed_this_week:
        total_points += 15

    # Add points based on competence factor
    competence_factor = task.calculate_competence_factor()
    total_points += competence_factor * 5

    return total_points


def recommend_next_task(tasks):
    # Sort tasks by points and select the one with highest points
    tasks_sorted = sorted(tasks, key=lambda t: t.points, reverse=True)
    return tasks_sorted[0]


def load_points_from_memory():
    # Load previously stored task points from file
    try:
        with open('task_points.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def update_memory(task_points_dict):
    # Save updated task points to file
    with open('task_points.json', 'w') as file:
        json.dump(task_points_dict, file)


# Load previously stored points
memory_points = load_points_from_memory()

# Load tasks from the external JSON file
with open('tasks.json', 'r') as file:
    tasks_data = json.load(file)

all_tasks = [ExtendedTask(**task_data) for task_data in tasks_data]

# Calculate or fetch points for each task
for task in all_tasks:
    if task.last_updated > datetime.fromisoformat(
            memory_points.get(task.task_type, {}).get('timestamp', '1970-01-01T00:00:00')):
        task.points = calculate_points(task)
        memory_points[task.task_type] = {
            'points': task.points,
            'timestamp': task.last_updated.isoformat()
        }
    elif task.task_type in memory_points:
        task.points = memory_points[task.task_type]['points']
    else:
        task.points = calculate_points(task)
        memory_points[task.task_type] = {
            'points': task.points,
            'timestamp': task.last_updated.isoformat()
        }

    # Update memory
    update_memory(memory_points)

# Recommend next task based on highest points
next_task = recommend_next_task(all_tasks)
print(f"The recommended next task is: {next_task.task_type}")


