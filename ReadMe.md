This will act as the instrunctions for further development of this part of the project and how it will be integrated into the system.

1. Understanding the intent of The Controller

In very basic terms the what we are trying to do is engaging user as much as possible and whitin their availibility. To achieve this we record a multitude of metrics:

    Time of Day 
    Time of Week
    Consecutive Terminations per Task  
    Time for completing one cycle of exercise for each task 
    Number of Reps before termination 
    Feedback for exhaustion 
    Feedback for discontent with the task
    Pressure Spread 
    Points for the Memory Task 
    Amount of Corrective Cues given per task cycle for each task 
    Maximum/Average force applied to each pad 
    Amount of times user standed up from their chair
    
Additionally control variables that maybe important for data allocation: 

    Stable Pressure point from the pressure spread 
    Maximal deviation from the Stable Pressure Point 
    Average of the deviations prior 
    Average of corrective cues prior 
    Average completion times prior 
    Average Scores of the points from the memory task 
    Averages of the prior forces applied 
    Lou sensor! How many times do they get up nightly... 

We use this information to assign points to each task. Then we record the points of each task and put them in a list in a decreasing order to indicate which task should be done next. To this extend we utilise the following files:

- Pre-Controller
- Engagement Data
- Point Based Controller
- Tasks
- Task Points

2. Understanding the Files

- Pre-Controller:

This is intended to run after a time-stamp we need to define where it describes the first initialisation of the machine. We run this script optimally for a week and ideally we try to cue users in short periods throughout the day to assess what task they are engaging and when. This creates a list where the times and days they interacted with the machine. We can create a histogram (this is not implemented yet) and use the hour data and day data to define optimal periods where the controller should cue the next task. We are doing this to get the estimate baseline time treshold they are most likely to interact with the machine.

Pre-controller also has logic to use user prompts. Namely we need to ask the user if they are able to do the exercise. (By able I mean literal ability) If not that task should be eleminated from the queue. We also record how many times the user gets up from their chair. This metric creates the baseline for how many times we can ask user in one day to do a task. (Since they are likely to get up that much anyway)

- Engagment Data:

Engagement Data is the json file where we record the data from the pre-controller. It creates a list with 15 minute intervals we record data under these periods.

- Point-Based Controller:

This script is the bulk of the logic. We define some functions to undertake the point assignment piecewise.


ExtendedTask Class: Represents an individual task with its related metrics. We assign task json values to these internal variables for use in the script. These are mainly the metrics we collect.

  Attributes:

 - task_type: Type of task (e.g., 'sit-up-down', 'balance', etc.).
 - initiated_today: Number of times the task was initiated today.
 - cancelled_in_a_row: Number of consecutive cancellations for this task.
 - last_feedback: Last feedback received for the task, could be 'positive' or otherwise.
 - performed_this_week: Boolean indicating if the task has been performed this week.
 - completion_time: Time taken to complete the task.
 - initial_completion_time: Initial time taken to complete the task.
 - previous_completion_times: List of times taken to complete the task in previous sessions.
 - correction_cues: Correction feedback received during the 'sit-up-down' task.
 - pressure_spread: Feedback on pressure distribution during the 'balance' task.
 - game_points: Points scored during the 'memory' game task.
 - weight_for_speed: Weight given to speed as a metric.
 - weight_for_correction: Weight given to correction feedback.
 - weight_for_pressure: Weight given to pressure distribution feedback.
 - weight_for_points: Weight given to points in the memory game.
 - last_updated: Timestamp indicating when the task metrics were last updated.
 - points: The total points calculated for the task based on its metrics.

= Methods =

- calculate_competence_factor(): Calculates a competence factor based on various task metrics. This is then added onto the point metric calculation.
- calculate_points(task): Computes the points for a given task. Points are based on frequency, cancellations, feedback, task performance, and the competence factor. The weight of the points can be changed for different intent.
- recommend_next_task(tasks) Recommends the next task from a list of tasks based on the highest points. This is essentially what we want to return to the machine. The next task and the current list which represents the task queue.
- load_points_from_memory(): Loads previously stored points for tasks from a JSON file (task_points.json). The 
- update_memory(task_points_dict): Updates the JSON file (task_points.json) with the latest task points.

= Execution Flow =

  1. Load previously stored points from task_points.json.
  2. Load tasks data from tasks.json.
  3. Convert JSON tasks data to ExtendedTask objects.
  4. For each task:
     - If the task's last update is more recent than what's stored in memory, recalculate the task points.
     - If the task points are stored in memory and are up-to-date, use the stored points.
     - Otherwise, calculate points for the task and update the memory.
  5. Recommend the next task based on the highest points.

= Outputs =

The script concludes by printing the recommended next task based on the calculated points. For example:

"The recommended next task is: sit-up-down"


- Tasks: This json file acts as the input from the both the Mongo server and the machine API. All the incoming data must be proccessed into this json structure.

- Task Points: This json records the values and when these values were recorded. This file needs to be seperate from the tasks.json so we have a clean way to define the input and the outputs of the system.



3. What needs to be done for future development:

- Initialising the server:

The intent is to run this system on a server which communicates with the machine (throught the api) and the mongo. The data coming in from these sources need an additional script to format them into the tasks.json format. Also server needs to be able to call the pre-controller in the first week and then the point controller afterwards.

- Better time tresholding:

Right now we are intending to decide when to recommend the task using the baseline engagement data we have. Ideally we want to extend the point based controller to ensure time tresholding isn't static. We want to have a window of time where we reccomend the task even if it is not the in the ideal period, more they engage with the task around that time more it should shift towards that. So it is dynamic histogram.

- Experimentation with weights:

Currently we don't have very rigirous reasons for assigning weights to the point allocations. Ideally we need them in place so when they are change we are able to change the intent of the controller. For example maximising compotance factor gain, minimising the task rejection etc. right now we priotrise engagement with the user.

- Better Integration Between the Pre-Controller and the Point Based Controller:

Point Based Controller should initially needs to recommend tasks (meaning adjust the next task's timestamp) by observing the data from the pre-controller. Also amount of times they get up from their chair in a day should reflect the amount of times point based controller cues the user. For instance if pre-controller recorded that the person stand up 10 times on Tuesday when precontroller was running, point based controller should at maximum cues exercised 10 times on a Tuesday. Like the time tresholding if this is dynamic it would be much better. One way to achieve this is recording the amount of times user engaged with the task last time and taking and average between the last and the current value to determine the new maximum limit of cueing the user. One other important bit would be to ensure the this number never reaches above or below a certain treshold meaning if user haven't interacted with the machine back to back, instead of limit reaching to a miniscule value it should default to the latest maximum instead if it gets too small.

Integrating the time data from the precontroller is quite straight forward. When the next task is decided, have the script look into the engagement_data.json and check is there was any exercise done in the current time create a time stamp for the next task within this time period. Else create the time stamp for the next time that is closest in the engagement data.

