def calculate_points(task):
    # Initialize total_points to 0
    total_points = 0

    # Assign points based on the number of times the task was initiated in a day
    if task.initiated_today <= 2:
        total_points += 10
    elif task.initiated_today <= 5:
        total_points += 5
    else:
        total_points += 1

    # Deduct points based on how many times the task was cancelled in a row, with a cap
    cancel_penalty = task.cancelled_in_a_row * 2
    if cancel_penalty > 10:
        cancel_penalty = 10
    total_points -= cancel_penalty

    # If the user gave positive feedback last time, add points
    if task.last_feedback == 'positive':
        total_points += 10

    # If the task hasn't been performed in a week, add points
    if not task.performed_this_week:
        total_points += 15

    # Add points based on task competence (i.e., speed of task completion)
    if task.completion_time < task.initial_completion_time:
        competence_factor = task.initial_completion_time / task.completion_time
        total_points += competence_factor * 5

    return total_points

# Sample Task class (replace this with your actual Task class if you have one)
class Task:
    def __init__(self, initiated_today, cancelled_in_a_row, last_feedback, performed_this_week, completion_time, initial_completion_time):
        self.initiated_today = initiated_today
        self.cancelled_in_a_row = cancelled_in_a_row
        self.last_feedback = last_feedback
        self.performed_this_week = performed_this_week
        self.completion_time = completion_time
        self.initial_completion_time = initial_completion_time

# Sample usage
task = Task(initiated_today=3, cancelled_in_a_row=2, last_feedback='positive', performed_this_week=False, completion_time=7, initial_completion_time=10)
points = calculate_points(task)
print("Total points:", points)

