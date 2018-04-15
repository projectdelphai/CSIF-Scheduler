#! /usr/bin/python

import xlrd
import csv
import os
import sys
from datetime import time

if len(sys.argv) == 1:
    print("You need to specify an excel sheet to convert")
    sys.exit()

filename =  sys.argv[1]
if (not os.path.isfile(filename)):
    print("The specified file doesn't exist")
    sys.exit()

with xlrd.open_workbook(filename) as book:
    num_employees = book.nsheets - 1
    print("There are " + str(num_employees) + " employees found in the excel sheet")
    for i in range(1,num_employees+1):
        sheet = book.sheet_by_index(i)
        employee = sheet.name
        print(employee)
        with open('./data/csv/' + employee + '.csv', 'wb') as f:
            c = csv.writer(f)
            for r in range(sheet.nrows):
                row = sheet.row_values(r)

                if row[0] != "Time":
                    raw_time = int(row[0] * 24 * 3600)
                    hour = raw_time//3600
                    mins = (raw_time%3600)//60
                    if mins == 0:
                        mins = "00"
                    row[0] = str(hour) + ":" + str(mins)
                c.writerow(row)
