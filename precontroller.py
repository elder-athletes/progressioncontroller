## Sample Code for the Pre-controller, the able feedback needs to cancel the task queuing and the sitting up from the chair needs to be recorded and used for how many times the task will be initiated in a day.
import json
from datetime import datetime
import calendar
from collections import deque

def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            print(f"Loaded data from {filename}: {data}")  # Print loaded data
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")  # Print the error
        return {}


def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Load tasks and engagement_data
tasks = load_data('tasks.json')
engagement_data = load_data('engagement_data.json')

if 'task_queue' in engagement_data:
    task_queue = deque(engagement_data['task_queue'])
else:
    tasks.sort(key=lambda x: datetime.fromisoformat(x['last_updated']))
    task_queue = deque([task['task_type'] for task in tasks])

def update_engagement_data(task_type, ability):
    current_time = datetime.now()

    # Calculate the 15-minute interval
    minutes = int(current_time.strftime("%M"))
    rounded_minutes = 15 * (minutes // 15)
    current_period = current_time.strftime(f"%H:{rounded_minutes:02}")

    current_day = calendar.day_name[current_time.weekday()]

    if current_day not in engagement_data:
        engagement_data[current_day] = {f"{hour:02}:{minute:02}": [] for hour in range(24) for minute in [0, 15, 30, 45]}

    engagement_data[current_day][current_period].append({
        'task_type': task_type,
        'able_to_complete': ability
    })

    # Update and save the rotated task queue
    task_queue.rotate(-1)
    engagement_data['task_queue'] = list(task_queue)
    save_data('engagement_data.json', engagement_data)

def engage_user():
    current_task_type = task_queue[0]

    able_to_complete = next((task['are_they_able'] for task in tasks if task['task_type'] == current_task_type), False)

    update_engagement_data(current_task_type, able_to_complete)

    return current_task_type

# Example of usage:
print(engage_user())




