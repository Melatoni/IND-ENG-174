from ArrivalProcess import simulate_arrival_process
import numpy as np
import heapq

arrival_times, severity_level_list = simulate_arrival_process()
average_length_of_stays = [3, 7, 15] # averagely, Mild - 3 days; Moderate - 7 days; Severe - 15 days.
capacity = 100

# This function tracks the departure times of patients under the assumption of FIFO.
def simulate_departure_process_FIFO(arrival_times = arrival_times, severity_level_list = severity_level_list, capacity = capacity):
    departure_times = []
    current_ICU_departures = [] # tracks the departure times of those patients currently in ICU.

    for i in range(len(arrival_times)):
        arrival_time = arrival_times[i]
        length_of_stay = np.random.exponential(average_length_of_stays[severity_level_list[i] - 1]) # in days

        if len(current_ICU_departures) >= capacity:
            earliest_available_time = heapq.heappop(current_ICU_departures)  
            start_time = max(arrival_time, earliest_available_time)
        else:
            start_time = arrival_time 

        departure_time = start_time + length_of_stay * 24
        departure_times.append(departure_time)

        heapq.heappush(current_ICU_departures, departure_time)
    
    return departure_times
        
print(len(arrival_times))
print(len(simulate_departure_process_FIFO()))