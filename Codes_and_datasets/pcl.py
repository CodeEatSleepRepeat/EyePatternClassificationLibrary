"""
Pattern Classification Library
Author: CodeEatSleepRepeat

Date: 18.09.2020.

Run the pcl.py script to classify the look patern of students into one of twelve classes.
Usage:
    test.py -i <inputfile>
    test.py -i <inputfile> -o <outputfile>
    test.py -i <inputfile> -o <outputfile> --quiet
    test.py -i <inputfile> -o <outputfile> -v
    test.py --input <inputfile> --output <outputfile> --verbose

Meaning:
    -i or --input   --> Input csv file with 1 look pattern or file with many csv files.
    -o or --output  --> Output csv file to store vectors of information for look patern and clusters'.
    --quiet    --> Do not write cluster numbers on console. Let it be empty. This requires -o argument!
    -v or --verbose --> Print everything on console.

Good luck user!
"""

from pypmml import Model
import numpy as np
import pandas as pd
import pickle
import os
import sys, argparse


global inputfile
global outputfile
global verbose
global quiet
inputfile = ''
outputfile = ''
verbose = False
quiet = False

# check if input path is file or directory and return input data from it in form of vector of inputs (evan if vector dim is 1 === input is file)
def get_input_data():
    if os.path.isdir(inputfile):  
        return collect_csv_data_collection_from_directory(inputfile)
    elif os.path.isfile(inputfile):  
        return collect_csv_data_from_file(inputfile)
    else:
        print("\nBad input file! Check input arguments and try again.")
        sys.exit(2)

# collecting all csv files from forwarded directory
def collect_csv_data_collection_from_directory(path):
    data_collection = []

    for csv_name in os.listdir(os.path.abspath(path)):
        csv_path = os.path.join(path, csv_name)
        data = pd.read_csv(csv_path, names=['Duration', 'AOI', 'Question'], skip_blank_lines=True, skiprows=[0])
        data_collection.append(data)
    return data_collection

# collecting data from csv file forwarded as input
def collect_csv_data_from_file(csv_path):
    data_collection = []
    
    data = pd.read_csv(csv_path, names=['Duration', 'AOI', 'Question'], skip_blank_lines=True, skiprows=[0])
    data_collection.append(data)
    
    return data_collection

# saving csv files into forwarded path
def save_data_as_csv(data):
    import csv

    is_csv = True

    if os.path.isdir(outputfile):  
        filename = os.path.join(outputfile + "gaze_clustering.csv")
    elif os.path.isfile(outputfile):  
        if str(outputfile).endswith(".csv"):
            filename = outputfile
        elif str(outputfile).endswith(".tsv"):
            filename = outputfile
            is_csv = False
        else:
            filename = os.path.join(outputfile + ".csv")
    else:
        print("\nBad outputfile file! Check output arguments and try again.")
        sys.exit(2)
    
    with open(filename, "w", newline='') as f:
        if is_csv:
            writer = csv.writer(f)
        else:
            writer = csv.writer(f, delimiter = '\t')
        writer.writerows(data)

# get total num of seconds
def total_secons_in_question(duration):
    return sum(duration)

# get no. of regions
def total_regions_in_question(aoi):
    return len(aoi)

# get sec on all regions [vector]
def seconds_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
    
    for i in range(0, len(duration)):
        vector[aoi[i]] += duration[i]

    return list(vector.values())

