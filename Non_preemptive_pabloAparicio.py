import matplotlib.pyplot as plt

periods = [10, 10, 20, 20, 40, 40, 80]
WCET = [2, 3, 2, 2, 2, 2, 3]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def hyperperiod(periods):
    result = periods[0]
    for period in periods[1:]:
        result = lcm(result, period)
    return result

hyperperiod_value = hyperperiod(periods)

# Builds all the jobs
jobs = []
for i in range(len(periods)):
    period = periods[i]
    wcet = WCET[i]
    num_jobs = hyperperiod_value // period
    for j in range(num_jobs):
        release = j * period
        deadline = release + period
        jobs.append({
            'task': i,
            'release': release,
            'deadline': deadline,
            'remaining': wcet,
            'finish': None,
            'waiting': 0,
            'start': None
        })

jobs.sort(key=lambda x: x['release'])

current_time = 0
schedule = []
current_job = None

while current_time < hyperperiod_value:
    if current_job is not None:
        schedule.append(current_job['task'] + 1)  # Shift to 1-based task index
        current_job['remaining'] -= 1

        if current_job['remaining'] == 0:
            current_job['finish'] = current_time + 1
            current_job = None
        current_time += 1
        continue

    eligible_jobs = []
    for job in jobs:
        if job['finish'] is None and job['release'] <= current_time:
            if job['task'] == 4 or (current_time + job['remaining'] <= job['deadline']):
                eligible_jobs.append(job)

    if eligible_jobs:
        selected_job = min(eligible_jobs, key=lambda x: x['deadline'])
        if selected_job['start'] is None:
            selected_job['start'] = current_time
        schedule.append(selected_job['task'] + 1)  # Shift to 1-based task index
        current_job = selected_job
        current_job['remaining'] -= 1

        if current_job['remaining'] == 0:
            current_job['finish'] = current_time + 1
            current_job = None
        current_time += 1
    else:
        schedule.append(0)  #no task running
        current_time += 1

# WT (wating time) and RT(Reponse time)
total_WT = 0
total_RT = 0

for job in jobs:
    if job['start'] is not None:
        total_WT += job['start'] - job['release']
    if job['finish'] is not None:
        total_RT += job['finish'] - job['release']


print(f"Total Waiting Time: {total_WT}")
print(f"Total Response Time: {total_RT}")

# Graph
tasks = list(range(1, len(periods)+1))  
colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
no_task_color = 'black'

fig, ax = plt.subplots(figsize=(15, 5))


current_task = schedule[0]
start_time = 0
for t, task in enumerate(schedule):
    if task != current_task or t == len(schedule) - 1:
        end_time = t if task != current_task else t + 1
        if current_task == 0:
            ax.broken_barh([(start_time, end_time - start_time)], (0, 1), facecolors=no_task_color)
        else:
            ax.broken_barh([(start_time, end_time - start_time)], (current_task, 1), facecolors=colors[current_task-1])
        current_task = task
        start_time = t

ax.set_yticks(range(0, len(periods)+1))
ax.set_yticklabels(['IDLE'] + [f"Task {i}" for i in range(1, len(periods)+1)])
ax.set_ylim(-0.5, len(periods)+1)
ax.set_xlabel("Time")
ax.set_ylabel("Tasks")
ax.set_title("Not Preemptive representation")
ax.grid(True)


import matplotlib.patches as mpatches
legend_handles = [mpatches.Patch(color=no_task_color, label='no Task')] + \
                 [mpatches.Patch(color=colors[i], label=f"Task {i+1}") for i in range(len(tasks))]
ax.legend(handles=legend_handles, loc='upper right')

plt.show()

