import numpy as np
import random

# this function aims at characterizing the rate distribution of one day
# number of patients per hour
# 0 <= t <= 24
def rate_distribution_pdf(t):
    return t #let's first consider a time-homogeneous poisson process.

#print(rate_distribution_pdf(1))

severity_levels = [1, 2, 3] # 1 - Mild; 2 - Moderate; 3 - Severe
probabilities = [0.2, 0.5, 0.3] 

# randomly generate the severity levels of incoming patients.
def severity_level_list(size, severity_levels = severity_levels, probabilities = probabilities):
    return np.random.choice(severity_levels, size, probabilities).tolist()

#print(severity_level_list(20))

# This function intends to simulate the arrival process of given time horizon.
# time_horizon: total number of days that we want to simulate
# lambda_max: the maximal arriving rate (number of patients per hour) in a day
def simulate_arrival_process(time_horizon, lambda_max, rate_distribution_pdf = rate_distribution_pdf,  severity_level_list = severity_level_list):
    t = 0 # in hours
    arrival_times = []

    while t < time_horizon * 24:
        t += random.expovariate(lambda_max)

        if t > time_horizon * 24:
            break

        # acceptance-rejection
        if random.uniform(0, 1) < rate_distribution_pdf(t % 24) / lambda_max:
            arrival_times.append(t)

    severity_level_list = severity_level_list(len(arrival_times))
    
    return arrival_times, severity_level_list

print(simulate_arrival_process(2, 24))