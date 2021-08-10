#dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv

import csv
import os
import sys
import traceback
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-hi", dest = "high", default = 270, help="USAGE_STRING", type=int)
parser.add_argument("-d", dest = "delta", default = 15, help="USAGE_STRING", type=int)
parser.add_argument("-l", dest = "low", default = 75, help="USAGE_STRING", type=int)
parser.add_argument("file", help="USAGE_STRING")


args = parser.parse_args()

HIGH_LIMIT = args.high
LOW_LIMIT = args.low
DELTA = args.delta
highest = None
lowest = None
#CSV_FILE = sys.argv[len(sys.argv) - 1]
CSV_FILE = args.file
#ERROR_STRING = 
USAGE_STRING = "\n Invalid arugments: dexhilo.py [-d DELTA][-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv"
INVALID_STRING = "Error: invalid arguments"

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        line_count = 0
        start = None;
        highest = None;
        lowest = None;
        last_egv = None;
        for row in reader:
            if row['Event Type'] != "EGV":
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                try:
                    if row['Glucose Value (mg/dL)'].isdigit():
                        egv = int(row['Glucose Value (mg/dL)'])
                    elif row['Glucose Value (mg/dL)'] == "High":
                        egv = 400
                    elif row['Glucose Value (mg/dL)'] == "Low":
                        egv = 30
                    #print(row['Glucose Value (mg/dL)'])
                    #print(row['Index'])
                    #print(int("10"))
                    #print(float(row['Glucose Value (mg/dL)'].strip()))
                    #print(type(row['Glucose Value (mg/dL)']))
                    
                    if egv > HIGH_LIMIT:
                        if start is None:
                            highest = egv
                            start = ['HIGH', row['Timestamp (YYYY-MM-DDThh:mm:ss)'], highest]
                            
                        elif egv > highest:
                            highest = egv
                            start[2] = highest
                    elif egv < LOW_LIMIT:
                        if start is None:
                            lowest = egv
                            start = ['LOW', row['Timestamp (YYYY-MM-DDThh:mm:ss)'], lowest]
                            
                        elif egv < lowest:
                            lowest = egv
                            start[2] = lowest
                    elif start is not None:
                        end = row['Timestamp (YYYY-MM-DDThh:mm:ss)']
                        fmt = '%Y-%m-%dT%H:%M:%S'
                        #print(start);
                        time_delta = datetime.strptime(end, fmt) - datetime.strptime(start[1], fmt)
                        print(start[0], ",",
                            start[1], ",",
                            end, ",",
                            int(time_delta.total_seconds()), ",",
                            start[2])
                        
                        start = None;
                        highest = None;
                        lowest = None;
                    line_count += 1
                except TypeError as err:
                    print(egv, lowest, highest)
                    print("Error in csv at line: ", line_count + 1,"\n")
                    print(row, "\n")
                    #print(err)
                    traceback.print_exc()
        # print(f'Processed {line_count} lines')