# get no. of looks at all regions [vector]
def no_looks_per_region(aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
    
    for i in range(0, len(aoi)):
        vector[aoi[i]] += 1

    return list(vector.values())

# mean sec by regions [vector]
def mean_seconds_per_region(duration, aoi):
    from statistics import mean
    
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': [], 'odgovori': [], 'pitanje': [], 'pitanje-kod': [], 'prazno': [], 'prethodno': [], 'sledece': [] }
    
    for i in range(0, len(aoi)):
        vector[aoi[i]].append(duration[i])

    rez_vector = []
    for v in vector.values():
        if not v:
            rez_vector.append(0.0)
        else:
            rez_vector.append(mean(v))
    
    return rez_vector

# get top viewed region before region x (for all regions) [vector]
def top_region_before_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod':
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'odgovori': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje-kod': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prazno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prethodno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'sledece': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
            }
    
    previous = aoi[0]

    # move through all regions except first one and add 1 for curren area whose previous one was "previous" area
    for i in range(1, len(aoi)):
        vector[aoi[i]][previous] += 1
        previous = aoi[i]
    
    vector = list(vector.values())
    ret_vector = []

    # loop each area vector and extract area postion wich was the top rated area that commed before current area
    for set_vector in vector:
        values = list(set_vector.values())
        
        if (set(values) == {0.0}):
            ret_vector.append(-1.0)
        else:
            ret_vector.append(values.index(max(values)))

    return ret_vector

# get top viewed region after region x (for all regions) [vector]
def top_region_after_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod':
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'odgovori': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje-kod': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prazno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prethodno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'sledece': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
            }
    
    current = aoi[0]

    # move through all regions except first and last one and add 1 for "curren" area whose previous one was this area
    for i in range(1, len(aoi)):
        vector[current][aoi[i]] += 1
        current = aoi[i]
    
    vector = list(vector.values())
    ret_vector = []

    # loop each area vector and extract area postion wich was the top rated area that commed before current area
    for set_vector in vector:
        values = list(set_vector.values())
        
        if (set(values) == {0.0}):
            ret_vector.append(-1.0)
        else:
            ret_vector.append(values.index(max(values)))

    return ret_vector

# group all info in one vector
def call_information_methods(duration, aoi):
    vector = []

    i1 = total_secons_in_question(duration)
    i2 = total_regions_in_question(aoi)
    i3 = seconds_per_region(duration, aoi)
    i4 = no_looks_per_region(aoi)
    i5 = mean_seconds_per_region(duration, aoi)
    i6 = top_region_before_per_region(duration, aoi)
    i7 = top_region_after_per_region(duration, aoi)

    vector.append(i1)
    vector.append(i2)
    vector.extend(i3)
    vector.extend(i4)
    vector.extend(i5)
    vector.extend(i6)
    vector.extend(i7)

    return vector

# get vector of question statistics based on question
def get_question_based_information_vector(data):

    duration = data[data.columns[0]]
    AOI = data[data.columns[1]]

    vector = call_information_methods(duration, AOI)
    return vector

# add row and column label before saving information vector to csv file
def add_labels_to_vector(vector):
    df = pd.DataFrame(vector,
                    columns=['cluster_no', '0', '1', '2', '3', '4', '5','6',
    '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
    '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
    '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'])

    return [df.columns.values.tolist()] + df.values.tolist()

# classify the data into one of the twelve different classes
def predict(data, model):
    x = model.predict([data])
    return x[0]

# load classification model from file named 'pickle_model.pkl'
def load_model():
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model

# main function for picking up arguments
def main(argv):
    global inputfile
    global outputfile
    global verbose
    global quiet
    
    parser = argparse.ArgumentParser(description="Run the pcl.py script to classify the look patern of students into one of twelve classes.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", help="Print everything on console. It's best not to use it with large pattern dataset.")
    group.add_argument("-q", "--quiet", action="store_true", help="Do not write cluster numbers on console. Let it be empty. This requires -o argument!")
    parser.add_argument("-i","--inputfile", type=str, help="Input csv file with 1 look pattern or file with many csv files. The predefined location is './gaze_dataset/csv/'.")
    parser.add_argument("-o","--outputfile", type=str, help="Output csv file to store vectors of information for look patern and clusters' short description.")
    args = parser.parse_args()
 
    
    if args.verbose:
        verbose = True
    if args.quiet:
        quiet = True
    if args.inputfile is None:
        inputfile = "./gaze_dataset/csv/"
    else:
        inputfile = args.inputfile
    if args.outputfile is not None:
        outputfile = args.outputfile
    
    if quiet and outputfile == '':
        print("usage: pcl.py [-h] [-v | -q] [-i INPUTFILE] [-o OUTPUTFILE]\npcl.py: error: argument -q/--quiet: not allowed without argument -o/--outputfile")
        sys.exit(2)

    if not quiet:
        print('Input file is ', inputfile)
    if outputfile != '' and not quiet:
        print('Output file is ', outputfile)

