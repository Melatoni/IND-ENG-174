from DepartureProcess import simultaneously_return
import numpy as np

severity_level_list, waiting_times = simultaneously_return()

#print(len(severity_level_list))
#print(len(waiting_times))

k = 1 # penalty scale
alpha = 0.001 # time_sensitivity

def penaltyFunction1(k = k, alpha = alpha, severity_level_list = severity_level_list, waiting_times = waiting_times):
    total_penalty = 0
    for i in range(len(waiting_times)):
        severity = severity_level_list[i]
        waiting_time = waiting_times[i]
        total_penalty += k * (severity ** 2) * np.exp(alpha * waiting_time)

    return total_penalty

print(penaltyFunction1())