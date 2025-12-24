import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# File path (can use file_path2 for comparison later)
file_path1 = '/Users/nongj/Desktop/Plasma_shock_simulation_backup/my_code/0.2/code_python/runtime_dump1'
specific_date = ''

def plot_runtime(filepath: str):
    dates = []
    times = []
    folders = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.split()
            # continue if format is not to be the exact form
            if len(parts) != 9:
                continue
            date_str = parts[5] + ' ' + parts[6]  # Date e.g. 'Jul 16'
            time_str = parts[7]  # UTC time e.g. '03:05'
            folder = parts[8]  # folder name e.g. 'T.96084'
            dt = datetime.strptime(f'2025 {date_str} {time_str}', '%Y %b %d %H:%M') # e.g. 2025-07-16 16:56:00

            if specific_date != "" and date_str != specific_date:
                continue

            dates.append(dt)
            times.append(time_str)
            folders.append(int(folder[2:]))

    times, folders = zip(*sorted(zip(times, folders)))

    fig, ax = plt.subplots()
    ax.set_title(f"Runtime {specific_date}")

    # # Plot HH:MM
    # ax.set_xlabel("Time HH:MM")
    # ax.plot(times, folders)
    #
    # num_ticks = 10
    # # Limit number of x-ticks
    # if len(times) > num_ticks:
    #     tick_indices = np.linspace(0, len(times) - 1, num_ticks, dtype=int)
    #     ax.set_xticks([times[i] for i in tick_indices])
    # # Limit number of y-ticks
    # ax.set_yticks(np.linspace(folders[0], folders[-1], num_ticks))

    # Plot Hour only
    # Convert each time string to total hours
    hours = [int(hh) + int(mm) / 60 for hh, mm in (t.split(':') for t in times)]
    hours = np.round(hours, 2)
    hours = hours - hours[0]
    ax.plot(hours, folders, label='real time')

    x1, x2 = 1.9, 2.63
    y1, y2 = 1.9e4, 2.24e4
    # plt.plot([x1, x2], [y1, y2]) # Plot arclength

    slope = int((y2 - y1) / (x2 - x1))
    x = np.arange(0, 30, 1)
    y = slope * x
    ax.set_xlabel([0, max(x)])
    ax.set_ylabel([0, max(y)])

    plt.plot(x + x1, y + y1, '--', alpha=0.5, label='predicted time')

    ax.set_ylabel("Timestep")
    ax.set_xlabel("Time (Hour)")

    plt.legend()
    plt.show()

plot_runtime(file_path1)