import numpy as np
import heapq
import matplotlib.pyplot as plt

from ArrivalProcess import simulate_arrival_process, generate_length_of_stays

arrival_times, severity_level_list = simulate_arrival_process()
length_of_stays = generate_length_of_stays(severity_level_list)
capacity = 100  

def simulate_departure_process_priority_queue(arrival_times=arrival_times, severity_level_list=severity_level_list, capacity=capacity):
    num_patients = len(arrival_times)
    start_times = [None] * num_patients
    departure_times = [None] * num_patients
    current_ICU_departures = []   #（departure_times， index）
    waiting_queue = []  #（-severity_level，arrival_times, index）

    for i in range(num_patients):
        arrival_time = arrival_times[i]
        severity = severity_level_list[i]
        length_of_stay = length_of_stays[i]

        # remove departure times before the arrival
        while current_ICU_departures and current_ICU_departures[0][0] <= arrival_time:
            heapq.heappop(current_ICU_departures)

        # add the current arrival
        heapq.heappush(waiting_queue, (-severity, arrival_time, i))

    
        while len(current_ICU_departures) < capacity and waiting_queue:
            _, w_arrival_time, w_index = heapq.heappop(waiting_queue)
            w_severity = severity_level_list[w_index]
            w_length_of_stay = length_of_stays[w_index]
            w_start_time = arrival_times[w_index]   
            start_times[w_index] = w_start_time
            w_departure_time = w_start_time + w_length_of_stay * 24 
            departure_times[w_index] = w_departure_time
            heapq.heappush(current_ICU_departures, (w_departure_time, w_index))


    # Process patients in the waiting queue until it's empty
    while waiting_queue:
        _, w_arrival_time, w_index = heapq.heappop(waiting_queue)
        w_severity = severity_level_list[w_index]
        w_length_of_stay = length_of_stays[w_index]
        w_start_time = current_ICU_departures[0][0]
        start_times[w_index] = w_start_time
        w_departure_time = w_start_time + w_length_of_stay * 24
        departure_times[w_index] = w_departure_time
        heapq.heappop(current_ICU_departures)
        heapq.heappush(current_ICU_departures, (w_departure_time, w_index))

    return departure_times, start_times


departure_times, start_times = simulate_departure_process_priority_queue()

def calculate_waiting_times(arrival_times = arrival_times, start_times = start_times):
    waiting_times = []

    for i in range(len(arrival_times)):
        waiting_time = start_times[i] - arrival_times[i]
        waiting_times.append(waiting_time)

    return waiting_times

waiting_times = calculate_waiting_times()

def simultaneously_return(arrival_times=arrival_times, severity_level_list=severity_level_list,
                          start_times=start_times, departure_times=departure_times, waiting_times=waiting_times):
    return arrival_times, severity_level_list, start_times, departure_times, waiting_times



