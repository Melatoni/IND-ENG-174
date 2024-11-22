import numpy as np
import heapq

from ArrivalProcess import simulate_arrival_process, generate_length_of_stays

arrival_times, severity_level_list = simulate_arrival_process()
average_length_of_stays = generate_length_of_stays(severity_level_list)
capacity = 100  # Maximum ICU capacity

def simulate_departure_process_priority(arrival_times=arrival_times, severity_level_list=severity_level_list, capacity=capacity):
    departure_times = []
    current_ICU_departures = []   
    start_times = []
    waiting_queue = []  # Priority queue to manage patients waiting for ICU admission

    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        severity = severity_level_list[i]
        length_of_stay = average_length_of_stays[i]

        # If there is an available bed in the ICU
        if len(current_ICU_departures) < capacity:
            start_time = arrival_time
            start_times.append(start_time)

            # Calculate departure time and add to ICU
            departure_time = start_time + length_of_stay * 24
            departure_times.append(departure_time)
            heapq.heappush(current_ICU_departures, departure_time)
        else:
            # If ICU is full, add the patient to the waiting queue
            heapq.heappush(waiting_queue, (-severity, severity, i))  # Use negative severity to implement a max heap
            start_times.append(None)  # Placeholder to indicate treatment has not started
            departure_times.append(None)  # Placeholder to indicate not yet admitted
            
            if i < len(arrival_times) - 1 and arrival_times[i+1] >= current_ICU_departures[0]:
                earliest_available_time = heapq.heappop(current_ICU_departures)

                # Assign the bed to the highest-priority patient from the waiting queue
                _, waiting_severity, waiting_index = heapq.heappop(waiting_queue)

                # Assign the bed to the patient in the waiting queue
                start_time = max(arrival_times[waiting_index], earliest_available_time)
                start_times[waiting_index] = start_time

                # Calculate departure time and add to ICU
                departure_time = start_time + average_length_of_stays[waiting_index] * 24
                departure_times[waiting_index] = departure_time
                heapq.heappush(current_ICU_departures, departure_time)
            
    return departure_times, start_times


# Call the simulation function with priority queue
departure_times, start_times = simulate_departure_process_priority()

# Calculate waiting times
def calculate_waiting_times(arrival_times=arrival_times, start_times=start_times):
    waiting_times = []
    for i in range(len(arrival_times)):
        if start_times[i] is not None:  # Only calculate for patients who were admitted
            waiting_time = start_times[i] - arrival_times[i]
        else:
            waiting_time = None  # Waiting time is None for patients not admitted
        waiting_times.append(waiting_time)
    return waiting_times

waiting_times = calculate_waiting_times()

# Package the results for return
def simultaneously_return(arrival_times=arrival_times, severity_level_list=severity_level_list,
                          start_times=start_times, departure_times=departure_times, waiting_times=waiting_times):
    return arrival_times, severity_level_list, start_times, departure_times, waiting_times


# Simulate data generation
arrival_times, severity_level_list, start_times, departure_times, waiting_times = simultaneously_return()




# Output part of the results for inspection
print(f"Total patients: {len(arrival_times)}")
print(f"Patients admitted: {sum(1 for t in start_times if t is not None)}")
print(f"Patients in waiting queue: {sum(1 for t in start_times if t is None)}")

# Visualize the distribution of waiting times (only for admitted patients)
import matplotlib.pyplot as plt

valid_waiting_times = [wt for wt in waiting_times if wt is not None]
plt.hist(valid_waiting_times, bins=10, alpha=0.7)
plt.xlabel("Waiting Time")
plt.ylabel("Number of Patients")
plt.title("Distribution of Waiting Times")
plt.show()
