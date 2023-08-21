### Sample Code for the Pre-controller, the able feedback needs to cancel the task queuing and the sitting up from the chair needs to be recorded and used for how many times the task will be initiated in a day.


import json
from datetime import datetime
import calendar
from collections import deque

# Load tasks
with open('tasks.json', 'r') as f:
    tasks = json.load(f)

# Sorting tasks based on their last initiation for initial queue creation
tasks.sort(key=lambda x: datetime.fromisoformat(x['last_updated']))
task_queue = deque([task['task_type'] for task in tasks])


# Update engagement_data.json
def update_engagement_data(task_type, ability):
    current_time = datetime.now()
    current_hour = current_time.strftime("%H")
    current_day = calendar.day_name[current_time.weekday()]

    # Load or initialize engagement_data
    try:
        with open('engagement_data.json', 'r') as file:
            engagement_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        engagement_data = {}

    if current_day not in engagement_data:
        engagement_data[current_day] = {f"{i:02}": [] for i in range(24)}

    engagement_data[current_day][current_hour].append({
        'task_type': task_type,
        'able_to_complete': ability
    })

    with open('engagement_data.json', 'w') as file:
        json.dump(engagement_data, file, indent=4)


# Engage user with the next task
def engage_user():
    current_task_type = task_queue[0]

    # Get the 'are_they_able' value for the current task from the tasks.json
    able_to_complete = False
    for task in tasks:
        if task['task_type'] == current_task_type:
            able_to_complete = task['are_they_able']

            # Update the engagement_data.json
            update_engagement_data(current_task_type, able_to_complete)

    # Move the current task to the back of the queue
    task_queue.rotate(-1)

    return current_task_type

# Example of usage:
engage_user()