if __name__ == "__main__":
   main(sys.argv[1:])


# MAIN
model = load_model()

information_vector = []
cluster_type_short_description = [
    "Fast and focused",
    "Thorough, where code and answer are essential",
    "Thorough with accent on code",
    "Thorough, where question and answer are essential",
    "Fast and thorough, where code and answer are essential",
    "Fast and focused only on question and answer",
    "Focused on answers",
    "Superficially, where code and answer are essential",
    "Superficially, where code and question are essential",
    "Haven't studied, trying to find answers in previous questions",
    "Haven't studied, don't care",
    "Haven't studied, trying to guess using answers"
]

cluster_type_long_description = [
    "Less than 10 different gazes on average. Spend less than 30 secons per question on average.",
    "Between 10 and 20 different gazes on average. Frequent looks on answers (more then 3 times per question on average). Frequent looks on code (more then 5 times per question on average). Spend more than 50 secons per question on average.",
    "Between 10 and 20 different gazes on average. Lots of time spent on code (average of at least 10 seconds per look). Spend more than 50 secons per question on average.",
    "Between 10 and 20 different gazes on average. Frequent looks on answers (more then 3 times per question on average). Frequent looks on code (more then 5 times per question on average). Look at the answers longer (average of at least 4 seconds per look). Some time spent looking at test question. Spend more than 50 secons per question on average.",
    "Between 10 and 20 different gazes on average. Frequent looks on answers (more then 3 times per question on average). Frequent looks on code (more then 5 times per question on average). Spend about 40 secons per question on average.",
    "Less than 10 different gazes on average. Look at the answers longer (average of at least 4 seconds per look). Lots of time spent on code (average of at least 10 seconds per look). Spend less than 20 secons per question on average.",
    "Between 10 and 20 different gazes on average. Frequent looks on answers (more then 3 times per question on average). Look at the answers longer (average of at least 4 seconds per look). Spend less than 30 secons per question on average.",
    "Frequent looks on answers (more then 3 times per question on average). Frequent looks on code (more then 5 times per question on average). More than 20 different gazes on average. Some time spent looking at test question. Spend about 40 secons per question on average.",
    "Frequent looks on code (more then 5 times per question on average). Frequent looks on question (more then 5 times per question on average). More than 20 different gazes on average. Some time spent looking at test question. Spend about 40 secons per question on average.",
    "Frequent looks at the back button. Less than 10 different gazes on average. Spend less than 10 secons per question on average.",
    "Less than 10 different gazes on average. Spend less than 10 secons per question on average.",
    "Less than 10 different gazes on average. Look at the answers longer (average of at least 4 seconds per look). Spend less than 20 secons per question on average."
]


test_data = get_input_data()
test_data = collect_csv_data_collection_from_directory("./gaze_dataset/csv/")
for i in range(0, len(test_data)):
    current_info = get_question_based_information_vector(test_data[i])
    cluster_prediction = predict(current_info, model)
    current_info.insert(0,cluster_prediction)
    information_vector.append(current_info)
    
    if not quiet and not verbose:
        print("Pattern number {} belongs to cluster '{}'".format(i+1, cluster_type_short_description[cluster_prediction-1]))
    elif verbose:
        print("\nPattern number {} belongs to cluster '{}'. Properties of this cluster are: '{}'".format(i+1, cluster_type_short_description[cluster_prediction-1], cluster_type_long_description[cluster_prediction-1]))

if outputfile != '':
    save_data_as_csv(add_labels_to_vector(information_vector))