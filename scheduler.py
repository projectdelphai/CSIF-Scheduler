#! /bin/python

import os
import csv
import numpy as np
import pandas as pd

class Employee:
    def __init__(self, username, requested_hours, availability):
        self.username = username;
        self.requested_hours = requested_hours
        self.availability = availability
    def __str__(self):
        return("username: " + self.username + "\nrequested hours: " + str(self.requested_hours))

def find_csv_files(directory):
    filenames = os.listdir(directory)
    return ['./data/csv/' + filename for filename in filenames if filename.endswith('.csv')]

# import csv file
def parse_csv(filename):
    raw_data = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            raw_data.append(row)
    return raw_data

# store employee raw data in a employee class
def create_employee(filename, raw_data):
    username = filename[11:-4]
    requested_hours = float(raw_data[1][10])
    num_second_choices = float(raw_data[2][10])
    num_third_choices = float(raw_data[3][10])

    #if num_second_choices < 20.0:
        #print(username + " does not have enough second choices")
        #return None

    #if num_third_choices < 10.0:
        #print(username + " does not have enough third choices")
        #return None

    if requested_hours > 19.5:
        print(username + " has too many requested hours")

    availability = []
    for i in raw_data[1:]:
        availability.append(i[1:8])
    
    avail = np.array(availability)
    employee = Employee(username, requested_hours, avail)

    return employee

# get everyone's preferred availability by day
# each column is a new employee, monday is 0, sunday is 6
def get_availabilities_by_day(employees):
    availabilities = []
    for i in range(0,7):
        t = []
        for employee in employees:
            monday = employee.availability[:,i]
            t.append(monday)
        arr = np.vstack(t).T
        availabilities.append(arr)
    return(availabilities)

filenames = find_csv_files("./data/csv")
employees = []
for filename in filenames:
    raw_data = parse_csv(filename)
    employee = create_employee(filename, raw_data)
    if (employee is not None):
        employees.append(employee)

raw_data = parse_csv(filename)
times = []
for i in raw_data[1:]:
    times.append(i[0])

# abd = availabilities by day
abd = get_availabilities_by_day(employees)
employee_names = [employee.username for employee in employees]
days = ['Monday', 'Tuesday', "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
for i in range(7):
    day = abd[i]
    df = pd.DataFrame(day, index=times, columns=employee_names)
    df.to_csv('data/days/' + days[i] + '.csv', index=True, header=True, sep=',')


