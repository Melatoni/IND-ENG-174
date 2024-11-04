import sys

project_root = '/Users/sizheli/Desktop/INDENG_174/IND-ENG-174'
sys.path.append(project_root)

from Part_1_IcuQueue.DepartureProcess import simultaneously_return

import heapq
import numpy as np
import random

arrival_times, severity_level_list, start_times, departure_times, waiting_times = simultaneously_return()
#print(arrival_times)

request_frequency = 2 # i.e. averagely, every patient request one service every two hours
number_of_care_givers = 50

capacity = 100 # If you want to modify this parameter, please simultaneously modify 'capacity' in Part_1_IcuQueue/DepartureProcess.py
time_horizon = 10 # If you want to modify this parameter, please simultaneously modify 'time_horizon' in Part_1_IcuQueue/ArrivalProcess.py

service_type = [1, 2, 3] # 1 - small-scale ; 2 - medium-scale ; 3 - large-scale
mean_service_time = [0.2, 0.5, 1] # in hours

mild_distribution = [0.6, 0.3, 0.1] # Patients with mild conditions have a 60% probability of requesting small-scale services, 30% probability of requesting medium_scale services....
moderate_distribution = [0.3, 0.4, 0.3]
severe_distribution = [0.7, 0.2, 0.1]

def simulate_service_process(request_frequency = request_frequency, capacity = capacity, number_of_care_givers = number_of_care_givers,
                             time_horizon = time_horizon, start_times = start_times, departure_times = departure_times, severity_level_list = severity_level_list,
                             service_type = service_type, mean_service_time = mean_service_time, mild_distribution = mild_distribution, 
                             moderate_distribution = moderate_distribution, severe_distribution = severe_distribution):
    patient_states = []
    for i in range(len(arrival_times)):
        patient_states.append(0)
    # patient_states can be used to track the status of all patients
    # 0 represents that the patient is not currently in ICU.
    # 1 represents that the patient is in ICU now, and is neither in service nor waiting to be served.
    # 2 represents that the patient is in ICU now, and is in service or waiting to be served.
    #print(patient_states)

    service_start_times = []
    for i in range(capacity):
        service_start_times.append(-1)
    # service_start_times can be used to track the current service start time in (i-1)-th hospital bed.
    # -1 represents that the bed is currently empty

    service_end_times = []
    for i in range(capacity):
        service_end_times.append(-1)
    # service_start_times can be used to track the current service end time in (i-1)-th hospital bed.
    # -1 represents that the bed is currently empty

    index_list = []
    for i in range(capacity):
        index_list.append(-1)
    # index_list can be used to track the index of patient in current hospital beds.
    # -1 represents that the bed is currently empty

    service_waiting_times = []
    severity_cor_waiting_times = []

    care_giver_heap = []
    # care_giver_heap can be used to track the current service_end_time of all care givers.

    service_lambda_max = request_frequency * capacity
    t = 0

    while t < time_horizon * 24:
        t += np.random.exponential(1 / service_lambda_max)

        if t > time_horizon * 24:
            break

        number_of_patients = len(start_times)

        # get into ICU
        for i in range(number_of_patients):
            if t > start_times[i] and t < departure_times[i] and patient_states[i] == 0:
                patient_states[i] = 1 

        # discharge
        for i in range(number_of_patients):
            if t > departure_times[i]:
                if patient_states[i] == 2:
                    bed_index = index_list.index(i)
                    service_start_times[bed_index] = -1
                    service_end_times[bed_index] = -1
                patient_states[i] = 0
                

        # termination of service
        for i in range(number_of_patients):
            if patient_states[i] == 2:
                bed_index = index_list.index(i)
                if service_end_times[bed_index] > 0 and service_end_times[bed_index] < t:
                    patient_states[i] = 1
                    service_start_times[bed_index] = -1
                    service_end_times[bed_index] = -1

        number_of_state_1_patients = patient_states.count(1)

        if random.uniform(0, 1) < number_of_state_1_patients / capacity:
            selection = np.where(np.array(patient_states) == 1)[0]
            patient_request_service = random.choice(selection)
            patient_states[patient_request_service] = 2
            severity = severity_level_list[patient_request_service]

            if severity == 1:
                service = np.random.choice(service_type, 1, p = mild_distribution)[0]
            if severity == 2:
                service = np.random.choice(service_type, 1, p = moderate_distribution)[0]
            if severity == 3:
                service = np.random.choice(service_type, 1, p = severe_distribution)[0]

            service_time = np.random.exponential(mean_service_time[service - 1]) # in hours
            choice = np.where(np.array(service_start_times) == -1)[0][0]
            

            if len(care_giver_heap) >= number_of_care_givers:
                earliest_available_time = heapq.heappop(care_giver_heap)
                service_start_times[choice] = max(earliest_available_time, t)
            else:
                service_start_times[choice] = t
            service_end_times[choice] = service_start_times[choice] + service_time

            index_list[choice] = patient_request_service

            heapq.heappush(care_giver_heap, service_end_times[choice])
            
            service_waiting_times.append(service_start_times[choice] - t)
            severity_cor_waiting_times.append(severity_level_list[patient_request_service])

    service_waiting_times = [x * 60 for x in service_waiting_times] # convert to minutes
    return service_waiting_times, severity_cor_waiting_times

#print(simulate_service_process())