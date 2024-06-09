def allocate_tasks(tasks, restriction_windows):
    all_hours = list(range(24))
    restricted_hours = []
    for start, end in restriction_windows:
        restricted_hours.extend(range(start, end))

    available_hours = [hour for hour in all_hours if hour not in restricted_hours]

    tasks.sort(key=lambda x: x[1], reverse=True)

    allocated_tasks = []
    current_hour = 0

    for task, duration in tasks:
        allocated = False
        for hour in available_hours:
            if hour >= current_hour and all(hour + i in available_hours for i in range(duration)):
                allocated_tasks.append((task, hour, hour + duration))
                for i in range(duration):
                    available_hours.remove(hour + i)
                current_hour = hour + duration
                allocated = True
                break
        if not allocated:
            return "Cannot allocate all tasks within the given restriction windows."

    free_time_slots = sorted(available_hours)

    return free_time_slots, allocated_tasks


def find_free_window(duration, free_time):
    consecutive_free = []
    current_window = []

    for hour in range(24):
        if hour in free_time:
            current_window.append(hour)
            if len(current_window) == duration:
                consecutive_free.append(current_window)
                current_window = []
        else:
            current_window = []

    return consecutive_free[0] if consecutive_free else None


def insert_task(task_name, duration, routine):
    free_time = routine.free_time
    tasks_time = routine.tasks_time

    free_window = find_free_window(duration, free_time)

    if not free_window:
        print("Error: No suitable free window available for the task.")
        return routine

    start = free_window[0]
    end = start + duration

    tasks_time.append((task_name, start, end))
    tasks_time.sort(key=lambda x: x[1])

    free_time = [hour for hour in free_time if not (start <= hour < end)]

    routine.free_time = free_time
    routine.tasks_time = tasks_time
    return routine


def delete_task(task_name, routine):
    free_time = routine.free_time
    tasks_time = routine.tasks_time

    task_to_remove = None

    for task in tasks_time:
        name, start, end = task
        if name == task_name:
            task_to_remove = task
            break

    if not task_to_remove:
        print("Error: Task not found.")
        return tasks_time, free_time

    tasks_time.remove(task_to_remove)
    _, start, end = task_to_remove

    free_time.extend(range(start, end))
    free_time.sort()

    routine.free_time = free_time
    routine.tasks_time = tasks_time
    return routine