import sys

project_root = '/Users/sizheli/Desktop/INDENG_174/IND-ENG-174'
sys.path.append(project_root)

from Part_1_IcuQueue.DepartureProcess import simultaneously_return
arrival_times, severity_level_list, start_times, departure_times, waiting_times = simultaneously_return()
