from CareRequest import simulate_service_process
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

service_waiting_times, severity_cor_waiting_times = simulate_service_process()

def plot_discrete_severity_distribution(service_waiting_times = service_waiting_times, severity_cor_waiting_times = severity_cor_waiting_times, bin_size=1):
    """
    Plots the distribution of waiting times (in minutes) with stacked bars representing severity levels,
    with slightly reduced gaps between bars.
    
    Parameters:
    - service_waiting_times: list or array of waiting times in minutes
    - severity_cor_waiting_times: list or array of severity levels corresponding to waiting times (e.g., [1, 2, 1, 3, ...])
    - bin_size: the size of each time bin in minutes (default is 1)
    
    Returns:
    - A stacked bar plot showing the distribution of waiting times by severity level, with minimal gaps.
    """
    # Define bins for waiting times based on the max waiting time in the data
    max_waiting_time = int(np.ceil(max(service_waiting_times) / bin_size) * bin_size)
    bins = np.arange(0, max_waiting_time + bin_size, bin_size)

    # Create a DataFrame from input data for easier manipulation
    df = pd.DataFrame({'waiting_times': service_waiting_times, 'severity_levels': severity_cor_waiting_times})

    # Group data by time bins and severity levels, then count occurrences
    df['time_bins'] = pd.cut(df['waiting_times'], bins=bins, right=False)
    grouped = df.groupby(['time_bins', 'severity_levels']).size().unstack(fill_value=0)

    # Remove empty bins (rows with all zero values) for a cleaner plot
    grouped = grouped.loc[(grouped.sum(axis=1) > 0)]
    
    # Calculate the positions of each bin
    bar_positions = np.arange(len(grouped))

    # Plot the stacked bar chart with slightly reduced gaps
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(bar_positions, grouped[1], color='#4e79a7', label='Mild', width=0.9)
    ax.bar(bar_positions, grouped[2], bottom=grouped[1], color='#f28e2c', label='Moderate', width=0.9)
    ax.bar(bar_positions, grouped[3], bottom=grouped[1] + grouped[2], color='#e15759', label='Severe', width=0.9)

    # Set labels and title
    ax.set_xlabel('Waiting Time (minutes)', fontsize=12)
    ax.set_ylabel('Number of Requests', fontsize=12)
    ax.set_title('Distribution of Waiting Times by Severity Level (Minutes)', fontsize=15, fontweight='bold')
    ax.legend(title="Severity Level")

    # Customize x-ticks to show bin ranges and set x-tick labels
    ax.set_xticks(bar_positions)
    ax.set_xticklabels([f"{int(interval.left)}-{int(interval.right)}" for interval in grouped.index], rotation=45)

    plt.tight_layout()
    plt.show()

plot_discrete_severity_distribution()

k = 0.01 # penalty scale
alpha = 0.01 # time sensitivity

def penaltyFunction2(k = k, alpha = alpha, service_waiting_times = service_waiting_times, severity_cor_waiting_times = severity_cor_waiting_times):
    total_penalty = 0
    for i in range(len(service_waiting_times)):
        severity = severity_cor_waiting_times[i]
        waiting_time = service_waiting_times[i]
        total_penalty += k * (severity ** 2) * np.exp(alpha * waiting_time)

    return total_penalty

print(penaltyFunction2())