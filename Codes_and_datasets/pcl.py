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
    test.py -i <inputfile> -roi <roifile>
    test.py --input <inputfile> --output <outputfile> --verbose

Meaning:
    -i or --input   --> Input csv file with 1 look pattern or file with many csv files.
    -o or --output  --> Output csv file to store vectors of information for look patern and clusters'.
    --quiet         --> Do not write cluster numbers on console. Let it be empty. This requires -o argument!
    -v or --verbose --> Print everything on console.
    -roi            --> Text file that contains all regions of interest that can be found in data

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
global roi
inputfile = ''
outputfile = ''
roi = ''
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

# check if ROI input path is file or directory and return ROI data from it in form of vector of ROI
def get_roi_data():
    if roi is '':
        return ['kod', 'odgovori', 'pitanje', 'pitanje-kod', 'prazno', 'prethodno', 'sledece']
    
    if os.path.isfile(roi):
        with open(roi, encoding="utf8") as f:
            lines = f.read().splitlines()
        return lines
    else:
        print("\nBad ROI file! Check input arguments and try again.")
        sys.exit(2)

# get description data if exists
def get_description(filepath):
    if os.path.isfile(filepath):
        with open(filepath, encoding="utf8") as f:
            lines = f.read().splitlines()
        return lines
    else:
        return None


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

# init vector to length of no. of regions - init with 0.0
def init_vector_real():
    vector = {}
    return vector.fromkeys(roi,0.0)

# init vector to length of no. of regions - init with empty array []
def init_vector_array():
    vector = {}
    return vector.fromkeys(roi,[])

# init 2D vector to dim of no. of regions x no. of regions
def init_2d_vector():
    vector = {}
    return vector.fromkeys(roi,vector.fromkeys(roi,0.0))

# get sec on all regions [vector]
def seconds_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = init_vector_real()
    
    for i in range(0, len(duration)):
        vector[aoi[i]] += duration[i]

    return list(vector.values())

# get no. of looks at all regions [vector]
def no_looks_per_region(aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = init_vector_real()
    
    for i in range(0, len(aoi)):
        vector[aoi[i]] += 1

    return list(vector.values())

# mean sec by regions [vector]
def mean_seconds_per_region(duration, aoi):
    from statistics import mean
    
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = init_vector_array()

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
    vector = init_2d_vector()

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
    vector = init_2d_vector()
    
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

    i1 = total_secons_in_question(duration) # len = 1
    i2 = total_regions_in_question(aoi) # len = 1
    i3 = seconds_per_region(duration, aoi) # len = len(aoi)
    i4 = no_looks_per_region(aoi) # len = len(aoi)
    i5 = mean_seconds_per_region(duration, aoi) # len = len(aoi)
    i6 = top_region_before_per_region(duration, aoi) # len = len(aoi)
    i7 = top_region_after_per_region(duration, aoi) # len = len(aoi)

    vector.append(i1)
    vector.append(i2)
    vector.extend(i3)
    vector.extend(i4)
    vector.extend(i5)
    vector.extend(i6)
    vector.extend(i7)

    return vector   # len = 5 * len(aoi) + 2

# get vector of question statistics based on question
def get_question_based_information_vector(data):

    duration = data[data.columns[0]]
    AOI = data[data.columns[1]]

    vector = call_information_methods(duration, AOI)
    return vector

# add row and column label before saving information vector to csv file
def add_labels_to_vector(vector):
    col = ['cluster_no']

    # total vector length
    for i in range(len(roi)*5+2):
        col.append(str(i))

    df = pd.DataFrame(vector, columns=col)

    return [df.columns.values.tolist()] + df.values.tolist()

# classify the data into one of the twelve different classes
def predict(data, model):
    try:
        x = model.predict([data])
        return x[0]
    except:
        print("\nModel.predict() expects input dimension {} - got {}! Please check your model input dimension and number of different ROI!\n".format(model.coef_.shape[1], len(data)))
        sys.exit(2)

# load classification model from file named 'pickle_model.pkl'
def load_model():
    pkl_filename = "D:\\Users\Boris\Documents\Fakultet\Master\SOTS\Projekat\EyePatternClassificationLibrary\Codes_and_datasets\pickle_model.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model

# main function for picking up arguments
def main(argv):
    global inputfile
    global outputfile
    global verbose
    global quiet
    global roi
    
    parser = argparse.ArgumentParser(description="Run the pcl.py script to classify the look patern of students into one of twelve classes.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true", help="Print everything on console. It's best not to use it with large pattern dataset.")
    group.add_argument("-q", "--quiet", action="store_true", help="Do not write cluster numbers on console. Let it be empty. This requires -o argument!")
    parser.add_argument("-i","--inputfile", type=str, help="Input csv file with 1 look pattern or file with many csv files. The predefined location is './gaze_dataset/csv/'.")
    parser.add_argument("-o","--outputfile", type=str, help="Output csv file to store vectors of information for look patern and clusters' short description.")
    parser.add_argument("-r","--roi", type=str, help="Text file that contains all regions of interest that can be found in data (one region per line).")
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
    
    if args.roi is not None:
        roi = args.roi
    
    if quiet and outputfile == '':
        print("usage: pcl.py [-h] [-v | -q] [-i INPUTFILE] [-o OUTPUTFILE] [-r ROIFILE]\npcl.py: error: argument -q/--quiet: not allowed without argument -o/--outputfile")
        sys.exit(2)

    if not quiet:
        print('Input file is ', inputfile)

    if outputfile != '' and not quiet:
        print('Output file is ', outputfile)
    
    if roi != '' and not quiet:
        print('ROI file is ', roi)

if __name__ == "__main__":
   main(sys.argv[1:])


# MAIN
model = load_model()

information_vector = []
cluster_type_short_description = get_description(".\gaze_dataset\cluster_short_desc.txt")
cluster_type_long_description = get_description(".\gaze_dataset\cluster_long_desc.txt")

roi = get_roi_data()
test_data = get_input_data()
for i in range(0, len(test_data)):
    current_info = get_question_based_information_vector(test_data[i])
    cluster_prediction = predict(current_info, model)
    current_info.insert(0,cluster_prediction)
    information_vector.append(current_info)
    
    if cluster_type_long_description is None or cluster_type_short_description is None:
        print("Pattern number {} belongs to cluster {}".format(i+1, cluster_prediction))
    elif not quiet and not verbose:
        print("Pattern number {} belongs to cluster '{}'".format(i+1, cluster_type_short_description[cluster_prediction-1]))
    elif verbose:
        print("\nPattern number {} belongs to cluster '{}'. Properties of this cluster are: '{}'".format(i+1, cluster_type_short_description[cluster_prediction-1], cluster_type_long_description[cluster_prediction-1]))

if outputfile != '':
    save_data_as_csv(add_labels_to_vector(information_vector))