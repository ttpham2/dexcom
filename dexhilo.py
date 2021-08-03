#dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv

import csv
import os
import sys
import traceback
from datetime import datetime

HIGH_LIMIT = 270
LOW_LIMIT = 75
highest = None
lowest = None
CSV_FILE = None

if len(sys.argv) < 2:
    print("Error: expected atleast two arguments")
    exit

elif len(sys.argv) == 2:
        CSV_FILE = sys.argv[1]
        
elif len(sys.argv) == 3:
    print("Error: invalid arguments")
    print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
    exit
    
if len(sys.argv) == 4:
    if sys.argv[1] == '-h':
        if not sys.argv[2].isdigit():
            print("Error: invalid argument: ", sys.argv[3])
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
            exit
        else:
            HIGH_LIMIT = int(sys.argv[2])
            CSV_FILE = sys.argv[3]
    elif sys.argv[1] == '-l':
        if not sys.argv[2].isdigit():
            print("Error: invalid argument: ", sys.argv[3])
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")        
            exit
        else:
            LOW_LIMIT = int(sys.argv[2])
            CSV_FILE = sys.argv[3]
if len(sys.argv) == 7:
    if sys.argv[1] == '-h':
        if not sys.argv[2].isdigit():
            print("Error: invalid argument: ", sys.argv[3])
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
            exit
        else:
            HIGH_LIMIT = int(sys.argv[2])
            CSV_FILE = sys.argv[3]
            
        if sys.argv[4] == '-l':
            if not sys.argv[5].isdigit():
                print("Error: invalid argument: ", sys.argv[3])
                print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
                exit
            else:
                LOW_LIMIT = int(sys.argv[5])
                CSV_FILE = sys.argv[6]
        else:
            print("Error: invalid arguments")
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
            exit
    elif sys.argv[1] == '-l':
        if not sys.argv[2].isdigit():
            print("Error: invalid argument: ", sys.argv[2])
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")        
            exit
        else:
            LOW_LIMIT = int(sys.argv[2])
            CSV_FILE = sys.argv[3]
        if sys.argv[4] == '-h':
            if not sys.argv[5].isdigit():
                print("Error: invalid argument: ", sys.argv[3])
                print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
                exit
            else:
                HIGH_LIMIT = int(sys.argv[5])
                CSV_FILE = sys.argv[6]
                
        else:
            print("Error: invalid arguments")
            print("\n Expected usage: dexhilo.py [-h HIGH_LIMIT] [-l LOW_LIMIT] INPUT_FILE.csv")
            exit

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